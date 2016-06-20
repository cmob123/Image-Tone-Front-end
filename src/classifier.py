import json
import time
from watson_developer_cloud import VisualRecognitionV3
#from visual_recognition_v3 import VisualRecognitionV3
import requests
import sys



apikey = 'cb413d69a797e117154d8474ea7397a04866551a'
anger_class_id ="Angerornotv2_2085176946"

# A class to analyze tone, some sort of ... Tone Analyzer
# Really only handles emotion data
class VisualTrainer:

	v = None
	
	def __init__(self):
		self.v = VisualRecognitionV3('2016-05-20', api_key=apikey)
	
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
	def new_classifier( self, classifier_name, class_names, zipfiles, neg_zipfile ):
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
			print( arguments_str )

		neg_zip = open( neg_zipfile, "rb" )
		open_files.append( neg_zip )
		arguments_str += "negative_examples=neg_zip"
		exec_str = "ret_json = self.v.create_classifier( \"{}\", {} )".format( classifier_name, arguments_str)
		print( exec_str )
		exec( exec_str )
		for f in open_files:
			f.close()
		return

	# Prints an unformatted, verbose list of all classifiers
	# Used soley for debugging, probably
	def list_classifiers(self):
		print( json.dumps( self.v.list_classifiers( verbose= True ), indent=4) )

	# deletes a classifier
	def del_classifier( self, classifier_id ):
			self.v.delete_classifier( classifier_id)

	def classify_zip_file( self, f_name ):
		img_file = open( f_name, "rb" )
		to_ret = self.v.classify( images_file = img_file, classifier_ids = self.get_classifier_ids(), threshold = 0.0 )
		return to_ret
		

	"""
	Classifies a single image using all classifiers we have created
	Returns a json struct containing all classification probabilities, no matter how small
	As a side effect, pretty prints the classification details
	"""
	def classify_single_image( self, url, classifier_ids = None ):
		to_ret = self.v.classify( images_url = url, classifier_ids = self.get_classifier_ids(), threshold = 0.0)
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
		for i in some_json["images"]:
			for c in i["classifiers"]:
				for cl in c["classes"]:
					print("{} : {}".format( cl["class"], cl["score"] ) )


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

	def get_classifier_ids( self ):
		to_ret = []
		class_list = self.v.list_classifiers( verbose = True )
		for c in class_list["classifiers"]:
			to_ret.append( c["classifier_id"] )
		return to_ret

	# Start from the ground up, nuke all classifiers and rebuild them.
	# This should only be called when the data has been updated, for instance
	def rebuild_classifiers( self ):
		self.del_aall_classifiers()
		vis.new_classifier(
				"angerclass",
				["anger"],
				["../data/anger.zip"],
				"../data/neg-anger.zip")
		vis.new_classifier(
				"disgustclass",
				["disgust"],
				["../data/disgust.zip"],
				"../data/neg-disgust.zip")
		vis.new_classifier(
				"fearclass",
				["fear"],
				["../data/fear.zip"],
				"../data/neg-fear.zip")
		vis.new_classifier(
				"joyclass",
				["joy"],
				["../data/joy.zip"],
				"../data/neg-joy.zip")
		vis.new_classifier(
				"sadnessclass",
				["sadness"],
				["../data/sadness.zip"],
				"../data/neg-sadness.zip")

def main( args ):

	vis = VisualTrainer()
	for a in args:
		if( a[-4:] == ".zip" ):
			vis.classify_zip_file( a )
		elif( a[-4:] == ".jpg" ):
			vis.classify_single_image( a )
		else:
			print( "Invalid file type, continuing" )
			continue

if( __name__ == "__main__" ):
	main( sys.argv[1:] )
