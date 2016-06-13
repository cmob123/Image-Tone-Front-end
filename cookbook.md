Visual Sentiment Analysis using Watson APIs and Data from reddit.com
====================================================================
Interfacing with the reddit API
-------------------------------

Rather than interacting with the reddit API directly, we will use a prebuilt python interface called [PRAW](https://github.com/praw-dev/praw)

Install using the python package manager, pip:  
`$pip install PRAW`

Our code is in redditDataGetter.py

__TODO__:fill in more later


Feed Information to Watson Tone Analyzer
----------------------------------------
See [here](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/tone-analyzer/api/v3/?python#) for the official IBM tutorial

The class we wrote to do this is in tone.py

For our application, we only care about emotion data.
To do this, we run the following:
`emotions = raw_json['document_tone']['tone_categories'][0]['tones']`
where raw_json is the full response from the tone analyzer.
This should narrow down the json to look something like this:
{
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
}

Once you have the simplified JSON, you can extract the scores: see emotions_num_extract()

