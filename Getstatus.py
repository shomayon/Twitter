
import twitter
import csv
import re
import nltk


import oauthlib
api = twitter.Api(consumer_key='',
  consumer_secret='',
  access_token_key='',
  access_token_secret='')

#
# with open('../untitled5/username.csv') as f:
#     reader = csv.DictReader(f) # read rows into a dictionary format
#     for row in reader:

#for items in l:

t = api.GetUserTimeline(screen_name="p", count=1000)

f = open('test.txt','w')
tweets = [i.AsDict() for i in t]
for t in tweets:
 #   print(t['id'], t['text'])
 #   print(t['text'])
    f.write(t['text'])
    f.write('\n')
f.close()
#c= []
#term = "@"
#with open('rosieatlarge.txt') as f:
#    for line in f:
#       str = line
#       h = line.strip()
 #      z =h.split()
 #      p = filter(lambda x: x[0] != '@', z)
 #      q = " ".join(filter(lambda x: x[0] != '@', p))
 #      c.append(q)
#print(c)

#resultFyle = open("output1.csv",'w')
#for r in c:
#    resultFyle.write(r + "\n")
#resultFyle.close()





