
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
search = api.GetSearch(term='depression', lang='en', result_type='recent', count=100, max_id='')
for tweet in search:
    l.append(tweet.user.id)
    m.append(tweet.text)
    print(tweet.user.screen_name, tweet.text)

# Getting Public tweets from Trump
#t = api.GetUserTimeline(screen_name="ellease_lydia", count=10)

# Tweets is a list . printing ID and text, t dic
#zip(l,m)
#with open('Dep3.csv', 'w') as f:
#writer = csv.writer(f, delimiter='\t')
#writer.writerows(zip(l,m))
#quit()

#f = open('Dep2.txt','w')
#for item in s:
#  f.write("%s\n" % item)
#tweets = [i.AsDict() for i in t]
#for t in tweets:
#    print(t['id'], t['text'])
#    print(t['text'])
#    f.write(t['text'])
#    f.write('\n')
#f.close()









