#
# Usage:
# python tweets_analyzer.py -n screen_name
#
# Install:
# pip install tweepy ascii_graph tqdm numpy

import json
import tweepy
import numpy
import argparse
import collections
import re
import string
import csv
import secrets
from tqdm import tqdm
import sys
import jsonpickle
import os

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

    #  print(json.dumps(tweet,indent=3))


def get_tweets(api, username, limit):
    """ Download Tweets from username account """
    for tweet in tqdm(tweepy.Cursor(api.user_timeline, screen_name=username,tweet_mode='extended').items(limit),unit="tw", total=limit):
        print(tweet)


def main():
    auth = tweepy.OAuthHandler(secrets.TWITTER_APP_KEY, secrets.TWITTER_APP_SECRET)
    auth.set_access_token(secrets.TWITTER_KEY, secrets.TWITTER_SECRET)
    api = tweepy.API(auth)

    user_info = api.get_user(screen_name=args.name)

    # Will retreive all Tweets from account (or max limit)
    num_tweets = numpy.amin([args.limit, user_info.statuses_count])
    print("[+] Retrieving last %d tweets..." % num_tweets)
    
    # Download tweets
    get_tweets(api, args.name, limit=num_tweets)
    print("[+] Downloaded %d tweets from %s to %s (%d days)" % (num_tweets, start_date, end_date, (end_date - start_date).days))


if __name__ == '__main__':
    try:
        main()
    except tweepy.error.TweepError as e:
        print("[\033[91m!\033[0m] Twitter error: %s" % e)
    except Exception as e:
        print("[\033[91m!\033[0m] Error: %s" % e)
