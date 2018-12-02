#analyzing tweets
import pandas as pd
import matplotlib.pyplot as plt
import users
import os
import json
import csv
import tweepy
from pathlib import Path
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from pprint import pprint
import pytz
import datetime as dt

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
def getLocalTime(time, timezone):
    utc_time = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)
    finaltime = local_time.strftime(format='%a %b %d %H:%M:%S %Y')
    return(finaltime)

def getTimeZone(latit, longit):
    #get timezone
    zone = TimezoneFinder().timezone_at(lng=longit,lat=latit)
    timezone = pytz.timezone(zone) #convert zone string to pytz format  
    return (timezone)


def cleanLocation(user, myGeo):

    file_name = user +'_tweets.csv'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = Path(dir_path+'/twitter_data/'+file_name)

    # fieldnames = ['Tweet_ID','Tweet','Screen_Name','Description','User_Location','Time','Geo_Enabled','Lat','Long']

    if path.exists():
        print("...%s file found" % user)
        with open(path, 'r') as infile:
            reader = csv.DictReader(infile)
            #writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)  
            for row in reader:
                location = row["User_Location"]
                time = row["Time"]
                lat = row["Lat"]
                longit = row["Long"]
                if location is None:
                    print("The user has no profile location... Thank you, next")
                    break
                #Base Case
                #if the dictionary is empy add the first user location
                if len(myGeo) == 0:
                    geolocator = Nominatim(user_agent="mental_health")
                    loc = geolocator.geocode(location)
                    #get timzone and store into hashmap
                    timezone = getTimeZone( loc.latitude, loc.longitude)
                    myGeo[location] = timezone               
                    finaltime = getLocalTime(time, timezone)
                    print(finaltime)
                else:   #check if individual tweets have a location
                    #check for new user location
                    #if it is not in dictionary add it
                    if location not in myGeo:
                        geolocator = Nominatim(user_agent="mental_health")
                        loc = geolocator.geocode(location)
                        timezone = getTimeZone(loc.latitude, loc.longitude)
                        myGeo[location] = timezone
                        finaltime = getLocalTime(time, timezone)
                        print(finaltime)
                    #how to find location given coordinates
                    if lat and longit is not None:
                       # timezone = getTimeZone(lat, longit)  
                        #lat = row["Lat"]
                        #longit = row["Long"]
                        print("Tweet has a location")
                        #print(lat)
                        #print(longit) 
    else:
        print("...%s file NOT found" % user)


if __name__ == "__main__":
    #create a dictionary
    myGeo = {}
    for user in users.SCREEN_NAME:
        cleanLocation(user, myGeo)
    print("myGeo dict():")
    for key, val in myGeo.items():
        print(key,"=>", val)
