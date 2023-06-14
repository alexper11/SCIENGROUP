# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import pandas as pd
import numpy as np
import re

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import json
from datetime import datetime as dt
from functions.csv_importer import gruplac_basico, gruplac_integrantes, elementos_gruplac_individual, fuente_dic, referencias, caracteristicas, caracteristicas_invertido, pmin, pmax, productos_ano, opciones_grupo, opciones_parametro_general

elementos_gruplac_general=elementos_gruplac_individual

#################################################################
#Funciones de filtros
############################################################
def filtro_gruplac_grupo_individual(grupo): #retorna opciones de elemento
    idgruplac=gruplac_basico[gruplac_basico['nombre']==grupo]['idgruplac'].iloc[0]
    opc_elementos=[]
    for elemento in elementos_gruplac_individual:
        data=fuente_dic['GRUPLAC'][elemento].dropna(subset='idgruplac')
        if idgruplac in data['idgruplac'].values:
            opc_elementos.append(elemento)
    #data=pd.DataFrame()
    return opc_elementos#, data

def filtro_gruplac_elemento_individual(grupo,elemento): #elemento no es 'Todos', retorna data
    #SI ELEMENTO ES TODOS LLAMARA OTRAS FUNCIONES DE GRAFICA PARA ESTE FIN
    ######################
    #if elemento=='Todos':
    #    data=pd.DataFrame()
    #else:
    idgruplac=gruplac_basico[gruplac_basico['nombre']==grupo]['idgruplac'].iloc[0]
    data=fuente_dic['GRUPLAC'][elemento].dropna(subset='idgruplac')
    data=data[data['idgruplac']==idgruplac]#.astype(globals()[str(referencias['GRUPLAC'][elemento])][data.columns.to_list()].dtypes.to_dict())
    return data

def filtro_gruplac_parametro_general(parametro): #retorna opciones de valor general
    if parametro=='Ingreso Manual':
        opc_valor_general=gruplac_basico['nombre'].drop_duplicates(keep='first').to_list()
    
    elif parametro=='Clasificación':
        opc_valor_general=fuente_dic['GRUPLAC']['Datos Básicos']['clasificacion'].drop_duplicates(keep='first').to_list()
        
    elif parametro=='Institución':
        opc_valor_general=fuente_dic['GRUPLAC']['Institución']['nombre'].drop_duplicates(keep='first').to_list()
    
    elif parametro=='Áreas':
        aux_list=[]
        fuente_dic['GRUPLAC']['Datos Básicos']['areas'].dropna().str.split(';').apply(lambda x: aux_list.extend(x))
        opc_valor_general=list(set(aux_list))
    
    elif parametro=='Líneas de Investigación':
        aux_list=[]
        fuente_dic['GRUPLAC']['Líneas de Investigación']['lineas'].dropna().str.split(';').apply(lambda x: aux_list.extend(x))
        opc_valor_general=list(set(aux_list))
    
    #data=pd.DataFrame()
    #opciones_elemento_general=None
    return opc_valor_general#, data

def filtro_gruplac_valor_general(parametro,valor): #grupos es una lista de grupos
    
    if parametro=='Ingreso Manual':
        idgruplacs=gruplac_basico[gruplac_basico['nombre'].isin(valor)]['idgruplac'].drop_duplicates(keep='first').to_list()
    
    elif parametro=='Clasificación':
        idgruplacs=gruplac_basico[gruplac_basico['clasificacion'].isin(valor)]['idgruplac'].drop_duplicates(keep='first').to_list()
        
    elif parametro=='Institución':
        data=fuente_dic['GRUPLAC']['Institución']
        idgruplacs=data[data['nombre'].isin(valor)]['idgruplac'].drop_duplicates(keep='first').to_list()
    
    elif parametro=='Áreas':
        pattern=re.compile('|'.join(valor)).pattern
        aux_data=gruplac_basico.copy().dropna()
        idgruplacs=aux_data[aux_data['areas'].str.contains(pattern)]['idgruplac'].drop_duplicates(keep='first').to_list()
    
    elif parametro=='Líneas de Investigación':
        pattern=re.compile('|'.join(valor)).pattern
        aux_data=fuente_dic['GRUPLAC']['Líneas de Investigación'].copy().dropna()
        idgruplacs=aux_data[aux_data['lineas'].str.contains(pattern)]['idgruplac'].drop_duplicates(keep='first').to_list()
    
    nombre_grupos=gruplac_basico[gruplac_basico['idgruplac'].isin(idgruplacs)]['nombre'].to_list()
    #data=pd.DataFrame()
    #elemento_general_seleccionado='Todos'
    return idgruplacs, nombre_grupos#, data

