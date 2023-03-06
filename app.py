# Import libraries
from dash import Dash, html #, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import sys
# import the layout module
sys.path.append(".") # Adds higher directory to python modules path.
from layout import layout

# Create the Dash app
app = Dash(external_stylesheets=[dbc.themes.DARKLY])

# Added line from dash render tutorial
server = app.server

# Server side
app.layout = layout.strava_layout

# Run local server
if __name__ == "__main__":
    app.run_server(debug=False)