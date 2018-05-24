#!/usr/bin/python
import tweepy
import csv #Import csv
import os

# Crusor methot for seaching twitter public tweets for certain keywords

# Consumer keys and access tokens, used for OAuth
consumer_key = 'GwpuXi1ZMyc0ATSb3FEPaTyOU'
consumer_secret = '0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ'
access_token = '220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE'
access_token_secret = 'WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77'


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)
# Open/Create a file to append data
csvFile = open('testtweepy.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)



#(api.user_timeline, username="line", tweet_mode='extended').items(1)

ids = set()
for tweet in tweepy.Cursor(api.user_timeline, username="shideh66", tweet_mode='extended').items(10):

  if not tweet.retweeted and 'RT @' not in tweet._json['full_text']:
        #Write a row to the csv file/ I use encode utf-8
        csvWriter.writerow(tweet._json['full_text'])
        #print "...%s tweets downloaded so far" % (len(tweet.id))
      #  ids.add(tweet.id) # add new id
       # print ("number of unique ids seen so far: {}",format(len(ids)))
csvFile.close()