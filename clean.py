import tweepy
import csv
import re
import string


alltweet =[]
tweet =[]

def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text
		
def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word == 'RT':
            word = word.replace('RT','')
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

with open('labeled_tweets.csv','r', encoding="utf-8") as f:
    for line in f:
        cleanline = strip_all_entities(strip_links(line))
        alltweet.append(cleanline)

with open("cleandata.csv",'w') as f:
    writer = csv.writer(f,dialect='excel')
    for t in alltweet:
        writer.writerow([t])




#for val in alltweet:
#    e= strip_all_entities(strip_links(val))
#    result = re.sub(r"http\S+", "", e)
#    result2= re.compile('\#').sub('', re.compile('RT @').sub('@', result))
#    result3= (re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", result2))
#    tweet.append(result3)



str_list = list(filter(None, tweet)) #remove empty string

