from textblob import TextBlob
import re
#from credentials import *
import tweepy
import pandas as pd
import numpy as np
import json
from timezonefinder import TimezoneFinder
import pytz
import datetime as dt
from geopy.geocoders import Nominatim
from pprint import pprint
# For plotting and visualization:
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline



def twitter_setup():

    # Authentication and access using keys:
    auth = tweepy.OAuthHandler('GwpuXi1ZMyc0ATSb3FEPaTyOU', '0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ')
    auth.set_access_token('220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE', 'WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77')

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

extractor = twitter_setup()


# create a tweet list as follows:
tweets = extractor.user_timeline(screen_name="Kyashi_Cosplay", count=10)
#print(tweets)

def getTime(tweet,latit,long):
      #get timezone
      zone = TimezoneFinder().timezone_at(lng=long,lat= latit)
      timezone = pytz.timezone(zone) #convert zone string to pytz format

      #convert to local time
      utc_time = dt.datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
      local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)
      time = local_time.strftime('%Y-%m-%d %H:%M:%S')
      print(time)

def store(tweet):
      if tweet["place"] is None:
            geolocator = Nominatim(user_agent="mental_health")
            location = geolocator.geocode(tweet["user"]["location"])
            getTime(tweet,location.latitude,location.longitude)
      else:
            latit = tweet["place"]["bounding_box"]["coordinates"][0][0][1]
            long = tweet["place"]["bounding_box"]["coordinates"][0][0][0]
            getTime(tweet,latit,long)
 
      #print(tweet.txt)
    #  print(json.dumps(tweet,indent=3))

for tweet in tweets[:20]:
      if not tweet.retweeted and 'RT @' not in tweet.text:
    #        print(tweet.text)
            store(tweet._json)

#print("100 recent tweets:\n")
#for tweet in tweets[:10]:
#    print(tweet.text)
#    print()

# create a pandas dataframe as follows:
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

#  display the first 100 elements of the dataframe:
display(data.head(100))


data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
display(data.head(100))
# extract the mean of lenghts:
mean = np.mean(data['len'])
print("The length's average in tweets: {}".format(mean))



tlen = pd.Series(data=data['len'].values, index=data['Date'])
tlen.plot(figsize=(16,4), color='r')
plt.show()
#
def clean_tweet(tweet):
    '''
     clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1


#  create a column with the result of the analysis:
data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])

# display the updated dataframe with the new column:
display(data.head(100))

# construct lists with classified tweets:

pos_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] < 0]

print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['Tweets'])))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['Tweets'])))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data['Tweets'])))
