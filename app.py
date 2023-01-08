import dash
# import the layout module
from layout.layout import layout

app = dash.Dash(__name__)

# Server side
app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=False)