# Basics Requirements
import pathlib
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

title = html.Div(
    className="dash-title",
    children=[
        dbc.Row(dbc.Col(html.H1("CVLAC Unicauca"), width={"size": 6, "offset": 3}))
    ],
    id="title",
)
