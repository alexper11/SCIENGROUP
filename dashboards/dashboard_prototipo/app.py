#######################################################
# Main APP definition.
#
# Dash Bootstrap Components used for main theme and better
# organization.
#######################################################

from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_labs as dl
import os

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
"""
request_path_prefix = None
workspace_user = os.getenv('JUPYTERHUB_USER')  # Get dash Workspace user name
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'
"""

# Dash instance declaration

app = Dash(__name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.FLATLY],
                meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
app.title = 'Dashboard Analytics'  

#server = app.server

# We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True
