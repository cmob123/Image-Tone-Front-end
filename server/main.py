try:
	from redditDataSaver import *
	from imageRanker import *
	from classifier import *
	from testClassifiers import *
except ImportError:
	from .redditDataSaver import *
	from .imageRanker import *
	from .classifier import *
	from .testClassifiers import *


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

class Main:
	def __init__(self):
		self.v = VisualTrainer()
		#self.update_files()
		self.test_fn = "test.csv"
		self.train_fn = "train.csv"
		self.data_dir = "./data/"


	def main(self):
		self.view_options()
		while( True ):
			text = input( "> " )
			if( text == "?" ):
				self.view_options()
			elif( text == "r" ):
				self.reddit_save_helper( self.data_dir, self.train_fn, self.test_fn, v=self.v )
			elif( text == "z" ):
				i = ImageRanker( self.train_fn, self.data_dir )
				i.write_pos_neg_files()
			elif( text == "d" ):
				tmp = input( "Classifier id? " )
				self.v.del_classifier( tmp )
				#self.v.del_all_classifiers()
			elif( text == "c" ):
				# The may want to delete classifiers first
				self.v.rebuild_classifiers()
				self.v.set_classifiers( self.v.get_classifier_ids() )
			elif( text == "l" ):
				self.v.list_classifiers()
			elif( text == "i" ):
				url = input(" url? : ")
				self.v.set_classifiers( self.v.get_classifier_ids() )
				j = self.v.classify_single_image( url )
				if( j is not None ):
					#print( json.dumps( j, indent=2 ) )
					self.v.pp_classify_response( j )
			elif( text == "f" ):
				self.update_files()
			elif( text == "t" ):
				self.v.set_classifiers( self.v.get_classifier_ids() )
				test_classifiers( self.v, self.test_fn, self.data_dir )
			elif( text == "q" ):
				break
			else:
				self.view_options()


	def view_options(self):
		print( "f : update data directory and file names" )
		print( "r : download data from reddit into csv files" )
		print( "z : create zip files" )
		print( "d : delete existing classifiers" )
		print( "c : retrain classifiers" )
		print( "t : test classifiers" )
		print( "l : list existing classifiers" )
		print( "i : classify single image" )
		print( "? : view options" )
		print( "q : quit" )


	"""
	Prompts the user to update test and train files, as well
	as the data directory.
	If this was going to see widespread use, I would have a submenu,
		but it isn't, so won't
	"""
	def update_files( self ):
		self.data_dir = input( "Enter data directory, leave blank for './data/': " )
		if( self.data_dir == "" ):
			self.data_dir = "./data/"
		print(" - Using {} as data directory".format( self.data_dir ) )

		self.train_fn = input( "Enter the name of the training csv file, leave blank for 'train.csv': " )
		if( self.train_fn == "" ):
			self.train_fn = "train.csv"
		print(" - Using {} as data file".format( self.data_dir + self.train_fn ) )

		self.test_fn = input( "Enter the name of the testing csv file, leave blank for 'test.csv : " )
		if( self.test_fn == "" ):
			self.test_fn = "test.csv"
		print(" - Using {} as data file".format( self.data_dir + self.test_fn ) )


	"""
	Sets up some of the messy stuff before we call redditDataSaver's functions
	"""
	def reddit_save_helper( self, data_dir, train_fn, test_fn, v ):
		n_posts = ""
		while( True ):
			str_n_posts = input( "How many records do you want to retrieve? ")
			try:
				n_posts = int( str_n_posts )
				break
			except ValueError:
				continue
		n_comments = 25
		print( " - This could take some time, go get lunch or something" )
		v.set_classifiers(None)
		save_submissions( n_posts=n_posts, n_comments=n_comments, data_dir=data_dir, train_fn=train_fn, test_fn=test_fn, v=v )
		print( " - Finished saving reddit data" )


if( __name__ == "__main__" ):
	m = Main()
	m.main()