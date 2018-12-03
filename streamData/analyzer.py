#analyzing tweets
import pandas as pd
import matplotlib.pyplot as plt
import users
import os
import json
import csv
import tweepy
from tqdm import tqdm
from pathlib import Path
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from pprint import pprint
import pytz
import datetime as dt
import collections
import argparse
from ascii_graph import Pyasciigraph
from ascii_graph.colors import Gre, Yel, Red
from ascii_graph.colordata import hcolor
import secrets
import numpy
import re
import time
from datetime import datetime
import string
"""
tweets = pd.read_csv("tweets.csv")
tweets.head()

def get_candidate(row):
    candidates = []
    text = row["text"].lower()
    if "clinton" in text or "hillary" in text:
        candidates.append("clinton")
    if "trump" in text or "donald" in text:
        candidates.append("trump")
    if "sanders" in text or "bernie" in text:
        candidates.append("sanders")
    return ",".join(candidates)
tweets["candidate"] = tweets.apply(get_candidate, axis=1)
counts = tweets["candidate"]. value_counts()
print(counts)
plt.bar(range(len(counts)),counts)
plt.show()
"""
# Here are globals used to store data - I know it's dirty, whatever
start_date = 0
end_date = 0
"""
activity_hourly = {
    ("%2i:00" % i).replace(" ", "0"): 0 for i in range(24)
}

activity_weekly = {
    "%i" % i: 0 for i in range(7)
}
"""
detected_langs = collections.Counter()
detected_sources = collections.Counter()
detected_places = collections.Counter()
geo_enabled_tweets = 0
detected_hashtags = collections.Counter()
detected_domains = collections.Counter()
detected_timezones = collections.Counter()
retweets = 0
retweeted_users = collections.Counter()
mentioned_users = collections.Counter()
id_screen_names = {}
friends_timezone = collections.Counter()
friends_lang = collections.Counter()

def int_to_weekday(day):
    weekdays = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
    return weekdays[int(day) % len(weekdays)]


def print_stats(dataset, top=5):
    """ Displays top values by order """
    sum = numpy.sum(list(dataset.values()))
    i = 0
    if sum:
        sorted_keys = sorted(dataset, key=dataset.get, reverse=True)
        max_len_key = max([len(x) for x in sorted_keys][:top])  # use to adjust column width
        for k in sorted_keys:
            try:
                print(("- \033[1m{:<%d}\033[0m {:>6} {:<4}" % max_len_key)
                      .format(k, dataset[k], "(%d%%)" % ((float(dataset[k]) / sum) * 100)))
            except:
                import ipdb
                ipdb.set_trace()
            i += 1
            if i >= top:
                break
    else:
        print("No data")
    print("")


def print_values(filename, data):
    fid = open(filename,'w')
    for line in data:
        fid.write("%s\n"%line)

def print_charts(dataset, title, weekday=False):
    """ Prints nice charts based on a dict {(key, value), ...} """
    chart = []
    keys = sorted(dataset.keys())
    mean = numpy.mean(list(dataset.values()))
    median = numpy.median(list(dataset.values()))

    for key in keys:
        if (dataset[key] >= median * 1.33):
            displayed_key = "%s (\033[92m+\033[0m)" % (int_to_weekday(key) if weekday else key)
        elif (dataset[key] <= median * 0.66):
            displayed_key = "%s (\033[91m-\033[0m)" % (int_to_weekday(key) if weekday else key)
        else:
            displayed_key = (int_to_weekday(key) if weekday else key)

        chart.append((displayed_key, dataset[key]))

    thresholds = {
        int(mean): Gre, int(mean * 2): Yel, int(mean * 3): Red,
    }
    data = hcolor(chart, thresholds)

    graph = Pyasciigraph(
        separator_length=4,
        multivalue=False,
        human_readable='si',
    )

    for line in graph.graph(title, data):
        print(line)
    print("")

def getLocalTime(time, timezone):
    utc_time = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)
    #finaltime = local_time.strftime(format='%a %b %d %H:%M:%S %Y')
    finaltime = local_time.strftime(format='%Y-%m-%d %H:%M:%S')
    return(finaltime)

