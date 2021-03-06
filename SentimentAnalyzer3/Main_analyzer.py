
#
# Usage:
# python tweets_analyzer.py -n screen_name
#
# Install:
# pip install tweepy ascii_graph tqdm numpy

from __future__ import unicode_literals

from ascii_graph import Pyasciigraph
from ascii_graph.colors import Gre, Yel, Red
from ascii_graph.colordata import hcolor
from tqdm import tqdm
from timezonefinder import TimezoneFinder
import datetime as dt
from geopy.geocoders import Nominatim
from pprint import pprint
import pytz
import json
import tweepy
import numpy
import argparse
import collections
import datetime
import re
import string
import csv



try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from secrets import consumer_key, consumer_secret, access_token, access_token_secret


parser = argparse.ArgumentParser(description=
                                 '')
parser.add_argument('-l', '--limit', metavar='N', type=int, default=3200,
                    help='limit the number of tweets to retreive (default=1000)')
parser.add_argument('-n', '--name', required=True, metavar="screen_name",
                    help='target screen_name')

parser.add_argument('-f', '--filter', help='filter by source (ex. -f android will get android tweets only)')

parser.add_argument('--no-timezone', action='store_true',
                    help='removes the timezone auto-adjustment (default is UTC)')

parser.add_argument('--utc-offset', type=int,
                    help='manually apply a timezone offset (in seconds)')

parser.add_argument('--friends', action='store_true',
                    help='will perform quick friends analysis based on lang and timezone (rate limit = 15 requests)')

args = parser.parse_args()

# Here are globals used to store data - I know it's dirty, whatever
start_date = 0
end_date = 0

activity_hourly = {
    ("%2i:00" % i).replace(" ", "0"): 0 for i in range(24)
}

activity_weekly = {
    "%i" % i: 0 for i in range(7)
}

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

def getTime(tweet,latit,long):
      #get timezone
      zone = TimezoneFinder().timezone_at(lng=long,lat= latit)
      timezone = pytz.timezone(zone) #convert zone string to pytz format

      #convert to local time
      utc_time = dt.datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
      local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)
    #  finaltime = local_time.strftime(format='%Y-%m-%d %H:%M:%S')
      return local_time

def store(tweet):
      if tweet["place"] is None:
            geolocator = Nominatim(user_agent="mental_health")
            location = geolocator.geocode(tweet["user"]["location"])
            locationtime = getTime(tweet,location.latitude,location.longitude)
      else:
            latit = tweet["place"]["bounding_box"]["coordinates"][0][0][1]
            long = tweet["place"]["bounding_box"]["coordinates"][0][0][0]
            locationtime = getTime(tweet,latit,long)
      return locationtime
    #  print(json.dumps(tweet,indent=3))

def process_tweet(tweet):
    """ Processing a single Tweet and updating our datasets """
    global start_date
    global end_date
    global geo_enabled_tweets
    global retweets
    # Check for filters before processing any further
    if args.filter and tweet.source:
        if not args.filter.lower() in tweet.source.lower():
            return
    # get correct time
    tw_date = store(tweet._json)
    # Updating most recent tweet
    end_date = end_date or tw_date
    start_date = tw_date

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

    # Updating our activity datasets (distribution maps)
    activity_hourly["%s:00" % str(tw_date.hour).zfill(2)] += 1
    activity_weekly[str(tw_date.weekday())] += 1

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


def process_friend(friend):
    """ Process a single friend """
    friends_lang[friend.lang] += 1 # Getting friend language & timezone
    if friend.time_zone:
        friends_timezone[friend.time_zone] += 1


def get_friends(api, username, limit):
    """ Download friends and process them """
    for friend in tqdm(tweepy.Cursor(api.friends, screen_name=username).items(limit), unit="friends", total=limit):
        process_friend(friend)
# def get_friends(api, username, limit):
#     """ Download friends and process them """
#     for friend in tqdm(tweepy.Cursor(api.friends, screen_name=username).items(limit), unit="friends", total=limit):
#         process_friend(friend)
"""
def getTime(tweet,latit,long):
      #get timezone
      zone = TimezoneFinder().timezone_at(lng=long,lat= latit)
      timezone = pytz.timezone(zone) #convert zone string to pytz format
      #convert to local time
      utc_time = dt.datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
      local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)
      time = local_time.strftime(format='%a %b %d %H:%M:%S +0000 %Y')
      return time
#      print(time)
def store(tweet):
      if tweet["place"] is None:
            geolocator = Nominatim(user_agent="mental_health")
            location = geolocator.geocode(tweet["user"]["location"])
            getTime(tweet,location.latitude,location.longitude)
      else:
            latit = tweet["place"]["bounding_box"]["coordinates"][0][0][1]
            long = tweet["place"]["bounding_box"]["coordinates"][0][0][0]
            getTime(tweet,latit,long)
      #print(tweet.txt)
    #  print(json.dumps(tweet,indent=3))
"""
def get_tweets(api, username, limit):
    alltweet =[]
    fid2 = open(args.name + '_3200unfilteredTweets.csv','w')

    """ Download Tweets from username account """
    for status in tqdm(tweepy.Cursor(api.user_timeline, screen_name=username,tweet_mode='extended').items(limit),
                       unit="tw", total=limit):

        alltweet.append(status.full_text)
    #    store(status._json)        
        process_tweet(status)
    for line in alltweet:
       fid2.write("%s\n"%line)


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


