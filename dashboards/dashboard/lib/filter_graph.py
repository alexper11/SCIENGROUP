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

# Plotly
import plotly.express as px
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

###############################################################################
#FIGURE FUNCTIONS
############################################################################

#GRUPLAC INDIVIDUAL: TODOS LOS PRODUCTOS
def time_series_all(series):
    series=series.to_frame().reset_index()
    series.columns=['fecha','productos']
    fig = px.line(series, x='fecha', y="productos", 
                  labels={
                      "fecha":"Años",
                      "productos":"Conteo de Productos"})
    fig.update_layout(title={
                  'text':"<b>Productos Anuales Generados</b>",
                  'xanchor':'center',
                  'x':0.5,
                  'yanchor':'top'},
                  font=dict(size=12))
    fig.update_traces(line_color='#0000ff', line_width=2)
    return fig

def bar_pie_all(grupo): #retorna dos graficas, recibe codigo de grupo
    dic={'producto':[],'count':[]}
    for key in list(set(fuente_dic['GRUPLAC'].keys())-set(['Institución','Líneas de Investigación','Datos Básicos'])):
        data=fuente_dic['GRUPLAC'][key]
        dic['count'].append(data[data['idgruplac']==grupo]['idgruplac'].count())
        dic['producto'].append(key)
    df=pd.DataFrame.from_dict(dic)
    df=df[df['count']>0]
    fig = px.bar(df, x="producto", y="count", color='producto',color_discrete_sequence=px.colors.sequential.Turbo,
                 labels={
                 "producto":"Tipo de Producto",
                 "count":"Cantidad de Productos"})
    fig.update(layout_showlegend=False)
    fig.update_layout(title={
               'text':"<b>Conteo de Productos</b>",
               'xanchor':'center',
               'x':0.5,
               'yanchor':'top'},
                xaxis={'categoryorder': 'total descending'},
               font=dict(size=12))
    fig_bar=fig
    fig_pie = px.pie(df, values='count', names='producto', color_discrete_sequence=px.colors.sequential.Aggrnyl,
                     hole=.3)
    fig_pie.update_layout(title={
               'text':"<b>Porcentaje de Productos</b>",
               'xanchor':'center',
               'x':0.5,
               'yanchor':'top'},
               font=dict(size=12))
    return fig_bar, fig_pie

#GRUPLAC INDIVIDUAL: ELEMENTO

def time_series_element(series, elemento):
    series=series.to_frame().reset_index()
    series.columns=['fecha','productos']
    y_label="Conteo de "+elemento
    title_label="<b>"+elemento+" Anuales Generados </b>"
    fig = px.line(series, x='fecha', y="productos", 
                  labels={
                      "fecha":"Años",
                      "productos":y_label})
    fig.update_layout(title={
                  'text':title_label,
                  'xanchor':'center',
                  'x':0.5,
                  'yanchor':'top'},
                  font=dict(size=12))
    fig.update_traces(line_color='#0000ff', line_width=2)
    return fig

def tree_author_element(data, elemento): #sólo para aquellos elementos con la columna 'autores' existente, se filtra a top 30 si hay mas
    warnings.filterwarnings(action='ignore', category=FutureWarning)#################
    dataset_autores=data[['idgruplac','autores']].copy()
    dataset_autores['autores']=dataset_autores['autores'].str.split(',')
    dataset_autores=dataset_autores.explode('autores')
    dataset_autores['autores']=dataset_autores['autores'].str.strip()
    dataset_autores=dataset_autores['autores'].value_counts().reset_index().rename(columns={'index':'autores','autores':'count'})
    dataset_autores['percents']=(dataset_autores['count']*100)/sum(dataset_autores['count'])
    if dataset_autores['autores'].count()>30:
        dataset_autores=dataset_autores.iloc[:30]
    fig = px.treemap(dataset_autores, path=[px.Constant("Top Autores"),'autores'], values='count', 
                     custom_data=['percents'])
    fig.update_traces(root_color="white")
    fig.data[0].texttemplate = "%{label}<br>"+elemento+":%{value}<br>%{customdata:.2f}%"
    fig.data[0].hovertemplate = '%{label}<br>'+elemento+':%{value}<br>%{customdata:.2f}%'
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25),
                      title={
                      'text':'<b>Participación de Autores</b>',
                      'xanchor':'center',
                      'x':0.5,
                      'yanchor':'top'},
                      font=dict(size=14))
    warnings.filterwarnings(action='default', category=FutureWarning)##################
    return fig

