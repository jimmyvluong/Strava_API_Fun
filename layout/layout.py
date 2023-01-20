# this is where functions are called and  the layout is defined

# import Dash packages
from dash import dcc
from dash import html
import plotly.express as px
import datetime
import sys
import numpy as np
sys.path.append(".") # Adds higher directory to python modules path.

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

# Create the DataFrames here #
# Build the 1v1 DataFrame
# ones_df= utils.aoe4helpers.build_ratings_list(17)

# Get the time last updated
time_updated_PST = datetime.datetime.now()
print(time_updated_PST)
print("Done.")