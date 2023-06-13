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


option_group = dcc.Dropdown(
        id='filter_group',
        options = ['filtro 1','filtro 2'],
        value = None  # Valor inicial seleccionado
    )
option_element = dcc.Dropdown(
        id='filter_element',
        options = ['filtro 1','filtro 2'],
        value = None  # Valor inicial seleccionado
    )
option_parameter = dcc.Dropdown(
        id='filter_parameter',
        options = ['filtro 1','filtro 2'],
        value = None  # Valor inicial seleccionado
    )
option_value = dcc.Dropdown(
        id='filter_value',
        options = ['filtro 1','filtro 2'],
        value = None  # Valor inicial seleccionado
    )
option_input = dcc.Dropdown(
        id='filter_inputs',
        options = ['filtro 1','filtro 2'],
        value = None  # Valor inicial seleccionado
    )
#############################################################################
# Sidebar Layout
#############################################################################
sidebar_graph = html.Div([
    html.H1('Opciones de filtrado',className="title_white",style={"color":"white"}),
    dcc.Tabs(id="tabs_filter_scienti", value='tab_individual', 
    children=[dcc.Tab(label='Individual', value='tab_individual'),
        dcc.Tab(label='Grupal', value='tab_grupal'),
    ]),    
    html.Div([    
        html.P("Filtros Grupo individual.",style={"color":"white"} ),   
        html.Hr(),  # Add an horizontal line
        ####################################################
        # Place the rest of Layout here
        ####################################################
        html.H5("Grupo:",className="title_white",style={"color":"white"}),
        option_group,
        html.H5("Elemento:",className="title_white",style={"color":"white"}),
        option_element,
    ],id="filtro_individual",style={}),
    html.Div([ 
        html.P("Filtros Grupos General.",style={"color":"white"} ),   
        html.Hr(),  # Add an horizontal line
        ####################################################
        # Place the rest of Layout here
        ####################################################
        html.H5("Parametro:",className="title_white",style={"color":"white"}),
        option_parameter,
        html.H5("Valor:",className="title_white",style={"color":"white"}),
        option_value,
        html.H5("Entrada:",className="title_white",style={"color":"white"}),
        option_input,
    ],id="filtro_grupal",style={}),
        html.Button('Filtrar', id='button_state', n_clicks=0),
],className="dash-sidebar",    
)
@callback(
    [Output('filtro_individual', 'style'),Output('filtro_grupal', 'style')],
    Input('tabs_filter_scienti', 'value'))
def render_content(tab):
    if tab == 'tab_individual':
        return {"display": "block"},{"display": "none"}
    else:
        return {"display": "none"},{"display": "block"}
