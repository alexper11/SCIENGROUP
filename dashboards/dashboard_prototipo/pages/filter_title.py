import dash

import pathlib
import os

from dash_labs.plugins import register_page

register_page(__name__, path="/filter_title")
# LOAD THE DIFFERENT FILES
from lib import sider_title

from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px

import plotly.graph_objects as go

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json


DATA_DIR = "data"

articulos_path = os.path.join(DATA_DIR, "articulos.csv")

df_articulos=pd.read_csv(articulos_path, sep='|', quoting=3)

df_articulos["nombre"]=df_articulos["nombre"].replace(np.nan,'')


table_title= dash_table.DataTable(
                    id='table_title',
                    columns = [{"name": i, "id": i} for i in df_articulos.columns],
                    data = df_articulos.head(10).to_dict("rows"),
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                    style_cell = {
                        'font_size': '80%',
                        'text_align': 'center'
                    }
                    )

@callback(
    Output('table_title', 'data'),
    [Input('input_title', 'value')]
)
def make_titletable(string):
    
    index_list=[]
    reporte=[{}]
    
    if (string is None) | (string == ''):
        return reporte
    else:
        
        reporte= df_articulos[df_articulos['nombre'].str.contains(pat=string,case=False)].to_dict("records")
        return reporte


layout =html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div([
                dbc.Col(
                    table_title
                    )
                ],className="dash-body"),
        sider_title.sidebar_title,
    ]
)

