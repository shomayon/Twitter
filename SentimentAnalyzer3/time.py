
import csv
import twitter
import oauthlib
import tweepy
import collections

# Rest API
import json
import csv
import twitter
import oauthlib
import sys
from datetime import datetime, date, time, timedelta






consumerKey="GwpuXi1ZMyc0ATSb3FEPaTyOU"
consumerSecret="0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ"

accessToken="220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE"
accessTokenSecret="WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth, wait_on_rate_limit=True)

username = 'shideh66'
startDate = datetime(2011, 6, 1, 0, 0, 0)
endDate =   datetime(2012, 1, 1, 0, 0, 0)

tweets = []
tmpTweets = api.user_timeline(username)
for tweet in tmpTweets:
    if tweet.created_at < endDate and tweet.created_at > startDate:
        tweets.append(tweet)

while (tmpTweets[-1].created_at > startDate):
    tmpTweets = api.user_timeline(username, max_id = tmpTweets[-1].id)
    for tweet in tmpTweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)