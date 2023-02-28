 from astropy.coordinates import SkyCoord, EarthLocation, ICRS, AltAz, FK5, solar_system_ephemeris, get_body
from astropy.time import Time
import numpy as np
import astropy.units as u


#################### CODE NOTES ####################
(ENU) system uses the Cartesian coordinates (xEast,yNorth,zUp) to represent position relative to a local origin.

(AltAZ) A coordinate or frame in the Altitude-Azimuth system (Horizontal coordinates) with respect to the WGS84 ellipsoid. 
Azimuth is oriented East of North (i.e., N=0, E=90 degrees). 
Altitude is also known as elevation angle, so this frame is also in the Azimuth-Elevation system.

(ICRS) The International Celestial Reference System (ICRS) is a celestial coordinate system fixed to the stars/constellations as would be seen from the Sun, or more precisely, from the barycenter of the solar system.
 It specifies the coordinate's epoch as J2000. 0.
 ###################################################
"""

with open('ConfigFile.txt') as f:
    for line in f:
        if line.startswith('//Star Name:'):
            star_name = line.strip().split(':')[1].strip()
        elif line.startswith('//Latitude:'):
            latitude = float(line.strip().split(':')[1].strip())
        elif line.startswith('//Longitude:'):
            longitude = float(line.strip().split(':')[1].strip())
        elif line.startswith('//Elevation:'):
            elevation = float(line.strip().split(':')[1].strip())
 
#Calculate RA & DEC of star from a given position
def radec(star_name, latitude, longitude, elevation):

    # set the location and time
    location = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg, height=elevation*u.m)
    time = Time.now() #TIME GMT #!!!    

    # Set the solar system ephemeris to 'jpl'
    with solar_system_ephemeris.set("jpl"):
        starpos = get_body(star_name, time, location)
    
    print(starpos)
    
    print("Name:", star_name)
    print("RA: ", starpos.ra.value)
    print("Dec: ", starpos.dec.value)
    
radec(star_name, latitude, longitude, elevation)
