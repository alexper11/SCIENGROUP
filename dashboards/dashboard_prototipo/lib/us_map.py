import dash
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px


from datetime import datetime as dt
import json
import numpy as np
import pandas as pd
import os


DATA_DIR = "data"
superstore_path = os.path.join(DATA_DIR, "superstore.csv")
us_path = os.path.join(DATA_DIR, "us.json")
states_path = os.path.join(DATA_DIR, "states.json")


basico_path = os.path.join(DATA_DIR, "basico.csv")
df_basico=pd.read_csv(basico_path, sep='|')

#############################
# Load map data
#############################
df_basico["categoria"]=df_basico["categoria"].replace({"Investigador Junior (IJ) con vigencia hasta la publicación de los resultados de la siguiente convocatoria": "Investigador Junior", 
                                "Investigador Asociado (I) con vigencia hasta la publicación de los resultados de la siguiente convocatoria":"Investigador Asociado",
                                "Investigador Senior (IS) con vigencia hasta la publicación de los resultados de la siguiente convocatoria":"Investigador Senior",
                                "Investigador Emérito (IE) con vigencia vitalicia":"Investigador Emérito"})

df_basico['sexo']=df_basico['sexo'].fillna('No especifica')

fig1 = px.pie(df_basico, values=df_basico["categoria"].value_counts().values, names=df_basico["categoria"].value_counts().index,
             color=df_basico["categoria"].value_counts().index,
             color_discrete_sequence=px.colors.sequential.ice,
             hole=.3)
fig1.update_layout(title="Categorias", paper_bgcolor="#F8F9F9")

fig2 = px.pie(df_basico, values=df_basico["sexo"].value_counts().values, names=df_basico["sexo"].value_counts().index,
             color=df_basico["sexo"].value_counts().index,
             color_discrete_sequence=px.colors.sequential.RdBu,
             hole=.3)
fig2.update_layout(title="Genero", paper_bgcolor="#F8F9F9")

fig3 = px.histogram(df_basico, x="nacionalidad", color='nacionalidad', title='Nacionalidad de investigadores en la universidad del Cauca')
fig3.update_layout(title="Nacionalidad", paper_bgcolor="#F8F9F9")
"""
df = pd.read_csv(superstore_path, parse_dates=["Order Date", "Ship Date"])

with open(us_path) as geo:
    geojson = json.loads(geo.read())

with open(states_path) as f:
    states_dict = json.loads(f.read())

df["State_abbr"] = df["State"].map(states_dict)


# Create the map:
dff = df.groupby("State_abbr").sum().reset_index()
Map_Fig = px.choropleth_mapbox(
    dff,
    locations="State_abbr",
    color="Sales",
    geojson=geojson,
    zoom=3,
    mapbox_style="carto-positron",
    center={"lat": 37.0902, "lon": -95.7129},
    color_continuous_scale="Viridis",
    opacity=0.5,
)
Map_Fig.update_layout(title="US map", paper_bgcolor="#F8F9F9")
"""

##############################
# Map Layout
##############################
map = html.Div(
    [
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        # Place the different graph components here.
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig1, id="fig1")),
                dbc.Col(dcc.Graph(figure=fig2, id="fig2"))
            ]
        ),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig3, id="fig3"))]),
    ],
    className="dash-body",
)
