#Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

###########################################################
#
#           APP LAYOUT:
#
###########################################################


# LOAD THE DIFFERENT FILES
from lib import title, sidebar, us_map, stats, selector


import dash
from dash import html , dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page


register_page(__name__, path="/cvlac")


layout = html.Div(
    [
        #title.title,
        us_map.map,
        stats.stats,
        sidebar.sidebar,
    ],
    className="dash-app",  # You can also add your own css files by storing them in the assets folder
)


###############################################
#
#           APP INTERACTIVITY:
#
###############################################

###############################################################
# Load and modify the data that will be used in the app.
#################################################################
DATA_DIR = "data"
superstore_path = os.path.join(DATA_DIR, "superstore.csv")
us_path = os.path.join(DATA_DIR, "us.json")
states_path = os.path.join(DATA_DIR, "states.json")
basico_path = os.path.join(DATA_DIR, "basico.csv")
articulos_path = os.path.join(DATA_DIR, "articulos.csv")


df = pd.read_csv(superstore_path, parse_dates=["Order Date", "Ship Date"])


df_basico=pd.read_csv(basico_path, sep='|')
df_articulos=pd.read_csv(articulos_path, sep='|', quoting=3)
df_articulos['fecha']=df_articulos['fecha'].str.strip()
for index, row in enumerate(df_articulos['fecha']):
    if len(str(row)) == 4:
        pass
    else:
        df_articulos['fecha'].iloc[index]=np.nan


with open(us_path) as geo:
    geojson = json.loads(geo.read())

with open(states_path) as f:
    states_dict = json.loads(f.read())

df["State_abbr"] = df["State"].map(states_dict)
df["Order_Month"] = pd.to_datetime(df["Order Date"].dt.to_period("M").astype(str))


#############################################################
# SCATTER & LINE PLOT : Add sidebar interaction here
#############################################################
@callback(
    [
        Output("Line", "figure"),
        Output("Hist", "figure"),
        #Output("Treemap", "figure"),
    ],
    [
        #Input("state_dropdown", "value"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date"),
    ],
)
def make_line_plot(start_date, end_date):
    df_articulos_cb=df_articulos[(df_articulos['fecha']>=start_date[:4]) & (df_articulos['fecha']<=end_date[:4])]
    Line_fig = px.line(df_articulos_cb, 
              x=df_articulos_cb['fecha'].value_counts().sort_index(ascending=True).index, 
              y=df_articulos_cb['fecha'].value_counts().sort_index(ascending=True).values, 
              title='Articulos por año en la universidad del Cauca')
    Line_fig.update_layout(xaxis_title="Año",
                  yaxis_title="Articulos publicados")
    
    
    top_autores = pd.Series([x.strip() for item in df_articulos_cb.autores.str.split(',') for x in item]).value_counts()
    top_autores=top_autores.head(8)
    Hist_fig = px.histogram(top_autores, x=top_autores.index,y=top_autores.values, color=top_autores.values, 
                        title='Articulos publicados por autores de la universidad del Cauca')
    Hist_fig.update_layout(xaxis_title="Autores",
                  yaxis_title="Count")
      
    return [Line_fig, Hist_fig]
