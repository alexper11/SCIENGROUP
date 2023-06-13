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

table_explorer= html.Div([
            # html.H3('Tabla de datos', id="title_table"),
            dash_table.DataTable(
                id='table_date',
                #columns=[{'name': i, 'id': i} for i in dataset_explorador.columns],
                data = None,
                page_size=100,
                virtualization = True,
                fixed_columns={'headers':True},
                cell_selectable=False,
                #page_action='none',
                # css=[{'rule':'height:inherit'}],
                style_table={'overflowX':'auto', 'height': '100%', 'maxWidth': 'auto', 'maxHeight':'100%'},
                style_cell={
                    'maxWidth': '500px',
                    'overflow': 'hidden',
                    'whiteSpace': 'normal',
                    'textAlign': 'left',
                    'fontSize': '12px',
                    'cursor': 'pointer'
                },
            ),
        ],className='table_explorer', style={'height':'93%','width':'93%'},
    )

layout= html.Div([    
    table_explorer,        
    sidebar_explorer,
    ],className="dash-body",style={"color":"black"})       


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
        filter = dcc.Input(id='filter_input', placeholder='Inactivo', value='', disabled=True)
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

@callback([Output('table_date', 'data'),Output('table_date', 'columns')],
          [Input('button_state','n_clicks'),
            State('filter_fuente', 'value'),
            State('filter_element', 'value'),
            State('filter_feature', 'value'),
            State('filter_input','value')])
def display(boton,fuente, elemento, caracteristica, entrada):
    try:
        if (entrada != None) and (entrada!=''):
            entrada_temp = eval(entrada)
            if type(entrada_temp) == tuple:
                entrada = entrada_temp
            else:
                raise ValueError
    except:
        pass
    if (elemento==None) and (caracteristica==None) and ((entrada==None) or (entrada=='')):
        data=pd.DataFrame()
        columns=None
        #tool_tip=[]
    elif (elemento != None) and (caracteristica==None) and ((entrada==None) or (entrada=='')):
        data = filtrar_elemento(elemento,fuente,'data')
        columns=[{'name': i, 'id': i} for i in data.columns]
        data=data.astype(str).fillna('No Aplica')
        #tool_tip=[{str(column): {'value': str(value), 'type': 'text'} for column, value in row.items()} for row in data]
    elif (elemento !=None) and (caracteristica != None) and ((entrada!=None) and (entrada!='')):
        data = filtrar_entrada(entrada,caracteristica,elemento,fuente)
        columns=[{'name': i, 'id': i} for i in data.columns]
        data=data.astype(str).fillna('No Aplica')
        #tool_tip=[{str(column): {'value': str(value), 'type': 'text'} for column, value in row.items()} for row in data]
    elif (elemento!= None) and (caracteristica !=None) and ((entrada==None) or (entrada=='')):
        data = filtrar_elemento(elemento,fuente,'data')
        columns=[{'name': i, 'id': i} for i in data.columns]
        data=data.astype(str).fillna('No Aplica')
    else:
        data=pd.DataFrame()
        columns=None
        #tool_tip=[]
    try:
        print(data['institucion'].iloc[5:7])
        data['institucion']=data['institucion'].str.slice(stop=500)
    except Exception as e:
        print(e)
        pass
    # try:
    #     print('print del try', data[0])
    # except:
    #     print('printl del exept: ', data)
    return data.to_dict('records'),columns#,tool_tip

