import dash
from dash_labs.plugins import register_page
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px

# LOAD THE DIFFERENT FILES
from lib import title, sidebar, us_map, stats, selector, scopus_static

# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

register_page(__name__, path="/scopus")

layout = html.Div(
    [
        scopus_static.scopus_static,
        stats.stats_sc,
        sidebar.sidebar,
    ]
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
autores_path = os.path.join(DATA_DIR, "autores_sc.csv")
productos_path = os.path.join(DATA_DIR, "productos.csv")

df_autores=pd.read_csv(autores_path)
df_productos=pd.read_csv(productos_path, sep='\t', quoting=3, parse_dates=["fecha_publicacion"])
df_productos=df_productos.replace('""',np.nan)


#############################################################
#LINE PLOT : Add sidebar interaction here
#############################################################
@callback(
    [
        Output("Line_Scopus", "figure"),
    ],
    [
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date"),
    ],
)
def make_line_plot_sc(start_date, end_date):
    
    df_productos_f=df_productos[(df_productos['fecha_publicacion']>=start_date) & (df_productos['fecha_publicacion']<=end_date)]
    df_grouped = (
    df_productos_f.groupby(
        # normalize all dates to start of month
        df_productos_f['fecha_publicacion']
            )['fecha_publicacion'].count().rename('Count').to_frame()
        )

    Line_fig_sc = px.line(
            df_grouped, y='Count', title='Publicaciones por fecha',
        )
    Line_fig_sc.update_traces(line_color='#FF7F50', line_width=2)
    return [Line_fig_sc]