#Visual Sentiment Analysis using Watson APIs and Data from reddit.com

Interfacing with the reddit API
-------------------------------

Rather than interacting with the reddit API directly, we will use a prebuilt python interface called [PRAW](https://github.com/praw-dev/praw)

Install using the python package manager, pip:  
`$pip install PRAW`

See redditDataGetter.py

__TODO__:fill in more later


Intro to Watson Tone Analyzer API
---------------------------------

Before you can use the Watson APIs, you must create a bluemix account [here](http://www.ibm.com/cloud-computing/bluemix/).

After that, you should create use the tone analyzer service. Add it to your dashboard and copy the service credentials.

There is an api reference [here](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/tone-analyzer/api/v3/?python#) that should help you get started. The tone analyzer is fairly simple to use. Since it is already trained, you can just pass in some text and get back a json-formatted response.

If you want to write your app in python, like we did, you'll want to use pip to download the watson-developer-cloud sdk. You can also download the sdk from [github](https://github.com/watson-developer-cloud/python-sdk). There are also libraries for java and nodeJS, or you use another language and make HTTP requests manually.

The class we wrote to do tone analysis this is in tone.py. The code is very simple.

For our purposes, the tone analyzer gives us a lot of data that we don't need.
We can discard personality and writing style data, as well as sentence-level analysis.
To trim our data, we run the following:

`emotions = raw_json['document_tone']['tone_categories'][0]['tones']`

where raw_json is the full response from the tone analyzer.
This should narrow down the JSON to look something like this:

`{
	"score": 0.25482,
	"tone_id": "anger",
	"tone_name": "Anger"
},
{
	"score": 0.345816,
	"tone_id": "disgust",
	"tone_name": "Disgust"
},
{
	"score": 0.121116,
	"tone_id": "fear",
	"tone_name": "Fear"
},
{
	"score": 0.078903,
	"tone_id": "joy",
	"tone_name": "Joy"
},
{
	"score": 0.199345,
	"tone_id": "sadness",
	"tone_name": "Sadness"
}`

Once you have the simplified JSON, you can extract the numerical scores using the JSON libraries

Intro to Watson Visual Classifer API
------------------------------------
Just like with the tone analyzer, you need to set up the service in Bluemix before you can get started. Be sure to save the service credentials.

The visual classifer API is significantly more complicated than the tone analysis, primarily because the default corpus is insufficient for our purposes, we must train our own.Again, there is an API reference [here](https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/visual-recognition/api/v3/), but as of when this was written, only curl examples are complete. We found it helpful to reference the python-sdk source code.

Watson's visual classifier, once trained, takes an image file or url, and outputs its confidence level that that image belongs in each of its pre-established classes. As an example, assume we have a classifier that hase been trained to recognize 2 classes of images, dogs and cats. If we give it a picture of a beagle, it may be 80% confident that that picture is a dog. However, it may also be 10% confident that it is a cat. By default, only 50%+ confidence levels are returned.

Training a classifier requires 2 things. Primarily, for each class of images you want the classifier to recognize, you need a zip file of examples. In our previous example, we would have trained the classifer with a zip file of dog images and a zip file containing cat images. More training data is always better, but as few as 10 training images can produce good results. The second thing you need is a zip file of negative examples. The only rule for negative examples is that they do not depict anything described by the other classes. In our dogs vs cats example, this could be pictures of horses, buildings, outer space, or anything else you like.

In the python-sdk, an example call to create a classifier looks like:

`create_cassifer( "Dog or Cat", dog_positive_examples=dogs_zipfile, cat_positive_examples=cats_zipfile, negative_examples=neg_zipfile)`

The *name*_positive_examples format is important. In our classifier.py file, you can see our wrapper for this function that uses exec to generate variable names for us. Feel free to use this.

Leveraging Watson APIs to Perform Visual Sentiment Analysis
-----------------------------------------------------------
We gathered data from the top 1000 all time posts on reddit.com/r/pics, saving the image url and the results of performing a tone analysis of the top 25 root level comments. (If there were were less than 25 root level comments, we used however many there were.) We did not consider albums or images not in .jpg format. We also did not consider the title of the post, which can often significantly affect the tone of the comments. In total, we were left with about 600 data points. We then split the data in half, using 50% for training and setting aside 50% for testing. This left us with about 300 posts worth of training data.

With this data, we partitioned the images by emotional scores. We saved the top third and bottom third in each emotional category. (about 100 images each.) We used these images sets to train 5 visual classifiers, one for each emotion, using the top third as the positive example, and the bottom third as the negative example.

Results
-------
__TODO__

Final Thoughts
--------------
How effective were we, what could we have done differently

More data

Different Sources

Different Classifier Schemes
