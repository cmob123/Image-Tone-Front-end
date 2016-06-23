from redditDataSaver import *
from imageRanker import *
from classifier import *
from testClassifiers import *


"""
r : download data from reddit into csv files
z : create zip files
c : retrain classifiers
t : test classifiers
l : list existing classifiers
q : quit
i : classify single image
? : view options

"""

def main():
	data_dir = input( "Enter data directory, leave blank for \'../data/\': " )
	if( data_dir == "" ):
		data_dir = "../data/"
	print(" - Using {} as data directory".format( data_dir ) )

	train_fn = input( "Enter the name of the training csv file, leave blank for \'train.csv\': " )
	if( train_fn == "" ):
		train_fn = "train.csv"
	print(" - Using {} as data file".format( data_dir + train_fn ) )

	test_fn = input( "Enter the name of the testing csv file, leave blank for \'test.csv\': " )
	if( test_fn == "" ):
		test_fn = "test.csv"
	print(" - Using {} as data file".format( data_dir + test_fn ) )

	if( get_response("Do you want to download new posts from reddit? (y/n) ") ):
		reddit_save_helper(data_dir, train_fn, test_fn)
	
	if( get_response("Do you need to download, sort, and zip image files? (y/n) ") ):
		i = ImageRanker( train_fn, data_dir )
		i.write_pos_neg_files()
		print( " - Writing new positive and negative files" )


	v = VisualTrainer()
	if( get_response("Do you want to delete all of your classifiers and train new ones? (y/n) ") ):
		v.rebuild_classifiers( data_dir = data_dir )
	

	print( " - All done, your classifiers should be ready to use shortly" )
	if( get_response( " - Do you want to test them (assuming they are ready? (y/n) " ) ):
		test_classifiers( v, test_fn, data_dir )

def get_response( question ):
	text = input(question)
	while( text != "y" and text != "n" ):
		text = input("(y/n) ")
	if( text == "y" ):
		return True
	else:
		return False




def reddit_save_helper(data_dir, train_fn, test_fn):
	# TODO: number of files, number of comments
	n_posts = 1000
	n_comments = 25
	print( " - This could take some time, go get lunch or something" )
	save_submissions( n_posts = n_posts, n_comments = n_comments, data_dir = data_dir, train_fn = train_fn, test_fn = test_fn)
	print( " - Finished saving reddit data" )


if( __name__ == "__main__" ):
	main()
