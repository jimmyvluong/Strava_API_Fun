# import secrets and tokens from config.py
from config import client_id, client_secret, refresh_token

import requests
import urllib3


#Pandas will be the backbone of our data manipulation.
import pandas as pd
from pandas.io.json import json_normalize

import numpy as np

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token,
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

print(my_dataset[0]["name"])
print(my_dataset[0]["map"]["summary_polyline"])

activities = json_normalize(my_dataset)
#activities.columns #See a list of all columns in the table
#activities.shape #See the dimensions of the table.

#Create new dataframe with only columns I care about
#cols = ['name', 'upload_id', 'type', 'distance', 'moving_time',   
#         'average_speed', 'max_speed','total_elevation_gain',
#         'start_date_local'
#       ]
#activities = activities[cols]
#Break date into start time and date
activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
activities['start_time'] = activities['start_date_local'].dt.time
activities['start_date_local'] = activities['start_date_local'].dt.date
activities.head(5)

# For testing, only take top 3 records
activities = activities.query("type == 'Ride'")
activities = activities.head(1)

print(my_dataset[0]["name"])
print(my_dataset[0]["map"]["summary_polyline"])
print(np.average(activities["average_speed"]))
print(np.average(activities["distance"]))
###################
# import modules
import os
import time
import matplotlib.pyplot as plt
import folium
import polyline
import base64
from tqdm import tqdm
# disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# add decoded summary polylines
activities['map.polyline'] = activities['map.summary_polyline'].apply(polyline.decode)
print("turkey")
#####################
# define function to get elevation data using the open-elevation API
def get_elevation(latitude, longitude):
    base_url = 'https://api.open-elevation.com/api/v1/lookup'
    payload = {'locations': f'{latitude},{longitude}'}
    r = requests.get(base_url, params=payload).json()['results'][0]
    return r['elevation']
# get elevation data
elevation_data = list()
for idx in tqdm(activities.index):
    activity = activities.loc[idx, :]
    elevation = [get_elevation(coord[0], coord[1]) for coord in activity['map.polyline']]
    elevation_data.append(elevation)
# add elevation data to dataframe
activities['map.elevation'] = elevation_data
print("turkey")
print("turkey_two")
######################
# convert data types
activities.loc[:, 'start_date'] = pd.to_datetime(activities['start_date']).dt.tz_localize(None)
activities.loc[:, 'start_date_local'] = pd.to_datetime(activities['start_date_local']).dt.tz_localize(None)
# convert values
activities.loc[:, 'distance'] /= 1000 # convert from m to km
activities.loc[:, 'average_speed'] *= 3.6 # convert from m/s to km/h
activities.loc[:, 'max_speed'] *= 3.6 # convert from m/s to km/h
# set index
activities.set_index('start_date_local', inplace=True)
# drop columns
activities.drop(
    [
        'map.summary_polyline', 
        'resource_state',
        'external_id', 
        'upload_id', 
        'location_city', 
        'location_state', 
        'has_kudoed', 
        'start_date', 
        'athlete.resource_state', 
        'utc_offset', 
        'map.resource_state', 
        'athlete.id', 
        'visibility', 
        'heartrate_opt_out', 
        'upload_id_str', 
        'from_accepted_tag', 
        'map.id', 
        'manual', 
        'private', 
        'flagged', 
    ], 
    axis=1, 
    inplace=True
)
print("turkey")
print("turkey_two")
######################
# select one activity
from IPython.display import display
my_ride = activities.iloc[0, :] # first activity (most recent)
# plot ride on map
centroid_lat_val_list = list()
centroid_long_val_list = list()
counter = 0
for idx in my_ride['map.polyline']:
    centroid_lat_val = my_ride['map.polyline'][counter][0]
    centroid_long_val = my_ride['map.polyline'][counter][1]
    counter += 1
    centroid_lat_val_list.append(centroid_lat_val)
    centroid_long_val_list.append(centroid_long_val)

#centroid = [
    #np.mean([my_ride['map.polyline'][0][0] for coord in my_ride['map.polyline'][0]]),
    #np.mean([coord[0] for coord in my_ride['map.polyline'][0]]), 
    #np.mean([coord[0] for coord in my_ride['map.polyline']]), 
    #np.mean([coord[1] for coord in my_ride['map.polyline'][0]])
#]
centroid = [np.mean(centroid_lat_val_list), np.mean(centroid_long_val_list)]

m = folium.Map(location=centroid, zoom_start=10)
folium.PolyLine(my_ride['map.polyline'], color='red').add_to(m)
display(m)

print("turkey")
print("turkey_two")