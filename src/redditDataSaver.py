import praw
import json
import time
import sys
import csv
from pprint import pprint
from tone import ToneAnalyzer

# Pulls in the top posts to r/pics
# For each post, stores the image link, and retrieves the top 10 root level comments
# The 10 comments are sent to the Watson tone analyzer, and the scores are saved
# Each image-tone pair is saved randomly in either a training set or a testing set

fieldnames = ['arbitrary_id', 'url', 'title', 'title_data', 'comments', 'comment_data']

def main():
	save_submissions( n_posts = 10000, n_comments = 25, data_dir = "../data/", data_fn = "data.csv")


def save_submissions( n_posts, n_comments = 25, data_dir = "../data/", data_fn = "data.csv" ):
	print( "Gathering submissions" )
	agent = praw.Reddit( user_agent='Comment-picture associator' )
	submissions = agent.get_subreddit( 'pics' ).get_top_from_all( limit=n_posts )
	print( "Finished getting submissions" )
# I'm not sure why these flush() calls are needed, but if they aren't there, nothing gets printed until the end
	sys.stdout.flush()

	# change to a if we want to append instead of overwrite
	data_file = open(data_dir + data_fn, "w", newline='' )
	csv_writer = csv.DictWriter( data_file, fieldnames=fieldnames)
	csv_writer.writeheader()
	t = ToneAnalyzer()
	n_records = 0
	n_submissions = 0
	# This guarantees that we will always get the same testing and training data

	for x in submissions:
		print( "Trying submission {}".format( n_submissions ) )
		sys.stdout.flush()
		n_submissions += 1
		try:
			# Make sure each image is a single .jpg, not an album or a .gif
			if( (x.url[-4:] != ".jpg") and (x.url[-4:] != ".png") ):
				continue

			comment_tree = x.comments
			comment_concat = ""
			# TODO: use n_comments, or the number of root comments, whichever is smaller
			num_comments = len( comment_tree ) - 1
			if( num_comments > n_comments ):
				num_comments = n_comments
			for i in range( 0, num_comments ):
				try:
					string = str( vars( comment_tree[i] )['body'] )
					comment_concat += string
				except:
					print( sys.exc_info() )
					continue

			tone = t.tone_analyze( comment_concat )
			comment_data = t.tone_all_num_extract( tone )
			title_tone = t.tone_analyze( x.title )
			title_data = t.tone_all_num_extract( title_tone )
			post_data = {'arbitrary_id': n_records, 'url': x.url, 'title': x.title, 'title_data': title_data, 'comments': comment_concat, 'comment_data': comment_data}

			csv_writer.writerow( post_data )


			print("Wrote record {}".format( n_records) )
			sys.stdout.flush()
			n_records += 1
		except UnicodeEncodeError as e:
			print("Unicode error, cannot save this submission, sorry")
			continue
		except:
			print(sys.exc_info())
			continue
		sys.stdout.flush()
	data_file.close()

if __name__ == "__main__":
    main()
