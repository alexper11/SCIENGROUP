import pathlib
import os

import dash
from dash_labs.plugins import register_page
# LOAD THE DIFFERENT FILES
from lib import sider_key

register_page(__name__, path="/keyword")

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

df_articulos["palabras"]=df_articulos["palabras"].str.upper()
df_articulos["palabras"]=df_articulos["palabras"].replace(np.nan,'')

#palabras=pd.Series([x.strip() for item in df_articulos.palabras.str.split(',') for x in item if x.strip() != '']).value_counts()
#palabras=list(palabras.index)

table_keywords= dash_table.DataTable(
                    id='table_id',
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
    Output('table_id', 'data'),
    [Input('key_dropdown', 'value')]
)
def make_keytable(keywords):
    
    index_list=[]
    reporte=[{}]
    
    if keywords is None:
        return reporte
    else:
        for index, row in enumerate(df_articulos['palabras']):
            row_stripped = list(map(str.strip, row.split(',')))
            check=all(x in row_stripped for x in keywords)
            if check:
                index_list.append(index)

        reporte=df_articulos.iloc[index_list].to_dict("records")
    
        return reporte


layout =html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div([
                dbc.Col(
                    table_keywords
                    )
                ],className="dash-body"),
        sider_key.sidebar_key,
        ])
