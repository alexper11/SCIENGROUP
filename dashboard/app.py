import dash
import flask

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True,meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
app.title = "Dashboard Scienti - Scopus"


# ------------------------------------------------------------------------------------------------


