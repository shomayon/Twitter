
# Rest API
import json
import nltk
import csv


import twitter

import oauthlib
api = twitter.Api(consumer_key='',
  consumer_secret='',
  access_token_key='',
  access_token_secret='')


word = ['Anxiety','depression','Bipolar', 'schizophrenia','disorder', 'PTSD', 'ADHD', 'Attention Deficit Hyperactivity Disorder']
m=[]
l= []
search = api.GetSearch(['I have been diagnosed with Anxiety']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)


search = api.GetSearch(['I have been diagnosed with depression'], lang='en') # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with dep']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with Bipolar']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with schizophrenia']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with post-traumatic stress disorder']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)


search = api.GetSearch(['I have been diagnosed with PTSD']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with ADHD']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with Attention Deficit Hyperactivity Disorder']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['I have been diagnosed with Attention Deficit Hyperactivity Disorder']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)


search = api.GetSearch(['I feel sad']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)


search = api.GetSearch(['I feel depressed']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)


search = api.GetSearch(['my life is a failure']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)


search = api.GetSearch(['I feel lonely']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)

search = api.GetSearch(['my suicide attempt']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)



with open('Data1.csv', 'w', newline='') as csvfile:
    fieldnames = ['Username', 'Text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, j in zip(l, m):
        writer.writerow({'Username': i, 'Text': j})







