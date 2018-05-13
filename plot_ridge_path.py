from TwitterSearch import *
import csv
import json
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['depression', 'diagnosed']) # let's define all words we would like to have a look for
    tso.set_language('en') # we want to see English tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'GwpuXi1ZMyc0ATSb3FEPaTyOU',
        consumer_secret = '0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ',
        access_token = '220846580-AtrY0FBq5Yd2OcHtjm4FL5KEdf31qzjOtFMDoE4m',
        access_token_secret = 'ID9RUnPxFmrMcOQNMNUwSy713CFLULNb21hKeZ57bLq4R'
     )

     # this is where the fun actually starts :)
    #for tweet in ts.search_tweets_iterable(tso):
     #   print( tweet['user']['screen_name'], tweet['text'] )

    m = []
    l = []
    for tweet in ts.search_tweets_iterable(tso):
        l.append(tweet['user']['screen_name'])
        m.append(tweet['text'])
    print(l)
    #  print(tweet.user.id, tweet.text)

except TwitterSearchException as e: # take care of all those ugly errors if there are some
   print(e)

#with open('username.csv', 'w') as f:
#writer = csv.writer(f, delimiter='\t')
#writer.writerows(l)
#quit()

# Open File
resultFyle = open("username.csv",'w')

# Write data to file
for r in l:
    resultFyle.write(r + "\n")
resultFyle.close()

#with open("../untitled5/username.csv",'wb') as output:
 #   writer = csv.writer(output, lineterminator='\n')
  #  for val in l:
   #     writer.writerow([val])




