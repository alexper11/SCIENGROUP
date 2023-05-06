from dash.dependencies import Input, Output, State
from dash import html
import dash_core_components as dcc
import dash_table
import pandas as pd
from functions.csv_importer import read_archive

# Datos de ejemplo
df = read_archive()
color = '#08469b'

layout= html.Div([
    #Header
    html.Div([
        html.H1("Exploración de datos"),
        html.P("filtros para explorar los datos." )
    ] ,
    className='col-12',
    style={'textAlign':'center'}
    ),

    #Dropdwon options, this configuration doesn't allow to change two filters at a time
    html.Div([
        dcc.Loading(dcc.Dropdown(options=[{'label': 'Opción 1', 'value': 'opcion1'},
            {'label': 'Opción 2', 'value': 'opcion2'}], placeholder="Elija primer filtro", id='filter-1'),parent_className='dropdown', className='dropdown-loading', color=color, type='dot'),
        dcc.Loading(dcc.Dropdown(["Opción 7","Opción 8"], placeholder="Elija cuarto filtro",id='filter-4'),parent_className='dropdown',  className='dropdown-loading',color=color, type='dot'),
        html.Div(id='filters-container')
    ] , 
    className='col-6',
    style={'textAlign':'center', 'display':'flex', 'justifyContent':'space-around'}
    ),

    #Dynamic Content
    html.Div([
        dcc.Loading(
            id="loading-2",
            children=[            
            #Reload button
            html.A([
                    html.Img(src='/assets/img/reload.png',className='whatsappIcon')
                ], id='reload-button')
            ],type="cube", fullscreen=False, color=color, style={'height':'100%', 'marginTop':'15rem'}
        ),
        # Table
        html.Div([
            html.H3('Tabla de datos'),
            html.Div(
                dash_table.DataTable(
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    data=df.to_dict('records')
                ),
                className='table-responsive',
                style={'maxHeight': '600px', 'overflowY': 'scroll', 'maxWidth': '1200px', 'width': '100%'}
            )
        ], style={'marginTop': '2em'})
    ] , 
    className='col-6',
    style={'textAlign':'center', 'display':'flex', 'justifyContent':'space-around'}
    ),    
],
style={"color":"black"}
)