def getTimeZone(latit, longit):
    #get timezone
    zone = TimezoneFinder().timezone_at(lng=longit,lat=latit)
    timezone = pytz.timezone(zone) #convert zone string to pytz format  
    return (timezone)

def process_tweet(tweet, localtime):
    """ Processing a single Tweet and updating our datasets """
    global start_date
    global end_date
    global geo_enabled_tweets
    global retweets
    # Check for filters before processing any further
    #if args.filter and tweet.source:
    #    if not args.filter.lower() in tweet.source.lower():
    #        return

    # get correct time
    tw_date = localtime
    #convert time to datetime in order to extract features
    date_object = datetime.strptime(tw_date,'%Y-%m-%d %H:%M:%S')
    end_date = end_date or tw_date
    start_date = tw_date
    """
    # Handling retweets
    try:
        # use id to get unique accounts (screen_name can be changed)
        rt_id_user = tweet.retweeted_status.user.id_str
        retweeted_users[rt_id_user] += 1

        if tweet.retweeted_status.user.screen_name not in id_screen_names:
            id_screen_names[rt_id_user] = "@%s" % tweet.retweeted_status.user.screen_name

        retweets += 1
    except:
        pass
    """
    # Updating our activity datasets (distribution maps)
    activity_hourly["%s:00" % str(date_object.hour).zfill(2)] += 1
    activity_weekly[str(date_object.weekday())] += 1

    
"""
    # Updating langs
    detected_langs[tweet.lang] += 1

    # Updating sources
    detected_sources[tweet.source] += 1

    # Detecting geolocation
    if tweet.place:
        geo_enabled_tweets += 1
        tweet.place.name = tweet.place.name
        detected_places[tweet.place.name] += 1


    # Updating hashtags list
    if tweet.entities['hashtags']:
        for ht in tweet.entities['hashtags']:
            ht['text'] = "#%s" % ht['text']
            detected_hashtags[ht['text']] += 1

    # Updating domains list
    if tweet.entities['urls']:
        for url in tweet.entities['urls']:
            domain = urlparse(url['expanded_url']).netloc
            if domain != "twitter.com":  # removing twitter.com from domains (not very relevant)
                detected_domains[domain] += 1

    # Updating mentioned users list
    if tweet.entities['user_mentions']:
        for ht in tweet.entities['user_mentions']:
            mentioned_users[ht['id_str']] += 1
            if not ht['screen_name'] in id_screen_names:
                id_screen_names[ht['id_str']] = "@%s" % ht['screen_name']
    """

def cleanLocation(user, myGeo):
    #file path made from pandastweets.py
    file_name = user +'_tweets.csv'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = Path(dir_path+'/twitter_data/'+file_name)

    #temporary file
    fieldnames = ['Tweet_ID','Tweet','Screen_Name','Description','User_Location','Time','Geo_Enabled','Place','Lat','Long']
    newfile_name= user+'_updatedtweets.csv'
    dir_path2 = os.path.dirname(os.path.realpath(__file__))
    newpath = Path(dir_path2+'/twitter_data/'+newfile_name)
    num_tweets = 0

    if path.exists():
        print("...%s file found" % user)
        with open(path, 'r') as infile, open(newpath,'w') as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)  
            for row in reader:
                #grab important attributes
                location = row["User_Location"]
                time = row["Time"]
                place = row["Place"]
                lat = row["Lat"]
                longit = row["Long"]
                finaltime = ''
                tweet = row['Tweet']
                if location is None:
                    print("The user has no profile location... Thank you, next")
                    break

                #if the dict is empty, add the first user location
                if len(myGeo) == 0:
                    geolocator = Nominatim(user_agent="twit_mental_health")
                    loc = geolocator.geocode(location)
                    #get timzone and store into hashmap
                    timezone = getTimeZone( loc.latitude, loc.longitude)
                    myGeo[location] = timezone               
                else:  
                    #if tweet has a location
                    if lat and longit is not None:
                        if place in myGeo:  #if tweetlocation is in the map
                            timezone = myGeo.get(place)
                        else:   #if tweetlocation isn't in map, add it
                            geolocator = Nominatim(user_agent="twit_mental_health")
                            loc = geolocator.geocode(place)
                            floatlat = float(lat)
                            floatlong = float(longit)

                            timezone = getTimeZone(floatlat, floatlong)
                            myGeo[place] = timezone  #add to map
                    else:   #no tweet location
                        if location in myGeo:
                            timzone = myGeo.get(location)
                        else:   #add location to map
                            geolocator = Nominatim(user_agent="twit_mental_health")
                            loc = geolocator.geocode(location)

                            timezone = getTimeZone(loc.latitude, loc.longitude)
                            myGeo[location] = timezone

                #get localtime
                finaltime = getLocalTime(time,timezone) 
                row["Time"] = finaltime
                #rewrite row with new localtime
                writer.writerow(row)
                num_tweets = num_tweets+1
                process_tweet(tweet, finaltime)
        os.remove(path)
        os.rename(newpath, path)
        print("myGeo dict():")
        for key, val in myGeo.items():
            print(key,"=>", val)


        #process_tweet(tweet, finaltime)        
 
        return num_tweets
    else:
        print("...%s file NOT found" % user)


