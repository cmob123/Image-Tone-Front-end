from imageRanker import *
from classifier import *
from tone import tone_names
from dataOps import *
import sys
import numpy
import array
import ast

data_fieldnames = ["name", "actual_data", "classifier_data"]
data_fn = "data.csv"

def test_classifiers( vis_trainer, test_fn, data_dir ):
	#classify_data( vis_trainer, test_fn, data_dir )
	f_data = open( data_dir + data_fn )
	csvr_data = csv.DictReader( f_data )

	actual_emos = {tone : [] for tone in tone_names }
	class_emos = {tone : [] for tone in tone_names }

	for row in csvr_data:
		test_img = dict.fromkeys( data_fieldnames )
		test_img["actual_data"] = ast.literal_eval( row["actual_data"] )
		test_img["classifier_data"] = ast.literal_eval( row["classifier_data" ] )
		for k,v in test_img["actual_data"].items():
			actual_emos[k].append(v)
		for k,v in test_img["classifier_data"].items():
			class_emos[k].append(v)
	f_data.close()

	for tone in tone_names:
		print( "Correlation coefficient of {}: {}".format( tone, correlation_coefficient( class_emos[tone], actual_emos[tone] ) ) )

def classify_data( vis_trainer, test_fn, data_dir ):
	vis_trainer.set_classifiers( vis_trainer.get_classifier_ids() )
	f_data = open( data_dir + data_fn, "w", newline="" )
	csvw_data = csv.DictWriter( f_data, fieldnames= data_fieldnames )
	csvw_data.writeheader()

	test_imgr = ImageRanker( test_fn, data_dir )
	i = 0
	for img in test_imgr.images:
		i += 1
		url = img["url"]
		post_name = img["name"]
		actual_data = img["comment_data"]

		j = vis_trainer.classify_single_image( url )
		if( j is None ):
			continue

		classifier_data = {}
		try:
			for classifier in j["images"][0]["classifiers"]:
				name = classifier["classes"][0]["class"]
				score = classifier["classes"][0]["score"]
				classifier_data[ name ] = score
			img["classifier_data"] = classifier_data
		except KeyError as e:
			print( "KeyError: {} possibly because the image is too big".format( e ) )
			print( json.dumps( j, indent=2 ) )
			continue
		print( "Classified {} successfully. ({}/{})".format( url, i, len( test_imgr.images) ) )
		#print( classifier_data.keys() )
		#print( actual_data.keys() )
		sys.stdout.flush()
		assert( set( classifier_data.keys() ) == set( actual_data.keys() ) )
		row = {
			"name": post_name,
			"actual_data": actual_data,
			"classifier_data": classifier_data}
		try:
			csvw_data.writerow( row )
		except:
			print("Something went wrong writing a testing data row")
			print(sys.exc_info()[0])
			continue
	f_data.close()
	

