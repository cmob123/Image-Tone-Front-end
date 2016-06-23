from imageRanker import *
from classifier import *
from tone import tone_names
import sys
import numpy
import array

def test_classifiers( vis_trainer, test_fn, data_dir ):
	test_imgr = ImageRanker( test_fn, data_dir )
	actual_emos = test_imgr.emotions
	num_emos = len( tone_names )
	assert( len( actual_emotions ) == num_emos )
	class_emos = [[]] * num_emos
	for img in test_imgr.images:
		url = img['url']
		vis_trainer.set_classifiers( vis_trainer.get_classifier_ids() )
		j = vis_trainer.classify_single_image( url )
		print( json.dumps( j, indent=2 ) )
		input()


"""
This file is used to test our classifiers.
It's pretty fragile, but powerful.
"""
def main():
	#TODO: Check if this is already done
	classify_images()
	actual = ImageRanker( image_file_name = "actual.txt", data_dir = "../data/")
	classified = ImageRanker( image_file_name = "classified.txt", data_dir = "../data/")
	a_bitmap = actual.emo_bitmap
	a_scores = actual.scores
	a_emotions = actual.emotions
	a_stddev = list( map( (lambda x: numpy.std(x) ), a_emotions ) )
	print( "Actual stats: ")
	print( "min: {}".format(list( map ( (lambda x: numpy.min(x) ) , a_emotions) ) ) )
	print( "max: {}".format(list( map ( (lambda x: numpy.max(x) ) , a_emotions) ) ) )
	print( "mean: {}".format(list( map ( (lambda x: numpy.mean(x) ) , a_emotions) ) ) )
	print( "stddev: {}".format(a_stddev) )
	print( "Length: {}".format( list( map( len, a_emotions ) ) ) )
	c_bitmap = classified.emo_bitmap
	c_scores = classified.scores
	c_emotions = classified.emotions
	c_stdev = map( (lambda x: numpy.std(x) ), c_emotions )
	c_stddev = list( map( (lambda x: numpy.std(x) ), c_emotions ) )
	print( "Classifier stats: ")
	print( "min: {}".format(list( map ( (lambda x: numpy.min(x) ) , c_emotions) ) ) )
	print( "max: {}".format(list( map ( (lambda x: numpy.max(x) ) , c_emotions) ) ) )
	print( "mean: {}".format(list( map ( (lambda x: numpy.mean(x) ) , c_emotions) ) ) )
	print( "stddev: {}".format(c_stddev) )
	print( "Length: {}".format( list( map( len, c_emotions ) ) ) )

	length = len( c_emotions[0] )
	assert( length == len( a_emotions[0] ) )
	control = [[1/3] * 5] * length

	print( "Length is {}".format( length ))
	correlation_cs = []
	for i in range(0, 5):
		correlation_cs.append( correlation_coefficient(a_emotions[i], c_emotions[i] ) )
	print( "Correlation coefficients: {}".format(correlation_cs) )



def classify_images():
	test_i = ImageRanker( test_file, "../data/" )
	images = test_i.images
	v = VisualTrainer()
	v.set_classifiers( v.get_classifier_ids() )
	c_scores = []
	controls = []
	a_scores = test_i.scores
	counter = 0
	classified_file = open( "../data/classified.txt", "w" )
	actual_file = open("../data/actual.txt", "w" )
	for i in images:
		try:
			json_score = v.classify_single_image( i )
		except:
			print("Error in classifing {}".format(i))
			continue
		try:
			arr = []
			for c in json_score["images"][0]["classifiers"]:
				arr.append( c["classes"][0]["score"] )
			c_scores.append( arr )
			controls.append( [1/3] * 5 )
			classified_file.write( "{}\n".format(i) )
			classified_file.write( "{}\n".format(c_scores[counter]) )
			actual_file.write( "{}\n".format(i) )
			actual_file.write( "{}\n".format( numpy.ndarray.tolist(a_scores[counter] ) ))
			print( "Image: {}".format( i ) )
			print( "Classifiers: {}".format( c_scores[counter] ) )
			print( "Actual: {}".format( numpy.ndarray.tolist( a_scores[counter] ) ) )
			counter += 1
			sys.stdout.flush()
		except:
			print( sys.exc_info() )
			print( json.dumps( json_score, indent=2 ) )
			continue
	classified_file.close()
	actual_file.close()

if( __name__ == "__main__" ):
	main()



