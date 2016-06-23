from imageRanker import *
from classifier import *
from tone import tone_names,tone_num
import sys
import numpy
import array

def test_classifiers( vis_trainer, test_fn, data_dir ):
	test_imgr = ImageRanker( test_fn, data_dir )
	actual_emos = test_imgr.emotions
	assert( len( actual_emos ) == tone_num )
	class_emos = [[]] * tone_num
	alpha_tone_names = sorted(tone_names)
	translation_table = {}
	# The order that tone names are stored is sorted by tone category,
	# but the order they are classified in is strictly alphabetical.
	# We need to be able to knew which ones to compare
	for emo in alpha_tone_names:
		translation_table[emo] = tone_names.index( emo )
	
	vis_trainer.set_classifiers( vis_trainer.get_classifier_ids() )
	for img in test_imgr.images:
		url = img['url']
		print( "Image: {}".format( url ) )
		print( "Actual: {}".format( img['comment_data'] ) )

		classifier_data = [None] * tone_num
		j = vis_trainer.classify_single_image( url )

		for classifier in j["images"][0]["classifiers"]:
			name = classifier["classes"][0]["class"]
			score = classifier["classes"][0]["score"]
			classifier_data[ translation_table[name] ] = score
		#vis_trainer.pp_classify_response( j )
		print( "Classifier: {}".format( classifier_data ) )
		input()
