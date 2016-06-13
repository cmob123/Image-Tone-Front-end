import json
from watson_developer_cloud import ToneAnalyzerV3

# A class to analyze tone, some sort of ... Tone Analyzer
# Really only handles emotion data
class ToneAnalyzer:
	def __init__(self):
		self.tone_analyzer = ToneAnalyzerV3(
				password='UPCemjhdhixD',
				username='05ec4a1d-6a90-47ab-bf15-f23dc733d9e1',
				version='2016-05-19'
				)

	# Analyzes the text tone
	# returns a JSON structure containing all document level tone data
	# Sentence level data is discarded
	def tone_analyze( self, text ):
		raw_json = self.tone_analyzer.tone( text = text )
		return raw_json['document_tone']

	
	# Discards writing style and personality data, returning
	# only emotion data
	def extract_emotions( self, doc_tone ):
		emotions = doc_tone['tone_categories'][0]['tones']
		return emotions

	# pretty prints the emotion score, expects json input in the same format returned
	# by extract_emotions
	def emotions_pp( self, emotions ):
		for e in emotions:
			print( e['tone_name'] + " : " + str( e['score'] ) )

	# extracts the 5 numbered emotion scores from the json
	# expects json input returned by extract_emotions
	def emotions_num_extract( self, emotions ):
		nums = []
		for e in emotions:
			nums.append( e['score'] )
		return nums

