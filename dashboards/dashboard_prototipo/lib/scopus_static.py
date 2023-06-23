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
autores_path = os.path.join(DATA_DIR, "autores_sc.csv")
productos_path = os.path.join(DATA_DIR, "productos.csv")

df_autores_sc=pd.read_csv(autores_path)
df_productos=pd.read_csv(productos_path, sep='\t', quoting=3, parse_dates=["fecha_publicacion"])
df_productos=df_productos.replace('""',np.nan)
#############################
# Load hists
#############################
fig_sc1 = px.pie(df_autores_sc, values=df_autores_sc["estado"].value_counts().values, names=df_autores_sc["estado"].value_counts().index,
             color=df_autores_sc["estado"].value_counts().index,
             color_discrete_sequence=px.colors.sequential.Plasma_r,
             title='Investigadores por estado en la universidad del Cauca',
             hole=.3)


df_autores_sc["departamento"]=df_autores_sc["departamento"].replace(np.nan,"No especifica")
autores_dep = pd.Series([x.strip() for item in df_autores_sc.departamento.str.split(',') for x in item if x.strip() != '']).value_counts()
autores_dep1= autores_dep.head(15)
fig_sc2 = px.histogram(autores_dep1, x=autores_dep1.index,y=autores_dep1.values, color=autores_dep1.values, title='Investigadores por departamento')
fig_sc2.update_layout(xaxis_title="Departamento",
                  yaxis_title="Count")


fig_sc3 = px.histogram(df_autores_sc.sort_values(by="h_index", ascending=False).head(15), x="nombre",y="h_index",
                    title='Investigadores por h-index')
fig_sc3.update_layout(xaxis_title="Investigadores",
                  yaxis_title="h-index")

##############################
# Map Layout
##############################
scopus_static = html.Div(
    [
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        # Place the different graph components here.
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig_sc1, id="fig_sc1")),
            ]
        ),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_sc2, id="fig_sc2")),
                ]),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_sc3, id="fig_sc3")),
                ]),
    ],
    className="dash-body",
)