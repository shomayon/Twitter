
import twitter
import csv
import oauthlib

api = twitter.Api(consumer_key='GwpuXi1ZMyc0ATSb3FEPaTyOU',
  consumer_secret='0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ',
  access_token_key='220846580-AtrY0FBq5Yd2OcHtjm4FL5KEdf31qzjOtFMDoE4m',
  access_token_secret='ID9RUnPxFmrMcOQNMNUwSy713CFLULNb21hKeZ57bLq4R')


p = ['StoneybrookVA']

with open('../untitled5/username.csv' "rb") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):

for items in p:

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





