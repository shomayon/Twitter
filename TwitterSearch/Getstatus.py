import tweepy
import csv
import re

# Consumer keys and access tokens, used for OAuth
consumer_key = 'GwpuXi1ZMyc0ATSb3FEPaTyOU'
consumer_secret = '0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ'
access_token = '220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE'
access_token_secret = 'WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

with open("test.csv",'w') as f:
    writer = csv.writer(f, dialect='excel')
alltweet =[]
with open('../untitled5/TwitterSearch/test10user.csv') as f:
    for line in f:
     for status in tweepy.Cursor(api.user_timeline, screen_name="line", tweet_mode='extended').items(10):
         if not status.retweeted and 'RT @' not in status._json['full_text']:
          alltweet.append(status._json['full_text'])



#write tweets in csv file
with open("test.csv",'w') as f:
    writer = csv.writer(f, dialect='excel')
    for val in alltweet:
        lambda val: re.compile('\#').sub('', re.compile('RT @').sub('@', x).strip())
        writer.writerow([val])

