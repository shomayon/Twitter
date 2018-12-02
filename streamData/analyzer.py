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

def getTimeZone(location):
    geolocator = Nominatim(user_agent="mental_health")
    loc = geolocator.geocode(location)
    #get timezone
    zone = TimezoneFinder().timezone_at(lng=loc.longitude,lat=loc.latitude)
    timezone = pytz.timezone(zone) #convert zone string to pytz format  
    return (timezone)

def store(tweet):
      if tweet["place"] is None:
            geolocator = Nominatim(user_agent="mental_health")
            location = geolocator.geocode(tweet["user"]["location"])
            locationtime = getTime(tweet,location.latitude,location.longitude)
      return locationtime
      print(json.dumps(tweet,indent=3))

#assuming the user has a location
def updateTime(location, time):
    if location is None:
        print("The user has no profile location")
        return
    else:
        geolocator = Nominatim(user_agent="mental_health")
        loc = geolocator.geocode(location)
        locationtime = getTime(time,loc.latitude,loc.longitude)   
    return locationtime 

def main():

    myGeo = {}
    for user in users.SCREEN_NAME:
        file_name = user +'_tweets.csv'
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = Path(dir_path+'/twitter_data/'+file_name)

        new_file_name = user+'clean_tweets.csv'
        newdir_path = os.path.dirname(os.path.realpath(__file__))
        newpath = Path(newdir_path+'/twitter_data/'+file_name)

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
                    #if the dictionary is empy add the first user location
                    if len(myGeo) == 0:
                        #geolocator = Nominatim(user_agent="mental_health")
                        #loc = geolocator.geocode(location)
                        #localtime = getTime(time, loc.latitude, loc.longitude)
                        #zone = TimezoneFinder().timezone_at(lng=loc.longitude,lat= loc.latitude)
                        
                        #timezone = pytz.timezone(zone) #convert zone string to pytz format
                        timezone = getTimezone(location)
                        myGeo[location] = timezone               
                        
                        finaltime = getLocalTime(time, timezone)
                        #convert to local time
                        utc_time = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
                        # utc_time = dt.datetime.strptime(time, '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
                        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)
                        #finaltime = local_time.strftime(format='%Y-%m-%d %H:%M:%S')
                        finaltime = local_time.strftime(format='%a %b %d %H:%M:%S %Y')
                        #writer.writerow(row)
                        print(finaltime)
                    else:   #check if individual tweets have a location
                        #check for new user location
                        if location not in myGeo:
                            geolocator = Nominatim(user_agent="mental_health")
                            loc = geolocator.geocode(location)
                            zone = TimezoneFinder().timezone_at(lng=loc.longitude, lat=loc.latitude)
                            timezone = pytz.timezone(zone)
                            myGeo[location] = timezone
                        elif lat and longit is not None:
                            #lat = row["Lat"]
                            #longit = row["Long"]
                            print("Tweet has a location")
                            print(lat)
                            print(longit) 
                for key, val in myGeo.items():
                    print(key,"=>", val)
    else:
        print("...%s file NOT found" % user)


if __name__ == "__main__":
    main()
