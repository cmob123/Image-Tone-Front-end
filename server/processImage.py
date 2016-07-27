# takes in link and prints results from Watson's Visual Recognition API. Writen by Jesse Earisman.

import sys
try:
	from classifier import VisualTrainer
except ImportError:
	from .classifier import VisualTrainer

def classify( url ):
	try:
		c = VisualTrainer()
		c.set_classifiers( c.get_classifier_ids() )
		d = c.dict_from_json( c.classify_single_image( url ) )
		output = ""
		if( d is None ):
			return "ERROR: Watson"
		for tone in ["Anger", "Disgust", "Fear", "Joy", "Sadness"]:
			if tone in d:
				output += str( d[tone]) + ' '
			else:
				return "ERROR: Classifiers"
		return output
	except:
		return "ERROR: Unknown"



if( __name__ == "__main__" ):
	main( sys.argv[1] )
