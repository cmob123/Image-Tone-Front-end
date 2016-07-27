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
		print( "Pre-normalized:" )
		print( single_scores )
		print( "mean: " + str(numpy.mean(single_scores)) )
		print( "max: " + str(numpy.max(single_scores)) )
		print( "min: " + str(numpy.min(single_scores)) )
		print( "Standarized" )
		print( standard )
		print( "mean: " + str(numpy.mean(standard)) )
		print( "max: " + str(numpy.max(standard)) )
		print( "min: " + str(numpy.min(standard)) )
		#print( "Normalized" )
		#print( normal )
		#print( "mean: " + str(numpy.mean(normal)) )
		#print( "max: " + str(numpy.max(normal)) )
		#print( "min: " + str(numpy.min(normal)) )
	return standard

# Calculates the euclidian distance between 2 scores. Should be used for testing
# How good our classifier is
def dataDistance( score1, score2 ):
	s = sum( map( (lambda x, y: (x - y)**2), score1, score2))
	return  s**(0.5)

"""
returns the number that forms the percentile, based on the value of prop
For example, if prop is 0.5, the number returned will be approximately the median
If prop is 0.33, the number returned will be larger than 33% of the sample, and smaller than 67%
"""
def bisect( prop, num_list ):
	assert( prop <= 1.0 )
	assert( prop >= 0.0 )
	length = len( num_list )
	sorted = numpy.sort( num_list )
	return sorted[int( length * prop )]

"""
Calculates the correlation coefficient between two lists of data
The lists should of course be the same length
"""
def correlation_coefficient( arr1, arr2 ):
	length = len( arr1 )
	assert( length == len( arr2 ) )
	x_sum = 0
	y_sum = 0
	xx_sum = 0
	yy_sum = 0
	xy_sum = 0
	for j in range( 0, length ):
		x = arr1[j]
		y = arr2[j]
		x_sum += x
		y_sum += y
		xy_sum += x*y
		xx_sum += x*x
		yy_sum += y*y
	x_mean = x_sum / length
	y_mean = y_sum / length
	numer = (xy_sum) - (length * x_mean * y_mean)
	denom = ( (xx_sum) - (length * x_mean * x_mean ) )**(1/2)
	denom *=( (yy_sum) - (length * y_mean * y_mean ) )**(1/2)
	#print("Numerator is {}".format( numer ) )
	#print("Denom is {}".format( denom ) )
	return numer / denom


"""
prints some useful information about a list of data
"""
def print_info( data ):
	print("Length: {}".format( len(data) ) )
	print("Min: {}".format( numpy.min(data) ) )
	print("Max: {}".format( numpy.max(data) ) )
	print("Mean: {}".format( numpy.mean(data) ) )
	print("StdDev: {}".format( numpy.std( data ) ) )
	return

