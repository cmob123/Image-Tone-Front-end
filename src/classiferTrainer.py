import json
import time
from watson_developer_cloud import VisualRecognitionV3

# A class to analyze tone, some sort of ... Tone Analyzer
# Really only handles emotion data
class VisualTrainer:

	visual_recognition = None
	
	def __init__(self):
		# TODO
		visual_recognition = VisualRecognitionV3('2016-05-20', api_key='')
	
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
		#print( visual_recognition.list_classifiers( verbose= True ) )
		text = input( "Type 'YES' to continue creating classifier {}: ".format( classifier_name ) )
		if( text != "YES" ):
			print( "exiting, no classifier created" )
			return None

		assert( len( class_names ) == len( zipfiles ) )
		n_classes = len( class_names )
		arguments_str = ""
		open_files = []
		for i in range( 0, n_classes ):
			zipf_name = class_names[i] + "_zip"
			exec( "{} = open( \"{}\", \"rb\")".format( zipf_name, zipfiles[i] ))
			exec( "open_files.append( {} )".format( zipf_name ) )
			arguments_str += "{}_positive_examples={}, ".format( class_names[i], zipf_name )

		neg_zip = open( neg_zipfile, "rb" )
		open_files.append( neg_zip )
		arguments_str += "negative_examples=neg_zip"
		exec_str = "ret_json = self.visual_recognition.create_classifier( \"{}\", {} )".format( classifier_name, arguments_str)
		print( exec_str )
		# exec( exec_str ) )
		for f in open_files:
			f.close()
		#return ret_json


def main():
	v = VisualTrainer()
	v.new_classifier( 
			"Dogs vs Cats", 
			["dog", "cat"], 
			["dogs.zip", "cat_ex.zip"], 
			"meese.zip")

if( __name__ == "__main__"):
	main()



