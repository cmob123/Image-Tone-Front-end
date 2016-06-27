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
from pprint import pprint
import urllib.request
import functools
import random
from dataOps import *
from tone import tone_names

class ImageRanker:

	def __init__( self, csv_file_name="data.csv", data_dir="../data/" ):
		random.seed(0)
		self.data_dir = data_dir
		csv_fn = self.data_dir + csv_file_name
		csvfile = open( csv_fn )
		self.images = []
		csv_reader = csv.DictReader(csvfile)
		self.emotions = {tone : [] for tone in tone_names }
		self.title_emotions = {tone : [] for tone in tone_names }
		for row in csv_reader:
			new_img = {}
			new_img["name"] = row["name"]
			new_img["id"] = int( row["arbitrary_id"] )
			new_img["url"] = row["url"]
			#new_img["title"] = row["title"]
			#new_img["comments"] = row["comments"]
			new_img["title_data"] = ast.literal_eval( row["title_data"] )
			new_img["comment_data"] = ast.literal_eval( row["comment_data" ] )
			for tone in tone_names:
				self.emotions[tone].append(new_img["comment_data"][tone])
				self.title_emotions[tone].append( new_img["title_data"][tone] )
			new_img["strong_tones"] = []
			new_img["weak_tones"] = []
			self.images.append( new_img )
		csvfile.close()

		assert( set(tone_names) == set(self.emotions.keys()) )
		assert( set(tone_names) == set(self.title_emotions.keys()) )
		self.sort_pos_neg()
		return

	"""
	Sorts the images in the top and bottom 1/3 of each emotion
	Also fills the image keys "strong_tones" and "weak_tones"
		based on whether they are in the top or bottom 1/3
	"""
	def sort_pos_neg( self ):
		#TODO, why are these all the same
		top_third_scores = dict.fromkeys( self.emotions.keys() )
		bot_third_scores = dict.fromkeys( self.emotions.keys() )
		for k,v in self.emotions.items():
			top_third_scores[k] = bisect( 2/3, v )
			bot_third_scores[k] = bisect( 1/3, v )
		#print( top_third_scores )
		#print( bot_third_scores )
		for img in self.images:
			# Maybe exec?
			img_scores = img["comment_data"]

			assert( set( tone_names ) == set( img_scores.keys() ) )
			img["strong_tones"] = []
			img["weak_tones"] = []

			for tone in tone_names:
				# This handles the confidant case: 75% of images have confidance of 0.0, leaving too few images to create a confidance class. We fudge things here to make it work
				if( bot_third_scores[tone] == 0.0 and img_scores[tone] == 0.0):
					r = random.random( )
					# Confidance is pretty rare on the internet
					# If we take all weakly confidant images, the file is too big
					# So we only take half of them
					# The exact number might need to be adjusted with more data
					# It's pretty trial and error
					if( r < 1/2 ):
						img["weak_tones"].append( tone )
				elif( img_scores[tone] <= bot_third_scores[tone] ):
					img["weak_tones"].append( tone )
				elif( img_scores[tone] > top_third_scores[tone] ):
					img["strong_tones"].append( tone )
		return
	
	"""
	Downloads all image files that were loaded by __init__ into a tmp directory
	Based on their "[strong|weak]_tones" tags, it creates zip files
	Containing positive and negative examples of the tone
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
		pos_files = dict.fromkeys( tone_names )
		neg_files = dict.fromkeys( tone_names )
		# Create and open zip files
		for tone in tone_names:
			pos_files[tone] = zipfile.ZipFile( self.data_dir+tone+".zip", "w", zipfile.ZIP_DEFLATED )
			neg_files[tone] = zipfile.ZipFile( self.data_dir+"neg-"+tone+".zip", "w", zipfile.ZIP_DEFLATED )


		for img in self.images:
			new_filename = str( img["name"] ) + ".jpg"
			new_path = tmp_dir_name + new_filename

			sys.stdout.flush()
			if( not os.path.exists( new_path ) ):
				print( "Downloading {} as {}".format( img["url"], new_path )  )
				try:
					urllib.request.urlretrieve( img["url"], new_path  )
				# catch errors
				except urllib.error.HTTPError as e:
					print( "Error (HTTP): couldn't retrieve image at {}".format( img["url"] ) )
					print( str( e ) )
					continue
				except urllib.error.URLError as e:
					print( "Error (URL): couldn't retrieve image at {}".format( img["url"] ) )
					print( str(e) )
					continue

			# Got the file, now to add it to some zip files
			#TODO: Check if file size is 503 bytes. That is the size of "removed.png" in imgur. If so, don't bother using it
			# The reason we use new_path and new_filename is due to the way
			# "/"s vs "\"s are resolved by the zipfile module
			for emo in img["strong_tones"]:
				pos_files[emo].write( new_path, new_filename )
			for emo in img["weak_tones"]:
				neg_files[emo].write( new_path, new_filename )

		for k,v in pos_files.items():
			v.close()
		for k,v in neg_files.items():
			v.close()
