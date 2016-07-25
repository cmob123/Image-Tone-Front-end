# takes in link and prints results from Watson's Visual Recognition API. Writen by Jesse Earisman, modified by Chris O'Brien.

#import urllib.error
from classifier import VisualTrainer

def classify(url):
	#return 'URL: ' + url
	#'''
	output = ''
	try:
		c = VisualTrainer()
		if(c.get_classifier_ids() != []):
			c.set_classifiers( c.get_classifier_ids() )
			d = c.dict_from_json( c.classify_single_image(url) )
			if( d is None ):
				output = '0 0 0 0 0'
			else:
				for tone in ['Anger', 'Disgust', 'Fear', 'Joy', 'Sadness']:
					if tone in d:
						output += str(d[tone]) + ' '
					else:
						output = 'ERROR: No tone information found.'
						break
				if output == "":
					output = 'THERE'
		else: output = 'ERROR: Cannot get classifiers (limit reached)'
	except urllib.error.HTTPError as err:
		if err.code == 404:
			output = 'ERROR: Page not found!'
		elif err.code == 403:
			output = 'ERROR: Access denied!'
		else: output = 'HERE' + str(err)
	except:
		output = 'ERROR: Unkown error during image classification'
	if output == "":
		output = 'hmmm'
	return output
	#'''