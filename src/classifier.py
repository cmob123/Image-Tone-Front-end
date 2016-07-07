import json
import time
from watson_developer_cloud import VisualRecognitionV3, WatsonException
#from visual_recognition_v3 import VisualRecognitionV3
import requests
import sys
from imageRanker import *
from tone import tone_names


apikey = "746a92d1543dc95c5c5eebc9900489b083d91cdc"

class VisualTrainer:

	v = None
	
	"""
	Note: After constructing one of these bad boys, you probably want
	to call set_classifiers(), even if just using the default
	"""
	def __init__(self):
		self.v = VisualRecognitionV3( 
			version="2016-05-20",
			url="https://gateway-a.watsonplatform.net/visual-recognition/api", 
			api_key=apikey )
		self.classifier_list = None
	
	"""
	Build a new classifier with the given name.
	Name could be something like "Cats vs Dogs"
	class_names is a list of names, like: ["cat", "dog"]
	zipfiles is a list of the same length, like: ["cat_pos_ex.zip", "dogs.zip"]
	zipfiles contains a list of .zip files containing examples of the associated class
	neg_zipfile is a .zip file containing images that do not fit into any classes
	returns a json description of the new classifier

	Prompts before constructing the new classifier
	"""
	def new_classifier( self, classifier_name, class_names, zipfiles, neg_zipfile, prompt=True ):
		if( prompt ):
			print( "Are you sure you want to create a new classifier" )
			print( "Current classifier list is:" )
			self.list_classifiers()
			text = input( "Type 'YES' to continue creating classifier '{}': ".format( classifier_name ) )
			if( text != "YES" ):
				print( "exiting, no classifier created" )
				return None

		assert( len( class_names ) == len( zipfiles ) )
		n_classes = len( class_names )
		arguments_str = ""
		open_files = []

		# This is a little weird, basically, we don't know the names or how many classes we want
		# we need to generate the parameter names on the fly and build the exec string
		# while maintaining a list of open files, so that we can close them later
		# I wouldn't touch this if I were you
		for i in range( 0, n_classes ):
			zipf_name = class_names[i] + "_zip"
			exec( "{} = open( '{}', 'rb')".format( zipf_name, zipfiles[i] ))
			exec( "open_files.append( {} )".format( zipf_name ) )
			arguments_str += "{}_positive_examples={}, ".format( 
					class_names[i], zipf_name )

		neg_zip = open( neg_zipfile, "rb" )
		open_files.append( neg_zip )
		arguments_str += "negative_examples=neg_zip"
		exec_str = "ret_json = self.v.create_classifier( '{}', {} )".format( 
				classifier_name, arguments_str)
		try:
			exec( exec_str )
			print( "Finished creating classifier {}".format( classifier_name ) )
			sys.stdout.flush()
		except WatsonException as e:
			print( "Something went wrong, could not make {} classifier".format( 
					classifier_name ) )
			print( e )
		for f in open_files:
			f.close()
		return

	"""
	Prints the json-formatted list of all classifiers
	In the future, we may want to have a prettier way of doing this
	"""
	def list_classifiers( self ):
		try:
			print( json.dumps( self.v.list_classifiers( verbose=False ), indent=2) )
		except WatsonException as e:
			print( "Something went wrong, maybe watson is down" )
			print( e )


	def set_classifiers( self, c_list ):
		self.classifier_list = c_list

	def del_classifier( self, classifier_id ):
			self.v.delete_classifier( classifier_id )

	"""
	Classifies a single image using all classifiers we have created
	Returns a json struct containing all classification probabilities, no matter how small
	"""
	def classify_single_image( self, url ):
		ret = None
		try:
			ret = self.v.classify( 
				images_url=url, 
				classifier_ids=self.classifier_list, 
				threshold=0.0 )
		except WatsonException as e:
			print("Error in classifying {}".format( url ) )
			print( e )
			return None
		return ret

	"""
	Like the previous function, but works on a compressed
	zip file of images
	YMMV, especially when passing this to other functions in this class
	"""
	def classify_zip_file( self, open_file ):
		ret = None
		try:
			ret = self.v.classify( 
				images_file=img_file, 
				classifier_ids=self.classifier_list, 
				threshold=0.0 )
		except WatsonException as e:
			print( e )
			return None
		return ret

	"""
	takes a json object like the one returned by classify_single_image
	Returns a dict containing all classes, and their associated confidence
		values
	Returns None on error
	"""
	def dict_from_json( self, j ):
		# Maybe we should treat this more like an error?
		if( j is None ):
			return None
		try:
			ret = {}
			for classifier in j["images"][0]["classifiers"]:
				for c in classifier["classes"]:
					ret[ c["class"] ] = c["score"]
		except KeyError as e:
			return None
		return ret
		



	"""
	pretty print the classifier response in a format like
	anger: 0.5386
	fear: 0.0245
	...

	This expects the format returned by classify_single_image
	"""
	def pp_classify_response( self, some_json):
		if( some_json is None ):
			print( "Error: Expected json object, got NoneType" )
			return
		d_tmp = self.dict_from_json( some_json )
		if( d_tmp is None ):
			print( "Error: classifier response was invalid" )
			print( json.dumps( some_json, indent=2 ) )
			return

		# Nothing past here should result in an error, we're just printing a dict
		for k,v in d_tmp.items():
			print( "{}: {}".format( k, v ) )

	"""
	Delete all classifiers. They are unrecoverable
	If prompt is given as false, this will not confirm your choice, it will just delete everything
	"""
	def del_all_classifiers( self, prompt=True ):
		if( prompt ):
			text = input( "This will delete ALL classifiers. Type 'YES' if you really want to do this: ")
			if( text != "YES" ):
				print( "exiting, nothing deleted created" )
				return None

		# Either they typed YES, or prompt is False
		# Proceed to delete everything
		class_list = self.v.list_classifiers( verbose=True )
		for c in class_list["classifiers"]:
			self.v.delete_classifier( c["classifier_id"] )

	# Return a list of all classifier ids known to Watson, excluding default
	def get_classifier_ids( self ):
		ret = []
		try:
			class_list = self.v.list_classifiers( verbose = False )
		except WatsonException as e:
			print( e )
			return ret
		try:
			for c in class_list["classifiers"]:
				if( c["status"] == "ready" ):
					ret.append( c["classifier_id"] )
		except KeyError as e:
			print( "Error in fetching classifier ids" )
			print( str( e ) )
			return ret
		return ret

	"""
	Rebuilds all classifiers based on zip files in the data directory.
	Make sure you called the appropriate method in imageRanker before
	calling this.
	"""
	def rebuild_classifiers( self, data_dir = "../data/" ):
		for tone in tone_names:
			classifier_name = tone + "class"
			class_name = tone
			filename = "../data/" + tone + ".zip"
			neg_filename = "../data/neg-" + tone + ".zip"
			self.new_classifier(
				classifier_name,
				[class_name],
				[filename],
				neg_filename,
				True )
		print( "Finished rebuilding classifiers, the new list is: " )
		self.v.list_classifiers()
