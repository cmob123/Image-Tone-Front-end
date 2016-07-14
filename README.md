#Visual Sentiment Analysis using Watson APIs and Data from reddit.com

Interfacing with the reddit API
-------------------------------

Rather than interacting with the reddit API directly, we will use a prebuilt python interface called [PRAW](https://github.com/praw-dev/praw)

Install using pip:
`$pip install PRAW`

By default, api responses are limited to 1000 entries. This is a hard limit imposed by reddit, and it is not designed to be circumvented. The only way to get more responses is to use the timestamp feature to search by time range. See the code in redditDataGetter.py for an implementation. Using this feature, we are able to collect data from more than 1000 posts.

Intro to Watson Tone Analyzer API
---------------------------------

Before you can use the Watson APIs, you must create a bluemix account [here](http://www.ibm.com/cloud-computing/bluemix/).

After that, you should create use the tone analyzer service. Add it to your dashboard and copy the service credentials.

There is an api reference [here](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/tone-analyzer/api/v3/?python#) that should help you get started. The tone analyzer is fairly simple to use. Since it is already trained, you can just pass in some text and get back a json-formatted response.

If you want to write your app in python, like we did, you'll want to use pip to download the watson-developer-cloud sdk. You can also download the sdk from [github](https://github.com/watson-developer-cloud/python-sdk). There are also libraries for java and nodeJS, or you use another language and make HTTP requests manually.

Tone data is returned for 13 tone markers, further subdivided into 3 broad categories.

Emotion: Anger, Disgust, Fear, Joy, Sadness
Writing Style: Analytic, Confident, Tentative
Personality: Agreeableness, Conscientiousness, Emotional Range, Extraversion, Openness

We saved all 13 markers, but our app only displays the five results from the emotion category.

The tone analyzer returns document-level as well as sentence-level tone data. We discarded the sentence level data and stored the document-level results.

`document_level_data = raw_json['document_tone']`

Where raw_json is the json struct returned by the Watson API call

We then further processed the information into a python dict that looked like:

`{"Anger":0.104957, "Disgust":0.3658, ... }`

See the src/tone.py file for more information.


Intro to Watson Visual Classifer API
------------------------------------

Just like with the tone analyzer, you need to set up the service in Bluemix before you can get started. Be sure to save the service credentials.

The visual classifer API is significantly more complicated than the tone analysis, primarily because the default corpus is insufficient for our purposes, so we have to train our own. Again, there is an API reference [here](https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/visual-recognition/api/v3/), but as of when this was written, only curl examples are complete. We found it helpful to reference the python-sdk source code.

Watson's visual classifier, once trained, takes an image file or url, and outputs its confidence level that that image belongs in each of its pre-established classes. As an example, assume we have a classifier that hase been trained to recognize 2 classes of images, dogs and cats. If we give it a picture of a beagle, it may be 80% confident that that picture is a dog. However, it may also be 10% confident that it is a cat. By default, only 50%+ confidence levels are returned.

Training a classifier requires 2 things. Primarily, for each class of images you want the classifier to recognize, you need a zip file of examples. In our previous example, we would have trained the classifer with a zip file of dog images and a zip file containing cat images. More training data is always better, but as few as 10 training images can produce good results. The second thing you need is a zip file of negative examples. The only rule for negative examples is that they do not depict anything described by the other classes. In our dogs vs cats example, this could be pictures of horses, buildings, outer space, or anything else you like.

In the python-sdk, an example call to create a classifier looks like:

`create_cassifer( "Dog or Cat", dog_positive_examples=dogs_zipfile.zip, cat_positive_examples=cats_zipfile.zip, negative_examples=neg_zipfile.zip)`

The *name*_positive_examples format is important. In our classifier.py file, you can see our wrapper for this function that uses exec to generate variable names for us. Feel free to use this.

Once you have a classifier, you can call it by listing all classifiers, choosing the appropriate classifier_id, and making an sdk call to classify.

The visual recognition API also includes a default classifier, used when no classifier_ids are given. The default classifier attempts to recognize things in the image, like beaches, people, etc. We found the results to range from fairly accurate to unintentianally hilarious, but for the most part did not use this data source, although each image's default classification was saved.

Leveraging Watson APIs to Perform Visual Sentiment Analysis
-----------------------------------------------------------
We gathered data from the top 5,000 all time posts on reddit.com/r/pics, saving the image url and the results of performing a tone analysis of up to the top 25 root-level comments. We did not consider albums or images not in .jpg or .png format. We tried performing tone analysis on the title, but it turned out to be less reliable than comment data. In total, we were left with about 3,000 data points. We then split the data in half, using 50% for training and setting aside 50% for testing, leaving us with about 1,500 posts worth of training data.

With this data, we partitioned the images by tone scores. We saved the top fifth and bottom fifth in each emotional category. (about 200 images each, close to the limit of the largest file accepted by the visual classifier) We used these image sets to train 13 visual classifiers, one for each tone, using the top fifth as positive examples, and the bottom fifth as negative examples.

Assessment
---------
Any hard statistical analysis is left as an excercise for the reader. (see data/data.csv)

We ran our newly created classifiers on the testing data set, comparing the classifier's confidence levels with the data from the tone analysis. Using these 2 data sets, we generated correlation coefficients between our classifiers and reality.

Correlation coefficient of Anger: 0.16750500103560734

Correlation coefficient of Disgust: 0.07663217586591686

Correlation coefficient of Fear: 0.04251686225532842

Correlation coefficient of Joy: 0.174911888103803

Correlation coefficient of Sadness: 0.04281021754469781

Correlation coefficient of Analytical: 0.03288946457777953

Correlation coefficient of Confident: -0.02465216079416054

Correlation coefficient of Tentative: -0.06429863738106256

Correlation coefficient of Openness: 0.24914027524948043

Correlation coefficient of Conscientiousness: 0.0427613161464976

Correlation coefficient of Extraversion: 0.31127442613382056

Correlation coefficient of Agreeableness: 0.17942931077655133

Correlation coefficient of Emotional_Range: 0.0317150556442275

These numbers should be interpreted like so: 

A negative number indicates negative correlation (i.e. Higher classifier confidence means *lower* scores on that tone analysis)

A positive number indicated a positive correlation (i.e. Higher confidence levels are correlated with higher scores on that tone analysis)

0 indicates random noise (i.e. the number sets aren't correlated)

We can see that our classifiers are far from accurate, but, on average, they are slightly better than random.

Web Front-End
--------------
For documentation on the creation of the web front-end and communication of the results between the server and the client, see the Readme in the 'Front-End' directory.


Final Thoughts
--------------

This problem has an absurd number of sources of complexity. A brief list:

Data variety: Any picture is fair game to be posted on reddit. As such, we had to cope with a huge variety of pictures. Limiting ourselves to a subset (like images of people), could have made the results more accurate. The comment variety was also enormous, including stories, poems, ascii art, and image, video, or web links. Unstructured data like this is difficult to reliably analyze.

Uncertainty surrounding tone analyzer: The results of tone analysis can be surprising. Often, the results from analyzing a piece of text were counter to what our team expected. The tone analyzer was also not trained on reddit comment data, so results skewed any number of ways: Anger and extraversion were consistenly above 0.5, and confidence was a flat 0.0 for more than a third of the posts analyzed.

Context blindness: Nothing is posted in a vaccuum. An image of a celebrity may elicit joy (or anger) one day, but there will be much different emotions (sadness) if that same image is posted the day of their death. Discarding title data makes this problem especially acute. A more thorough solution could involve reading a post's timestamp and performing some kind of analysis on news articles from the same day or week that feature the same concepts.

Despite the low correlation values, we are fairly content with how this project went. Overall, we think that it is just too complex of a problem for machines to solve given the restraints on the size of input, and the fact that we got anything at all is encouraging.

Future Work
-----------

More complex algorithms, more preprocessing of images.

Limit training data to a certain subset (e.g. pictures of people)

A different data source.
