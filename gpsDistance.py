
import math as math

__author__ = "Alexis Torrano"
__email__ = "a.torrano.m@gmail.com"
__status__ = "Production"


## *************************************************************
def GPS2Cartesian(p):
    R = 6371 # Km, Earth's Radius
    lat,lon = p
    x = R * math.cos(lat) * math.cos(lon)
    y = R * math.cos(lat) * math.sin(lon)
    return (x,y)

## *************************************************************
def GPS_directTrig_ManhattanDist(alfa,omega):

    ## MANHATTAN Distance for GPS coordinates
    ## formulae sources at : http://www.movable-type.co.uk/scripts/latlong.html
    
    ## example alfa and omega points.
    ## google maps : street/bike distance = 4.4km [3.8..4.8], time = [12'..15']
    
    
    lamb1,delt1 = alfa
    
    lamb2,delt2 = omega
    
    
    ## latitude difference:    
    deltPhi = abs(delt2 - delt1)
    
    ## longitude difference:    
    deltLamb = abs(lamb2-lamb1)
    
    ## The haversine formula. 
    ## The webpage it uses the haversine formula, 
    # but that would give us a straight-line distance. 
    # So to do it with Manhattan distance, we will do the latitude and longitude 
    # distances sepparatedly.
    
    ### latitude distance, as if longitude was 0 (a big part of the formula got ommited):
    
    aSqrt = math.sin(deltPhi / 2.0)
    a = aSqrt ** 2    
    c = 2.0 * math.atan2(aSqrt,math.sqrt(1.0-a))
    R = 6371 # Km, Earth radius    
    latitudeDistance = R*c 
    
    ### longitude distance, as if the latitude was 0:    
    aSqrt = math.sin(deltLamb/2.0)
    a = aSqrt**2    
    c = 2.0 * math.atan2(aSqrt, math.sqrt(1.0-a))    
    longitudeDistance = R*c
    
    
    Manhattan =  abs(latitudeDistance) + abs(longitudeDistance)
    
    return(Manhattan)

## *************************************************************
def GPS_gps2cartesian_ManhattanDist(alfa,omega):
    
    alfaX, alfaY = GPS2Cartesian(alfa)
    omegaX, omegaY = GPS2Cartesian(omega)
    
    Manhattan = abs(alfaX - omegaX) + abs(alfaY-alfaY)
    return(Manhattan)
## *************************************************************

#function to convert degrees to radians
def deg2rad(deg): return(deg*math.pi/180.0)

def gcd_slc(long1, lat1, long2, lat2):
    # source : https://enholm.net/2017/07/14/crime-analysis-series-calculating-great-circle-distance-two-points-r-using-haversine-formula/
    # Convert degrees to radians
    long1=deg2rad (long1)
    lat1=deg2rad(lat1)
    long2=deg2rad(long2)
    lat2=deg2rad(lat2)
    R = 3959.0 # Earth mean radius [miles]
    d = math.acos(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2) * math.cos(long2-long1)) * R
    return(d*1.60934) # Distance in miles converted to Km


def manhattanDist(alfa,omega):
    ## source : https://enholm.net/2017/07/17/crime-analysis-series-manhattan-distance-r/
    lat1, long1 = alfa
    lat2, long2 = omega
    v_dist=gcd_slc(long1, lat1, long1, lat2)
    h_dist=gcd_slc(long1, lat2, long2, lat2)
    return (v_dist+h_dist)

## *************************************************************



def test1():
    alfa = (41.395048,2.161913) # Pedrera
    omega = (41.387868,2.164649) # ALIBRI
    googleD=1.14 #km
    
    
    print ( "GPS_directTrig_ManhattanDist(alfa,omega) = " + str(GPS_directTrig_ManhattanDist(alfa,omega)))
    print ( "GPS_gps2cartesian_ManhattanDist(alfa,omega) = " + str(GPS_gps2cartesian_ManhattanDist(alfa,omega)))
    print ("manhattanDist(alfa,omega) = " + str(manhattanDist(alfa,omega)))

def test2():
    alfa = (41.403923,2.156779) # Cine Verdi
    omega = (41.384366,2.176134) # La Catedral
    googleD=3,1 #km, t=9min
    
    print("alfa:gracia, omega: catedral")
    print ( "GPS_directTrig_ManhattanDist(alfa,omega) = " + str(GPS_directTrig_ManhattanDist(alfa,omega)))
    print ( "GPS_gps2cartesian_ManhattanDist(alfa,omega) = " + str(GPS_gps2cartesian_ManhattanDist(alfa,omega)))
    print ("manhattanDist(alfa,omega) = " + str(manhattanDist(alfa,omega)))
    # GPS_directTrig_ManhattanDist(alfa,omega) = 247.908352
    # GPS_gps2cartesian_ManhattanDist(alfa,omega) = 123.572524318
    # manhattanDist(alfa,omega) = 3.78962413695
    # 3.78 vs 3.1 ... it is almost good enough

