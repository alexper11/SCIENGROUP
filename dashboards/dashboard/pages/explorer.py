from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import pandas as pd
from functions.csv_importer import referencias

# LOAD THE DIFFERENT FILES
from lib.filter_explorer import dataset, fuente_seleccionada, caracteristica_seleccionada, entrada_seleccionada, sidebar_explorer,filtrar_fuente,filtrar_entrada, filtrar_elemento,filtrar_caracteristica, dataset_explorer

elemento_seleccionado='Artículos'

color = '#08469b'
dataset_explorador = dataset_explorer(dataset,elemento_seleccionado)
table_explorer= html.Div([     
        # Table
        html.Div([
            html.H3(f'Tabla de datos'),
            html.Div(
                dash_table.DataTable(
                    id='table_date',
                    #columns=[{'name': i, 'id': i} for i in dataset_explorador.columns],
                    #data = None,
                    page_size=9,
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
    Output('filter_element', 'options'),
    Input('filter_fuente', 'value')
)
def actualizar_fuente_seleccionada(fuente):    
    fuente_seleccionada = fuente
    dataset, opciones_elemento, opciones_caracteristica, valor_entrada = filtrar_fuente(fuente_seleccionada)    
    #dataset_explorador = dataset_explorer(dataset)    
    return opciones_elemento

@callback(
    [Output('filter_feature', 'options'),Output('table_date', 'data')],
    #Output('filter_feature', 'options'),
    [Input('filter_element', 'value'), Input('filter_fuente', 'value')]
)
def actualizar_elemento_seleccionado(elemento, fuente): 
    dataset, opciones_caracteristica, valor_entrada=filtrar_elemento(elemento, fuente)
    dataset_explorador = dataset_explorer(dataset, elemento).astype(str).fillna('No aplica').to_dict("records")
    print(type(dataset_explorador))
    print(opciones_caracteristica)
    return opciones_caracteristica, dataset_explorador
    #return opciones_caracteristica
# @callback(
#     Output('option_inputs', 'children'),
#     Input('filter_feature', 'value')
# )
# def actualizar_caractersitica_seleccionada(caracteristica):  
#     print('caracteristica',str(caracteristica))  
#     caracteristica_seleccionada = caracteristica
#     valor_entrada, opciones_entrada=filtrar_caracteristica(caracteristica_seleccionada)
#     print('Tipo de entrada: ',type(valor_entrada))
#     if type(valor_entrada) == list:
#         filter =  dcc.Input(
#                     id='input_value',
#                     placeholder='Digite el filtro',
#                     type='text',
#                     value=''
#                 )
#     elif type(valor_entrada) == str:
#         filter = dcc.Dropdown(
#                     id="input_value",
#                     # options=[{"label": tags, "value": tags} for tags in opciones_entrada.index],
#                     options= opciones_entrada,
#                     multi=True
#                 )
#     elif type(valor_entrada) == tuple:
#         filter = dcc.Input(
#                     id='input_value1',
#                     placeholder='Digite el año',
#                     type='text',
#                     value=''
#                 ),
#         dcc.Input(
#                     id='input_value2',
#                     placeholder='Digite el año',
#                     type='text',
#                     value=''
#                 )
#     return filter