def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter_api = tweepy.API(auth)
    allusers= ['zangerdanger',
               'R2D1ck2',
               'AIIStarBacon',
               'Kyashi_Cosplay', #Geo_enable#500
               'Froymyjoy', ##
              'aloofloofah', #Geo_enable#
               'bethwithanf_', #Geo_enable#o
               'JWebbConsulting',
               'toxidlotus', #Geo_enable#
               'Sandford_Police',
               'saveyoursellf',
               'melbendito']
    # Getting general account's metadata
    print("[+] Getting @%s account data..." % args.name)
    user_info = twitter_api.get_user(screen_name=args.name)

    print("[+] lang           : \033[1m%s\033[0m" % user_info.lang)
    print("[+] geo_enabled    : \033[1m%s\033[0m" % user_info.geo_enabled)
    print("[+] time_zone      : \033[1m%s\033[0m" % user_info.time_zone)
    print("[+] utc_offset     : \033[1m%s\033[0m" % user_info.utc_offset)

    if user_info.utc_offset is None:
        print("[\033[91m!\033[0m] Can't get specific timezone for this user")

    if args.utc_offset:
        print("[\033[91m!\033[0m] Applying timezone offset %d (--utc-offset)" % args.utc_offset)

    print("[+] statuses_count : \033[1m%s\033[0m" % user_info.statuses_count)

    # Will retreive all Tweets from account (or max limit)
    num_tweets = numpy.amin([args.limit, user_info.statuses_count])
    print("[+] Retrieving last %d tweets..." % num_tweets)

    # Download tweets
    get_tweets(twitter_api, args.name, limit=num_tweets)
    print("[+] Downloaded %d tweets from %s to %s (%d days)" % (num_tweets, start_date, end_date, (end_date - start_date).days))

    # Checking if we have enough data (considering it's good to have at least 30 days of data)
    if (end_date - start_date).days < 30 and (num_tweets < user_info.statuses_count):
        print("[\033[91m!\033[0m] Looks like we do not have enough tweets from user, you should consider retrying (--limit)")

    if (end_date - start_date).days != 0:
        print("[+] Average number of tweets per day: \033[1m%.1f\033[0m" % (num_tweets / float((end_date - start_date).days)))

    # Print activity distrubution charts
    print_charts(activity_hourly, "Daily activity distribution (per hour)")
    print_charts(activity_weekly, "Weekly activity distribution (per day)", weekday=True)

    print("[+] Detected languages (top 5)")
    print_stats(detected_langs)

    print("[+] Detected sources (top 10)")
    print_stats(detected_sources, top=10)

    print("[+] There are \033[1m%d\033[0m geo enabled tweet(s)" % geo_enabled_tweets)
    if len(detected_places) != 0:
        print("[+] Detected places (top 10)")
        print_stats(detected_places, top=10)

    print("[+] Top 10 hashtags")
    print_stats(detected_hashtags, top=10)

    print("[+] @%s did \033[1m%d\033[0m RTs out of %d tweets (%.1f%%)" % (args.name, retweets, num_tweets, (float(retweets) * 100 / num_tweets)))

    # Converting users id to screen_names
    retweeted_users_names = {}
    for k in retweeted_users.keys():
        retweeted_users_names[id_screen_names[k]] = retweeted_users[k]

    print("[+] Top 5 most retweeted users")
    print_stats(retweeted_users_names, top=5)

    mentioned_users_names = {}
    for k in mentioned_users.keys():
        mentioned_users_names[id_screen_names[k]] = mentioned_users[k]
    print("[+] Top 5 most mentioned users")
    print_stats(mentioned_users_names, top=5)

    print("[+] Most referenced domains (from URLs)")
    print_stats(detected_domains, top=6)

    if args.friends:
        max_friends = numpy.amin([user_info.friends_count, 300])
        print("[+] Getting %d @%s's friends data..." % (max_friends, args.name))
        try:
            get_friends(twitter_api, args.name, limit=max_friends)
        except tweepy.error.TweepError as e:
            if e[0][0]['code'] == 88:
                print("[\033[91m!\033[0m] Rate limit exceeded to get friends data, you should retry in 15 minutes")
            raise

        print("[+] Friends languages")
        print_stats(friends_lang, top=6)

        print("[+] Friends timezones")
        print_stats(friends_timezone, top=8)

    activities = []
    for i in range(24):
        activities.append(str(activity_hourly["%s:00" % str(i).zfill(2)]))
    print_values(args.name + '_activity_hourly.csv', activities)
    activities = []
    for i in range(7):
        activities.append(str(activity_weekly["%s" % str(i)]))
    print_values(args.name + '_activity_weekly.csv', activities)


if __name__ == '__main__':
    try:
        main()
    except tweepy.error.TweepError as e:
        print("[\033[91m!\033[0m] Twitter error: %s" % e)
    except Exception as e:
        print("[\033[91m!\033[0m] Error: %s" % e)
