# Import libraries
from dash import Dash, html #, dcc, Input, Output
# import the layout module
#from layout.layout import layout

# Create the Dash app
app = Dash()

# Added line from dash render tutorial
server = app.server

# Server side
# app.layout = layout
app.layout = html.Div(children=[
    html.H1(children='Sample Dashboard')
])

# Run local server
if __name__ == "__main__":
    app.run_server(debug=False)