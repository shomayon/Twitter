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
from pathlib import Path

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
        print("...User file exists already")
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
            """           
            while len(recent_tweets) > 0:
                print("getting tweets before %s", oldest)
                recent_tweets = api.user_timeline(screen_name= screen_name, count = 200, max_id = oldest, since_id = since_id)
                newtweets.extend(recent_tweets)
                oldest = newtweets[-1].id-1
                print("...%s tweets have been downloaded so far", len(newtweets))
            """
            outtweet = [[
                        tweet.id_str,
                        tweet.created_at,
                        tweet.text.encode("utf-8")]
                        for tweet in newtweets]
            with open(path, newline='') as f:
                next(f)
                r = csv.reader(f)
                data = [line for line in r]
            with open(path, 'w', encoding='utf8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Tweet_ID", "Time", "Tweet"])
                writer.writerows(outtweet)
                writer.writerows(data)
            f.close()
            pass

    else:
        print("User file does not exist")
	
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
        outtweets = [[
                    tweet.id_str,
                    tweet.created_at,
                    tweet.text.encode("utf-8")]
                    for tweet in alltweets]	
        #write the csv	
        
        with open(path, 'a', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(["Tweet_ID", "Time", "Tweet"])
            writer.writerows(outtweets)
        pass


if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("girlbosskaty")
