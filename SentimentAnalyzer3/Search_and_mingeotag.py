
import csv
import twitter
import tweepy
import collections
import pandas as pd


import twitter

dict_ = {'user':[],'text':[],'place':[],'created_at':[]}
consumer_key="GwpuXi1ZMyc0ATSb3FEPaTyOU"
consumer_secret="0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ"

access_token="220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE"
access_token_secret="WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api2 = tweepy.API(auth)


api = twitter.Api(consumer_key='GwpuXi1ZMyc0ATSb3FEPaTyOU',
                  consumer_secret='0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ',
                  access_token_key='220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE',
                  access_token_secret='WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77')




keyword1 = ['depression','dep']
keyword2= ['sad','depressed', 'blue', 'upset','lonely']
keyword3= ['my suicide attempt','my life is a failure']



for i in keyword1:
    str= ('I have been diagnosed with'+i)
    search = api.GetSearch([str])

    for tweet in search:
       if not tweet.retweeted and 'RT @' not in tweet.text:
            if tweet.place or tweet.user.location:

             dict_['user'].append(tweet.user.screen_name)
             dict_['text'].append(tweet.text)
             dict_['place'].append(tweet.user.location)
             dict_['created_at'].append(tweet.created_at)



for i in keyword2:
    str= ('I feel '+i)
    search = api.GetSearch([str])

    for tweet in search:
        if not tweet.retweeted and 'RT @' not in tweet.text:
            if tweet.place or tweet.user.location:

                dict_['user'].append(tweet.user.screen_name)
                dict_['text'].append(tweet.text)
                dict_['place'].append(tweet.user.location)
                dict_['created_at'].append(tweet.created_at)

for i in keyword3:
    str= (i)
    search = api.GetSearch(i)

    for tweet in search:
        if not tweet.retweeted and 'RT @' not in tweet.text:
            if tweet.place or tweet.user.location:

              dict_['user'].append(tweet.user.screen_name)
              dict_['text'].append(tweet.text)
              dict_['place'].append(tweet.user.location)
              dict_['created_at'].append(tweet.created_at)

df = pd.DataFrame(dict_)
print(df)