def filtro_gruplac_elemento_general(idgruplacs,elemento):
    #if elemento=='Todos':
    #    data=pd.DataFrame()
    #else:
    data=fuente_dic['GRUPLAC'][elemento].dropna(subset='idgruplac')
    data=data[data['idgruplac'].isin(idgruplacs)]#.astype(globals()[str(referencias['GRUPLAC'][elemento])][data.columns.to_list()].dtypes.to_dict())
    return data

def get_indicadores(idgruplac):
    serie_fechas=pd.Series([],dtype='float64')
    #serie_fechas= pd.concat([serie_fechas,gruplac_basico[gruplac_basico['idgruplac']==idgruplac]['fecha_formacion'].dropna().dt.year])
    serie_fechas= pd.concat([serie_fechas,pd.Series([pmax])])
    #formatear
    data=fuente_dic['GRUPLAC']['Artículos']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Libros']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Capítulos']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Programa de Doctorado']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Programa de Maestría']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Cursos de Doctorado']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Cursos de Maestría']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Otros Artículos']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Otros Libros']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Diseño industrial']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Innovación Empresarial']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Planta Piloto']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Otros Productos Tecnológicos']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Prototipos']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Software']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    data=fuente_dic['GRUPLAC']['Empresa Tecnológica']
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac']==idgruplac]['fecha_registro'].dropna().dt.year])
    serie_fechas=serie_fechas.value_counts().sort_index().astype('float64')

    #serie_fechas.iloc[0]=serie_fechas.iloc[0]-1 #fecha_formación
    serie_fechas.iloc[-1]=serie_fechas.iloc[-1]-1
    serie_fechas=serie_fechas.reindex(list(range(serie_fechas.index.min(),serie_fechas.index.max()+1)),fill_value=0)
    mean=serie_fechas.mean()
    #mean=serie_fechas.sum()/(serie_fechas.index[-1]-serie_fechas.index[0]+1)
    if mean==0:
        consistency_value=0
    else:    
        std=serie_fechas.std()
        consistency_value=1/(std/mean)
    products_count=serie_fechas.sum()
    #La serie "serie_fechas" sirve para series de tiempo ya que contiene productos por año desde fecha de creación del grupo hasta
    #el ultimo año que registra el dataset general de la producción en el Cauca
    #print('total last 3 years: ',sum(productos_ano.iloc[-3:]))
    pdly=(sum(serie_fechas.iloc[-3:])*100)/sum(productos_ano.iloc[-3:])
    #print(sum(serie_fechas.iloc[-3:]))
    return round(consistency_value,2), round(mean,2), round(pdly,2), int(products_count), serie_fechas

def get_indicadores_relativos(idgruplac,elemento):
    serie_fechas=pd.Series([],dtype='float64')
    df=fuente_dic['GRUPLAC'][elemento].copy()
    #serie_fechas= pd.concat([serie_fechas,gruplac_basico[gruplac_basico['idgruplac']==idgruplac]['fecha_formacion'].dropna().dt.year])
    serie_fechas= pd.concat([serie_fechas,pd.Series([pmax])])
    if elemento=='Empresa Tecnológica':
        serie_fechas= pd.concat([serie_fechas,df[df['idgruplac']==idgruplac]['fecha_registro'].dropna().dt.year])
    else:
        serie_fechas= pd.concat([serie_fechas,df[df['idgruplac']==idgruplac]['fecha'].dropna().dt.year])
    serie_fechas=serie_fechas.value_counts().sort_index().astype('float64')
    #serie_fechas.iloc[0]=serie_fechas.iloc[0]-1 #fecha_formacion
    serie_fechas.iloc[-1]=serie_fechas.iloc[-1]-1
    serie_fechas=serie_fechas.reindex(list(range(serie_fechas.index.min(),serie_fechas.index.max()+1)),fill_value=0)
    
    mean=serie_fechas.mean()
    #mean=serie_fechas.sum()/(serie_fechas.index[-1]-serie_fechas.index[0]+1)
    
    if mean == 0:
        consistency_value=0
    else:
        std=serie_fechas.std()
        consistency_value=1/(std/mean)
    products_count=serie_fechas.sum()
    
    if elemento=='Empresa Tecnológica':
        df=df['fecha_registro'].dropna().dt.year.value_counts().sort_index().astype('float64')
        df=df.reindex(list(range(df.index.min(),df.index.max()+1)),fill_value=0).iloc[-3:]
    else:
        df=df['fecha'].dropna().dt.year.value_counts().sort_index().astype('float64')
        df=df.reindex(list(range(df.index.min(),df.index.max()+1)),fill_value=0).iloc[-3:]
    
    #print('total last 3 years: ',sum(df))
    pdly=(sum(serie_fechas.iloc[-3:])*100)/sum(df)
    #print('group elements last 3 years: ',sum(serie_fechas.iloc[-3:]))
    return round(consistency_value,2), round(mean,2), round(pdly,2), int(products_count), serie_fechas

