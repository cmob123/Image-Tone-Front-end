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
	translation_table = {}
	# The order that tone names are stored is sorted by tone category,
	# but the order they are classified in is strictly alphabetical.
	# We need to be able to knew which ones to compare
	for emo in alpha_tone_names:
		translation_table[emo] = tone_names.index( emo )
	
	vis_trainer.set_classifiers( vis_trainer.get_classifier_ids() )
	image_data_set = []
	i = 0;

	for img in test_imgr.images:
		i += 1
		url = img['url']

		j = vis_trainer.classify_single_image( url )
		if( j is None ):
			continue

		classifier_data = [None] * tone_num
		try:
			for classifier in j["images"][0]["classifiers"]:
				name = classifier["classes"][0]["class"]
				score = classifier["classes"][0]["score"]
				classifier_data[ translation_table[name] ] = score
			img['classifier_data'] = classifier_data
			print("Classified {} successfully. ({}/{})".format( url, i, len( test_imgr.images) ) )
			sys.stdout.flush()
			image_data_set.append( img )
		except KeyError as e:
			print("KeyError: {} probably because the image is too big".format( e ) )
			print( json.dumps( j, indent=2 ) )
	actual_emos = []
	class_emos = []
	for i in range( 0, tone_num ):
		actual_emos.append( [] )
		class_emos.append( [] )
	assert( len( actual_emos ) == tone_num )
	assert( len( class_emos ) == tone_num )
	for img in image_data_set:
		if( 'classifier_data' in img and 'comment_data' in img ):
			assert( tone_num == len( img['classifier_data'] ) )
			assert( tone_num == len( img['comment_data'] ) )
			for i in range(0, tone_num ):
				actual_emos[i].append( img['comment_data'][i] )
				class_emos[i].append( img['classifier_data'][i] )
	sys.stdout.flush()
	input()
	for i in range( 0, tone_num ):
		print( "Correlation coefficient of {}: {}".format( tone_names[i], correlation_coefficient( class_emos[i], actual_emos[i] ) ) )

