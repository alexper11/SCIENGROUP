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


##############################################################################
# key Picker
##############################################################################
# palabras=pd.Series([x.strip() for item in df_articulos.palabras.str.split(',') for x in item if x.strip() != '']).value_counts()
# key_picker = dcc.Dropdown(id="key_dropdown", options=[{"label": palabra, "value": palabra} for palabra in palabras.index], multi=True)

# Define las opciones del Dropdown
opciones = [
    {'label': 'Opción 1', 'value': 'opcion1'},
    {'label': 'Opción 2', 'value': 'opcion2'},
    {'label': 'Opción 3', 'value': 'opcion3'}
]
option = dcc.Dropdown(
        id='mi-dropdown',
        options=opciones,
        value='opcion1'  # Valor inicial seleccionado
    )
#############################################################################
# Sidebar Layout
#############################################################################
sidebar_explorer = html.Div(
    [
        html.P("filtros para explorar los datos." ),   
        html.Hr(),  # Add an horizontal line
        ####################################################
        # Place the rest of Layout here
        ####################################################
        html.H5("Filtrar por keywords",className="title_white"),
        option,
        html.Hr(),   
    ],
    className="dash-sidebar",
)
