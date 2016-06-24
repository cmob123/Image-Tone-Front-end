from imageRanker import *
from classifier import *
from tone import tone_names,tone_num
from dataOps import *
import sys
import numpy
import array

def test_classifiers( vis_trainer, test_fn, data_dir ):
	test_imgr = ImageRanker( test_fn, data_dir )
	alpha_tone_names = sorted(tone_names)

	vis_trainer.set_classifiers( vis_trainer.get_classifier_ids() )
	image_data_set = []
	i = 0;

	for img in test_imgr.images:
		i += 1
		url = img['url']

		j = vis_trainer.classify_single_image( url )
		if( j is None ):
			continue

		classifier_data = {}
		try:
			for classifier in j["images"][0]["classifiers"]:
				name = classifier["classes"][0]["class"]
				score = classifier["classes"][0]["score"]
				classifier_data[ name ] = score
			img['classifier_data'] = classifier_data
		except KeyError as e:
			print("KeyError: {} possibly because the image is too big".format( e ) )
			print( json.dumps( j, indent=2 ) )
		print("Classified {} successfully. ({}/{})".format( url, i, len( test_imgr.images) ) )
		sys.stdout.flush()
		image_data_set.append( img )
	actual_emos = dict.fromkeys( tone_names, list )
	class_emos = dict.fromkeys( tone_names, list )
	assert( len( actual_emos ) == tone_num )
	assert( len( class_emos ) == tone_num )
	for img in image_data_set:
		if( 'classifier_data' in img and 'comment_data' in img ):
			assert( set( tone_names ) == set( img['classifier_data'].keys) )
			assert( set( tone_names ) == set( img['comment_data'].keys) )
			for tone in tone_names:
				actual_emos[tone].append( img['comment_data'][tone] )
				class_emos[tone].append( img['classifier_data'][tone] )
		else:
			print( "Image is in image_data_set, but lacks complete data")
			print( img )
	sys.stdout.flush()
	input()
	for tone in tone_names:
		print( "Correlation coefficient of {}: {}".format( tone_names[i], correlation_coefficient( class_emos[i], actual_emos[i] ) ) )

