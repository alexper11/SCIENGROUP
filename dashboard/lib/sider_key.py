# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import json
from datetime import datetime as dt


####################################################################################
# Add the dash_Img
####################################################################################

#############################################################################
# State Dropdown
#############################################################################
DATA_DIR = "data"
states_path = os.path.join(DATA_DIR, "states.json")
with open(states_path) as f:
    states = json.loads(f.read())


##############################################################################
# key Picker
##############################################################################
key_picker = dcc.Dropdown(['cvlac', 'bibliometric', 'Scopus'], 'bibliometric', multi=True)


#############################################################################
# Sidebar Layout
#############################################################################
sidebar_key = html.Div(
    [
        
        html.Hr(),  # Add an horizontal line
        ####################################################
        # Place the rest of Layout here
        ####################################################
        html.H5("Filtrar por keywords",className="title_white"),
        key_picker,
        html.Hr(),
        
                
    ],
    className="dash-sidebar",
)
