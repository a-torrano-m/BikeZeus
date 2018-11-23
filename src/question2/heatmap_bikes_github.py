#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
QUESTION 2 for HOSCO Data Engineer assignment.

    Find most favourable bike-stations to choose a place for living in Gracia district..

'''

import requests
import urllib, json

import datetime

import pymongo as mongo
from pymongo import MongoClient

import folium
from folium import plugins
from folium.plugins import HeatMap
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import matplotlib.pyplot as plt
import random as rnd

import bson

__author__ = "Alexis Torrano"
__email__ = "a.torrano.m@gmail.com"
__status__ = "Production"

# %matplotlib inline

##***********************************************************************

def countZeroBikeStations(snapshot,tablCounter):
    GraciaStations = snapshot['gracia']
    neighbourStations = snapshot['neighbours']    
    
    # Increase the counter of each station when bikes are depleted.
    # If station is stil not registered in the counters list, it
    # sets a counter to 0 for the station.
    for x in GraciaStations:        
        if not x['id'] in tablCounter:
            tablCounter[x['id']] = 0
                
        if 0 == x['free_bikes']:            
            tablCounter[x['id']] += 1
        

    for x in neighbourStations:        
        if not x['id'] in tablCounter:
            tablCounter[x['id']] = 0
                
        if 0 == x['free_bikes']:            
            tablCounter[x['id']] += 1



def getStaticFeaturesOfStations(snapshot,volatileFeatures):
    GraciaStations = snapshot['gracia']
    neighbourStations = snapshot['neighbours']       
    
    pandasGraciaStations = pd.DataFrame.from_dict(GraciaStations)
    pandasNeighbourStations = pd.DataFrame.from_dict(neighbourStations)
        
    pandasGraciaStations.drop(volatileFeatures,axis=1)
    pandasNeighbourStations.drop(volatileFeatures,axis=1)
        
    return pandasGraciaStations,pandasNeighbourStations

def getHeatSpots(pandasDF,counterDF,stats,m,inverseHeat,heatSpotsList):
    
    '''
    For each station <getHeatSpots> produces a list of spots for a heatmap. 
    Each spot originally represents a segment of time where the station had 0 free_bikes.
    The more time a station has been depleted the hotter it should appear in
    the heatmap.
    
    There is an option for the inverseHeat version of the heatmap. Then, <heat>
    measures availability of bikes in the station.
    
    The amount of time segments of depletion induces the color of the station marker
    in the city map. The color assignation follows the quantiles in the distribution
    of depleted time segments. And such assignation is inmovable whether <inverseHeat>
    is chosen or not.
    '''
    
    for index, row in pandasDF.iterrows():
        heat = counterDF[row.id]
        
        # Basic semantics of <heat> is applied in marker color assignation 
        if heat <= stats['min']:
            st_marker_color='blue'
        elif heat < stats['25%']:
            st_marker_color='green'            
        elif heat < stats['75%']:
            st_marker_color='orange'            
        elif heat < stats['max']:
            st_marker_color='red'
        elif heat == stats['max']:
            st_marker_color='black'
                     
        # Once color marker is assigned, <inverseHeat> may be activated
        if inverseHeat:
            # The parameters for <inverseHeat> were found uppon manual factor exploration
            # based on visual identification for better distinguishable separation area.
            heat = stats['max'] - heat            
            ratioHeat = float(heat) / float(stats['max'])            
            stdev = 2.0 * ratioHeat * ratioHeat * ratioHeat
            scale = 1000.0            
        else:
            ratioHeat = float(heat) / float(stats['max'])
            stdev = 1.0
            scale = 1000.0

        
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=15,
                            popup=row['name'],
                            fill_color="#3db7e4", # divvy color
                           ).add_to(m)
        
        folium.Marker([row['latitude'], row['longitude']],                        
                            popup=str(row['name']+"::"+str(heat)),
                            icon=folium.Icon(color=st_marker_color)
                           ).add_to(m)
         
         
        # produce a list of coordinates for each bike in order to feed the heatmap        
        for s in range(int(100.0*ratioHeat)):        
            disturbLat = ((-stdev+2.0*stdev*rnd.random())/scale)
            disturbLon = ((-stdev+2.0*stdev*rnd.random())/scale)
            heatSpotsList.append([row['latitude']+disturbLat, row['longitude']+disturbLon])
        
        '''
        For each station, each 5' segment with 0 bikes will entail an occurrency 
        in the heatmap giving a random perturbation to original station coordinates.
        '''
        
def heatmap(pandasGraciaStations,neighboursDF,counterDF,inverseHeat=False):
    ## Must paint in map all x in list <GraciaStations> and all y in y.extra.NearbyStationList
    
    '''
    I got Gracia district coordinates from openstreetmap: 
    https://nominatim.openstreetmap.org/details.php?place_id=198819829
    https://www.openstreetmap.org/relation/3773080#map=14/41.4102/2.1599
    
    map center: 41.41023,2.15087 view on osm.org
    map zoom: 14
    viewbox: 2.08989,41.42632,2.21177,41.39413
    '''    
    
    m = folium.Map([41.41023, 2.15087], zoom_start=14)
      
    # mark each station as a point: put a marker and a pop-up with station name
    # todo : add free_bikes at the pop-up
    zeroBikesList = []    
    #count,mean,std,mini,pct25,pct50,pct75,maxi=counterDF.describe()
    stats=counterDF.describe()
    
    # Get coordinates for occurences to add to heatmap and at markers in map for each Bicing Station
    getHeatSpots(pandasGraciaStations,counterDF,stats,m,inverseHeat,zeroBikesList)    
    getHeatSpots(neighboursDF,counterDF,stats,m,inverseHeat,zeroBikesList)        
    
    ## HEATMAP CALL
    if inverseHeat:
        min_opacity=0.1
        max_val=0.8
    else:
        min_opacity=0.5
        max_val=1.0
    
    
    m.add_child(plugins.HeatMap(zeroBikesList, radius=50,blur=70,min_opacity=min_opacity,max_val=max_val))    
    
    return(m)
    
    #TODO Heatmap radius : add a slider to Jupyter

##***********************************************************************
## Please remember advice from question_0, the leeching process.
## Jupyter notebook will generate results not from a mongoDB query but from 
## a query to mongoDB database dump file.
## All code line preceded by "### MONGO ###" was used in case of direct mongoDB interaction.

### MONGO ### mongoC = MongoClient('mongodb://localhost:27017/')
### MONGO ### dbHosco = mongoC['HOSCO']
### MONGO ### timeBikeAllocation = dbHosco['timeBikeAllocation']

bsonfilePath = '../../data/HOSCO/'
bsonfileName = 'timeBikeAllocation.bson'

try:
    with open(bsonfilePath+bsonfileName,'rb') as f:
        timeBikeAllocation_list = bson.decode_all(f.read())
      
except Exception as e:
    print(str(e))



# Get the first snapshot to build the dataframe with station's 
# static features.
### MONGO ### snapshot = timeBikeAllocation.find_one()
snapshot = timeBikeAllocation_list[0]

volatileFeatures = ['free_bikes', 'empty_slots', 'timestamp']
pandasGraciaStations,pandasNeighbourStations = getStaticFeaturesOfStations(snapshot,volatileFeatures)
# remove from pandasNeighbourStations any station contained at pandasGraciaStations 
pandasNeighbourStations = pandasNeighbourStations[~ pandasNeighbourStations.id.isin(pandasGraciaStations.id)]
    
tablCounter = {}
### MONGO ### cursor = timeBikeAllocation.find({})
timeSliceCount = 0
### MONGO ### for snapshot in cursor:
for snapshot in timeBikeAllocation_list:
    countZeroBikeStations(snapshot,tablCounter)
    timeSliceCount += 1

## Prepare data for graphical report;
## paint heatmap from tablCounter

pandasTablCounter = pd.Series(tablCounter, name='countTimeSliceZeroBikes')
pandasTablCounter.index.name = 'id'
pandasTablCounter.reset_index()

outputPath="../../html/"
m = heatmap(pandasGraciaStations,pandasNeighbourStations,pandasTablCounter)
m.save(outputPath+"heatmap.html")

m = heatmap(pandasGraciaStations,pandasNeighbourStations,pandasTablCounter,inverseHeat=True)
m.save(outputPath+"heatmap_inverseHeat.html")






