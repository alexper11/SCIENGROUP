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
from functions.csv_importer import gruplac_basico, scopus_productos, scopus_autores, elementos_scopus_lista, fuente_dic, referencias, caracteristicas, caracteristicas_invertido, pmin, pmax, productos_ano, opciones_parametro_general

# Plotly
import plotly.express as px
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots


opciones_grupo_scopus=[]
scopus_productos['nombre_grupo'].dropna().str.split(';').apply(lambda x: opciones_grupo_scopus.extend(x)) #variable para opciones del filtro de grupo
opciones_grupo_scopus=list(map(str.strip, list(set(opciones_grupo_scopus))))

elementos_scopus_general=elementos_scopus_lista
options_general_element_scopus=elementos_scopus_general[:]
options_general_element_scopus.append('Todos')

#######################################
#FUNCIONES DE FILTRADO
########################################
#INDICADORES
def get_codigo_grupo(nombre):
    codigo=gruplac_basico[gruplac_basico['nombre']==nombre]['idgruplac'].iloc[0]
    return codigo

def citation_output(idgruplac):
    scopus_productos_aux=scopus_productos.dropna(subset='idgruplac').copy()
    mean=scopus_productos_aux[scopus_productos_aux['idgruplac'].str.contains(idgruplac)]['citado'].mean()
    return round(mean,2)

def citation_output_relativo(idgruplac,elemento):
    scopus_productos_aux=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac').copy()
    mean=scopus_productos_aux[scopus_productos_aux['idgruplac'].str.contains(idgruplac)]['citado'].astype('int64').mean()
    return round(mean,2)

def citation_count(idgruplac):
    scopus_productos_aux=scopus_productos.dropna(subset='idgruplac').copy()
    count=scopus_productos_aux[scopus_productos_aux['idgruplac'].str.contains(idgruplac)]['citado'].sum()
    return count

def citation_count_relativo(idgruplac,elemento):
    scopus_productos_aux=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac').copy()
    #scopus_productos_aux=scopus_productos_aux.astype(scopus_productos[scopus_productos_aux.columns.to_list()].dtypes.to_dict())
    count=scopus_productos_aux[scopus_productos_aux['idgruplac'].str.contains(idgruplac)]['citado'].astype('int64').sum()
    return count

def products_count(idgruplac):
    scopus_productos_aux=scopus_productos.dropna(subset='idgruplac').copy()
    count=scopus_productos_aux[scopus_productos_aux['idgruplac'].str.contains(idgruplac)]['idgruplac'].count()
    return count

def products_count_relativo(idgruplac, elemento):
    scopus_productos_aux=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac').copy()
    count=scopus_productos_aux[scopus_productos_aux['idgruplac'].str.contains(idgruplac)]['idgruplac'].count()
    return count

def authors_count(idgruplac):
    scopus_autores_aux=scopus_autores.dropna(subset='idgruplac')
    count=scopus_autores_aux[scopus_autores_aux['idgruplac'].str.contains(idgruplac)]['idgruplac'].count()
    return count

def get_h1_index(idgruplac):
    scopus_productos_aux=scopus_productos.dropna(subset='idgruplac').copy()
    scopus_productos_aux=sorted(scopus_productos_aux[scopus_productos_aux['idgruplac'].str.contains(idgruplac)]['citado'].astype('int64').to_list(),reverse=True)
    if len(scopus_productos_aux)==0:
        return 0
    else:
        for idx, item in enumerate(scopus_productos_aux, 1):
            if item < idx:
                break
        return idx - 1
    
def get_h1_index_relativo(idgruplac,elemento):
    scopus_productos_aux=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac').copy()
    scopus_productos_aux=sorted(scopus_productos_aux[scopus_productos_aux['idgruplac'].str.contains(idgruplac)]['citado'].astype('int64').to_list(),reverse=True)
    if len(scopus_productos_aux)==0:
        return 0
    else:
        for idx, item in enumerate(scopus_productos_aux, 1):
            if item < idx:
                break
        return idx - 1

def get_h2_index(idgruplac):
    scopus_autores_aux=scopus_autores.dropna(subset='idgruplac')
    scopus_autores_aux=sorted(scopus_autores_aux[scopus_autores_aux['idgruplac'].str.contains(idgruplac)]['h_index'].astype('int64').to_list(),reverse=True)
    if len(scopus_autores_aux)==0:
        return 0
    else:
        for idx, item in enumerate(scopus_autores_aux, 1):
            if item < idx:
                break
        return idx - 1

