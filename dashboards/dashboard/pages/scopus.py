
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


@callback(
    Output('loading_scopus', 'children'),
    Input('tabs_filter_scopus', 'value'))
def render_content(tab):
    if tab == 'tab_individual':
        return [html.Div([
                    dbc.Alert(
                        html.P(children='', id="msj_alert_individual_scopus",),
                        id="fade-alert-individual-scopus",
                        dismissable=True,
                        is_open=False,
                        style={'text-align':'center'}
                    ),
                    html.H1(children="Indicadores para grupos de investigación: ", id="indicators_group_scopus", className="group_graph_info"),
                    html.H1(children="Por favor selecciones elementos a filtrar",id="products_element_group_scopus", className="group_graph_info"),
                    html.Div([
                        html.Div([html.H1("H1 index", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_1',className='badge')], className='score-card'),
                        html.Div([html.H1("H2 index", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_2',className='badge')], className='score-card'),
                        html.Div([html.H1("AC", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_3',className='badge')], className='score-card'),
                        html.Div([html.H1("PC", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_4',className='badge')], className='score-card'),
                        html.Div([html.H1("CC", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_5',className='badge')], className='score-card'),
                        html.Div([html.H1("CO", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_6',className='badge')], className='score-card'),
                    ],className='card-score-targets'),                  
                ],id="kpi_all_scopus" ,className='card-score-container', style={'display':'none'}),
                #Charts or Graphs
                html.Div([
                    html.P(children='', id='title_individual_scopus_graph1', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_individual_scopus_graph1',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_group_scopus_figure1', className='card-graph card-body col-graph-big', style={'display':'none'}),             
                html.Div([
                    html.Div([      
                        html.P(children='', id='title_individual_scopus_graph2', className='title_graph'),                  
                        dcc.Graph(figure={}, id='dash_individual_scopus_graph2',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_group_scopus_figure2', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                    html.Div([
                        html.P(children='', id='title_individual_scopus_graph3', className='title_graph'),
                        dcc.Graph(figure={}, id='dash_individual_scopus_graph3',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_group_scopus_figure3', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
                html.Div([
                    html.P(children='', id='title_individual_scopus_graph4', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_individual_scopus_graph4',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_group_scopus_figure4', className='card-graph card-body col-graph-big', style={'display':'none'}),
            ]
    else:
        return [html.Div([
                dbc.Alert(
                    html.P(children='', id="msj_alert_general_scopus",),
                    id="fade-alert-general-scopus",
                    dismissable=True,
                    is_open=False,
                    style={'text-align':'center'}
                ),
                html.Div([
                    html.P(children='', id='title_general_scopus_graph1', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_general_scopus_graph1',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_scopus_figure1', className='card-graph card-body col-graph-big', style={'display':'none'}),
                html.Div([
                    html.P(children='', id='title_general_scopus_graph2', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_general_scopus_graph2',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_scopus_figure2', className='card-graph card-body col-graph-big', style={'display':'none'}),            
                html.Div([
                    html.Div([
                        html.P(children='', id='title_general_scopus_graph3', className='title_graph'),                      
                        dcc.Graph(figure={}, id='dash_general_scopus_graph3',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_scopus_figure3', className='card-graph_middle col-graph-middle', style={'display':'none'}),
                    html.Div([
                        html.P(children='', id='title_general_scopus_graph4', className='title_graph'),
                        dcc.Graph(figure={}, id='dash_general_scopus_graph4',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_scopus_figure4', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
                html.Div([
                    html.Div([                        
                        html.P(children='', id='title_general_scopus_graph5', className='title_graph'),
                        dcc.Graph(figure={}, id='dash_general_scopus_graph5',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_scopus_figure5', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                    html.Div([
                        html.P(children='', id='title_general_scopus_graph6', className='title_graph'),
                        dcc.Graph(figure={}, id='dash_general_scopus_graph6',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_scopus_figure6', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
                html.Div([
                    html.P(children='', id='title_general_scopus_graph7', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_general_scopus_graph7',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_scopus_figure7', className='card-graph card-body col-graph-big', style={'display':'none'}),
                html.Div([
                    html.Div([
                        html.P(children='', id='title_general_scopus_graph8', className='title_graph'),        
                        dcc.Graph(figure={}, id='dash_general_scopus_graph8',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_scopus_figure8', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                    html.Div([
                        html.P(children='', id='title_general_scopus_graph9', className='title_graph'),
                        dcc.Graph(figure={}, id='dash_general_scopus_graph9',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_scopus_figure9', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
            ])]