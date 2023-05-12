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

df = pd.read_csv(superstore_path, parse_dates=["Order Date", "Ship Date"])

##############################################################
# SCATTER PLOT
###############################################################

Scatter_fig = px.scatter(
    df,
    x="Sales",
    y="Profit",
    color="Category",
    hover_data=["State", "Sub-Category", "Order ID", "Product Name"],
)
Scatter_fig.update_layout(
    title="Sales vs. Profit in selected states", paper_bgcolor="#F8F9F9"
)


###############################################################
# LINE PLOT
###############################################################

df["Order_Month"] = pd.to_datetime(df["Order Date"].dt.to_period("M").astype(str))

# Next, we filter the data by month and selected states
states = ["California", "Texas", "New York"]

ddf = df[df["State"].isin(states)]
ddf = ddf.groupby(["State", "Order_Month"]).sum().reset_index()

Line_fig = px.line(ddf, x="Order_Month", y="Sales", color="State")
Line_fig.update_layout(title="Montly Sales in selected states", paper_bgcolor="#F8F9F9")


Treemap_fig = px.treemap(
    df,
    path=["Category", "Sub-Category", "State"],
    values="Sales",
    color_discrete_sequence=px.colors.qualitative.Dark24,
)

#################################################################################
# Here the layout for the plots to use.
#################################################################################
stats = html.Div(
    [
        # Place the different graph components here.
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=Line_fig, id="Line")),
            ]
        ),
        dbc.Row([dbc.Col(dcc.Graph(figure=Scatter_fig, id="Hist"))]),
        #dbc.Row([dbc.Col(dcc.Graph(figure=Treemap_fig, id="Treemap"))]),
    ],
    className="dash-body",
)

stats_sc = html.Div(
    [
        # Place the different graph components here.
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=Line_fig, id="Line_Scopus")),
            ]
        ),
    ],
    className="dash-body",
)