TWITTER_APP_KEY="PLoBOvek1BRQUCe9sUqIb8nlS"
TWITTER_APP_SECRET="WpuhSqp5944W3Xt5oTHtJCje25840clSwJ9s7UEbkcAdgveONO"

TWITTER_KEY="1054970208803344384-ptpHbL3nmxP9RLNFcse4dtjfs9Bbw2"
TWITTER_SECRET="MtOLdYvf8Ib7osqGEJaQKJgkAeDyIHMqKdL253uhYqpRf"

#TWITTER_APP_KEY = "GwpuXi1ZMyc0ATSb3FEPaTyOU"
#TWITTER_APP_SECRET="0Y1jaPrDOa0uGsxQc4DSDphRWPPYCtVZ0TtvgZorAvzywIZtXJ"

#TWITTER_KEY="220846580-ZUElx1lLAd5XRxrL9hYVG6CBkbjLUl3ftvCGIMqE"
#TWITTER_SECRET="WEFkSeH59z92ptB76tGKnh8l6mMKmWN1fVKqV6dYCuc77"

USER_IDS = ["26459251"]
TRACK_TERMS = ["trump","bernie", "clinton","hillary clinton", "donald trump"]
CONNECTION_STRING = "sqlite:///tweets.db"
CSV_NAME = "tweets.csv"
TABLE_NAME = "tweets"
CSV_NAME = "tweetResults"

try:
    from private import *
except Exception:
    pass
