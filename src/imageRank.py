# Goal of this file, check for existance of image/data file
#1) Check for existance of train.txt and test.txt
#1.5) If the don't exist, run reddittest.py to create them (TODO)
#2) Import data into internal data structures
#3) Preprocess the numbers in any way necessary. (Normalize, etc)
#4) Sort the data and save positive and negative examples into the ../data/ directory

import numpy
from dataOps import *

data_dir = "../data/"

emo_names = ["Anger", "Disgust", "Fear", "Joy", "Sadness"]
train_file = data_dir + "train.txt"
test_file = data_dir + "test.txt"

def main():
	images = []
	scores = []
	emotions = numpy.array([])
	train = open( train_file, "r" )
	text = train.readline( )
	#Pull scores and images out of the file
	while( text != "" ):
		images.append( text.strip() )
		text = train.readline( )
		if( text != "" ):
			scores.append(eval ( "numpy.array(" +text + ")" ) )
		else:
			print( "Mismatch between number of images and number of scores, check your data")
			return
		text = train.readline()

	# Turns out that this is handy to have.
	emotions = numpy.transpose( scores )
	


	# Print the images with the highest score for each emotion

	print( "Highest values" )
	for i in range(0, len(emotions)):
		fplus = open( data_dir + "Positive_" + emo_names[i], "w" )
		fminus = open( data_dir + "Negative_" + emo_names[i], "w" )
		index = 0
		maxScore = 0
		topThird = bisect( 2/3, emotions[i] )
		bottomThird = bisect( 1/3, emotions[i])
		for j in range(0, len( emotions[i] ) ):
			if( emotions[i][j] > maxScore ):
				maxScore = scores[j][i]
				index = j
			if( emotions[i][j] > topThird ):
				fplus.write( images[j] + "\n" )
			elif( emotions[i][j] <= bottomThird ):
				fminus.write( images[j] + "\n"  )
		fplus.close()
		fminus.close()

		print( emo_names[i] + ": " + images[index] )
	fneg = open( data_dir + "Negative_all", "w" )
	low_emo = lowEmotion( images, scores )
	#fneg.write( lowEmotion( images, scores ) )
	for e in low_emo:
		fneg.write( e + "\n")
	fneg.close()

if __name__ == "__main__":
    main()



