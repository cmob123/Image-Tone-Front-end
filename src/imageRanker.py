# Goal of this file, check for existance of image/data file
#1) Check for existance of train.txt and test.txt
#1.5) If the don't exist, run reddittest.py to create them (TODO)
#2) Import data into internal data structures
#3) Preprocess the numbers in any way necessary. (Normalize, etc)
#4) Sort the data and save positive and negative examples into the ../data/ directory


import numpy
import csv
import ast
from dataOps import *
from tone import tone_names
from redditDataSaver import fieldnames

#fieldnames = ['arbitrary_id', 'url', 'title', 'title_data', 'comments', 'comment_data']

class ImageRanker:

	def __init__( self, csv_file_name = "data.csv", data_dir = "../data/" ):
		self.data_dir = data_dir
		csv_fn = data_dir + csv_file_name
		csvfile = open( csv_fn )
		self.images = []
		csv_reader = csv.DictReader(csvfile)
		print( csv_reader.fieldnames )
		for row in csv_reader:
			print( row['url'] )
			print( row['comment_data'] )
			data_list = ast.literal_eval( row['comment_data'] )
			print( len( data_list ) )
			self.images.append( row )
			input()
		self.scores = list( map( (lambda x: x['comment_data'] ), self.images ) )
		self.title_scores = list( map( (lambda x: x['title_data'] ), self.images ) )

		self.emotions = numpy.transpose( self.scores )
		self.title_emotions = numpy.transpose( self.scores )
		self.sort_pos_neg()
		return

	# Saves the images in the top and bottom 1/3
	# Any image not in *any* top 1/3 gets saved in a Negative_all file
	# As a side effect, prints the images with the highest score for each emotion
	def sort_pos_neg( self ):
		self.pos_imgs = []*5
		self.neg_imgs = []*5
		self.neg_all_imgs = []
		top_third_scores = list( map( (lambda x: bisect(2/3, x)), self.emotions ) )
		bot_third_scores = list( map( (lambda x: bisect(1/3, x)), self.emotions ) )
		for img in self.images:
			# Maybe exec?
			img_scores = list( img['comment_data'] )

			assert( len(img_scores) == len( self.emotions ) )

			is_low_emo = True
			for i in range(0, len( img_scores ) ):
				if( img_scores[i] <= bot_third_scores[i] ):
					self.neg_imgs[i].append( img ) 
				elif( img_scores[i] > top_third_scores[i] ):
					self.pos_imgs[i].append( img )
					is_low_emo = False
			if( is_low_emo ):
				self.neg_all_imgs.append( img )
		return
	
	"""
	Writes the positive and negative file data to files in the data directory
	"""
	def write_pos_neg_files( self ):
		tmp_dir_name = self.data_dir + "tmp/"
		try:
			if( not os.path.exists(tmp_dir_name) ):
				os.makedirs( tmp_dir_name )
		except OSError as e:
			print("Could not make temporary directory, no files created:")
			print( e.exc_info() )
			return
		for img in self.images:
			try:
				urllib.request.urlretrieve(img['url'], tmp_dir_name+str(img['id']+".jpg"))
			# catch errors
			except urllib.error.HTTPError:
				print ("Error (HTTP): couldn't retrieve image at line", count+1)
			except urllib.error.URLError:
				print ("Error (URL): couldn't retrieve image at line", count+1)
