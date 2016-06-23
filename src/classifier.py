import json
import time
from watson_developer_cloud import VisualRecognitionV3
#from visual_recognition_v3 import VisualRecognitionV3
import requests
import sys
from imageRanker import *
from tone import tone_names



apikey = 'cb413d69a797e117154d8474ea7397a04866551a'
anger_class_id ="Angerornotv2_2085176946"

# A class to analyze tone, some sort of ... Tone Analyzer
# Really only handles emotion data
class VisualTrainer:

	v = None
	
	def __init__(self):
		self.v = VisualRecognitionV3('2016-05-20', api_key=apikey)
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
	def new_classifier( self, classifier_name, class_names, zipfiles, neg_zipfile, prompt = True ):
		if( prompt ):
			print( "Are you sure you want to create a new classifier" )
			print( "Current classifier list is:" )
			self.list_classifiers()
			text = input( "Type 'YES' to continue creating classifier \"{}\": ".format( classifier_name ) )
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
			exec( "{} = open( \"{}\", \"rb\")".format( zipf_name, zipfiles[i] ))
			exec( "open_files.append( {} )".format( zipf_name ) )
			arguments_str += "{}_positive_examples={}, ".format( class_names[i], zipf_name )
			#print( arguments_str )

		neg_zip = open( neg_zipfile, "rb" )
		open_files.append( neg_zip )
		arguments_str += "negative_examples=neg_zip"
		exec_str = "ret_json = self.v.create_classifier( \"{}\", {} )".format( classifier_name, arguments_str)
		#print( exec_str )
		exec( exec_str )
		for f in open_files:
			f.close()
		print( "Finished creating classifier {}".format( classifier_name ) )
		return

	# Prints an unformatted, verbose list of all classifiers
	# Used soley for debugging, probably
	def list_classifiers(self):
		print( json.dumps( self.v.list_classifiers( verbose = False ), indent=2) )

	def set_classifiers( self, c_list ):
		self.classifier_list = c_list

	# deletes a classifier
	def del_classifier( self, classifier_id ):
			self.v.delete_classifier( classifier_id)

	def classify_zip_file( self, open_file ):
		to_ret = self.v.classify( images_file = img_file, classifier_ids = self.classifier_list, threshold = 0.0 )
		return to_ret
		

	"""
	Classifies a single image using all classifiers we have created
	Returns a json struct containing all classification probabilities, no matter how small
	As a side effect, pretty prints the classification details
	"""
	def classify_single_image( self, url ):
		to_ret = None
		try:
			to_ret = self.v.classify( images_url = url, classifier_ids = self.classifier_list, threshold = 0.0)
		except:
			print("Error in classifying {}".format( url ) )
			print( sys.exc_info() )
		return to_ret

	"""
	pretty print the classifier response in a format like
	anger: 0.5386
	fear: 0.0245
	...

	This is pretty fragile, it more or less expects the format returned by classify_single_image, and if there are any errors it will break
	Someone should fix this later
	"""
	def pp_classify_response( self, some_json):
		try:
			for i in some_json["images"]:
				if( "error" in i ):
					print( "Error in image" )
					continue
				for c in i["classifiers"]:
					for cl in c["classes"]:
						print("{} : {}".format( cl["class"], cl["score"] ) )
		except KeyError as e:
			print("KeyError when printing the classify response")
			print("Maybe something went wrong in classification?")
			print( e )


	# Delete all classifiers. They are unrecoverable
	# If prompt is given as false, this will not confirm your choice, it will just delete everything
	def del_all_classifiers( self, prompt = True ):
		if( prompt ):
			text = input( "This will delete ALL classifiers. Type \"YES\" if you really want to do this: ")
			if( text != "YES" ):
				print( "exiting, nothing deleted created" )
				return None

		# Either they typed YES, or prompt is False
		# Proceed to delete everything
		class_list = self.v.list_classifiers( verbose = True )
		for c in class_list["classifiers"]:
			self.v.delete_classifier( c["classifier_id"] )

	# Return a list of all classifier ids known to Watson, excluding default
	def get_classifier_ids( self ):
		to_ret = []
		class_list = self.v.list_classifiers( verbose = False )
		try:
			for c in class_list["classifiers"]:
				if( c["status"] == "ready" ):
					to_ret.append( c["classifier_id"] )
			return to_ret
		except KeyError as e:
			print( "Error in fetching classifier ids" )
			print( str( e ) )
			return to_ret

	# Start from the ground up, nuke all classifiers and rebuild them.
	# There are very few good reasons to call this. The primary one being that the data has been updated
	def rebuild_classifiers( self, data_dir = "../data/" ):
		# make tone names lowercase
		# lc_tone_names = map( (lambda x: x.lower()), tone_names )
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

def main( args ):
	vis = VisualTrainer()
	i = ImageRanker( "data.csv", "../data/" )
	vis.rebuild_classifiers( )
	vis.list_classifiers()
	return
	vis.set_classifiers( vis.get_classifier_ids() )
	text = input( "Enter an image link or zip file to classify -> " )
	while( text != "" ):
		print( text )
		if( text[-4:] == ".zip" ):
			f = open( text, "rb" )
			j = vis.classify_zip_file( f )
			vis.pp_classify_response( j )

		elif( text[-4:] == ".jpg" or text[-4:] == ".png" ):
			j= vis.classify_single_image( text )
			print( json.dumps( j, indent=2 ) )
			vis.pp_classify_response( j )
		else:
			print( "Sorry, i didn't understand that file type" )
		text = input( "Enter an image link or zip file to classify -> " )


if( __name__ == "__main__" ):
	main( sys.argv[1:] )
