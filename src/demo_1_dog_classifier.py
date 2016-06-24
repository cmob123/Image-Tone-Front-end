# This moduel include information and sample codes for 
# accessing VR service on Bluemix.


import os
import json
from watson_developer_cloud import VisualRecognitionV3

# Here are the parameters required to apply a pre-trained
# classifer which can recognized pictures of dogs, better for beagles.

# The two parameters can be used in codes writing in other 
# language, e.g. Jave, Javascript, et. 

# If you want to try different classifers, replace parameter 
# values with new ones.  
api_key = "dfb48eeb05a0258553c5aa5371426e50cee88bc9"
classifier_id='dogs_train_small_data_981092928'

# Create a visual recgonition instance
vr = VisualRecognitionV3('2016-05-20', api_key=api_key)

# Analyze a picture on web
# You can replce the url link of your interest.
url = 'http://cdn3-www.dogtime.com/assets/uploads/2011/01/file_23012_beagle.jpg'

rlt = vr.classify(images_url = url, classifier_ids=classifier_id)
print(json.dumps(rlt, indent = 2))

# Analyze a picture in local disk
# There is a sample jpg file in the data_pics folder on github
# Download it to your local disk and get the absolute file path
file_path_name = 'absolute path and file name'
with open(file_path_name, 'rb') as file:
	rlt = vr.classify(images_file = file, classifier_ids=classifier_id)
	print(json.dumps(rlt, indent = 2))




# The result returns as a json file. See an example below
# If it returns no classifaction information,
# it means the classifer takes that the picture has now or few relation
# to the class of interest

# {
#   "images_processed": 0,
#   "images": [
#     {
#       "classifiers": [
#         {
#           "classifier_id": "dogs_train_small_data_981092928",
#           "name": "dogs_train_small_data",
#           "classes": [
#             {
#               "score": 0.654941,
#               "class": "dogs"
#             }
#           ]
#         }
#       ],
#       "source_url": "http://cdn3-www.dogtime.com/assets/uploads/2011/01/file_23012_beagle.jpg",
#       "resolved_url": "http://cdn3-www.dogtime.com/assets/uploads/2011/01/file_23012_beagle.jpg"
#     }
#   ]
# }