def get_series_scopus(idgruplac,elemento='Todos'):
    serie_fechas=pd.Series([],dtype='float64')
    serie_fechas= pd.concat([serie_fechas,pd.to_datetime(pd.Series([pmax]),format='%Y').dt.to_period('m')])
    
    data=scopus_productos.dropna(subset='idgruplac').copy()
    if elemento!='Todos':
        data=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac').copy()
    data['fecha_publicacion']=pd.to_datetime(data.fecha_publicacion, format='%Y-%m').dt.to_period('m')
    serie_fechas= pd.concat([serie_fechas,data[data['idgruplac'].str.contains(idgruplac)]['fecha_publicacion'].dropna()])
    #serie_fechas= pd.concat([serie_fechas,gruplac_basico[gruplac_basico['idgruplac']==idgruplac]['fecha_formacion'].dropna().dt.year])
    serie_fechas=serie_fechas.astype('object')
    serie_fechas=serie_fechas.value_counts().sort_index().astype('float64')
    #serie_fechas.iloc[0]=serie_fechas.iloc[0]-1 #fecha_formación
    serie_fechas.iloc[-1]=serie_fechas.iloc[-1]-1
    serie_fechas.index=serie_fechas.index.to_timestamp().to_period('m')
    serie_fechas=serie_fechas.reindex(pd.period_range(start=min(serie_fechas.index),end=max(serie_fechas.index)).to_list(),fill_value=0)
    return serie_fechas

def get_indicadores_scopus_general(grupos):
    #PARA OBTENER UN DATAFRAME CON LOS INDICADORES DE TODOS LOS GRUPOS EN SCOPUS
    dic={'idgruplac':[],'cit_output':[],'citations':[],'h1_index':[],'h2_index':[],'PC':[]}
    list_series=[]
    for grup in grupos:
        dic['idgruplac'].append(grup)
        dic['cit_output'].append(citation_output(grup))
        dic['citations'].append(citation_count(grup))
        dic['h1_index'].append(get_h1_index(grup))
        dic['h2_index'].append(get_h2_index(grup))
        dic['PC'].append(products_count(grup))
        list_series.append(get_series_scopus(grup))
    indicadores_grupos_scopus= pd.DataFrame.from_dict(dic).sort_values(by='h2_index',ascending=False)
    return indicadores_grupos_scopus, list_series

def get_indicadores_scopus_relativo(grupos,elemento):
    #PARA OBTENER UN DATAFRAME CON LOS INDICADORES DE TODOS LOS GRUPOS EN SCOPUS
    dic={'idgruplac':[],'cit_output':[],'citations':[],'h1_index':[],'PC':[]}
    list_series=[]
    for grup in grupos:
        dic['idgruplac'].append(grup)
        dic['cit_output'].append(citation_output_relativo(grup,elemento))
        dic['citations'].append(citation_count_relativo(grup,elemento))
        dic['h1_index'].append(get_h1_index_relativo(grup,elemento))
        dic['PC'].append(products_count_relativo(grup,elemento))
        list_series.append(get_series_scopus(grup,elemento))
    indicadores_grupos_scopus= pd.DataFrame.from_dict(dic).sort_values(by='PC',ascending=False)
    return indicadores_grupos_scopus, list_series

#INDIVIDUAL

def filtro_scopus_grupo_individual(grupo):
    idgruplac=gruplac_basico[gruplac_basico['nombre']==grupo]['idgruplac'].iloc[0]
    opc_elementos=[]
    for elemento in elementos_scopus_lista:
        data=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac').copy()
        if data['idgruplac'].str.contains(idgruplac).shape[0] >= 1:
            opc_elementos.append(elemento)
    # data=pd.DataFrame()
    return opc_elementos

def filtro_scopus_elemento_individual(grupo,elemento):
    idgruplac=gruplac_basico[gruplac_basico['nombre']==grupo]['idgruplac'].iloc[0]
    if elemento=='Todos':
        data=scopus_productos.dropna(subset='idgruplac').copy()
        data=data[data['idgruplac'].str.contains(idgruplac)]#.astype(globals()[str(referencias['SCOPUS'][elemento])][data.columns.to_list()].dtypes.to_dict())
    else:
        data=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac').copy()
        data=data[data['idgruplac'].str.contains(idgruplac)]#.astype(globals()[str(referencias['SCOPUS'][elemento])][data.columns.to_list()].dtypes.to_dict())
    return data
    
