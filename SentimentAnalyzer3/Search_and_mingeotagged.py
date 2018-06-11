
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


# Creation of the actual interface, using authentication
# Consumer keys and access tokens, used for OAuth
consumer_key="GwpuXi1ZMyc0ATSb3FEPaTyOU"
consumer_secret="0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ"

access_token="220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE"
access_token_secret="WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77"
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Creation of the actual interface, using authentication
api2 = tweepy.API(auth)



detected_places = collections.Counter()
alluser =[]
alltweet= []
geo_enabled_tweets = 0


api = twitter.Api(consumer_key='GwpuXi1ZMyc0ATSb3FEPaTyOU',
                  consumer_secret='0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ',
                  access_token_key='220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE',
                  access_token_secret='WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77')




keyword1 = ['ADHD','anxiety','depression','Bipolar', 'schizophrenia','disorder', 'PTSD', 'Attention Deficit Hyperactivity Disorder',
        'post-traumatic stress disorder','dep',' seasonal affective disorder']
keyword2= ['sad','depressed', 'blue', 'upset','lonely']
keyword3= ['my suicide attempt','my life is a failure']
m=[]
l= []


for i in keyword1:
    str= ('I have been diagnosed with '+i)
    search = api.GetSearch([str])

    for tweet in search:
        if not tweet.retweeted and 'RT @' not in tweet.text:
             l.append(tweet.user.screen_name)
             m.append(tweet.text)



for i in keyword2:
    str= ('I feel '+i)
    search = api.GetSearch([str])

    for tweet in search:
        if not tweet.retweeted and 'RT @' not in tweet.text:
            if tweet.user.screen_name not in l:
                l.append(tweet.user.screen_name)
                m.append(tweet.text)

for i in keyword3:
    str= (i)
    search = api.GetSearch(i)

    for tweet in search:
        if not tweet.retweeted and 'RT @' not in tweet.text:
            if tweet.user.screen_name not in l:
                l.append(tweet.user.screen_name)
                m.append(tweet.text)


print('list is:', l)
for val in l:
    for status in tweepy.Cursor(api2.user_timeline, screen_name=val, tweet_mode='extended', lang= 'en').items(1000):
             if status.place:
                          geo_enabled_tweets += 1
                          status.place.name = status.place.name
                          detected_places[status.place.name] += 1
                          if status.user.screen_name not in alluser:

                              alluser.append(status.user.screen_name)



for val in alluser:
        if geo_enabled_tweets >50:
               print(alltweet.append(status.user.screen_name))


with open("Geo_tagged_usernames.csv",'w') as f:
    writer = csv.writer(f, dialect='excel')
    for t in alluser:
        writer.writerow([t])