
# Rest API
import json
import nltk
import csv


import twitter

import oauthlib
api = twitter.Api(consumer_key='GwpuXi1ZMyc0ATSb3FEPaTyOU',
  consumer_secret='0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ',
  access_token_key='220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE',
  access_token_secret='WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77')

m=[]
l= []
search = api.GetSearch(['I have been diagnosed with Anxiety']) # Replace any words with your search
for tweet in search:
    l.append(tweet.user.screen_name)
    m.append(tweet.text)
    print(tweet.text)


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


#data1sample for now
#with open("data1sample.csv",'w') as f:
#    writer = csv.writer(f, dialect='excel')
#    for val in m:
#        writer.writerow([val])