if __name__ == "__main__":
    auth = tweepy.OAuthHandler(secrets.TWITTER_APP_KEY, secrets.TWITTER_APP_SECRET)
    auth.set_access_token(secrets.TWITTER_KEY, secrets.TWITTER_SECRET)
    twitter_api = tweepy.API(auth)

    #create a dictionary
    myGeo = {}
    finalDict = {}
    for user in users.SCREEN_NAME:
        act_hour_name = user+'_activity_hourly.csv'
        dir_path3 = os.path.dirname(os.path.realpath(__file__))
        path3 = Path(dir_path3+'/twitter_data/'+act_hour_name)

        act_week_name = user+'_activity_weekly.csv'
        dir_path4 = os.path.dirname(os.path.realpath(__file__))
        path4 = Path(dir_path4+'/twitter_data/'+act_week_name)


        activity_hourly = {
            ("%2i:00" % i).replace(" ", "0"): 0 for i in range(24)
        }

        activity_weekly = {
            "%i" % i: 0 for i in range(7)
        }

        num_tweets = cleanLocation(user, myGeo)

        print("[+] Getting @%s account data..." % user)
        user_info = twitter_api.get_user(screen_name=user)

        print("[+] lang           : \033[1m%s\033[0m" % user_info.lang)
        print("[+] geo_enabled    : \033[1m%s\033[0m" % user_info.geo_enabled)
        print("[+] time_zone      : \033[1m%s\033[0m" % user_info.time_zone)
        print("[+] utc_offset     : \033[1m%s\033[0m" % user_info.utc_offset)


        print("[+] statuses_count : \033[1m%s\033[0m" % user_info.statuses_count)

        # Will retreive all Tweets from account (or max limit)
        print("[+] Retrieving last %d tweets..." % num_tweets)
        """
        # Download tweets
       # get_tweets(twitter_api, user, path, limit=num_tweets)
        print("[+] Downloaded %d tweets from %s to %s (%d days)" % (num_tweets, start_date, end_date, (end_date - start_date).days))
    
        # Checking if we have enough data (considering it's good to have at least 30 days of data)
        if (end_date - start_date).days < 30 and (num_tweets < user_info.statuses_count):
            print("[\033[91m!\033[0m] Looks like we do not have enough tweets from user, you should consider retrying (--limit)")

        if (end_date - start_date).days != 0:
            print("[+] Average number of tweets per day: \033[1m%.1f\033[0m" % (num_tweets / float((end_date - start_date).days)))
        """
        # Print activity distrubution charts
        print_charts(activity_hourly, "Daily activity distribution (per hour)")
        print_charts(activity_weekly, "Weekly activity distribution (per day)", weekday=True)

        hactivities = []
        for i in range(24):
            hactivities.append(str(activity_hourly["%s:00" % str(i).zfill(2)]))
        print_values(path3, hactivities)
        wactivities = []
        for i in range(7):
            wactivities.append(str(activity_weekly["%s" % str(i)]))
        print_values(path4, wactivities)

