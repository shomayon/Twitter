#streaming data per user

import json
import tweepy
import numpy
from textblob import TextBlob
import dataset
import secrets
from sqlalchemy.exc import ProgrammingError

db = dataset.connect(secrets.CONNECTION_STRING)

#Setting up a listener to print text 
class StreamListener(tweepy.StreamListener):

    #An instance of the Status class which contains properties describing tweet
    def on_status(self, status):
        if status.retweeted:
            return

        #extracting information
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color

        #processing tweets
        blob = TextBlob(text)
        sent = blob.sentiment
        polarity = sent.polarity
        subjectivity = sent.subjectivity
    
        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

        table = db[secrets.TABLE_NAME]
        try:
            table.inset(dict(
                user_description=description,
                user_location=loc,
                coordinates=coords,
                text=text,
                geo=geo,
                user_name=name,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color,
                polarity=sent.polarity,
                subjectivity=sent.subjectivity,
            ))
        except ProgramminError as err:
            print(err)

    #disconnect when reached rate limit for API
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

def main():
    auth = tweepy.OAuthHandler(secrets.TWITTER_APP_KEY, secrets.TWITTER_APP_SECRET)
    auth.set_access_token(secrets.TWIITER_KEY, secrets.TWITTER_SECRET)
    api = tweepy.API(auth)

    #create instance of StreamListener class
    stream_listener = StreamListener()
    #create instance of tweepy Stream class which streams tweets
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=secrets.TRACK_TERMS)
