# Import libraries
from dash import Dash, html #, dcc, Input, Output
import sys
# import the layout module
sys.path.append(".") # Adds higher directory to python modules path.
from layout import layout

# Create the Dash app
app = Dash()

# Added line from dash render tutorial
server = app.server

# Server side
app.layout = layout.strava_layout

# Run local server
if __name__ == "__main__":
    app.run_server(debug=False)