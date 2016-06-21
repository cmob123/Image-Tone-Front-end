import praw
import json
import random
import time
import sys
from pprint import pprint
from tone import ToneAnalyzer

# Pulls in the top posts to r/pics
# For each post, stores the image link, and retrieves the top 10 root level comments
# The 10 comments are sent to the Watson tone analyzer, and the scores are saved
# Each image-tone pair is saved randomly in either a training set or a testing set

data_dir = "../data/"
n_posts = 10000
n_comments = 25

training = "train2.txt"
testing = "test2.txt"

def main():

	print( "Gathering submissions" )
	agent = praw.Reddit( user_agent='Comment-picture associator' )
	submissions = agent.get_subreddit( 'pics' ).get_top_from_all( limit=n_posts )
	print( "Finished getting submissions" )
# I'm not sure why these flush() calls are needed, but if they aren't there, nothing gets printed until the end
	sys.stdout.flush()

	# change to a if we want to append instead of overwrite
	train = open(data_dir + training, "w" )
	test = open(data_dir + testing, "w" )
	t = ToneAnalyzer()
	n_records = 0

	for x in submissions:
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
			print( num_comments )
			sys.stdout.flush()
			f = random.choice( [test, train] )
			f.write( x.url )
			f.write( "\n" )
			for i in range( 0, num_comments ):
				try:
					string = str( vars( comment_tree[i] )['body'] )
					f.write(string)
					f.write("\n")
					comment_concat += string
				except:
					#print( sys.exc_info() )
					#print( "Problems were encountered appending {}".format(vars( comment_tree[i])['body'] ) )
					continue

			tone = t.tone_analyze( comment_concat )
			emotions = t.extract_emotions( tone )
			f.write( str( t.emotions_num_extract( emotions ) ) )
			f.write("\n==========================================================\n")
			print("Wrote record {}".format( n_records) )
			sys.stdout.flush()
			n_records += 1
		except:
			print( sys.exc_info() )
			continue
	train.close()
	test.close()

if __name__ == "__main__":
    main()
