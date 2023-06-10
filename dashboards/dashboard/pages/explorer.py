from dash.dependencies import Input, Output

from dash import dcc
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, callback, dash_table
import pandas as pd
from functions.csv_importer import referencias

# LOAD THE DIFFERENT FILES
from lib.filter_explorer import dataset, fuente_seleccionada, caracteristica_seleccionada, entrada_seleccionada, sidebar_explorer,filtrar_fuente,filtrar_entrada, filtrar_elemento,filtrar_caracteristica, dataset_explorer

elemento_seleccionado='Artículos'

color = '#08469b'
#dataset_explorador = dataset_explorer(dataset,elemento_seleccionado)
table_explorer= html.Div([     
        # Table
        html.Div([
            html.H3(f'Tabla de datos'),
            html.Div(
                dash_table.DataTable(
                    id='table_date',
                    #columns=[{'name': i, 'id': i} for i in dataset_explorador.columns],
                    data = None,
                    page_size=100,
                    #page_action='none',
                    style_table={'height': '350px', 'overflowY': 'auto', 'maxWidth': '1100px'},
                    style_cell={
                        'maxWidth': '200px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'whiteSpace': 'nowrap',
                        'textAlign': 'center',
                        'fontSize': '12px',
                         'cursor': 'pointer'
                    },
                    # tooltip_data=[
                    #     {
                    #         column: {'value': str(value), 'type': 'text'}
                    #         for column, value in row.items()#usar pandas
                    #     } for row in dataset_explorador.to_dict("records")
                    # ],
                    # tooltip_duration=None,  # Para mantener visible el tooltip al mover el cursor dentro de la celda
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
style={"color":"black"}
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
                disabled =True
            ),
        id='div_feature'),
        html.H5("Entrada:",className="title_white",style={"color":"white"}),
        html.Div(
            dcc.Input(
                id='input_value',
                placeholder='Digite el filtro',
                type='text',
                disabled =True
            ),
        id='div_element')]
    else:
        opciones_caracteristica=filtrar_elemento(elemento, fuente,'option')
        div_component = [html.H5("Caracteristica:",className="title_white",style={"color":"white"}),
        html.Div(
            dcc.Dropdown(
                id='filter_feature',
                options = opciones_caracteristica                
            ),
        id='div_feature'),
        html.H5("Entrada:",className="title_white",style={"color":"white"}),
        html.Div(
            dcc.Input(
                id='input_value',
                placeholder='Digite el filtro',
                type='text',
                disabled =True
            ),
        id='div_element')]  
    return div_component
@callback(
    Output('option_inputs', 'children'),
    [Input('filter_feature', 'value'),Input('filter_element', 'value'), Input('filter_fuente', 'value')]
)
def actualizar_caractersitica_seleccionada(caracteristica,elemento,fuente):  
    print('caracteristica',str(caracteristica))
    valor_entrada, opciones_entrada=filtrar_caracteristica(caracteristica,elemento,fuente)
    print('Tipo de entrada: ',type(valor_entrada))
    if type(valor_entrada) == list:
        filter =  dcc.Input(id='input_value', placeholder='Digite el filtro', type='text', value='')
    elif type(valor_entrada) == str:
        filter = dcc.Dropdown(id="input_value", options= opciones_entrada, multi=True)
    elif type(valor_entrada) == tuple:
        filter = dcc.Input(id='input_value', placeholder='Digite el a1', value=''),dcc.Input(id='input_value2', placeholder='Digite el a2', type='text', value='')
    return filter