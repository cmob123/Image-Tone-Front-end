import praw
import json
import time
import sys
import csv
import random
from pprint import pprint
from tone import ToneAnalyzer

# Pulls in the top posts to r/pics
# For each post, stores the image link, and retrieves the top 10 root level comments
# The 10 comments are sent to the Watson tone analyzer, and the scores are saved
# Each image-tone pair is saved randomly in either a training set or a testing set

fieldnames = ['arbitrary_id', 'url', 'title', 'title_data', 'comments', 'comment_data']

def main():
	save_submissions( n_posts = 10000, n_comments = 25, data_dir = "../data/", data_fn = "data.csv")


def save_submissions( n_posts, n_comments = 25, data_dir = "../data/", train_fn = "train.csv", test_fn = "test.csv" ):
	print( "Gathering the top {} posts from r/pics".format( n_posts ) )
	agent = praw.Reddit( user_agent='Comment-picture associator' )
	submissions = agent.get_subreddit( 'pics' ).get_top_from_all( limit=n_posts )
# I'm not sure why these flush() calls are needed, but if they aren't there, nothing gets printed until the end
	sys.stdout.flush()

	# change to a if we want to append instead of overwrite
	train_file = open(data_dir + train_fn, "w", newline='' )
	train_csv_writer = csv.DictWriter( train_file, fieldnames=fieldnames)
	train_csv_writer.writeheader()
	test_file = open(data_dir + test_fn, "w", newline='' )
	test_csv_writer = csv.DictWriter( test_file, fieldnames=fieldnames)
	test_csv_writer.writeheader()
	t = ToneAnalyzer()
	records_count = 0
	posts_count = 0
	# This guarantees that we will always get the same testing and training data

	random.seed(0)
	for x in submissions:
		print( "Retriving post {}".format( posts_count ) )
		sys.stdout.flush()
		posts_count += 1
		# Make sure each image is a single image, not an album or a .gif
		if( (len(x.url) < 4) or ((x.url[-4:] != ".jpg") and (x.url[-4:] != ".png"))):
			continue

		try:
			comment_tree = x.comments
			comment_concat = ""
			num_comments = len( comment_tree ) - 1
			if( num_comments > n_comments ):
				num_comments = n_comments
			for i in range( 0, num_comments ):
				if( "body" in vars( comment_tree[i] ) ):
					comment_concat += str( vars( comment_tree[i])["body"])
		except:
			print( "Error getting comments, are we being throttled by reddit?" )
			print( sys.exc_info() )
			if( comment_concat == "" ):
				continue

		tone = t.tone_analyze( comment_concat )
		comment_data = t.tone_all_num_extract( tone )
		title_tone = t.tone_analyze( x.title )
		title_data = t.tone_all_num_extract( title_tone )
		post_data = {'arbitrary_id': records_count, 'url': x.url, 'title': x.title, 'title_data': title_data, 'comments': comment_concat, 'comment_data': comment_data}
			
		try:
			csv_writer = random.choice( [train_csv_writer, test_csv_writer] )

			csv_writer.writerow( post_data )
		except UnicodeEncodeError as e:
			print("Unicode error, cannot save this submission, sorry")
			continue
		except:
			print("Something went wrong processing this post")
			print(sys.exc_info()[0])
			continue

		print("Wrote record {}".format( records_count) )
		records_count += 1
		sys.stdout.flush()
	train_file.close()
	test_file.close()

if __name__ == "__main__":
    main()
