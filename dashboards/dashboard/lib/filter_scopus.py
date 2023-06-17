# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import pandas as pd
import numpy as np
import re

from dash import no_update

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import json
from datetime import datetime as dt
from functions.csv_importer import gruplac_basico, gruplac_integrantes, elementos_gruplac_individual, fuente_dic, referencias, caracteristicas, caracteristicas_invertido, pmin, pmax, productos_ano, opciones_grupo, opciones_parametro_general

# Plotly
import plotly.express as px
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#############################################################################
# State Dropdown
#############################################################################


option_group_scopus = dcc.Dropdown(
        id='filter_group_scopus',
        options = opciones_grupo,
        value = None  # Valor inicial seleccionado
    )
option_element_scopus = dcc.Dropdown(
        id='filter_element_scopus',
        options = [],
        disabled=True,
        value = None  # Valor inicial seleccionado
    )
option_parameter_scopus = dcc.Dropdown(
        id='filter_parameter_scopus',
        options = opciones_parametro_general,
        value = None  # Valor inicial seleccionado
    )
option_value_scopus = dcc.Dropdown(
        id='filter_value_scopus',
        options = [],
        value = [],  # Valor inicial seleccionado
        disabled= True,
        multi=True
    )
option_element_scopus_general = dcc.Dropdown(
        id='filter_element_scopus_general',
        options = [],        
        value = None,  # Valor inicial seleccionado
        disabled=True,
        maxHeight=160
        # style = {"bottom": "100%", "transform": "translateY(-100%)"}
    )
#############################################################################
# Sidebar Layout
#############################################################################
sidebar_scopus = html.Div([
    # html.H1('Opciones de filtrado',className="text_filter_scopus"),
    html.Hr(),  # Add an horizontal line
    dcc.Tabs(id="tabs_filter_scopus", value='tab_individual', 
    children=[dcc.Tab(label='Individual', value='tab_individual'),
        dcc.Tab(label='General', value='tab_general'),
    ]),       
    html.Div([
        html.H5("Grupo:",className="text_filter_scopus"),
        option_group_scopus,
        html.H5("Elemento:",className="text_filter_scopus"),
        option_element_scopus,
        html.Button('Filtrar', id='button_scopus_filter_indiv', n_clicks=0),
    ],id="filtro_individual_scopus"),
    html.Div([
        html.H5("Parametro:",className="text_filter_scopus"),
        option_parameter_scopus,
        html.H5("Valor:",className="text_filter_scopus"),
        option_value_scopus,
        html.H5("Elemento:",className="text_filter_scopus"),
        option_element_scopus_general,
        html.Button('Filtrar', id='button_scopus_filter_group', n_clicks=0),
    ],id="filtro_general_scopus"),        
],id="menu_filter_flex_scopus",className="dash-sidebar-graph",style={'background-color':'#A8AAAC'},    
)

#  ---------------------callback---------------
@callback(
    [Output('filtro_individual_scopus', 'hidden'),Output('filtro_general_scopus', 'hidden')],
    Input('tabs_filter_scopus', 'value'))
def render_content(tab):
    if tab == 'tab_individual':
        return False, True
    else:
        return True, False