#GENERAL
def filtro_scopus_parametro_general(parametro):
    if parametro=='Ingreso Manual':
        opc_valor_general=opciones_grupo_scopus
    
    elif parametro=='Clasificación':
        opc_valor_general=gruplac_basico['clasificacion'].drop_duplicates(keep='first').to_list()
        
        
    elif parametro=='Institución':
        data=fuente_dic['GRUPLAC']['Institución'].copy()
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
        data=fuente_dic['GRUPLAC']['Institución'].copy()
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
    data=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac').copy()
    data_aux=data.copy()
    data_aux['id']=data_aux.index
    indexes=[]
    data_aux[['id','idgruplac']].dropna(subset='idgruplac').apply(lambda x: indexes.append(x['id']) if len(set(x['idgruplac'].split(';')).intersection(set(idgruplacs)))>=1 else None,axis=1)
    data=data.loc[indexes].astype(globals()[str(referencias['SCOPUS'][elemento])][data.columns.to_list()].dtypes.to_dict())
    return data

########## graficas
def time_series_all_scopus(series, elemento='Todos'):
    series=series.to_frame().reset_index()
    series.columns=['fecha','productos']
    #series['fecha']=series['fecha'].dt.to_timestamp(freq='M')
    series['fecha']=series['fecha'].dt.strftime('%Y-%m') 
    if elemento=='Todos':
        title_label="<b>Productos Anuales Generados: Todos</b>"
        axis_label="Conteo de Productos"
    else:
        title_label="<b>Productos Anuales Generados: "+elemento+"</b>"
        axis_label="Conteo de "+elemento
    fig = px.line(series, x='fecha', y="productos", 
                  labels={
                      "fecha":"Años",
                      "productos":axis_label})
    fig.update_layout(title={
                  'text':title_label,
                  #'xanchor':'center',
                  #'x':0.5,
                  #'yanchor':'top'
                  },
                  font=dict(size=12))
    fig.update_traces(line_color='#0000ff', line_width=2)
    return fig

def get_fig_title(fig):
    #fig.update_layout(title={'text':None})
    return fig['layout']['title']['text']

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

@callback(
    [
    Output('kpi_all_scopus','style'),
    Output('indicators_group_scopus','children'),Output('products_element_group_scopus','children'),
    Output('kpi_scopus_1','children'),Output('kpi_scopus_2','children'),Output('kpi_scopus_3','children'),Output('kpi_scopus_4','children'),Output('kpi_scopus_5','children'),Output('kpi_scopus_6','children'),
    Output('dash_individual_scopus_graph1','figure'),Output('div_group_scopus_figure1','style'),
    Output('dash_individual_scopus_graph2','figure'),Output('div_group_scopus_figure2','style'),
    Output('dash_individual_scopus_graph3','figure'),Output('div_group_scopus_figure3','style'),
    Output('dash_individual_scopus_graph4','figure'),Output('div_group_scopus_figure4','style'),
    #titulo
    Output('title_individual_scopus_graph1','children'),
    Output('title_individual_scopus_graph2','children'),
    Output('title_individual_scopus_graph3','children'),
    Output('title_individual_scopus_graph4','children'),
    #
    Output('msj_alert_individual_scopus','children'),Output('fade-alert-individual-scopus','is_open'),
    ],
    [State('filter_group_scopus', 'value'), State('filter_element_scopus', 'value'),
    Input('button_scopus_filter_indiv','n_clicks')]
 )
