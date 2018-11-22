#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Get a snapshot of Gracia district and whereabouts 
from "http://api.citybik.es/v2/networks/bicing".

Store the snapshot in mongoDB and tag it with a timestamp.

'bike_leeching.py' belongs to the process of data retrieval for statistics ellaboration.
The corpus of data will be a recurrent 5 minute snapshot from the API.
Instead of coding a loop of retrieval and sleep for 5 minutes, the process
is managed from linux cron command. 
A loop/sleeping retrieval daemon needs to manage KILL interruptions in order to avoid 
getting killed while writing data into the DB. I chosed a simple solution: not to code
the management of KILLs and let cron to manage the retrieve-sleep loop. 

'''

import requests
import urllib, json

import datetime

import pymongo as mongo
from pymongo import MongoClient


__author__ = "Alexis Torrano"
__email__ = "a.torrano.m@gmail.com"
__status__ = "Production"


##***********************************************************************
url = "http://api.citybik.es/v2/networks/bicing"
response = requests.get(url, timeout=15)
now = datetime.datetime.now()
timeStampStr = str(now)
timeStampSeconds = now.timestamp()


# Check for HTTP codes other than 200
if response.status_code != 200:
    print("ERROR ", str(response.status_code))
    import sys
    sys.exit()

jsresp = response.json()
originPBOX = '08012'
stations = jsresp['network']['stations']        
# expand fields in 'extra' dictionary as new columns for one-step access
for x in stations:
    for k,v in x['extra'].items():
        x[k] = v    

## ASSUMPTION: 'name' attribute is ALTERNATIVE KEY for any station -> so, no repeats in loop
GraciaStations = [x for x in stations if originPBOX == x['extra']['zip']]
neighbourIdxSet = set(n for g in GraciaStations for n in g['extra']['NearbyStationList'])
NeighbourStations = [x for x in stations if x['uid'] in neighbourIdxSet]

'''
Short of time, many decissions and things to solve; so, store full json for
every station. After 24h leeching I will purge what I do not need and prepare a CHEN
to store a retrieval of statistics.
'''

# store dataframes in mongo with a timestamp

mongoC = MongoClient('mongodb://localhost:27017/')
dbHosco = mongoC['HOSCO']
createIndex = not ("timeBikeAllocation " in dbHosco.list_collection_names())
timeBikeAllocation = dbHosco['timeBikeAllocation']
if createIndex:
    # collection "timeBikeAllocation" did not exist previously. It needs an index after creation.    
    dbHosco['timeBikeAllocation'].create_index("timeStampStr", unique=True)
    dbHosco['timeBikeAllocation'].create_index("timeStampSeconds", unique=True)

try:
    timeBikeAllocation.insert_one({
        "_id":timeStampSeconds,
        "timeStampStr":timeStampStr,
        "timeStampSeconds":timeStampSeconds,
        "gracia":GraciaStations,
        "neighbours":NeighbourStations})
        
except Exception as e:
    print(str(e))


### timeBikeAllocation.delete_one({'timeStamp':timestamp})        
#**************************************************************

