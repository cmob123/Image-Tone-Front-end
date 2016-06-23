# Goal of this file, check for existance of image/data file
#1) Check for existance of train.txt and test.txt
#1.5) If the don't exist, run reddittest.py to create them (TODO)
#2) Import data into internal data structures
#3) Preprocess the numbers in any way necessary. (Normalize, etc)
#4) Sort the data and save positive and negative examples into the ../data/ directory


import numpy
import csv
import ast
import os
import sys
import zipfile
import urllib.request
import random
from dataOps import *
from tone import tone_names

class ImageRanker:

	def __init__( self, csv_file_name = "data.csv", data_dir = "../data/" ):
		random.seed(0)
		self.data_dir = data_dir
		csv_fn = self.data_dir + csv_file_name
		csvfile = open( csv_fn )
		self.images = []
		self.num_emos = len( tone_names )
		csv_reader = csv.DictReader(csvfile)
		for row in csv_reader:
			new_img = {}
			new_img['id'] = int( row['arbitrary_id'] )
			new_img['url'] = row['url']
			#new_img['title'] = row['title']
			new_img['title_data'] = ast.literal_eval( row['title_data'] )
			#new_img['comments'] = row['comments']
			new_img['comment_data'] = ast.literal_eval( row['comment_data' ] )
			new_img['strong_emos'] = []
			new_img['weak_emos'] = []
			self.images.append( new_img )
		csvfile.close()
		scores = list( map( (lambda x: x['comment_data'] ), self.images ) )
		title_scores = list( map( (lambda x: x['title_data'] ), self.images ) )

		self.emotions = numpy.transpose( scores )
		assert( self.num_emos == len( self.emotions ) )
		self.title_emotions = numpy.transpose( title_scores )
		assert( self.num_emos == len( self.title_emotions ) )
		self.sort_pos_neg()
		return

	# Saves the images in the top and bottom 1/3
	# Any image not in *any* top 1/3 gets saved in a Negative_all file
	# As a side effect, prints the images with the highest score for each emotion
	def sort_pos_neg( self ):
		top_third_scores = list( map( (lambda x: bisect(2/3, x)), self.emotions ) )
		bot_third_scores = list( map( (lambda x: bisect(1/3, x)), self.emotions ) )
		self.pos_imgs = [[]] * self.num_emos
		self.neg_imgs = [[]] * self.num_emos
		for img in self.images:
			# Maybe exec?
			img_scores = img['comment_data']

			assert( len(img_scores) == self.num_emos )
			img['strong_emos'] = []
			img['weak_emos'] = []

			for i in range(0, self.num_emos ):
				# This handles the confidant case: 75% of images have confidance of 0.0, leaving too few images to create a confidance class. We fudge things here to make it work
				if( top_third_scores[i] == 0.0 and img_scores[i] == 0.0):
					if( random.choice( [True, False] ) ):
						img['strong_emos'].append( tone_names[i] )
						continue
				if( img_scores[i] <= bot_third_scores[i] ):
					img['weak_emos'].append( tone_names[i] )
					self.neg_imgs.append( img )
				elif( img_scores[i] > top_third_scores[i] ):
					img['strong_emos'].append( tone_names[i] )
					self.pos_imgs.append( img )
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
		# Create and open zip files
		pos_files = {}
		neg_files = {}
		for emo in tone_names:
			pos_files[emo] = zipfile.ZipFile( self.data_dir + emo + ".zip", "w", zipfile.ZIP_DEFLATED )
			neg_files[emo] = zipfile.ZipFile( self.data_dir + "neg-" + emo + ".zip", "w", zipfile.ZIP_DEFLATED )


		for img in self.images:
			new_filename = str( img['id'] ) + ".jpg"
			new_path = tmp_dir_name + new_filename

			sys.stdout.flush()
			if( not os.path.exists( new_path ) ):
				print("Downloading {} as {}".format( img['url'], new_path ) )
				try:
					urllib.request.urlretrieve(img['url'], new_path )
				# catch errors
				except urllib.error.HTTPError as e:
					print ("Error (HTTP): couldn't retrieve image at {}".format( img['url'] ))
					print( str( e ) )
					continue
				except urllib.error.URLError as e:
					print ("Error (URL): couldn't retrieve image at {}".format( img['url'] ))
					print( str(e) )
					continue
			# Got the file, now to add it to some zip files
			#TODO: Check if file size is 503 bytes. That is the size of "removed.png" in imgur. If so, don't bother using it
			for emo in img['strong_emos']:
				pos_files[emo].write( new_path, new_filename )
			for emo in img['weak_emos']:
				neg_files[emo].write( new_path, new_filename )

		for f in pos_files:
			pos_files[f].close()
		for f in neg_files:
			neg_files[f].close()


