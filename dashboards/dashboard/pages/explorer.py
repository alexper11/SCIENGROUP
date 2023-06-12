from dash.dependencies import Input, Output
from datetime import date
from dash import dcc
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, callback, dash_table, State
import pandas as pd
from functions.csv_importer import referencias
import json
from dash import no_update
from dash import ctx


# LOAD THE DIFFERENT FILES
from lib.filter_explorer import dataset, fuente_seleccionada, caracteristica_seleccionada, entrada_seleccionada, sidebar_explorer,filtrar_fuente,filtrar_entrada, filtrar_elemento,filtrar_caracteristica, dataset_explorer

elemento_seleccionado='Artículos'

color = '#08469b'
#dataset_explorador = dataset_explorer(dataset,elemento_seleccionado)
table_explorer= html.Div([     
        # Table
        html.Div([
            html.H3('Tabla de datos', id="title_table", style={'display': 'block'}),
            html.Div(
                dash_table.DataTable(
                    id='table_date',
                    #columns=[{'name': i, 'id': i} for i in dataset_explorador.columns],
                    data = None,
                    page_size=100,
                    #page_action='none',
                    style_table={'height': '350px', 'overflowY': 'auto', 'maxWidth': '1000px'},
                    style_cell={
                        'maxWidth': '500px',
                        'overflow': 'hidden',
                        'whiteSpace': 'normal',
                        'textAlign': 'center',
                        'fontSize': '12px',
                         'cursor': 'pointer'
                    },
                    #tooltip_data=[],
                    #tooltip_duration=None,  # Para mantener visible el tooltip al mover el cursor dentro de la celda
                ),
                className='table-responsive',               
            )
        ], style={'marginTop': '2em'})
    ] , 
    className='col-6',
    style={'textAlign':'center', 'display':'flex', 'justifyContent':'space-around'}
    )
layout= html.Div([    
    html.Div([
                dbc.Col(
                    table_explorer
                    )
                ],className="dash-body"),
        sidebar_explorer,
],
className="dash-content",style={"color":"black"}
)

@callback(
    [Output('filter_element', 'options'), Output('filter_element','value')],
    Input('filter_fuente', 'value')
)
def actualizar_fuente_seleccionada(fuente):
    opciones_elemento = filtrar_fuente(fuente, 'option')    
    return opciones_elemento, None

@callback(
    Output('component_filters', 'children'),
    [Input('filter_element', 'value'), Input('filter_fuente', 'value')]
)
def actualizar_elemento_seleccionado(elemento, fuente): 
    if elemento == None:
        div_component= [html.H5("Caracteristica:",className="title_white",style={"color":"white"}),
        html.Div(
            dcc.Dropdown(
                id='filter_feature',
                options = [],
                disabled =True,
                value = None
            ),
        id='div_feature'),
        html.H5("Entrada:",className="title_white",style={"color":"white"}),
        html.Div(children=[
            dcc.Input(
                id='filter_input',
                placeholder='Digite el filtro',
                type='text',
                disabled =True,
                value = None
            )],
        id='div_input')]
    else:
        opciones_caracteristica=filtrar_elemento(elemento, fuente,'option')
        div_component = [html.H5("Caracteristica:",className="title_white",style={"color":"white"}),
        html.Div(
            dcc.Dropdown(
                id='filter_feature',
                options = opciones_caracteristica,
                value = None             
            ),
        id='div_feature'),
        html.H5("Entrada:",className="title_white",style={"color":"white"}),
        html.Div(children=[
            dcc.Input(
                id='filter_input',
                placeholder='Inactivo',
                type='text',
                disabled =True,
                value = None
            )],
        id='div_input')]  
    return div_component
@callback(
    Output('div_input', 'children'),
    [Input('filter_feature', 'value'),Input('filter_element', 'value'), Input('filter_fuente', 'value')]
)
def actualizar_caractersitica_seleccionada(caracteristica,elemento,fuente):  
    
    if (elemento == None) or (caracteristica == None):
        valor_entrada = None
    else:
        valor_entrada, opciones_entrada=filtrar_caracteristica(caracteristica,elemento,fuente)
    
    if type(valor_entrada) == str:
        filter =  dcc.Input(id='filter_input', placeholder='Digite el filtro', type='text', value='')
    elif type(valor_entrada) == list:
        filter = dcc.Dropdown(id="filter_input", options= opciones_entrada, multi=True)
    elif type(valor_entrada) == tuple:
        year_today = date.today().year
        option_drop = list(range(1975,date.today().year))
        print('drop: ',option_drop)   
        #filter = dbc.Input(id="date_start", type="number", min=1975, max=year_today, step=1, placeholder='Año inicial'), dcc.Input(id="date_end", type="number", min=0, max=year_today, step=1 , disabled = True, placeholder='Año final'), dcc.Input(id='filter_input', style={'display': 'none'})
        filter = dcc.Dropdown(id="date_start", placeholder='Año inicial', options = option_drop, value=None), dcc.Dropdown(id="date_end", options= [],disabled = True, placeholder='Año final', value= None), dcc.Input(id='filter_input', style={'display': 'none'})

    else:
        print('entro aqui')
        filter = dcc.Input(id='filter_input', placeholder='Inactivo', value=None, disabled=True)
    return filter

@callback(
     [Output('date_end', 'options'),Output('date_end','disabled')],
     Input('date_start', 'value')
 )
def validate_date_end(minimo):
     if minimo == None:
         return [1975,date.today().year], True
     return list(range(minimo,date.today().year)), False

@callback(
    Output('filter_input', 'value'),
    State('date_start', 'value'),
    Input('date_end','value')
 )
def filter_input_contructor(inicial, final):
    if final == None:
        fechas = str((1975, date.today().year))
    else:
        fechas = str((inicial, final))
    return fechas

@callback(Output('table_date', 'data'),
          [Input('button_state','n_clicks'),
            State('filter_fuente', 'value'),
            State('filter_element', 'value'),
            State('filter_feature', 'value'),
            State('filter_input','value')])
def display(boton,fuente, elemento, caracteristica, entrada):
    try:
        entrada_temp = eval(entrada)
        if type(entrada_temp) == tuple:
            entrada = entrada_temp
        else:
            raise ValueError
    except:
        pass
    if (elemento==None) and (caracteristica==None) and (entrada==None):
        data=pd.DataFrame().to_dict('records')
        #tool_tip=[]
    elif (elemento != None) and (caracteristica==None) and (entrada==None):
        data = filtrar_elemento(elemento,fuente,'data').astype(str).fillna('No Aplica').to_dict('records')
        #tool_tip=[{str(column): {'value': str(value), 'type': 'text'} for column, value in row.items()} for row in data]
    elif (elemento !=None) and (caracteristica != None) and (entrada!=None):
        data = filtrar_entrada(entrada,caracteristica,elemento,fuente).astype(str).fillna('No Aplica').to_dict('records')
        #tool_tip=[{str(column): {'value': str(value), 'type': 'text'} for column, value in row.items()} for row in data]
    elif (elemento!= None) and (caracteristica !=None) and (entrada == None):
        data = filtrar_elemento(elemento,fuente,'data').astype(str).fillna('No Aplica').to_dict('records')

    else:
        data=pd.DataFrame().to_dict('records')
        #tool_tip=[]
    try:
        print('print del try', data[0])
    except:
        print('printl del exept: ', data)
    return data#,tool_tip

