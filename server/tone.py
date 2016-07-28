import json
import time
import sys
from watson_developer_cloud import ToneAnalyzerV3, WatsonException

tone_names = [
	"Anger", 
	"Disgust",
	"Fear",
	"Joy",
	"Sadness",
	"Analytical",
	"Confident",
	"Tentative",
	"Openness",
	"Conscientiousness",
	"Extraversion",
	"Agreeableness",
	"Emotional_Range" ]

# A class to analyze tone, some sort of ... Tone Analyzer
# Really only handles emotion data
class ToneAnalyzer:
	def __init__( self ):
		self.tone_analyzer = ToneAnalyzerV3(
				password = "tbcGKRwREvC8",
    			username = "0d44496f-11a7-4552-9145-d03acd1bf293",
				version  = "2016-05-19")

	# Analyzes the text tone
	# returns a JSON structure containing all document level tone data
	# Sentence level data is discarded
	# Occasionally, this fails, since Watson is rate limiting us
	# In that case, we just want to wait 60 seconds and try again
	def tone_analyze( self, text ):
		try:
			raw_json = self.tone_analyzer.tone( text=text )
		except WatsonException as e:
			print( "Looks like we're being rate limited" )
			print( e )
			time.sleep( 60 )
			return self.tone_analyze( text )
		if( "document_tone" in raw_json ):
			return raw_json["document_tone"]

	def tone_all_num_extract( self, doc_tone ):
		ret = {}
		try:
			for t in doc_tone["tone_categories"]:
				for e in t["tones"]:
					# Can't have spaces in tone names, only relevant for Emotional Range
					tone_name = e["tone_name"].replace( " ", "_" )
					ret[ tone_name ] = e["score"]
		except:
			print("Failed to extract tone data")
			print( sys.exc_info()[0] )
			return None
		return ret

	
	# Discards writing style and personality data, returning
	# only emotion data
	def extract_emotions( self, doc_tone ):
		emotions = doc_tone["tone_categories"][0]["tones"]
		return emotions

	# pretty prints the emotion score, expects json input in the same format returned
	# by extract_emotions
	def emotions_pp( self, emotions ):
		for e in emotions:
			print( e["tone_name"] + " : " + str( e["score"] ) )

	# extracts the 5 numbered emotion scores from the json
	# expects json input returned by extract_emotions
	def emotions_num_extract( self, emotions ):
		nums = []
		for e in emotions:
			nums.append( e["score"] )
		return nums