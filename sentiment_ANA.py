

from textblob import TextBlob
import re
from credentials import *
import tweepy
import pandas as pd
import numpy as np

# For plotting and visualization:
from IPython.display import display
import matplotlib.pyplot as plt
#import seaborn as sns
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
tweets = extractor.user_timeline(screen_name="zangerdanger", count=10)


# We print the most recent 100 tweets:
print("10 recent tweets:\n")
for tweet in tweets[:10]:
    print(tweet.text)
    print()

# create a pandas dataframe as follows:
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

#  display the first 100 elements of the dataframe:
display(data.head(100))


data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
#data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
display(data.head(100))
# extract the mean of lenghts:
mean = np.mean(data['len'])
print("The lenght's average in tweets: {}".format(mean))

tlen = pd.Series(data=data['len'].values, index=data['Date'])
tlen.plot(figsize=(16,4), color='r')
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
