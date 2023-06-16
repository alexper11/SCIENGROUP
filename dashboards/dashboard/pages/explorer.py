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
from functions.csv_importer import gruplac_articulos, gruplac_basico, gruplac_caplibros, gruplac_integrantes,gruplac_libros, gruplac_oarticulos, gruplac_olibros, gruplac_cdoctorado, gruplac_cmaestria, gruplac_disenoind,gruplac_empresatec,gruplac_innovaempresa,gruplac_instituciones,gruplac_lineas,gruplac_otecnologicos,gruplac_pdoctorado,gruplac_plantapiloto,gruplac_pmaestria,gruplac_prototipos,gruplac_software,scopus_autores,scopus_productos,cvlac_articulos,cvlac_basico,cvlac_caplibros,cvlac_libros,cvlac_empresatec,cvlac_innovaempresa,cvlac_lineas,cvlac_tecnologicos,cvlac_prototipos,cvlac_software,cvlac_areas,cvlac_reconocimiento,cvlac_identificadores


elemento_seleccionado='Artículos'

table_explorer= dcc.Loading([dbc.Toast(
            id="auto-toast",
            header="No hay datos disponibles",
            color='secondary',
            # duration=4000,
            dismissable=True,
            is_open=False,
            # style={"color":"white",'backgroundColor': 'red','padding-top': '50px'}
            ),
            # html.H3('Tabla de datos', id="title_table"),
            dash_table.DataTable(
                id='table_date',
                #columns=[{'name': i, 'id': i} for i in dataset_explorador.columns],
                data = None,
                page_size=100,
                #virtualization = True,
                #fixed_rows={'headers':True,'data':0},
                cell_selectable=False,
                style_header={'position': 'sticky', 'top': 0},
                style_table={'overflowX':'auto', 'maxHeight':'74vh','maxWidth':'95vw'},
                # style_cell_conditional=[
                #     {'if': {'column_id': 'autores'},
                #     'width': '500px'},
                #     {'if': {'column_id': 'institucion'},
                #     'width': '500px'},
                #     {'if': {'column_id': 'titulo'},
                #     'width': '500px'},
                # ],
                style_cell={
                    'maxHeight': '50px',
                    'overflow': 'hidden',
                    'whiteSpace': 'normal',
                    'textAlign': 'left',
                    'fontSize': '12px',
                    'cursor': 'pointer'
                },
            ),
        ],className='loader_explorer',
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
                value = None,
                placeholder='Elemento Requerido'
            ),
        id='div_feature'),
        html.H5("Entrada:",className="title_white",style={"color":"white"}),
        html.Div(children=[
            dcc.Input(
                id='filter_inputs',
                placeholder='Característica Requerida',
                type='text',
                disabled =True,
                value = None,
            )],
            id='div_input')]
    else:
        opciones_caracteristica=filtrar_elemento(elemento, fuente,'option')
        div_component = [html.H5("Caracteristica:",className="title_white",style={"color":"white"}),
        html.Div(
            dcc.Dropdown(
                id='filter_feature',
                options = opciones_caracteristica,
                value = None,             
            ),
        id='div_feature'),
        html.H5("Entrada:",className="title_white",style={"color":"white"}),
        html.Div(children=[
            dcc.Input(
                id='filter_inputs',
                placeholder='Característica Requerida',
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
        filter =  dcc.Input(id='filter_inputs', placeholder='', type='text', value='')
    elif type(valor_entrada) == list:
        filter = dcc.Dropdown(id="filter_inputs", options= opciones_entrada, multi=True, optionHeight=45)#,maxHeight=100)
    elif type(valor_entrada) == tuple:
        #year_today = date.today().year
        option_drop = list(range(1975,date.today().year+1))
        print('drop: ',option_drop)   
        #filter = dbc.Input(id="date_start", type="number", min=1975, max=year_today, step=1, placeholder='Año inicial'), dcc.Input(id="date_end", type="number", min=0, max=year_today, step=1 , disabled = True, placeholder='Año final'), dcc.Input(id='filter_inputs', style={'display': 'none'})
        filter = dcc.Dropdown(id="date_start", placeholder='Año inicial', options = option_drop, value=None), dcc.Dropdown(id="date_end", options= [],disabled = True, placeholder='Año final', value= None), dcc.Input(id='filter_inputs', style={'display': 'none'})

    else:
        filter = dcc.Input(id='filter_inputs', placeholder='Característica Requerida', value='', disabled=True)
    return filter

@callback(
     [Output('date_end', 'options'),Output('date_end','disabled')],
     Input('date_start', 'value')
 )
def validate_date_end(minimo):
    if minimo == None:
        return [1975,date.today().year], True
    return list(range(minimo,date.today().year+1)), False

@callback(
    Output('filter_inputs', 'value'),
    State('date_start', 'value'),
    Input('date_end','value')
 )
def filter_inputs_contructor(inicial, final):
    if final == None:
        fechas = str((1975, date.today().year))
    else:
        fechas = str((inicial, final))
    return fechas

@callback([Output('table_date', 'data'),Output('table_date', 'columns'),Output("auto-toast", "is_open")],
          [Input('button_state','n_clicks'),
            State('filter_fuente', 'value'),
            State('filter_element', 'value'),
            State('filter_feature', 'value'),
            State('filter_inputs','value')])
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
        #tool_tip=[]
    elif (elemento != None) and (caracteristica==None) and ((entrada==None) or (entrada=='')):
        data = filtrar_elemento(elemento,fuente,'data')
        #tool_tip=[{str(column): {'value': str(value), 'type': 'text'} for column, value in row.items()} for row in data]
    elif (elemento !=None) and (caracteristica != None) and ((entrada!=None) and (entrada!='')):
        data = filtrar_entrada(entrada,caracteristica,elemento,fuente)
        #tool_tip=[{str(column): {'value': str(value), 'type': 'text'} for column, value in row.items()} for row in data]
    elif (elemento!= None) and (caracteristica !=None) and ((entrada==None) or (entrada=='')):
        data = filtrar_elemento(elemento,fuente,'data')
    else:
        data=pd.DataFrame()
    print(data.shape[0])
    if data.shape[0]>=1:
        data=globals()[str(referencias[fuente][elemento])].loc[list(data.index)].astype(str).fillna('No Aplica')
        if fuente=='SCOPUS':
            data=data.drop(['scopus_id','eid','issue','numero_articulo','pag_inicio','pag_fin','pag_count','affil_id','abstract','etapa_publicacion','autores_id'], axis=1, errors='ignore')
            locs=data[data['institucion'].str.len()>300].index.tolist()
            data['institucion'].loc[locs]=data['institucion'].loc[locs].str.slice(stop=300)+'...'
            locs=data[data['autores'].str.len()>300].index.tolist()
            data['autores'].loc[locs]=data['autores'].loc[locs].str.slice(stop=200)+'...'
            locs=data[data['pais'].str.len()>300].index.tolist()
            data['pais'].loc[locs]=data['pais'].loc[locs].str.slice(stop=300)+'...'
        else:
            data=data.drop(['volumen','fasciculo','paginas'], axis=1, errors='ignore')
        columns=[{'name': i, 'id': i} for i in data.columns]
        toast=False
    else:
        columns=None
        toast=True
        
    return data.to_dict('records'),columns, toast

