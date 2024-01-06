# this is where functions are called and  the layout is defined

# import Dash packages
from dash import dcc
from dash import html
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
# import sys
# import packages for data manipulation
import pandas as pd
#from pandas.io.json import json_normalize
import numpy as np

import os

# import packages for requesting data from the API
import requests
import urllib3

# import mapping packages

import os
import folium
import polyline
import base64
# tqdm is only needed for getting elevation data
# from tqdm import tqdm

# See Github secrets: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/GitHub-Actions-Secrets-Example-Token-Tutorial#:~:text=Go%20to%20the%20Settings%20tab,text%20secret.%20to%20the%20identifier

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#############################################################################################

# create a dictionary of Strava profile access information

## Use this version to run locally

# import secrets and tokens from config.py
#from scripts.config import client_id, client_secret, refresh_token

# payload = {
#     'client_id': client_id,
#     'client_secret': client_secret,
#     'refresh_token': refresh_token,
#     'grant_type': "refresh_token",
#     'f': 'json'
# }

## Use this version to run using Render
payload = {
    'client_id': os.getenv('client_id'),
    'client_secret': os.getenv('client_secret'),
    'refresh_token': os.getenv('refresh_token'),
    'grant_type': "refresh_token",
    'f': 'json'
}
#############################################################################################

# get the data in json format
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
# print("Access Token = {}\n".format(access_token))
print("Success, token acquired!")
header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

#############################################################################################
# create the DataFrames here

activities = pd.json_normalize(my_dataset)
# break date into start time and date
activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
activities['start_time'] = activities['start_date_local'].dt.time
activities['start_date_local'] = activities['start_date_local'].dt.date

# make a copy of activities DataFrame for feature engineering
activities_copy = activities.copy()

# filter down to Ride, Run, and Swim activities
activities_copy = activities_copy.query("type == 'Ride' | type == 'Run' | type == 'Swim'")

# convert data types
activities_copy.loc[:, 'start_date'] = pd.to_datetime(activities_copy['start_date']).dt.tz_localize(None)
activities_copy.loc[:, 'start_date_local'] = pd.to_datetime(activities_copy['start_date_local']).dt.tz_localize(None)
# convert values
activities_copy.loc[:, 'distance'] /= 1609.344 # convert from meters to miles
activities_copy.loc[:, 'average_speed'] *= 2.23693629 # convert from meters/second to miles/hour
activities_copy.loc[:, 'max_speed'] *= 2.23693629 # convert from meters/second to miles/hour
# set index
# activities_copy.set_index('start_date_local', inplace=True)

#############################################################################################
# separate out by sport or group here
# nfs team activities

activities_nfs = activities_copy.query('name.str.contains("NFS")', engine ='python')
# https://stackoverflow.com/questions/25146121/extracting-just-month-and-year-separately-from-pandas-datetime-column
# create a column that extracts month and year from the activity
activities_nfs['Month_Year'] = pd.to_datetime(activities_nfs['start_date']).dt.strftime('%Y-%m')
############

activities_nfs_copy = activities.copy(deep = True)
# the line below is likely causing the "A value is trying to be set on a copy of a slice from a DataFrame." warning.
activities_nfs_map = activities_nfs_copy.query('name.str.contains("NFS")', engine = 'python')
activities_nfs_map.reset_index(drop = True, inplace = True)

# add decoded summary polylines
# activities['map.summary_polyline'] contains an encoded polyline
# .apply(polyline.decode) decodes that polyline into latitude and longitude
activities_nfs_map['map.polyline'] = activities_nfs_map['map.summary_polyline'].apply(polyline.decode)

# location is currently assigned to start at the first coordinate of the first ride.
# an improvement would be to set the location to the centroid of all rides
# m = folium.Map(location = activities_nfs_map['map.polyline'][0][0], zoom_start= 12.25)
# counter = 0

# while counter < len(activities_nfs_map):
    
#     ride = activities_nfs_map.iloc[counter, :]
#     folium.PolyLine(ride['map.polyline'], color = 'red').add_to(m)
#     counter+=1

# m.save('nfs_map.html')
#############################################################################################

# https://stackoverflow.com/questions/25146121/extracting-just-month-and-year-separately-from-pandas-datetime-column
# create a column that extracts month and year from the activity
# df['yyyy-mm'] = pd.to_datetime(df['ArrivalDate']).dt.strftime('%Y-%m')
activities_copy['Month_Year'] = pd.to_datetime(activities_copy['start_date_local']).dt.strftime('%Y-%m')
# https://stackoverflow.com/questions/2600775/how-to-get-week-number-in-python
# make a Week_Of_Year column
activities_copy['Week_Of_Year'] = pd.to_datetime(activities_copy['start_date_local']).dt.strftime('%U')
# get weekly mileage and total weekly moving time
df_miles_per_week = pd.DataFrame(activities_copy.groupby(['Week_Of_Year'])['distance', 'moving_time'].sum().reset_index())
# make a average mph column
df_miles_per_week['Average Moving Speed (mph)'] = df_miles_per_week['distance']/(df_miles_per_week['moving_time']/(60*60))
df_miles_per_week.rename(columns={"distance": "Weekly Mileage", "moving_time": "Total Moving Time (seconds)"})
# convert the Week_Of_Year column to numeric type so we can filter on it
df_miles_per_week["Week_Of_Year"] = pd.to_numeric(df_miles_per_week["Week_Of_Year"])
df_miles_per_week['Training Week'] = df_miles_per_week['Week_Of_Year'] - 30
df_miles_per_week['distance']= round(df_miles_per_week['distance'],1)



