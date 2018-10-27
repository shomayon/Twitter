import tweepy
import csv
import re
import string


alltweet =[]
tweet =[]
# infname='SentimentAnalyzer3/DATA/merged/Merged_all_fornow.csv'
with open('Merged_all_fornow.csv') as f:
    for line in f:
        myNames = [line.strip() for line in f]
        print("n")



def strip_links(myName):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, alltweet)
    for link in links:
        text = alltweet.replace(link[0], ', ')
    return alltweet

def strip_all_entities(alltweet):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = alltweet.replace(separator,' ')
    words = []
    for word in alltweet.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)





for val in alltweet:
    e= strip_all_entities(strip_links(val))
    result = re.sub(r"http\S+", "", e)
    result2= re.compile('\#').sub('', re.compile('RT @').sub('@', result))
    result3= (re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", result2))
    tweet.append(result3)



str_list = list(filter(None, tweet)) #remove empty string

#write tweets in csv file
with open("1000tweet.csv",'w') as f:
    writer = csv.writer(f, dialect='excel')
    for t in str_list:

        writer.writerow([t])