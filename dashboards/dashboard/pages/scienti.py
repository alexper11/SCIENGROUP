
from dash.dependencies import Input, Output, State
from dash import  html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from index import app
import numpy as np
import plotly.graph_objects as go


# LOAD THE DIFFERENT FILES
from lib.filter_graph import sidebar_graph

layout = html.Div([
        html.Div(
            children=[
            ],id="div_gruplac",
        ),        
        sidebar_graph,
    ],className="dash-body-graph", style={"color": "black"},
) 

#-----------------------------------Callbacks ---------------------------------

@callback(
    Output('div_gruplac', 'children'),
    Input('tabs_filter_scienti', 'value'))
def render_content(tab):
    if tab == 'tab_individual':
        return dcc.Loading(
            id="loading2",
            # children=[html.H2("Información filtrado individual (eliminar msj)", className="title_graph_main"),                
                children=[html.Div([                    
                    html.H1(children="Indicadores para grupos de investigación: ", id="indicators_group", className="group_graph_info"),
                    html.H1(children="Por favor selecciones elementos a filtrar",id="products_element_group", className="group_graph_info"),
                    html.Div([
                        html.Div([html.H1("Consistencia", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-1',className='badge')], className='score-card'),
                        html.Div([html.H1("PPA", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-2',className='badge')], className='score-card'),
                        html.Div([html.H1("PPUA", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-3',className='badge')], className='score-card'),
                        html.Div([html.H1("PG", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-4',className='badge')], className='score-card'),
                        html.Div([html.H1("Autores", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-5',className='badge')], className='score-card'),
                    ],className='card-score-targets'),
                    html.H1(html.Span(dcc.Link("Abrir enlace del grupo en GrupLac", href="", id="url_group_grouplac",target="_blank", className="group_graph_url", style={"color":"#08469b"}))),
                    html.H1(html.Span(dcc.Link("Abrir indicadores del grupo en Minciencias", id="group_minciencias", href="", target="_blank", className="group_graph_url",style={"color":"#08469b"}))),

                ],id="kpi_all" ,className='card-score-container', style={'display':'none'}),
                #Charts or Graphs
                html.Div([
                    dcc.Graph(figure={}, id='dash_individual_graph1',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_group_figure1', className='card-graph card-body col-graph-big', style={'display':'none'}),             
                html.Div([
                    html.Div([                        
                        dcc.Graph(figure={}, id='dash_individual_graph2',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_group_figure2', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                    html.Div([
                        dcc.Graph(figure={}, id='dash_individual_graph3',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_group_figure3', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
                html.Div([
                    dcc.Graph(figure={}, id='dash_individual_graph4',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_group_figure4', className='card-graph card-body col-graph-big', style={'display':'none'}),
            ], type="cube", fullscreen=False, style={'height':'100%', 'marginTop':'15rem','textAlign':'center', 'display':'flex', 'justifyContent':'space-around',"color":"black"}
        )
    else:
        return dcc.Loading(
            id="loading1",
            #children=[html.H2("Indicadores General", className="title_graph_main"),
            children=[html.Div([
                html.Div([
                    dcc.Graph(figure={}, id='dash_general_graph1',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_figure1', className='card-graph card-body col-graph-big', style={'display':'none'}),
                html.Div([
                    dcc.Graph(figure={}, id='dash_general_graph2',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_figure2', className='card-graph card-body col-graph-big', style={'display':'none'}),            
                html.Div([
                    html.Div([                        
                        dcc.Graph(figure={}, id='dash_general_graph3',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure3', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                    html.Div([
                        dcc.Graph(figure={}, id='dash_general_graph4',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure4', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
                html.Div([
                    html.Div([                        
                        dcc.Graph(figure={}, id='dash_general_graph5',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure5', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                    html.Div([
                        dcc.Graph(figure={}, id='dash_general_graph6',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure6', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
                html.Div([
                    dcc.Graph(figure={}, id='dash_general_graph7',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_figure7', className='card-graph card-body col-graph-big', style={'display':'none'}),
                html.Div([
                    html.Div([                        
                        dcc.Graph(figure={}, id='dash_general_graph8',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure8', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                    html.Div([
                        dcc.Graph(figure={}, id='dash_general_graph9',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure9', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
            ])],type="cube", fullscreen=False, style={'height':'100%', 'marginTop':'15rem','textAlign':'center', 'display':'flex', 'justifyContent':'space-around',"color":"black"},
        )