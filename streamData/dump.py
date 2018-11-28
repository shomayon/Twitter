import secrets
import tweepy
import dataset
from textblob import TextBlob
from datafreeze import freeze

db = dataset.connect(secrets.CONNECTION_STRING)
result = db[secrets.TABLE_NAME].all()
freeze(result, format='csv', filename=secrets.CSV_NAME)
