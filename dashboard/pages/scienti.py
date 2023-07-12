
from dash.dependencies import Input, Output, State
from dash import  html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from index import app
import numpy as np
import plotly.graph_objects as go


# LOAD THE DIFFERENT FILES
from lib.filter_gruplac import sidebar_gruplac

layout = html.Div([
        html.Div(
            children=dcc.Loading(
            id="loading",
            children=[],
            type="cube",
            fullscreen=False,
            style={'height':'100%', 'marginTop':'15rem','textAlign':'center', 'display':'flex', 'justifyContent':'space-around',"color":"black"}
            ),id="div_gruplac",                          
        ),
        dbc.Offcanvas(
            sidebar_gruplac,
            id="offcanvas",
            keyboard = True,
            close_button = False,
            scrollable=True,
            is_open=True,            
        ),
        html.Img(src="/assets/img/filter.png",id="boton_filter_flex",n_clicks=0),
        # dbc.Popover(
        #     "Botón para ocultar y mostrar los filtros",
        #     target="boton_filter_flex",
        #     body=True,
        #     trigger="hover",
        #     style={'color':'black'}
        # ),
    ],className="dash-body-graph", style={"color": "black"},
) 

#-----------------------------------Callbacks ---------------------------------
@callback(
    Output("offcanvas", "is_open"),
    Input("boton_filter_flex", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

@callback(
    Output('loading', 'children'),
    Input('tabs_filter_scienti', 'value'))
def render_content(tab):
    if tab == 'tab_individual':
        return [html.Div([
                    dbc.Alert(
                        html.P(children='', id="msj_alert_individual",),
                        id="fade-alert-individual",
                        dismissable=True,
                        is_open=False,
                    ),
                    html.H1(children="Indicadores para grupos de investigación: ", id="indicators_group", className="group_graph_info"),
                    html.H1(children="Por favor selecciones elementos a filtrar",id="products_element_group", className="group_graph_info"),
                    html.Div([
                        html.Div([html.H1("Consistencia", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-1',className='badge')], id='kpi_1_all',className='score-card'),
                        html.Div([html.H1("PPA", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-2',className='badge')], id='kpi_2_all', className='score-card'),
                        html.Div([html.H1("PPUA", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-3',className='badge')], id='kpi_3_all', className='score-card'),
                        html.Div([html.H1("Productos Generados", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-4',className='badge')], id='kpi_4_all', className='score-card'),
                        html.Div([html.H1("Autores", style={'fontSize':'1.3rem'}),html.P(children='0', id='kpi-5',className='badge')], id='kpi_5_all', className='score-card'),
                        dbc.Popover("Mide la actividad de un grupo de investigación según su consistencia generando productos nuevos a lo largo de un periodo de tiempo.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_1_all", trigger="hover"),
                        dbc.Popover("(Promedio de productos por año): Indicador absoluto que representa la media de documentos publicados en un periodo de tiempo para un tema específico.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_2_all", trigger="hover"),
                        dbc.Popover("(Porcentaje de productos en los últimos años): Representa el porcentaje de la producción cientifica de un grupo en los últimos 3 años con respecto a la producción general de todos los grupos del departamento.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_3_all", trigger="hover"),
                        dbc.Popover("Muestra el número total de productos publicados en GrupLAC por un grupo de investigación.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_4_all", trigger="hover"),
                        dbc.Popover("Representa el número total de autores registrados en un grupo de investigación.", style={'color':'white','background-color':'#2e2ef9','border-radius':'2rem','padding':'1rem 1rem','max-width':'40rem','text-align':'justify'}, body=True, target="kpi_5_all", trigger="hover"),
                    ],className='card-score-targets'),
                    html.H1(html.Span(dcc.Link("Abrir enlace del grupo en GrupLac", href="", id="url_group_grouplac",target="_blank", className="group_graph_url", style={"color":"#1970eb"}))),
                    html.H1(html.Span(dcc.Link("Abrir indicadores del grupo en Minciencias", id="group_minciencias", href="", target="_blank", className="group_graph_url",style={"color":"#1970eb"}))),

                ],id="kpi_all" ,className='card-score-container', style={'display':'none'}),
                #Charts or Graphs
                html.Div([
                    html.P(children='', id='title_individual_graph1', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_individual_graph1',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_group_figure1', className='card-graph card-body col-graph-big', style={'display':'none'}),             
                html.Div([
                    html.Div([      
                        html.P(children='', id='title_individual_graph2', className='title_graph'),                  
                        dcc.Graph(figure={}, id='dash_individual_graph2',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_group_figure2', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                    html.Div([
                        html.P(children='', id='title_individual_graph3', className='title_graph'),
                        dcc.Graph(figure={}, id='dash_individual_graph3',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_group_figure3', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
                html.Div([
                    html.P(children='', id='title_individual_graph4', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_individual_graph4',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_group_figure4', className='card-graph card-body col-graph-big', style={'display':'none'}),
            ]
    else:
        return [html.Div([
                dbc.Alert(
                    html.P(children='', id="msj_alert_general",),
                    id="fade-alert-general",
                    dismissable=True,
                    is_open=False,
                    style={'textAlign':'center','max-width': '60%','margin-left': 'auto','margin-right': 'auto'}
                ),
                html.Div([
                    html.P(children='', id='title_general_graph1', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_general_graph1',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_figure1', className='card-graph card-body col-graph-big', style={'display':'none'}),
                html.Div([
                    html.P(children='', id='title_general_graph2', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_general_graph2',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_figure2', className='card-graph card-body col-graph-big', style={'display':'none'}),            
                html.Div([
                    html.Div([
                        html.P(children='', id='title_general_graph3', className='title_graph'),                      
                        dcc.Graph(figure={}, id='dash_general_graph3',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure3', className='card-graph_middle col-graph-middle', style={'display':'none'}),
                    html.Div([
                        html.P(children='', id='title_general_graph4', className='title_graph'),
                        dcc.Graph(figure={}, id='dash_general_graph4',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure4', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
                html.Div([
                    html.Div([                        
                        html.P(children='', id='title_general_graph5', className='title_graph'),
                        dcc.Graph(figure={}, id='dash_general_graph5',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure5', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                    html.Div([
                        html.P(children='', id='title_general_graph6', className='title_graph'),
                        dcc.Graph(figure={}, id='dash_general_graph6',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure6', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
                html.Div([
                    html.P(children='', id='title_general_graph7', className='title_graph'),
                    dcc.Graph(figure={}, id='dash_general_graph7',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                ],id='div_general_figure7', className='card-graph card-body col-graph-big', style={'display':'none'}),
                html.Div([
                    html.Div([
                        html.P(children='', id='title_general_graph8', className='title_graph'),        
                        dcc.Graph(figure={}, id='dash_general_graph8',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure8', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                    html.Div([
                        html.P(children='', id='title_general_graph9', className='title_graph'),
                        dcc.Graph(figure={}, id='dash_general_graph9',style={'Width':'100%', "height":'95%'}, config={"displaylogo":False, "displayModeBar":True})
                    ],id='div_general_figure9', className='card-graph_middle card-body col-graph-middle', style={'display':'none'}),
                ],className='col-graph-father'),
            ])]