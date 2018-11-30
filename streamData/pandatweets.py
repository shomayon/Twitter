# Individual user csv files will be saved to
# directory "twitter_data"
# This script gathers the tweets of a user
# and will also update the csv file of the most recent
# tweets since the last fetch



import tweepy #https://github.com/tweepy/tweepy
import csv
import secrets
import json
import os
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import users

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
	
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(secrets.TWITTER_APP_KEY, secrets.TWITTER_APP_SECRET)
    auth.set_access_token(secrets.TWITTER_KEY, secrets.TWITTER_SECRET)
    api = tweepy.API(auth)

    max_id = 0
    file_name = screen_name+'_tweets.csv' 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = Path(dir_path+'/twitter_data/'+file_name)
    path.parent.mkdir(parents = True, exist_ok=True)
    if path.exists():
        print("...%s file exists already" % screen_name)
        with open(path, 'r') as f:
            for row in csv.DictReader(f):
                since_id = row["Tweet_ID"]
                if since_id is None:
                    print("Existing user file is empty")
                    return
                else:
                    break
        newtweets = []
        
        recent_tweets = api.user_timeline(screen_name = screen_name, count = 200, since_id = since_id)
        newtweets.extend(recent_tweets)
        #oldest = newtweets[-1].id -1
        if len(recent_tweets) == 0:
            print ("...%s has no new tweets" % screen_name)
            return
        else:
            if len(recent_tweets) == 1:
                print ("...%s has %d new tweet"% (screen_name, len(recent_tweets)))
            else:
                print("...%s has %d new tweets" % (screen_name, len(recent_tweets)))
            
            #dataFrame of original tweets from csv file
            df = pd.DataFrame()
            final = pd.DataFrame()
            col_to_use = ['Tweet_ID','Tweet','Screen_Name','Description','User_Location','Time','Geo_Enabled','Lat','Long']
            df = pd.read_csv(path, index_col=False,usecols=col_to_use)[col_to_use]
            display(df.head(10))
            # copy new tweets on top of old tweets
            newdata = pd.DataFrame()
            newdata['Tweet_ID'] = np.array([tweet.id_str for tweet in newtweets])
            newdata['Tweet'] = np.array([tweet.text for tweet in newtweets])
            newdata['Screen_Name'] = np.array([tweet.user.screen_name for tweet in newtweets])
            newdata['Description'] = np.array([tweet.user.description for tweet in newtweets])
            newdata['User_Location'] = np.array([tweet.user.location for tweet in newtweets])
            newdata['Time'] = np.array([tweet.user.created_at for tweet in newtweets])
            newdata['Geo_Enabled'] = np.array([tweet.user.geo_enabled for tweet in newtweets])
           # newdata['Coords'] = list(map(lambda tweet: tweet.coordinates["coordinates"] if tweet.place != None else None, newtweets))
            newdata['Lat'] = list(map(lambda tweet: tweet.coordinates["coordinates"][1] if tweet.place != None else None, newtweets))
            newdata['Long'] = list(map(lambda tweet: tweet.coordinates["coordinates"][0] if tweet.place != None else None, newtweets))
            display(newdata.head(10))
            final = newdata.append(df, sort = False)
            print("Concatenated data")
            display(final.head(10))
            #display(newdata.head(10))
            final.to_csv(path, encoding='utf-8', index=False)
    else:
        print("...%s file does not exist" % screen_name)
        #initialize a list to hold all the tweepy Tweets
        alltweets = []	
        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=200)

        #save most recent tweets
        alltweets.extend(new_tweets)
	
       #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
	
       #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print("getting tweets before %s",oldest)
            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		    #save most recent tweets
            alltweets.extend(new_tweets)
            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            print("...%s tweets have been downloaded so far",len(alltweets))
        #transforming the tweets into a 2D array that will be used to populate the csv
        
        data = pd.DataFrame()
        data['Tweet_ID'] = np.array([tweet.id_str for tweet in alltweets])
        data['Tweet'] = np.array([tweet.text for tweet in alltweets])
        data['Screen_Name'] = np.array([tweet.user.screen_name for tweet in alltweets])
        data['Description'] = np.array([tweet.user.description for tweet in alltweets])
        data['User_Location'] = np.array([tweet.user.location for tweet in alltweets])
        data['Time'] = np.array([tweet.user.created_at for tweet in alltweets])
        data['Geo_Enabled'] = np.array([tweet.user.geo_enabled for tweet in alltweets])
        #data['Coords'] = list(map(lambda tweet: tweet.coordinates["coordinates"] if tweet.place != None else None, alltweets))
        data['Lat'] = list(map(lambda tweet: tweet.coordinates["coordinates"][1] if tweet.place != None else None, alltweets))
        data['Long'] = list(map(lambda tweet: tweet.coordinates["coordinates"][0] if tweet.place != None else None, alltweets))
        display(data.head(10))
        data.to_csv(path, encoding='utf-8', index=False)


if __name__ == '__main__':
    #pass in the username of the account you want to download
    for user in users.SCREEN_NAME:
        get_all_tweets(user)
        print("\n")   
