#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

'''
QUESTION 1 for HOSCO Data Engineer assignment.

    Get bike and slot availability for the places
    in the assignment.
    ORIGIN : C/ SARDENYA, 292 08025
    DESTINATION : AV. DE LA CATEDRAL, 6 08002
'''

import requests
import urllib, json

__author__ = "Alexis Torrano"
__email__ = "a.torrano.m@gmail.com"
__status__ = "Production"


##***********************************************************************
url = "http://api.citybik.es/v2/networks/bicing"
response = requests.get(url, timeout=15)    
# Check for HTTP codes other than 200
if response.status_code != 200:
    print("ERROR ", str(response.status_code))
    import sys
    sys.exit()

jsresp = response.json()
originStationName=u'C/ SARDENYA, 292'
stations = jsresp['network']['stations']        
## ASSUMPTION: 'name' attribute is ALTERNATIVE KEY for any station -> so, no repeats in loop
fbikes = [x['free_bikes'] for x in stations if originStationName in x['name']][0]

destStationName=u'AV. DE LA CATEDRAL 6'
stations = jsresp['network']['stations']        
## ASSUMPTION: 'name' attribute is ALTERNATIVE KEY for any station -> so, no repeats in loop
fslots = [x['empty_slots'] for x in stations if destStationName in x['name']][0]

data = {}
data['ORIGIN'] = {'free_bikes':fbikes, 'station_name':originStationName}
data['DESTINATION'] = {'free_slots':fslots, 'station_name':destStationName}
json_data = json.dumps(data)
print(json_data)



