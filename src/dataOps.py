import numpy
import copy

# Takes in an array of floats in [0.0, 1.0]
# Returns a normalized array with a range of [0.0, 1.0]
# Will not correct left or right skew, average is not guaranteed to be 0.5, or anywhere close
# TODO: use numpy to do this right
def normalizeData( single_scores ):
	#This actually might require some statistics...
	standard = copy.deepcopy( single_scores )
	max_score = 0
	min_score = 1
	score_sum = 0
	length = len( single_scores )
	for score in single_scores:
		if( score > max_score ):
			max_score = score
		if( score < min_score ):
			min_score = score
		score_sum += score
	score_mult = 1 / (max_score - min_score)
	standard -= min_score
	standard *= score_mult
	mu = numpy.mean( standard )
	verbose = False
	#normal = list( map ( (lambda x: x + (x * (1-x))/(mu * (1-mu)) * (0.5-mu)), standard) )
	if( verbose ):
		print("Pre-normalized:")
		print( single_scores )
		print( "mean: " + str(numpy.mean(single_scores)) )
		print( "max: " + str(numpy.max(single_scores)) )
		print( "min: " + str(numpy.min(single_scores)) )
		print("Standarized")
		print( standard )
		print( "mean: " + str(numpy.mean(standard)) )
		print( "max: " + str(numpy.max(standard)) )
		print( "min: " + str(numpy.min(standard)) )
		#print("Normalized")
		#print( normal )
		#print( "mean: " + str(numpy.mean(normal)) )
		#print( "max: " + str(numpy.max(normal)) )
		#print( "min: " + str(numpy.min(normal)) )
	return standard

# Calculates the euclidian distance between 2 scores. Should be used for testing
# How good our classifier is
def dataDistance( score1, score2 ):
	s = sum( map( (lambda x, y: (x - y)**2 ), score1, score2))
	return  s**(0.5)

# returns all images that are in the bottom 50% of all emotion scores
def lowEmotion( images, scores ):
	l = len( scores )
	emotions = numpy.transpose( scores )
	avgs = list( map ( (lambda x: bisect( 2/3, x) ) , emotions) )
	low_emo = []
	for i in range(0, l):
		is_low_emo = True
		for j in range( 0, len(scores[i])):
			if( scores[i][j] > avgs[j] ):
				is_low_emo = False
				break
		if( is_low_emo ):
			low_emo.append( images[i] )
	return low_emo

def bisect( prop, scores ):
	length = len(scores)
	sorted = numpy.sort( scores )
	return sorted[int( length * prop )]
	

