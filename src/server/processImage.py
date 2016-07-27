# takes in link and prints results from Watson's Visual Recognition API. Writen by Jesse Earisman.

import sys
try:
	from classifier import VisualTrainer
except ImportError:
	from .classifier import VisualTrainer

def main( url ):
	try:
		c = VisualTrainer()
		c.set_classifiers( c.get_classifier_ids() )
		d = c.dict_from_json( c.classify_single_image( url ) )
		if( d is None ):
			print ("0 0 0 0 0")
			return
		output = ""
		for tone in ["Anger", "Disgust", "Fear", "Joy", "Sadness"]:
			if tone in d:
				output += str(d[tone]) + ' '
			else:
				output += '0 '
		print (output)
	except:
		print ("0 0 0 0 0")


if( __name__ == "__main__" ):
	main( sys.argv[1] )
