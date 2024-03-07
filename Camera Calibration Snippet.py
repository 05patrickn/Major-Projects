from astropy.coordinates import SkyCoord, EarthLocation, ICRS, AltAz, solar_system_ephemeris, get_body
from astropy.time import Time
import numpy as np
import astropy.units as u
import pandas as pd
import geopy
from geopy import distance
import math
from GenerateStarList import matrix_multiply

 
 ############################## Note this is a section of the code, the rest is protected for intellectual property. #########################

def radec_planet(planet_name, origin_camera_system):
    results = []
    for i in range(len(planet_name['//TIMEUTC'])):
        # set the location and time
        location = EarthLocation(lat=origin_camera_system["//Latitude N:"]*u.deg, 
                                 lon=origin_camera_system["//Longitude E:"]*u.deg, 
                                 height=origin_camera_system["//Elevation in m"]*u.m)       
        time = Time(str(planet_name.iloc[i, planet_name.columns.get_loc('//TIMEUTC')]), 
                    format="isot",  scale='utc')
        
        observationFrame = AltAz(obstime=time, location=location)
        with solar_system_ephemeris.set('jpl'):
            planet = get_body(str(planet_name.iloc[1, 0]), time, location)
    
        planetFromFrame = planet.transform_to(observationFrame)
        


        # append the results to a list of dictionaries
        results.append({
            'planet_name': str(planet_name.iloc[1, 0]),
            'time_utc': str(time),
            'ra':planet.ra.value[0]/15 ,
            'dec':planet.dec.value[0] ,
            'x': x[0],
            'y': y[0],
            'z': z[0]
        })
        return x,y,z
        
    # convert the list of dictionaries to a Pandas dataframe
    df = pd.DataFrame(results)
    df.to_csv("results2.txt", sep="\t", index=True, header=True)
    return df 
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
    
def main():
    #Config file reader (Note structure of config file)
    jupiter= pd.read_excel('ConfigFile.xlsx', sheet_name='jupiter')
    sirius = pd.read_excel('ConfigFile.xlsx', sheet_name='sirius')
    origin_camera_system= pd.read_excel('ConfigFile.xlsx', sheet_name='origin_camera_system')
    camera_position=pd.read_excel('ConfigFile.xlsx', sheet_name='camera_position')


    #Call Functions
    #radec_star(sirius, origin_camera_system)
    #radec_planet(jupiter, origin_camera_system)
    calculate_distance(camera_position)
