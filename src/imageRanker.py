# Goal of this file, check for existance of image/data file
#1) Check for existance of train.txt and test.txt
#1.5) If the don't exist, run reddittest.py to create them (TODO)
#2) Import data into internal data structures
#3) Preprocess the numbers in any way necessary. (Normalize, etc)
#4) Sort the data and save positive and negative examples into the ../data/ directory


import numpy
from dataOps import *

class ImageRanker:
	emo_names = ["Anger", "Disgust", "Fear", "Joy", "Sadness"]

	def __init__( self, image_file_name = "train.txt", data_dir = "../data/" ):
		self.data_dir = data_dir
		image_file = data_dir + image_file_name
		f = open( image_file, "r" )
		text = f.readline( )
		self.images = []
		self.scores = []
		#Pull scores and images out of the file
		while( text != "" ):
			self.images.append( text.strip() )
			text = f.readline()
			if( text != "" ):
				self.scores.append(eval ( "numpy.array(" +text + ")" ) )
			else:
				print( "Mismatch between number of images and number of scores, check your data")
				return
			text = f.readline()

		# Turns out that this is handy to have.
		self.emotions = numpy.transpose( self.scores )
		self.sort_pos_neg()
		return

	# Saves the images in the top and bottom 1/3
	# Any image not in *any* top 1/3 gets saved in a Negative_all file
	# As a side effect, prints the images with the highest score for each emotion

	# FUTURE JESSE: YOU NEED TO USE THE emo_bitmap COMPARED AGAINST [ 1/3 ] * 5 TO DETERMINE THE CLASSIFIERS EFFECTIVENESS
	def sort_pos_neg( self ):
		self.pos_imgs = [None]*5
		self.neg_imgs = [None]*5
		self.neg_all_imgs = []
		self.emo_bitmap = []
		for i in range( 0, len(self.images) ):
			self.emo_bitmap.append( [] )
		for i in range(0, len( self.emotions )):
			self.pos_imgs[i] = []
			self.neg_imgs[i] = []
			index = 0
			topThird = bisect( 2/3, self.emotions[i] )
			bottomThird = bisect( 1/3, self.emotions[i])
			for j in range(0, len( self.images ) ):
				bit = 0
				if( self.emotions[i][j] > topThird ):
					self.pos_imgs[i].append( self.images[j] )
					bit = 1
				elif( self.emotions[i][j] <= bottomThird ):
					self.neg_imgs[i].append( self.images[j] )
				self.emo_bitmap[j].append( bit )
		low_emo = self.find_low_emotion( )
		for e in low_emo:
			self.neg_all_imgs.append(e + "\n")
		return
	
	"""
	Writes the positive and negative file data to files in the data directory
	"""
	def write_pos_neg_files( self ):
		assert( len(self.neg_names) == len(self.pos_imgs) )
		assert( len(self.emo_names) == len(self.pos_imgs) )
		assert( self.data_dir is not None )
		for i in range( 0, len(pos_imgs) ):
			fplus = open( data_dir + "Positive_" + emo_names[i], "w" )
			fminus = open( data_dir + "Negative_" + emo_names[i], "w" )
			for img in pos_imgs[i]:
				fplus.write( img + "\n" )
			for img in neg_imgs[i]:
				fminus.write( img + "\n" )
		fneg = open( data_dir + "Negative_all", "w" )
		for img in neg_all_imgs:
			fneg.write( img + "\n" )
		fplus.close()
		fminus.close()


	"""
	Returns a list of all images that are below the cutoff percentage
	"""
	def find_low_emotion( self, cutoff = 2/3 ):
		assert( self.emotions is not None )
		assert( self.scores is not None )
		assert( self.images is not None )
		assert( len( self.scores ) == len( self.images ) )
		l = len( self.scores )
		avgs = list( map ( (lambda x: bisect( cutoff, x) ) , self.emotions) )
		#print( avgs )
		low_emo = []
		for i in range(0, l):
			is_low_emo = True
			for j in range( 0, len( self.scores[i]) ):
				if( self.scores[i][j] > avgs[j] ):
					is_low_emo = False
					break
			if( is_low_emo ):
				low_emo.append( self.images[i] )
		return low_emo
