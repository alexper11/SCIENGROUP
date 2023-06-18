# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import pandas as pd
import numpy as np
import re

from dash import no_update

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import json
from datetime import datetime as dt
from functions.csv_importer import gruplac_basico, scopus_productos, elementos_scopus, fuente_dic, referencias, caracteristicas, caracteristicas_invertido, pmin, pmax, productos_ano, opciones_parametro_general

# Plotly
import plotly.express as px
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots


opciones_grupo_scopus=[]
scopus_productos['nombre_grupo'].dropna().str.split(';').apply(lambda x: opciones_grupo_scopus.extend(x)) #variable para opciones del filtro de grupo
opciones_grupo_scopus=list(map(str.strip, list(set(opciones_grupo_scopus))))

elementos_scopus_general=elementos_scopus
options_general_element_scopus=elementos_scopus_general[:]
options_general_element_scopus.append('Todos')

#######################################
#FUNCIONES DE FILTRADO
########################################
#INDIVIDUAL
def filtro_scopus_grupo_individual(grupo):
    idgruplac=gruplac_basico[gruplac_basico['nombre']==grupo]['idgruplac'].iloc[0]
    opc_elementos=[]
    for elemento in elementos_scopus:
        data=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac')
        if data['idgruplac'].str.contains(idgruplac).shape[0] > 1:
            opc_elementos.append(elemento)
    data=pd.DataFrame()
    return opc_elementos

def filtro_scopus_elemento_individual(grupo,elemento):
    idgruplac=gruplac_basico[gruplac_basico['nombre']==grupo]['idgruplac'].iloc[0]
    if elemento=='Todos':
        data=scopus_productos.dropna(subset='idgruplac').copy()
        data=data[data['idgruplac'].str.contains(idgruplac)]#.astype(globals()[str(referencias['SCOPUS'][elemento])][data.columns.to_list()].dtypes.to_dict())
    else:
        data=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac')
        data=data[data['idgruplac'].str.contains(idgruplac)]#.astype(globals()[str(referencias['SCOPUS'][elemento])][data.columns.to_list()].dtypes.to_dict())
    return data
    
#GENERAL
def filtro_scopus_parametro_general(parametro):
    if parametro=='Ingreso Manual':
        opc_valor_general=opciones_grupo_scopus
    
    elif parametro=='Clasificación':
        opc_valor_general=gruplac_basico['clasificacion'].drop_duplicates(keep='first').to_list()
        
        
    elif parametro=='Institución':
        data=fuente_dic['GRUPLAC']['Institución']
        opc_valor_general=data['nombre'].drop_duplicates(keep='first').to_list()
    
    elif parametro=='Áreas':
        aux_list=[]
        gruplac_basico['areas'].dropna().str.split(';').apply(lambda x: aux_list.extend(x))
        opc_valor_general=list(set(aux_list))
    
    elif parametro=='Líneas de Investigación':
        aux_list=[]
        fuente_dic['GRUPLAC']['Líneas de Investigación']['lineas'].dropna().str.split(';').apply(lambda x: aux_list.extend(x))
        opc_valor_general=list(set(aux_list))
        opc_valor_general=list(map(str.strip, list(set(opc_valor_general))))
    
    #data=pd.DataFrame()
    #opciones_elemento_general_scopus=None
    return opc_valor_general#, data
    
def filtro_scopus_valor_general(parametro,valor): #grupos e suna lista de grupos
    
    if parametro=='Ingreso Manual':
        idgruplacs=gruplac_basico[gruplac_basico['nombre'].isin(valor)]['idgruplac'].drop_duplicates(keep='first').to_list()
        
    elif parametro=='Clasificación':
        idgruplacs=gruplac_basico[gruplac_basico['clasificacion'].isin(valor)]['idgruplac'].drop_duplicates(keep='first').to_list()
        
    elif parametro=='Institución':
        data=fuente_dic['GRUPLAC']['Institución']
        idgruplacs=data[data['nombre'].isin(valor)]['idgruplac'].drop_duplicates(keep='first').to_list()
    
    elif parametro=='Áreas':
        list_aux=[]
        for x in valor:
            x=x.replace("(","")
            x=x.replace(")","")
            list_aux.append(x)
        valor=list_aux
        pattern=re.compile('|'.join(valor)).pattern
        aux_data=gruplac_basico.copy().dropna(subset='areas').replace(to_replace={'\(':'','\)':''},regex=True)
        idgruplacs=aux_data[aux_data['areas'].str.contains(pattern)]['idgruplac'].drop_duplicates(keep='first').to_list()
    
    elif parametro=='Líneas de Investigación':
        list_aux=[]
        for x in valor:
            x=x.replace("(","")
            x=x.replace(")","")
            list_aux.append(x)
        valor=list_aux
        pattern=re.compile('|'.join(valor)).pattern
        aux_data=fuente_dic['GRUPLAC']['Líneas de Investigación'].copy().dropna(subset='lineas').replace(to_replace={'\(':'','\)':''},regex=True)
        idgruplacs=aux_data[aux_data['lineas'].str.contains(pattern)]['idgruplac'].drop_duplicates(keep='first').to_list()
    
    nombre_grupos=gruplac_basico[gruplac_basico['idgruplac'].isin(idgruplacs)]['nombre'].to_list()
    nombre_grupos=list(set(opciones_grupo_scopus).intersection(set(nombre_grupos))) #Solo grupos visibles en Scopus
    nombre_grupos=list(map(str.strip, list(set(nombre_grupos))))
    
    #data=pd.DataFrame()
    #elemento_general_seleccionado_scopus='Todos'
    return idgruplacs, nombre_grupos#, data

