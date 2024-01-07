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

# filter down to Run and TrailRun activties
activities_copy = activities_copy.query("type == 'Run' | type == 'TrailRun'")

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
# create map here

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
df_marathon = df_miles_per_week.query("Week_Of_Year >= 31")


# Instead, read in the weekly mileage goals from a .csv file
# goal_df = pd.read_csv('..\data\CIM Training Plans 2023 - Weekly Mileage Goals.csv')
# df_marathon = df_miles_per_week.query("Week_Of_Year >= 31")
# # merge Weekly_Mileage_Goal onto the df_marathon
# df_combined = df_marathon.merge(goal_df, how = 'left', left_on='Week_Of_Year', right_on='Week')
# df_combined['Training Week'] = df_combined['Week_Of_Year'] - 30
# df_combined['distance']= round(df_combined['distance'],1)
# df_combined['Mileage Difference'] = round(df_combined['distance'] - df_combined['Total Mileage'], 1)

#############################################################################################
# header_img_link = "https://images.unsplash.com/photo-1586280246643-9e2f01e3c14e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
header_img_link = "https://raw.githubusercontent.com/jimmyvluong/Strava_API_Fun/main/pictures/2_CIM_Start.jpg"

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

# plot weekly mileage
import plotly.express as px

fig0 = px.bar(
    df_marathon, x = "Training Week", y = "distance",
    labels = dict(Week_Of_Year ="Training Week", distance ="Distance (miles) "),
    #hover_data=["start_date_local"],
    title = "CIM Weekly Mileage Log",
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
        ##### HEADER IMAGE #####
        html.Img(src=header_img_link, style={
            "width": "587px", 
            "height": "391px"}),

        html.H1("Learning how to run far with the help of Strava's API."),
        # Add the time last updated.
        html.H3("Last updated: " + time_updated_UTC.strftime("%B %d %Y at %H:%M UTC")),

        html.Span(
            children=[
                html.Br(),
                html.H4("How it works: A Python script sources my Strava data using the Strava API."),
                html.H4("Render.com handles CI and deployment for free."),         
                html.H4("Front end built using dash and plotly."),        
                html.H4("Github repo: https://github.com/jimmyvluong/Strava_API_Fun"),
                html.Br(),
                html.P("In Fall of 2022 my friend Jason invited me to run a 10k at the Clarksburg Country Run. \
                       I didn’t have any background in running, but I had been playing pickup basketball here and there.  \
                       I signed up on a whim and ended up loving the challenge of pushing myself to run farther than I had ever run before. \
                       6.2 miles seemed really far at the time. Little did I know I’d be running 20 more miles on top of that in a year.")
            ]
        
        ),
        ##### SHAMROCK IMAGE #####
        html.Img(src="https://raw.githubusercontent.com/jimmyvluong/Strava_API_Fun/main/pictures/9_shamrock_2023.jpg", 
            style={
            "width": "750px", 
            "height": "500px"}),
        html.P("Fast forward to Spring 2023 and I signed up for a training group for the Shamrock Half Marathon. \
               I had caught the running bug."),
        html.P("The next logical step for any runner is to sign up for a race that’s twice the distance of your past race, right? \
               I knew training with others is how I run best, so once again I joined a Fleet Feet training group - this time for the California International Marathon (CIM)."),
        html.P("At the same time I was itching to learn more about the Strava API and how to get access to my training data. \
               I was curious to see how my training was measuring up to the prescribed Fleet Feet training program."),
        
        html.Div(
        ##### WEEKLY MILES CHART #####
            dcc.Graph(
                figure = fig0,
                style={
                    "width": "1000px", 
                    "height": "700px", 
                    "margin": "auto"},
            )
        ),
        html.P("What you see above is the total mileage of every single training session in the 23 weeks leading up to CIM. \
               Can you tell which weeks I was injured? Which week had the 20-mile test race? When did I start tapering?"),
        html.P("I calculated the mileage we were 'supposed' to reach each week according to the training plan, \
               and it ranged from a MINIMUM of 22.5 miles per week and a maximum of 42.75 miles per week. \
               My training mileage peaked at 31.4 miles per week, with a low of 4 miles per week when I was injured.\
               This simple analysis confirmed that I was undertrained for the marathon (my quads confirmed it too during the race!) \
               "),
        ##### CELEBRATION IMAGE #####
        html.Img(src="https://raw.githubusercontent.com/jimmyvluong/Strava_API_Fun/main/pictures/8_the_support_crew.png", 
            style={
            "width": "826px", 
            "height": "458px"}),
        ##### CIM RUNS MAP #####
        html.H4("Map of all CIM training runs, using the folium package."),
        html.P("The training runs took me as far as the north part of Lake Natomas!"),       
        html.P("Many weekend mornings were spent trotting along the American River Trail."),    
        html.Iframe(src="https://jimmyvluong.github.io/Strava_API_Fun/cim_map.html",
                style={
                    "height": "1067px", 
                    "width": "1000px",
                    "margin": "auto",
                    "text-align": "center"}),
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
        "text-align": "left",
        "font-size": 24,
        # Update the background color to the entire app
        "background-color": "black",
        # Change the text color for the whole app
        "color": "white",
        "font-family" : "Helvetica"
    }
)

