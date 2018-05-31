from TwitterSearch import *
import csv
import json


#This code search twitter for keywords to identify users who have shared their mental health diagnosis

m = [] #list of match tweet's text
l = [] #list of match tweet's Username

try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with Anxiety' ]) # let's define words we would like to have a look for
    tso.set_language('en') # we want to see English tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # create a TwitterSearch object with our secret tokens ()
    ts = TwitterSearch(
        consumer_key = 'GwpuXi1ZMyc0ATSb3FEPaTyOU',
        consumer_secret = '0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ',
        access_token = '220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE',
        access_token_secret = 'WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77'
     )



    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])
     #  print(l)
     #   print(tweet['user']['screen_name'], tweet['text'])


    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with depression']) # let's define words we would like to have a look for
    tso.set_language('en') # we want to see English tweets only
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])

    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with dep' ])
    tso.set_language('en')
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])


    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with Bipolar' ])
    tso.set_language('en')
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])


    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with schizophrenia' ])
    tso.set_language('en')
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])


    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with post-traumatic stress disorder' ])
    tso.set_language('en')
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])



    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with PTSD' ])
    tso.set_language('en')
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])



    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with Eating Disorders' ])
    tso.set_language('en')
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])


    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with ADHD' ])
    tso.set_language('en') # we want to see English tweets only
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])


    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with Attention Deficit Hyperactivity Disorder'])
    tso.set_language('en') # we want to see English tweets only
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])


    so = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with mental health disorder'])
    tso.set_language('en') # we want to see English tweets only
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])


    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['I have been diagnosed with Bipolar' ])
    tso.set_language('en')
    tso.set_include_entities(False)

    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])





except TwitterSearchException as e: # take care of all those ugly errors if there are some
   print(e)


with open('Data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Username', 'Text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, j in zip(l, m):
        writer.writerow({'Username': i, 'Text': j})
