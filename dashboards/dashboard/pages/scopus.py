
from dash.dependencies import Input, Output, State
from dash import  html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from index import app
import numpy as np
import plotly.graph_objects as go


# LOAD THE DIFFERENT FILES
from lib.filter_scopus import sidebar_scopus

layout = html.Div([
        html.Div(
            children=dcc.Loading(
            id="loading_scopus",
            children=[],
            type="cube",
            fullscreen=False,
            style={'height':'100%', 'marginTop':'15rem','textAlign':'center', 'display':'flex', 'justifyContent':'space-around',"color":"black"}
            ),id="div_scopus",                          
        ),
        dbc.Offcanvas(
            sidebar_scopus,
            id="offcanvas_scopus",
            keyboard = True,
            close_button = False,
            scrollable=True,
            is_open=True,            
        ),
        html.Img(src="/assets/img/filter_scopus.png",id="boton_filter_flex_scopus"),
        # dbc.Popover(
        #     "Botón para ocultar y mostrar los filtros",
        #     target="boton_filter_flex_scopus",
        #     body=True,
        #     trigger="hover",
        #     style={'color':'black'}
        # ),
    ],className="dash-body-scopus", style={"color": "black"},
) 

#-----------------------------------Callbacks ---------------------------------
@callback(
    Output("offcanvas_scopus", "is_open"),
    Input("boton_filter_flex_scopus", "n_clicks"),
    [State("offcanvas_scopus", "is_open")],
)
def toggle_offcanvas_scopus(n1, is_open):
    if n1:
        return not is_open
    return is_open