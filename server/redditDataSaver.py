import praw
import time
import sys
import csv
import time
import random
import math
try:
	from tone import ToneAnalyzer
	from classifier import VisualTrainer
except ImportError:
	from .tone import ToneAnalyzer
	from .classifier import VisualTrainer


# Pulls in the top posts to r/pics
# For each post, stores the image link, and retrieves the top 10 root level comments
# The 10 comments are sent to the Watson tone analyzer, and the scores are saved
# Each image-tone pair is saved randomly in either a training set or a testing set

fieldnames = [
	"name", "arbitrary_id", "url", "title", 
	"title_data", "comments", "comment_data",
	"default_classifier_data"]

def main():
	save_submissions( n_posts=2048, n_comments=25, data_dir="./data/", train_fn="train.csv", test_fn="test.csv", v=VisualTrainer())


"""
Pulls down top posts from reddit
Analyzes the comments, and extracts tone data using the Watson APIs
Saves ~50% of the data in a training file (using a repeatably seeded prng)
Saves the rest in a testing file
"""
def save_submissions( n_posts, n_comments = 25, data_dir = "./data/", train_fn = "train.csv", test_fn = "test.csv", v=VisualTrainer() ):
	print( "Retrieving {} data points from r/pics".format( n_posts ) )
	sys.stdout.flush()

	# change to a if we want to append instead of overwrite
	f_train = open( data_dir+train_fn, "w", newline="" )
	csvw_train = csv.DictWriter( f_train, fieldnames=fieldnames )
	csvw_train.writeheader()
	f_test = open( data_dir+test_fn, "w", newline="" )
	csvw_test = csv.DictWriter( f_test, fieldnames=fieldnames )
	csvw_test.writeheader()
	t = ToneAnalyzer()
	c_records = 0
	c_posts = 0
	# Current timestamp
	ts_now = int(time.time())
	# timestamp from 2011-1-1 @ 00:00:00
	ts_first = 1388534400
	n_max_step_posts = 500
	n_steps = int( math.ceil( n_posts / n_max_step_posts ) )
	ts_step_size = (ts_now - ts_first) / n_steps
	ts_step = ts_now

	agent = praw.Reddit( user_agent="Comment-picture associator" )

	# This guarantees that we will always get the same testing and training data
	random.seed(0)
	while( True ):
		c_step_posts = 0
		str_timestamp_range = "{}..{}".format( int( ts_step - ts_step_size ), int(ts_step) )
		print("Current timestamp range is " + str_timestamp_range)
		print("c_posts = {}".format( c_posts ) )
		str_search = "timestamp:" + str_timestamp_range
		submissions = agent.search( str_search, subreddit="pics", sort="top", limit=None, syntax="cloudsearch" )
		ts_step -= ts_step_size
		for sub in submissions:
			print( "Retriving post {}".format( c_posts ) )
			sys.stdout.flush()
			c_step_posts += 1
			c_posts += 1

			#Process the image, returns true if it processed successfully
			if( process_post( sub, t, random.choice( [csvw_train, csvw_test] ), n_comments, c_records, v ) ):
				c_records += 1
				print( "Wrote record {}".format( c_records ) )
				sys.stdout.flush()

			if( c_step_posts >= n_max_step_posts ):
				break
			if( c_posts >= n_posts ):
				f_train.close()
				f_test.close()
				return

"""
Processes a reddit image post, extracting comment data and storing it
	in a csv file with a link to the image
This csv file (once filled) is used to test and train visual classifiers
"""
def process_post( sub, ta, csvw_choice, n_comments, id_to_use, vis_classifier ):
	if(len(sub.url) < 4):
		return False
	if( (sub.url[-4:] != ".jpg") and (sub.url[-4:] != ".png") ):
		return False
	try:
		comment_tree = sub.comments
		comment_concat = ""
		c_post_comments = len( comment_tree ) - 1
		if( c_post_comments > n_comments ):
			c_post_comments = n_comments
		for i in range( 0, c_post_comments ):
			if( "body" in vars( comment_tree[i] ) ):
				comment_concat += str( vars( comment_tree[i] )["body"] )
	except:
		print( "Error getting comments, are we being throttled by reddit?" )
		print( sys.exc_info()[0] )
		if( comment_concat == "" ):
			return False

	tone = ta.tone_analyze( comment_concat )
	comment_data = ta.tone_all_num_extract( tone )
	title_tone = ta.tone_analyze( sub.title )
	title_data = ta.tone_all_num_extract( title_tone )

	j = vis_classifier.classify_single_image( sub.url )
	if( j is None ):
		return False
	d_tmp = vis_classifier.dict_from_json( j )
	if( d_tmp is None ):
		return False

	post_data = { 
		"name": sub.name,
		"arbitrary_id": id_to_use,
		"url": sub.url,
		"title": sub.title,
		"title_data": title_data,
		"comments": comment_concat,
		"comment_data": comment_data,
		"default_classifier_data": d_tmp}
		
	try:
		csvw_choice.writerow( post_data )
	except UnicodeEncodeError as e:
		print("Unicode error, cannot save this submission, sorry")
		return False
	except:
		print("Something went wrong processing this post")
		print(sys.exc_info()[0])
		return False
	return True

if __name__ == "__main__":
    main()