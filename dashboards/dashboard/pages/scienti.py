
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
                    html.H1(children="Indicadores del grupo de investigación: ", id="indicators_group", className="group_graph_info"),
                    html.H1(children="Todos los productos: ",id="products_element_group", className="group_graph_info"),
                    html.Div([
                        html.Div([html.H1("Indicador 1", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-1',className='badge')], className='score-card'),
                        html.Div([html.H1("Indicador 2", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-2',className='badge')], className='score-card'),
                        html.Div([html.H1("Indicador 3", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-3',className='badge')], className='score-card'),
                        html.Div([html.H1("Indicador 4", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-4',className='badge')], className='score-card'),
                        html.Div([html.H1("Indicador 5", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-5',className='badge')], className='score-card'),
                    ],className='card-score-targets'),
                    html.H1(html.Span(dcc.Link("Abrir enlace del grupo en GrupLac", href="", id="url_group_grouplac",target="_blank", className="group_graph_url", style={"color":"#08469b"}))),
                    html.H1(html.Span(dcc.Link("Abrir indicadores del grupo en Minciencias", id="group_minciencias", href="", target="_blank", className="group_graph_url",style={"color":"#08469b"}))),

                ],className='card-score-container'),
                #Charts or Graphs
                html.Div([
                    dcc.Graph(figure={}, id='dash_individual_graph1',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})
                ],id='div_group_figure1', className='card-graph card-body col-graph-big'),             
                html.Div([
                    html.Div([                        
                        dcc.Graph(figure={}, id='dash_individual_graph2',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})
                    ],id='div_group_figure2', className='card-graph_middle card-body col-graph-middle'),
                    html.Div([
                        dcc.Graph(figure={}, id='dash_individual_graph3',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})
                    ],id='div_group_figure3', className='card-graph_middle card-body col-graph-middle'),
                ],className='col-graph-father'),
                html.Div([
                    dcc.Graph(figure={}, id='dash_individual_graph4',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})
                ],id='div_group_figure4', className='card-graph card-body col-graph-big'),
            ],type="cube", fullscreen=False, style={'height':'100%', 'marginTop':'15rem','textAlign':'center', 'display':'flex', 'justifyContent':'space-around',"color":"black"}
        )
    else:
        return dcc.Loading(
            id="loading1",
            children=[html.H2("Indicadores General", className="title_graph_main"),
                html.Div([
                html.Div([html.Div([html.H1("Grafica 1"),dcc.Graph(id='violin-plot',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})],className='card-graph card-body')], className='col-graph-big'),
                html.Div([html.Div([html.H1("Grafica 2"),dcc.Graph(id='pie-1',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})],className='card-graph card-body')], className='col-graph-big'),
                html.Div([html.Div([html.H1("Grafica 3 media pantalla"),dcc.Graph(id='histogram',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph_50'),
                html.Div([html.Div([html.H1("Grafica 4 pantalla completa"),dcc.Graph(id='path',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph_100'),
                html.Div([html.Div([html.H1("Grafica 5"),dcc.Graph(id='radial',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph'),
                html.Div([html.Div([html.H1("Grafica 6"),dcc.Graph(id='radial',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph'),  
            ])],type="cube", fullscreen=False, style={'height':'100%', 'marginTop':'15rem','textAlign':'center', 'display':'flex', 'justifyContent':'space-around',"color":"black"},
        )