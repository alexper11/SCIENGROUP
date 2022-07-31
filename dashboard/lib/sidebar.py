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
# Date Picker
##############################################################################
date_picker = dcc.DatePickerRange(
    id="date_picker",
    min_date_allowed=dt(1963, 1, 1),
    max_date_allowed=dt(2022, 12, 31),
    start_date=dt(2000, 1, 1).date(),
    end_date=dt(2021, 12, 31).date(),
)


#############################################################################
# Sidebar Layout
#############################################################################
sidebar = html.Div(
    [
        
        html.Hr(),  # Add an horizontal line
        ####################################################
        # Place the rest of Layout here
        ####################################################
        html.H5("Select dates",className="title_white"),
        date_picker,
        html.Hr(),
        
        #html.H5("Select states"),
        #dropdown,
        #html.Hr(),
        
    ],
    className="dash-sidebar",
)