# Instead, read in the weekly mileage goals from a .csv file
# goal_df = pd.read_csv('..\data\CIM Training Plans 2023 - Weekly Mileage Goals.csv')
# df_marathon = df_miles_per_week.query("Week_Of_Year >= 31")
# # merge Weekly_Mileage_Goal onto the df_marathon
# df_combined = df_marathon.merge(goal_df, how = 'left', left_on='Week_Of_Year', right_on='Week')
# df_combined['Training Week'] = df_combined['Week_Of_Year'] - 30
# df_combined['distance']= round(df_combined['distance'],1)
# df_combined['Mileage Difference'] = round(df_combined['distance'] - df_combined['Total Mileage'], 1)

#############################################################################################
# run
activities_run = activities_copy.query("type == 'Run'")
# swim
activities_swim = activities_copy.query("type == 'Swim'")
# bike
activities_bike = activities_copy.query("type == 'Ride'")
#############################################################################################
# header_img_link = "https://images.unsplash.com/photo-1524646349956-1590eacfa324?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80"
# new temp img
# header_img_link = "https://dgalywyr863hv.cloudfront.net/pictures/clubs/338556/8042232/8/large.jpg"
header_img_link = "https://images.unsplash.com/photo-1586280246643-9e2f01e3c14e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"

# get the time last updated in UTC (only for Render)
time_updated_UTC = datetime.datetime.now()
print(time_updated_UTC)

#############################################################################################
# build graphs here
# fig0 = px.bar(
#     activities_nfs, x = "Month_Year", y = "distance",
#     labels = dict(Month_Year ="Month and Year ", distance ="Distance (miles) "),
#     hover_data=["start_date_local"],
#     title = "NFS Team Rides",
#     width = 1000
# )
# # Hover over should be the day, not the first of the month
# fig0.add_hline(y = 20*8)
# fig0.update_traces(marker_line_width = 2.5)
# fig0.update_yaxes(range = [0, 300])
# fig0.update_layout(bargap = 0.8)

# fig1 = px.box(
#     activities_copy, x = "distance", 
#     title="1. Boxplot: Distance by Activity Type", 
#     color="sport_type", 
#     points="all"
# )

# plot weekly mileage
import plotly.express as px

fig0 = px.bar(
    df_miles_per_week, x = "Training Week", y = "distance",
    labels = dict(Week_Of_Year ="Training Week", distance ="Distance (miles) "),
    #hover_data=["start_date_local"],
    title = "CIM Weekly Mileage Log - Can you see which weeks I was injured?",
    width = 1000
)
# Hover over should be the day, not the first of the month
# fig0.add_hline(y = 20*8)
fig0.update_traces(marker_line_width = 2.5)
fig0.update_yaxes(range = [0, 50])
#fig0.update_layout(bargap = 0.8)
fig0.show() 

#############################################################################################

strava_layout = html.Div(

    [

        # Set the new white-text image.
        html.Img(src=header_img_link, style={"width": "587px", "height": "391px"}),

        html.H1("Using Strava's API to track CIM training!"),
        # Add the time last updated.
        html.H3("Last updated: " + time_updated_UTC.strftime("%B %d %Y at %H:%M UTC")),
        # Show the total player count.
        # html.H4("Total player count: " + f"{(len(ones_df['Rating'])):,}"),
        # # html.H4("Total player count: " + str(len(ones_df['Rating']))),
        # html.Div(
        #     dcc.Graph(
        #         figure=fig1,
        #         style={"width": "1000px", "height": "700px", "margin": "auto"},
        #     )
        # ),
        html.Span(
            children=[
                # html.H4("Bike rides with friends :)"),
                html.Br(),
                html.H4("A Python script sources data using the Strava API, and Render.com handles CI and deployment for free."),         
                html.H4("Front end built using dash and plotly."),        
                html.H4("More features are in the works..."),
                html.Br(),
                html.H4("Github repo: https://github.com/jimmyvluong/Strava_API_Fun")
            ]
        ),        
        html.Div(
            dcc.Graph(
                figure = fig0,
                style={"width": "1000px", "height": "700px", "margin": "auto"},
            )
        ),
        # html.Iframe(src="https://www.ons.gov.uk/visualisations/dvc914/map/index.html",
        #         style={"height": "1067px", "width": "100%"}),
        html.H4("Map of all CIM training runs, using the folium package."),
        html.Iframe(src="https://jimmyvluong.github.io/Strava_API_Fun/cim_map.html",
                style={"height": "1067px", "width": "1000px"}),
        # html.Div(
        #     dcc.Graph(
        #         figure=fig2,
        #         style={"width": "1000px", "height": "700px", "margin": "auto"},
        #     )
        # ),               
        html.Br(),
        html.Span(
            children=[
                html.Br(),
                html.I("This website was created under Strava's API Agreement and \
                     it is not endorsed by or affiliated with Strava."),
                html.Br(),
                html.I("Data sourced from https://developers.strava.com/")
            ]
        ),
    ],
    style={
        "text-align": "center",
        "font-size": 24,
        # Update the background color to the entire app
        "background-color": "black",
        # Change the text color for the whole app
        "color": "white",
        "font-family" : "Helvetica"
    }
)

