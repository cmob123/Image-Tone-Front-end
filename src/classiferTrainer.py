import json
import time
from watson_developer_cloud import VisualRecognitionV3
#from visual_recognition_v3 import VisualRecognitionV3
import requests



apikey = 'cb413d69a797e117154d8474ea7397a04866551a'

# A class to analyze tone, some sort of ... Tone Analyzer
# Really only handles emotion data
class VisualTrainer:

	visual_recognition = None
	
	def __init__(self):
		# TODO
		"""
		self.visual_recognition = VisualRecognitionV3(
			password = "awDho4FkDovI",
        	username = "b9917582-7ff3-49a4-9104-aae4b64035b2",
			version  = "2016-05-20")
		"""
		self.visual_recognition = VisualRecognitionV3('2016-05-20', api_key=apikey)
	
	# Build a new classifier with the given name.
	# Name could be something like "Cats vs Dogs"
	# class_names is a list of names, like: ["cat", "dog"]
	# zipfiles is a list of the same length, like: ["cat_pos_ex.zip", "dogs.zip"]
	#  zipfiles contains a list of .zip files containing examples of the associated class
	# neg_zipfile is a .zip file containing images that do not fit into any classes
	# returns a json description of the new classifier
	def new_classifier( self, classifier_name, class_names, zipfiles, neg_zipfile ):
		print( "Are you sure you want to create a new classifier" )
		print( "Current classifier list is:" )
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

		neg_zip = open( neg_zipfile, "rb" )
		open_files.append( neg_zip )
		arguments_str += "negative_examples=neg_zip"
		exec_str = "ret_json = self.visual_recognition.create_classifier( \"{}\", {} )".format( classifier_name, arguments_str)
		#print( exec_str )
		exec( exec_str )
		for f in open_files:
			f.close()
		if( ret_json is not None ):
			print( json.dumps( ret_json, indent=2) )
			return ret_json

	def list_classifiers(self):
		print( json.dumps( self.visual_recognition.list_classifiers( verbose= True ), indent=4) )

	def del_classifier( self, classifier_id ):
			self.visual_recognition.delete_classifier( classifier_id)
		

	def classify_single_image( self, url, classifier_id = None ):
		return self.visual_recognition.classify( images_url= url, classifier_ids=classifier_id )

		


def main():
	v = VisualTrainer()

	url = "http://i.imgur.com/Yq1mc9H.jpg"
	v.list_classifiers()
	print( 
			json.dumps(
				v.visual_recognition.classify( 
					images_url=url, 
					classifier_ids="Angerornot_1582529321",
					owners=apikey),
				indent=2 ) )



if( __name__ == "__main__"):
	main()
