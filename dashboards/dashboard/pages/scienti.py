
from dash.dependencies import Input, Output, State
from dash import  html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from index import app
import numpy as np
import plotly.graph_objects as go


# LOAD THE DIFFERENT FILES
from lib.filter_graph import sidebar_graph

indicadores= dcc.Loading(
            id="loading2",
            children=[html.Div([
                html.Div([html.H1("Indicador 1", style={'fontSize':'2rem'}),html.P('0', id='badge')], className='score-card'),
                html.Div([html.H1("Indicador 2", style={'fontSize':'2rem'}),html.P('0', id='badge')], className='score-card'),
                html.Div([html.H1("Indicador 3", style={'fontSize':'2rem'}),html.P('0', id='badge')], className='score-card'),
                html.Div([html.H1("Indicador 4", style={'fontSize':'2rem'}),html.P('0', id='badge')], className='score-card'),
                ],className='card-score-container'),
                #Charts or Graphs
                html.Div([
                    html.Div([
                        html.H1("Gráfica 1"),
                        dcc.Graph(id='violin-plot',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})
                    ],className='card-graph card-body')
                ], className='col-graph-big'),
                html.Div([
                    html.Div([
                        html.H1("Gráfica 2 mitad1"),
                        dcc.Graph(id='histogram',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})
                    ], className='card-graph card-body'),
                    html.Div([
                        html.H1("Gráfica 2 mitad2"),
                        dcc.Graph(id='path',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})
                    ], className='card-graph card-body'),
                ], className='col-graph_middle'),
            ],type="cube", fullscreen=False, style={'height':'100%', 'marginTop':'15rem','textAlign':'center', 'display':'flex', 'justifyContent':'space-around',"color":"black"}
        )
# indicadores_grupales= dcc.Loading(
#             id="loading1",
#             children=[html.Div([
#                 html.Div([html.Div([html.H1("Grafica 1"),dcc.Graph(id='violin-plot',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})],className='card-graph card-body')], className='col-graph-big'),
#                 html.Div([html.Div([html.H1("Grafica 2"),dcc.Graph(id='pie-1',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})],className='card-graph card-body')], className='col-graph-big'),
#                 html.Div([html.Div([html.H1("Grafica 3 media pantalla"),dcc.Graph(id='histogram',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph_50'),
#                 html.Div([html.Div([html.H1("Grafica 4 pantalla completa"),dcc.Graph(id='path',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph_100'),
#                 html.Div([html.Div([html.H1("Grafica 5"),dcc.Graph(id='radial',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph'),
#                 html.Div([html.Div([html.H1("Grafica 6"),dcc.Graph(id='radial',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph'),  
#             ])],type="cube", fullscreen=False, style={'height':'100%', 'marginTop':'15rem','textAlign':'center', 'display':'flex', 'justifyContent':'space-around',"color":"black"},
#         )     

layout = html.Div([
        html.Div(
            children=[
            html.H2("Indicadores", className="title_graph_main"),
            indicadores,
            ],id="div_indicadores",
        ),        
        sidebar_graph,
    ],className="dash-body-graph", style={"color": "black"},
) 

#-----------------------------------Callbacks ---------------------------------

@callback(
    Output('div_indicadores', 'children'),
    Input('tabs_filter_scienti', 'value'))
def render_content(tab):
    if tab == 'tab_individual':
        return dcc.Loading(
            id="loading2",
            children=[html.H2("Indicadores Individual", className="title_graph_main"),
                html.Div([
                html.Div([html.H1("Indicador 1", style={'fontSize':'2rem'}),html.P('0', id='badge')], className='score-card'),
                html.Div([html.H1("Indicador 2", style={'fontSize':'2rem'}),html.P('0', id='badge')], className='score-card'),
                html.Div([html.H1("Indicador 3", style={'fontSize':'2rem'}),html.P('0', id='badge')], className='score-card'),
                html.Div([html.H1("Indicador 4", style={'fontSize':'2rem'}),html.P('0', id='badge')], className='score-card'),
                ],className='card-score-container'),
                #Charts or Graphs
                html.Div([
                    html.H1("Gráfica 1"),
                    dcc.Graph(id='violin-plot',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})
                ],className='card-graph card-body col-graph-big'),                
                html.Div([
                    html.Div([
                        html.H1("Gráfica 2 mitad1"),
                        dcc.Graph(id='histogram',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})
                    ], className='child card-graph'),
                    html.Div([
                        html.H1("Gráfica 2 mitad2"),
                        dcc.Graph(id='path',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})
                    ], className='child card-graph'),
                ],className='col-graph-big1'), 
            ],type="cube", fullscreen=False, style={'height':'100%', 'marginTop':'15rem','textAlign':'center', 'display':'flex', 'justifyContent':'space-around',"color":"black"}
        )
    else:
        return dcc.Loading(
            id="loading1",
            children=[html.H2("Indicadores Grupal", className="title_graph_main"),
                html.Div([
                html.Div([html.Div([html.H1("Grafica 1"),dcc.Graph(id='violin-plot',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})],className='card-graph card-body')], className='col-graph-big'),
                html.Div([html.Div([html.H1("Grafica 2"),dcc.Graph(id='pie-1',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})],className='card-graph card-body')], className='col-graph-big'),
                html.Div([html.Div([html.H1("Grafica 3 media pantalla"),dcc.Graph(id='histogram',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph_50'),
                html.Div([html.Div([html.H1("Grafica 4 pantalla completa"),dcc.Graph(id='path',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph_100'),
                html.Div([html.Div([html.H1("Grafica 5"),dcc.Graph(id='radial',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph'),
                html.Div([html.Div([html.H1("Grafica 6"),dcc.Graph(id='radial',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph'),  
            ])],type="cube", fullscreen=False, style={'height':'100%', 'marginTop':'15rem','textAlign':'center', 'display':'flex', 'justifyContent':'space-around',"color":"black"},
        )