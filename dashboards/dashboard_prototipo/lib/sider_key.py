# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import json
from datetime import datetime as dt
# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

####################################################################################
# Add the dash_Img
####################################################################################

#############################################################################
# State Dropdown
#############################################################################
DATA_DIR = "data"

articulos_path = os.path.join(DATA_DIR, "articulos.csv")

df_articulos=pd.read_csv(articulos_path, sep='|', quoting=3)

df_articulos["palabras"]=df_articulos["palabras"].str.upper()
df_articulos["palabras"]=df_articulos["palabras"].replace(np.nan,'')

##############################################################################
# key Picker
##############################################################################
palabras=pd.Series([x.strip() for item in df_articulos.palabras.str.split(',') for x in item if x.strip() != '']).value_counts()
key_picker = dcc.Dropdown(id="key_dropdown", options=[{"label": palabra, "value": palabra} for palabra in palabras.index], multi=True)


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
