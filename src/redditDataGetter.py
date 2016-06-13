import praw
import json
import random
from pprint import pprint
from tone import ToneAnalyzer

# Pulls in the top posts to r/pics
# For each post, stores the image link, and retrieves the top 10 root level comments
# The 10 comments are sent to the Watson tone analyzer, and the scores are saved
# Each image-tone pair is saved randomly in either a training set or a testing set
n_submissions = 1000

training = "train.txt"
testing = "test.txt"

def main():
	agent = praw.Reddit( user_agent='Comment-picture associator' )
	submissions = agent.get_subreddit( 'pics' ).get_top_from_all( limit=n_submissions )

	# change to a if we want to append instead of overwrite
	train = open(training, "w" )
	test = open(testing, "w" )
	t = ToneAnalyzer()

	for x in submissions:
		# Make sure each image is a single .jpg, not an album or a .gif
		if( x.url[-4:] != ".jpg" ):
			continue

		comment_tree = x.comments
		comment_concat = ""
		for i in range( 0, 10 ):
			comment_concat += str( vars( comment_tree[i] )['body'] ) + "\n"

		tone = t.tone_analyze( comment_concat )
		emotions = t.extract_emotions( tone )
		info = x.url + "\n" + str( ( t.emotions_num_extract( emotions ) )) + "\n"
		f = random.choice( [test, train] )
		f.write( info )
	train.close()
	test.close()

if __name__ == "__main__":
    main()