def pie_place_element(data):  #solo para elementos con dato de lugar de publicacion
    fig_pie = px.pie(data, values=data['lugar'].value_counts(), 
                     names=data['lugar'].value_counts().index, color_discrete_sequence=px.colors.sequential.Aggrnyl,
                     hole=.3)
    fig_pie.update_layout(title={
               'text':"<b>Lugar de Publicación</b>",
               'xanchor':'center',
               'x':0.5,
               'yanchor':'top'},
               font=dict(size=12))
    return fig_pie

def pie_type_element(data): #solo elementos con columna "tipo" existente
    fig_pie = px.pie(data, values=data['tipo'].value_counts(), 
                     names=data['tipo'].value_counts().index, color_discrete_sequence=px.colors.qualitative.Dark2,
                     hole=.3)
    fig_pie.update_layout(title={
               'text':"<b>Publicaciones por Tipo</b>",
               'xanchor':'center',
               'x':0.5,
               'yanchor':'top'},
               font=dict(size=12))
    return fig_pie

def pie_journal_element(data): #solo para elementos con columna "revista" existente, se filtra a top 30 si hay mas
    if data['revista'].value_counts().shape[0]>30:
        data_aux=data['revista'].value_counts().iloc[:30]
    else:
        data_aux=data['revista'].value_counts()
    fig_pie = px.pie(data_aux, values=data_aux, 
                     names=data_aux.index, color_discrete_sequence=px.colors.cyclical.Edge,
                     hole=.3)
    fig_pie.update_layout(title={
               'text':"<b>Publicaciones en Revistas</b>",
               'xanchor':'center',
               'x':0.5,
               'yanchor':'top'},
               font=dict(size=12))
    return fig_pie

def pie_editorial_element(data): #solo para elementos con columna "editorial" existente, se filtra a top 30 si hay mas
    if data['editorial'].value_counts().shape[0]>30:
        data_aux=data['editorial'].value_counts().iloc[:30]
    else:
        data_aux=data['editorial'].value_counts()
    fig_pie = px.pie(data_aux, values=data_aux, 
                     names=data_aux.index, color_discrete_sequence=px.colors.cyclical.Edge,
                     hole=.3)
    fig_pie.update_layout(title={
               'text':"<b>Publicaciones por Editoriales</b>",
               'xanchor':'center',
               'x':0.5,
               'yanchor':'top'},
               font=dict(size=12))
    return fig_pie

#GRUPLAC GENERAL: TODOS LOS PRODUCTOS


#GRUPLAC GENERAL: ELEMENTO


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
        dcc.Tab(label='General', value='tab_general'),
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
        html.Button('Filtrar1', id='button_group_filter_indiv', n_clicks=0),
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
        html.Button('Filtrar2', id='button_group_filter_group', n_clicks=0),
    ],id="filtro_grupal",style={}),        
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
        option_elements.append('Todos')
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

@callback(
    [
    Output('indicators_group','children'),Output('products_element_group','chilren'),
    Output('url_group_grouplac','href'),Output('group_minciencias','href'),
    Output('kpi-1','children'),Output('kpi-2','children'),Output('kpi-3','children'),Output('kpi-4','children'),Output('kpi-5','children'),
    Output('dash_individual_graph1','figure'),Output('div_group_figure1','style')
    ]
 )
def callback_filter():
    pass