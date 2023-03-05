# this is where functions are called and  the layout is defined

# import Dash packages
from dash import dcc
from dash import html
import plotly.express as px
import datetime
#import sys
import numpy as np
#sys.path.append(".") # Adds higher directory to python modules path.

# import secrets and tokens from config.py'
from scripts.config import client_id, client_secret, refresh_token

# See Github secrets: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/GitHub-Actions-Secrets-Example-Token-Tutorial#:~:text=Go%20to%20the%20Settings%20tab,text%20secret.%20to%20the%20identifier

payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token,
    'grant_type': "refresh_token",
    'f': 'json'
}

import requests
import urllib3

# import packages for data manipulation
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np

# LOGO_LINK = "https://images.unsplash.com/photo-1501949997128-2fdb9f6428f1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"

# Get the time last updated
time_updated_PST = datetime.datetime.now()
print(time_updated_PST)
print("Done.")

# Create the DataFrames here #
# Build the 1v1 DataFrame
# ones_df= utils.aoe4helpers.build_ratings_list(17)



strava_layout = html.Div(
    [

        # Set the new white-text image.
        # html.Img(src=LOGO_LINK, style={"width": "587px", "height": "391px"}),
        html.H1("Strava API Project"),
        # Add the time last updated.
        html.H3("Last updated: " + time_updated_PST.strftime("%B %d %Y at %H:%M PST")),
        # Show the total player count.
        # html.H4("Total player count: " + f"{(len(ones_df['Rating'])):,}"),
        # # html.H4("Total player count: " + str(len(ones_df['Rating']))),
        # html.Div(
        #     dcc.Graph(
        #         figure=fig1,
        #         style={"width": "1000px", "height": "700px", "margin": "auto"},
        #     )
        # ),
        # html.Div(
        #     dcc.Graph(
        #         figure=fig3,
        #         style={"width": "1000px", "height": "700px", "margin": "auto"},
        #     )
        # ),
        html.Br(),
        html.Span(
            children=[
                html.H4("This website is in active development."),
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

