import dash
# import the layout module
from layout.layout import layout

# Create the Dash app
app = Dash()

# Added line from dash render tutorial
server = app.server

# Server side
app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=False)