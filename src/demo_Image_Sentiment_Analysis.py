import os
import json
from watson_developer_cloud import VisualRecognitionV3


# This module can be used to test trained Image Sentiment Analyzer
# Use analyze() method to analyze an online or local image of interest


def analyze_local_picture(local_file, vr_service, classifier_ids):
	with open(local_file, 'rb') as file:
		rlt = vr_service.classify(images_file = file, classifier_ids=classifier_ids)
		print ("Analyze results for " + local_file + "\n")
		print (json.dumps(rlt, indent = 2))


	rlt = vr.classify(images_url = url, classifier_ids=classifier_ids)

def analyze_online_picture(image_url, vr_service, classifier_ids):
	rlt = vr_service.classify(images_url = image_url, classifier_ids=classifier_ids)
	print ("Analyze results for " + image_url + "\n")
	print (json.dumps(rlt, indent = 2))


def analyze_meta(image_url = None, local_file= None, api_key = None, classifier_ids = ['default']):
	# Check parameters
	if api_key is None:
		print("Please provide an Bluemix api key.")
		return

	if image_url is None and local_file is None:
		print("You must provide a picture to start.")
		return

	# Initial Bluemix Visual Recognition service
	vr = VisualRecognitionV3('2016-05-20', api_key=api_key)

	# Do analysis
	if image_url is not None:
		analyze_online_picture(image_url, vr, classifier_ids)

	if local_file is not None:
		analyze_local_picture(local_file, vr, classifier_ids)


#  Using this function to test the Image Sentiment Analyzer
def analyze(image_url = None, local_file= None):
	api_key = 'cb413d69a797e117154d8474ea7397a04866551a'
	classifier_ids =  ['Disgustclass_1700472121', 'Joyclass_739515442', 'Confidentclass_1819922821', 'Tentativeclass_139186933', 'Extraversionclass_307029591', 'Analyticalclass_1811963953', 'Opennessclass_1578785479', 'Sadnessclass_1925437149', 'Fearclass_684490622', 'Agreeablenessclass_811417195', 'Conscientiousnessclass_261720898', 'Emotional_Rangeclass_1457198434', 'Angerclass_369684005']
	analyze_meta(image_url = image_url, local_file =local_file, api_key = api_key, classifier_ids = classifier_ids)



