
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
    html.Img(src="/assets/img/filter_scopus.png",id="boton_filter_flex_scopus", n_clicks=0),
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
                    ),
                    html.H1(children=" ", id="indicators_group_scopus", className="group_graph_info"),
                    html.H1(children=" ",id="products_element_group_scopus", className="group_graph_info"),
                    html.Div([
                        html.Div([html.H1("H1 index", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_1',className='badge')], id='kpi_scopus_1_all', className='score-card'),
                        html.Div([html.H1("H2 index", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_2',className='badge')], id='kpi_scopus_2_all', className='score-card'),
                        html.Div([html.H1("Autores", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_3',className='badge')], id='kpi_scopus_3_all', className='score-card'),
                        html.Div([html.H1("Conteo Productos", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_4',className='badge')], id='kpi_scopus_4_all', className='score-card'),
                        html.Div([html.H1("Conteo Citaciones", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_5',className='badge')], id='kpi_scopus_5_all', className='score-card'),
                        html.Div([html.H1("Citaciones por Producto", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi_scopus_6',className='badge')], id='kpi_scopus_6_all', className='score-card'),
                        dbc.Popover("H index de primer orden, indica que el grupo ha publicado H1 productos con al menos H1 citaciones.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_scopus_1_all", trigger="hover"),
                        dbc.Popover("H index de segundo orden, indica que el grupo tiene al menos H2 investigadores, cada uno con un H index de Scopus de al menos H2.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_scopus_2_all", trigger="hover"),
                        dbc.Popover("Representa el número de autores de un grupo de investigación que fueron emparejados de GrupLAC y Scopus.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_scopus_3_all", trigger="hover"),
                        dbc.Popover("Muestra el número total de productos publicados en Scopus por un grupo de investigación.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_scopus_4_all", trigger="hover"),
                        dbc.Popover("Suma total de citas de los productos del grupo de investigación analizado.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_scopus_5_all", trigger="hover"),
                        dbc.Popover("Promedio de citas que ha recibido una entidad hasta la fecha por cada salida. Una entidad puede ser una institución, un grupo de investigación o un investigador.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_scopus_6_all", trigger="hover"),
                    ],className='card-score-targets'),                  
                ],id="kpi_all_scopus" ,className='card-score-container', style={'display':'none'}),
                #Charts or Graphs
                html.Div([
                    html.P(children='', id='title_individual_scopus_graph1', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_individual_scopus_graph1',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_group_scopus_figure1', className='card-graph card-body col-graph-big', style={'display':'none'}),             
                html.Div([
                    html.P(children='Red de colaboración', id='title_individual_scopus_graph6', className='title_graph'),
                    html.Div(children=html.Img(src='./assets/img/init.png', id='image_network_path'), id='dash_individual_scopus_graph6',className='network_img',style={'Width':'100%', "height":'95%'})
                ],id='div_group_scopus_figure6', className='card-graph card-body col-graph-big', style={'display':'none'}), 
                html.Div([
                    html.P(children='', id='title_individual_scopus_graph5', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_individual_scopus_graph5',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_group_scopus_figure5', className='card-graph card-body col-graph-big', style={'display':'none'}),
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
                    style={'textAlign':'center','max-width': '60%','margin-left': 'auto','margin-right': 'auto'}
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
                    html.P(children='', id='title_general_scopus_graph5', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_general_scopus_graph5',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_scopus_figure5', className='card-graph card-body col-graph-big', style={'display':'none'}),
                html.Div([
                    html.P(children='', id='title_general_scopus_graph6', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_general_scopus_graph6',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_scopus_figure6', className='card-graph card-body col-graph-big', style={'display':'none'}),
            ])]