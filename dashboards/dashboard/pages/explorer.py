from dash.dependencies import Input, Output, State
from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from functions.csv_importer import read_archive

# LOAD THE DIFFERENT FILES
from lib.filter_explorer import sidebar_explorer

# Datos de ejemplo
df = read_archive()
color = '#08469b'

table_explorer= html.Div([        
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

layout= html.Div([
    #Header
    html.Div([
        html.H1("Exploración de datos")
    ] ,
    className='col-12',
    style={'textAlign':'center'}
    ),    
    html.Div([
                dbc.Col(
                    table_explorer
                    )
                ],className="dash-body"),
        sidebar_explorer,
],
style={"color":"black"}
)