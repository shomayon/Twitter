
# Rest API
import json
import nltk
import csv


import twitter

import oauthlib
api = twitter.Api(consumer_key='GwpuXi1ZMyc0ATSb3FEPaTyOU',
  consumer_secret='0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ',
  access_token_key='220846580-AtrY0FBq5Yd2OcHtjm4FL5KEdf31qzjOtFMDoE4m',
  access_token_secret='ID9RUnPxFmrMcOQNMNUwSy713CFLULNb21hKeZ57bLq4R')

m=[]
l= []
search = api.GetSearch(['I have been diagnosed with Anxiety' ]) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)


search = api.GetSearch(['I have been diagnosed with depression' ]) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with dep' ]) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with Bipolar' ]) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with schizophrenia' ]) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with post-traumatic stress disorder' ]) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)


search = api.GetSearch(['I have been diagnosed with PTSD' ]) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with ADHD' ]) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with Attention Deficit Hyperactivity Disorder' ]) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)



with open('Data1.csv', 'w', newline='') as csvfile:
    fieldnames = ['Username', 'Text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, j in zip(l, m):
        writer.writerow({'Username': i, 'Text': j})







