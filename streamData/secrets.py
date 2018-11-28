TWITTER_APP_KEY="PLoBOvek1BRQUCe9sUqIb8nlS"
TWITTER_APP_SECRET="WpuhSqp5944W3Xt5oTHtJCje25840clSwJ9s7UEbkcAdgveONO"

TWITTER_KEY="1054970208803344384-ptpHbL3nmxP9RLNFcse4dtjfs9Bbw2"
TWITTER_SECRET="MtOLdYvf8Ib7osqGEJaQKJgkAeDyIHMqKdL253uhYqpRf"

TRACK_TERMS = ["trump","bernie", "clinton","hillary clinton", "donald trump"]
CONNECTION_STRING = "sqlite:///tweets.db"
CSV_NAME = "tweets.csv"
TABLE_NAME = "election"
CSV_NAME = "electionResults"

try:
    from private import *
except Exception:
    pass