def filtro_scopus_elemento_general(idgruplacs, elemento):
    #if elemento=='Todos':
    #    data=pd.DataFrame()
    #else:
    data=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac')
    data_aux=data.copy()
    data_aux['id']=data_aux.index
    indexes=[]
    data_aux[['id','idgruplac']].dropna(subset='idgruplac').apply(lambda x: indexes.append(x['id']) if len(set(x['idgruplac'].split(';')).intersection(set(idgruplacs)))>=1 else None,axis=1)
    data=data.loc[indexes].astype(globals()[str(referencias['SCOPUS'][elemento])][data.columns.to_list()].dtypes.to_dict())
    return data


#############################################################################
# State Dropdown
#############################################################################


option_group_scopus = dcc.Dropdown(
        id='filter_group_scopus',
        options = opciones_grupo_scopus,
        value = None  # Valor inicial seleccionado
    )
option_element_scopus = dcc.Dropdown(
        id='filter_element_scopus',
        options = [],
        disabled=True,
        value = None  # Valor inicial seleccionado
    )
option_parameter_scopus = dcc.Dropdown(
        id='filter_parameter_scopus',
        options = opciones_parametro_general,
        value = None  # Valor inicial seleccionado
    )
option_value_scopus = dcc.Dropdown(
        id='filter_value_scopus',
        options = [],
        value = [],  # Valor inicial seleccionado
        disabled= True,
        multi=True
    )
option_element_scopus_general = dcc.Dropdown(
        id='filter_element_scopus_general',
        options = options_general_element_scopus,        
        value = None,  # Valor inicial seleccionado
        disabled=True,
        maxHeight=160
        # style = {"bottom": "100%", "transform": "translateY(-100%)"}
    )
#############################################################################
# Sidebar Layout
#############################################################################
sidebar_scopus = html.Div([
    # html.H1('Opciones de filtrado',className="text_filter_scopus"),
    html.Hr(),  # Add an horizontal line
    dcc.Tabs(id="tabs_filter_scopus", value='tab_individual', 
    children=[dcc.Tab(label='Individual', value='tab_individual'),
        dcc.Tab(label='General', value='tab_general'),
    ]),       
    html.Div([
        html.H5("Grupo:",className="text_filter_scopus"),
        option_group_scopus,
        html.H5("Elemento:",className="text_filter_scopus"),
        option_element_scopus,
        html.Button('Filtrar', id='button_scopus_filter_indiv', n_clicks=0),
    ],id="filtro_individual_scopus"),
    html.Div([
        html.H5("Parametro:",className="text_filter_scopus"),
        option_parameter_scopus,
        html.H5("Valor:",className="text_filter_scopus"),
        option_value_scopus,
        html.H5("Elemento:",className="text_filter_scopus"),
        option_element_scopus_general,
        html.Button('Filtrar', id='button_scopus_filter_group', n_clicks=0),
    ],id="filtro_general_scopus"),        
],id="menu_filter_flex_scopus",className="dash-sidebar-graph",style={'background-color':'#A8AAAC'},    
)

#  ---------------------callback---------------
@callback(
    [Output('filtro_individual_scopus', 'hidden'),Output('filtro_general_scopus', 'hidden')],
    Input('tabs_filter_scopus', 'value'))
def render_content(tab):
    if tab == 'tab_individual':
        return False, True
    else:
        return True, False

#----------------------individual
@callback(
    [Output('filter_element_scopus', 'value'),Output('filter_element_scopus', 'disabled'),Output('filter_element_scopus', 'options')],
    Input('filter_group_scopus', 'value'))
def callback_element(grupo):
    if grupo == None:
        return None, True, []
    else:
        option_elements= filtro_scopus_grupo_individual(grupo)
        option_elements.append('Todos')
        return 'Todos', False, option_elements
#-----------------general
@callback(
    [Output('filter_value_scopus', 'value'),Output('filter_value_scopus', 'disabled'),Output('filter_value_scopus', 'options')],
    Input('filter_parameter_scopus', 'value'))
def callback_parameter(parametro):
    if parametro == None:
        return None, True, []
    else:
        option_elements= filtro_scopus_parametro_general(parametro)
        return None, False, option_elements
    
@callback(
    [Output('filter_element_scopus_general', 'disabled'),Output('filter_element_scopus_general', 'value')],
    [State('filter_parameter_scopus', 'value'),
    State('filter_element_scopus_general', 'value'),
    Input('filter_value_scopus', 'disabled'),
    Input('filter_value_scopus', 'value')])
def callback_value(parameter, state, disable_value, value):
    if disable_value == True:
        return True, None
    if (value == None) and (parameter == None):
        return True, None
    elif (value == None) or (parameter == None) or (value == []) or (parameter == []):
        return True, None
    elif (state!=None) and (state!='Todos'):        
        return False, no_update 
    else:
        return False, 'Todos'