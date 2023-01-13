# this is where functions are called and  the layout is defined

# had to change back to importing dcc and html this way to work on pythonanywhere
from dash import dcc
from dash import html
import plotly.express as px
import datetime
import sys
import numpy as np
sys.path.append("..") # Adds higher directory to python modules path.

# LOGO_LINK = "https://images.unsplash.com/photo-1501949997128-2fdb9f6428f1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"

# Create the DataFrames here #
# Build the 1v1 DataFrame
# ones_df= utils.aoe4helpers.build_ratings_list(17)


# Get the time last updated
time_updated_PST = datetime.datetime.now()
print(time_updated_PST)
print("Done.")