def callback_filter_individual_scopus(grupo, elemento, boton):
    kpi_all_scopus = {'display':'none'}
    indicators_group_scopus = ''
    products_element_group_scopus = ''    
    kpi_scopus1 = ''
    kpi_scopus2 = ''
    kpi_scopus3 = ''
    kpi_scopus4 = ''
    kpi_scopus5 = ''
    kpi_scopus6 = ''
    dash_individual_scopus_graph1 = {}
    dash_individual_scopus_graph2 = {}
    dash_individual_scopus_graph3 = {}
    dash_individual_scopus_graph4 = {}
    div_scopus_figure1 = {'display':'none'}
    div_scopus_figure2 = {'display':'none'}
    div_scopus_figure3 = {'display':'none'}#,'width':'47%'}
    div_scopus_figure4 = {'display':'none'}
    titulo_individual_scopus1=''
    titulo_individual_scopus2=''
    titulo_individual_scopus3=''
    titulo_individual_scopus4=''    
    msj_alert_individual_scopus = ''
    fade_alert_individual_scopus = False

    if boton == 0 or elemento == None:
        return kpi_all_scopus, indicators_group_scopus, products_element_group_scopus, kpi_scopus1, kpi_scopus2, kpi_scopus3, kpi_scopus4, kpi_scopus5, kpi_scopus6, dash_individual_scopus_graph1, div_scopus_figure1, dash_individual_scopus_graph2, div_scopus_figure2, dash_individual_scopus_graph3, div_scopus_figure3, dash_individual_scopus_graph4, div_scopus_figure4, titulo_individual_scopus1, titulo_individual_scopus2, titulo_individual_scopus3, titulo_individual_scopus4, msj_alert_individual_scopus, fade_alert_individual_scopus
    
    kpi_all_scopus = {'display':'block','width':'80vw', 'margin-left':'auto', 'margin-right':'auto'}
    #indicadores    
    grupo_cod_scopus=get_codigo_grupo(grupo)    
    indicators_group_scopus = 'Grupo: '+grupo
    products_element_group_scopus ='Indicadores analizados para: '+elemento

    if elemento == 'Todos':
        print('codigo grupo:',grupo_cod_scopus)
        series_scopus=get_series_scopus(grupo_cod_scopus)
        print(series_scopus)             
        kpi_scopus1 = str(get_h1_index(grupo_cod_scopus))
        kpi_scopus2 = str(get_h2_index(grupo_cod_scopus))
        kpi_scopus3 = str(authors_count(grupo_cod_scopus))
        kpi_scopus4 = str(products_count(grupo_cod_scopus))
        kpi_scopus5 = str(citation_count(grupo_cod_scopus))  
        kpi_scopus6 = str(citation_output(grupo_cod_scopus) )     
        dash_individual_scopus_graph1 = time_series_all_scopus(series_scopus) #Grafica_hacer
        titulo_individual_scopus1 = get_fig_title(dash_individual_scopus_graph1)
        dash_individual_scopus_graph1.update_layout(title={'text':None})
        dash_individual_scopus_graph2 = {} #Grafica_hacer
        dash_individual_scopus_graph3 = {} #Grafica_hacer
        #titulo_individual_scopus2 = get_fig_title(dash_individual_scopus_graph2)
        #dash_individual_scopus_graph2.update_layout(title={'text':None})
        #titulo_individual_scopus3 = get_fig_title(dash_individual_scopus_graph3)
        #dash_individual_scopus_graph3.update_layout(title={'text':None})
        div_scopus_figure1 = {'display':'block', 'height':'70vh', 'max-height':'75vh','margin-top':'5px','padding-top':'5px','margin-left':'auto','margin-right':'auto','max-width':'80vw', 'margin-bottom':'7px'}
        div_scopus_figure2 = {'display':'inline-block', 'height':'70vh','max-height':'75vh', 'margin-bottom':'5vh','padding-bottom':'5px', 'margin-top':'7px','padding-top':'5px'}
        div_scopus_figure3 = {'display':'inline-block','height':'70vh', 'max-height':'75vh','margin-bottom':'5vh','padding-bottom':'5px', 'margin-top':'7px','padding-top':'5px'}
    else:
        series_scopus=get_series_scopus(grupo_cod_scopus,elemento) #OBTIENE LA SERIE RELATIVA AL ELEMENTO
        kpi_scopus1 = str(get_h1_index_relativo(grupo_cod_scopus,elemento))
        kpi_scopus2 = str(get_h2_index(grupo_cod_scopus))
        kpi_scopus3 = str(authors_count(grupo_cod_scopus))
        kpi_scopus4 = str(products_count_relativo(grupo_cod_scopus,elemento))
        kpi_scopus5 = str(citation_count_relativo(grupo_cod_scopus,elemento))
        kpi_scopus6 = str(citation_output_relativo(grupo_cod_scopus,elemento))
        dash_individual_scopus_graph1 = {} #Grafica_hacer
        #titulo_individual_scopus1 = get_fig_title(dash_individual_scopus_graph1)
        #dash_individual_scopus_graph1.update_layout(title={'text':None})
        div_scopus_figure1 = {'display':'block', 'height':'70vh', 'max-height':'80vh','margin-top':'5px','padding-top':'5px','margin-left':'auto','margin-right':'auto','max-width':'80vw', 'margin-bottom':'7px'}
        data = filtro_scopus_elemento_individual(grupo,elemento)
        if data.shape[0]==0:
            msj_alert_individual_scopus = 'No existen datos'
            fade_alert_individual_scopus = True
            return kpi_all_scopus, indicators_group_scopus, products_element_group_scopus, kpi_scopus1, kpi_scopus2, kpi_scopus3, kpi_scopus4, kpi_scopus5, kpi_scopus6, dash_individual_scopus_graph1, div_scopus_figure1, dash_individual_scopus_graph2, div_scopus_figure2, dash_individual_scopus_graph3, div_scopus_figure3, dash_individual_scopus_graph4, div_scopus_figure4, titulo_individual_scopus1, titulo_individual_scopus2, titulo_individual_scopus3, titulo_individual_scopus4, msj_alert_individual_scopus, fade_alert_individual_scopus
    
        if ('revista' in data) and ('tipo' in data):
            dash_individual_scopus_graph2 = {} #Grafica_hacer
            #titulo_individual_scopus2 = get_fig_title(dash_individual_scopus_graph2)
            #dash_individual_scopus_graph2.update_layout(title={'text':None})
            dash_individual_scopus_graph3 = {} #Grafica_hacer
            #titulo_individual_scopus3 = get_fig_title(dash_individual_scopus_graph3)
            #dash_individual_scopus_graph3.update_layout(title={'text':None})
            div_scopus_figure2 = {'display':'inline-block', 'height':'70vh','max-height':'75vh', 'margin-bottom':'5px','padding-bottom':'5px', 'margin-top':'7px'}
            div_scopus_figure3 = {'display':'inline-block', 'height':'70vh','max-height':'75vh', 'margin-bottom':'5px','padding-bottom':'5px', 'margin-top':'7px'}
        elif ('editorial' in data) and ('tipo' in data):
            dash_individual_scopus_graph2 = {} #Grafica_hacer
            #titulo_individual_scopus2 = get_fig_title(dash_individual_scopus_graph2)
            #dash_individual_scopus_graph2.update_layout(title={'text':None})
            dash_individual_scopus_graph3 = {} #Grafica_hacer
            #titulo_individual_scopus3 = get_fig_title(dash_individual_scopus_graph3)
            #dash_individual_scopus_graph3.update_layout(title={'text':None})
            div_scopus_figure2 = {'display':'inline-block', 'height':'50vh','max-height':'65vh', 'margin-bottom':'5px','padding-bottom':'5px', 'margin-top':'7px'}
            div_scopus_figure3 = {'display':'inline-block', 'height':'50vh','max-height':'65vh', 'margin-bottom':'5px','padding-bottom':'5px', 'margin-top':'7px'}
        elif ((('revista' in data) and ('editorial' in data)) != True) and ('tipo' in data):
            dash_individual_scopus_graph3 = {} #Grafica_hacer
            #titulo_individual_scopus3 = get_fig_title(dash_individual_scopus_graph3)
            #dash_individual_scopus_graph3.update_layout(title={'text':None})
            div_scopus_figure3 = {'display':'inline-block', 'height':'63vh','max-height':'65vh', 'margin-bottom':'5px','padding-bottom':'5px', 'margin-left':'30vw', 'margin-right':'30vw','width':'40vw','margin-top':'7px'}
        if 'autores' in data:
            dash_individual_scopus_graph4 = {} #Grafica_hacer  
            #titulo_individual_scopus4 = get_fig_title(dash_individual_scopus_graph4)
            #dash_individual_scopus_graph4.update_layout(title={'text':None})      
            div_scopus_figure4 = {'display':'block','height':'80vh','max-height':'83vh','margin-bottom':'5vh','margin-top':'7px','padding-top':'5px'}

    return kpi_all_scopus, indicators_group_scopus, products_element_group_scopus, kpi_scopus1, kpi_scopus2, kpi_scopus3, kpi_scopus4, kpi_scopus5, kpi_scopus6, dash_individual_scopus_graph1, div_scopus_figure1, dash_individual_scopus_graph2, div_scopus_figure2, dash_individual_scopus_graph3, div_scopus_figure3, dash_individual_scopus_graph4, div_scopus_figure4, titulo_individual_scopus1, titulo_individual_scopus2, titulo_individual_scopus3, titulo_individual_scopus4, msj_alert_individual_scopus, fade_alert_individual_scopus