def get_author_count(idgruplac):
    count=gruplac_integrantes[gruplac_integrantes['idgruplac']==idgruplac]['url'].count()
    return count

def get_perfil_minciencias(idgruplac):
    url='https://scienti.minciencias.gov.co/gruplac/jsp/Medicion/graficas/verPerfiles.jsp?id_convocatoria=21&nroIdGrupo='+idgruplac
    return url

def get_codigo_grupo(nombre):
    codigo=gruplac_basico[gruplac_basico['nombre']==nombre]['idgruplac'].iloc[0]
    return codigo
####################################################################################
# Add the dash_Img
####################################################################################

#############################################################################
# State Dropdown
#############################################################################


option_group = dcc.Dropdown(
        id='filter_group',
        options = opciones_grupo,
        value = None  # Valor inicial seleccionado
    )
option_element = dcc.Dropdown(
        id='filter_element_gruplac',
        options = [],
        disabled=True,
        value = None  # Valor inicial seleccionado
    )
option_parameter = dcc.Dropdown(
        id='filter_parameter',
        options = opciones_parametro_general,
        value = None  # Valor inicial seleccionado
    )
option_value = dcc.Dropdown(
        id='filter_value',
        options = [],
        value = None,  # Valor inicial seleccionado
        disabled= True
    )
option_element_gruplac_general = dcc.Dropdown(
        id='filter_element_gruplac_general',
        options = elementos_gruplac_general,
        value = None,  # Valor inicial seleccionado
        disabled=True
    )
#############################################################################
# Sidebar Layout
#############################################################################
sidebar_graph = html.Div([
    html.H1('Opciones de filtrado',className="title_white",style={"color":"white"}),
    dcc.Tabs(id="tabs_filter_scienti", value='tab_individual', 
    children=[dcc.Tab(label='Individual', value='tab_individual'),
        dcc.Tab(label='Grupal', value='tab_grupal'),
    ]),    
    html.Div([    
        html.P("Filtros Grupo individual.",style={"color":"white"} ),   
        html.Hr(),  # Add an horizontal line
        ####################################################
        # Place the rest of Layout here
        ####################################################
        html.H5("Grupo:",className="title_white",style={"color":"white"}),
        option_group,
        html.H5("Elemento:",className="title_white",style={"color":"white"}),
        option_element,
    ],id="filtro_individual",style={}),
    html.Div([ 
        html.P("Filtros Grupos General.",style={"color":"white"} ),   
        html.Hr(),  # Add an horizontal line
        ####################################################
        # Place the rest of Layout here
        ####################################################
        html.H5("Parametro:",className="title_white",style={"color":"white"}),
        option_parameter,
        html.H5("Valor:",className="title_white",style={"color":"white"}),
        option_value,
        html.H5("Elemento:",className="title_white",style={"color":"white"}),
        option_element_gruplac_general,
    ],id="filtro_grupal",style={}),
        html.Button('Filtrar', id='button_state', n_clicks=0),
],className="dash-sidebar",    
)

#  ---------------------callback---------------
@callback(
    [Output('filtro_individual', 'style'),Output('filtro_grupal', 'style')],
    Input('tabs_filter_scienti', 'value'))
def render_content(tab):
    if tab == 'tab_individual':
        return {"display": "block"},{"display": "none"}
    else:
        return {"display": "none"},{"display": "block"}

@callback(
    [Output('filter_element_gruplac', 'value'),Output('filter_element_gruplac', 'disabled'),Output('filter_element_gruplac', 'options')],
    Input('filter_group', 'value'))
def callback_element(grupo):
    if grupo == None:
        return None, True, []
    else:
        option_elements= filtro_gruplac_grupo_individual(grupo)
        return 'Todos', False, option_elements

@callback(
    [Output('filter_value', 'value'),Output('filter_value', 'disabled'),Output('filter_value', 'options')],
    Input('filter_parameter', 'value'))
def callback_parameter(parametro):
    if parametro == None:
        return None, True, []
    else:
        option_elements= filtro_gruplac_parametro_general(parametro)
        return None, False, option_elements
    
@callback(
    [Output('filter_element_gruplac_general', 'disabled'),Output('filter_element_gruplac_general', 'value')],
    [State('filter_parameter', 'value'), Input('filter_value', 'disabled'),
    Input('filter_value', 'value')])
def callback_value(parameter, disable_value, value):
    if disable_value == True:
        return True, None
    if (value == None) and (parameter == None):
        return True, None
    elif (value == None) or (parameter == None):
        return True, None
    else:        
        return False, None