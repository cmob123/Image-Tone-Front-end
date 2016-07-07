import sys
from classifier import VisualTrainer

def main( url ):
	try:
		c = VisualTrainer()
		c.set_classifiers( c.get_classifier_ids() )
		d = c.dict_from_json( c.classify_single_image( url ) )
		if( d is None ):
			for i in range( 0, 5 ):
				print( 0 )
			return

		for tone in ["Anger", "Disgust", "Fear", "Joy", "Sadnes"]:
			if tone in d:
				print( d[tone] )
			else:
				print( 0 )
	except:
		for i in range( 0, 5 ):
			print( 0 )


if( __name__ == "__main__" ):
	main( sys.argv[1] )

