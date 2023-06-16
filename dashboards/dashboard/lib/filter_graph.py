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
from functions.csv_importer import gruplac_basico, gruplac_integrantes, elementos_gruplac_individual, fuente_dic, referencias, caracteristicas, caracteristicas_invertido, pmin, pmax, productos_ano, opciones_grupo, opciones_parametro_general

# Plotly
import plotly.express as px
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots

elementos_gruplac_general=elementos_gruplac_individual
options_general_element=elementos_gruplac_general[:]
options_general_element.append('Todos')
#################################################################
#Funciones de filtros
############################################################
def filtro_gruplac_grupo_individual(grupo): #retorna opciones de elemento
    idgruplac=gruplac_basico[gruplac_basico['nombre']==grupo]['idgruplac'].iloc[0]
    opc_elementos=[]
    for elementox in elementos_gruplac_individual:
        data=fuente_dic['GRUPLAC'][elementox].dropna(subset='idgruplac').copy()
        if idgruplac in data['idgruplac'].values:
            opc_elementos.append(elementox)
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

#PARA OBTENER UN DATAFRAME CON LOS INDICADORES DE TODOS LOS GRUPOS EN TODOS LOS ELEMENTOS O PRODUCTOS
def get_indicadores_gruplac_general(grupos):
    dic={'idgruplac':[],'consistencia':[],'ppa':[],'ppua':[],'pg':[]}
    list_series=[]
    for grupo in grupos:
        consistency,apy,pdly,pc,x =get_indicadores(grupo)
        dic['idgruplac'].append(grupo)
        dic['consistencia'].append(consistency)
        dic['ppa'].append(apy)
        dic['ppua'].append(pdly)
        dic['pg'].append(pc)
        list_series.append(x)
    indicadores_grupos_general= pd.DataFrame.from_dict(dic)
    return indicadores_grupos_general, list_series

#PARA OBTENER UN DATAFRAME CON LOS INDICADORES DE TODOS LOS GRUPOS EN UN ELEMENTO RELATIVO
def get_indicadores_gruplac_relativo(grupos,elemento):
    dic={'idgruplac':[],'consistencia':[],'ppa':[],'ppua':[],'pg':[]}
    list_series=[]
    for grupo in grupos:
        consistency,apy,pdly,pc,x =get_indicadores_relativos(grupo,elemento)
        dic['idgruplac'].append(grupo)
        dic['consistencia'].append(consistency)
        dic['ppa'].append(apy)
        dic['ppua'].append(pdly)
        dic['pg'].append(pc)
        list_series.append(x)
    indicadores_grupos_relativo= pd.DataFrame.from_dict(dic)
    return indicadores_grupos_relativo, list_series
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
                  font=dict(size=12),
                  height=500)
    fig.update_traces(line_color='#0000ff', line_width=2)
    return fig

def bar_pie_all(grupo): #retorna dos graficas, recibe codigo de grupo
    dic={'producto':[],'count':[]}
    for key in list(set(fuente_dic['GRUPLAC'].keys())-set(['Institución','Líneas de Investigación','Datos Básicos'])):
        data=fuente_dic['GRUPLAC'][key]
        dic['count'].append(data[data['idgruplac']==grupo]['idgruplac'].count())
        dic['producto'].append(key)
    df=pd.DataFrame.from_dict(dic)
    df['producto']=df['producto'].str.wrap(15,break_long_words=False).str.replace('\n','<br>')
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
                height= 450, 
               font=dict(size=10))
    fig.update_layout(xaxis = dict(tickfont = dict(size=11)))
    fig_bar=fig
    if df['producto'].nunique()>8:
        fig_bar.update_xaxes(tickangle=90)
        
    fig_pie = px.pie(df, values='count', names='producto', color_discrete_sequence=px.colors.sequential.Aggrnyl,
                     hole=.3)
    fig_pie.update_layout(title={
               'text':"<b>Porcentaje de Productos</b>",
               'xanchor':'center',
               'x':0.5,
               'yanchor':'top'},
                height= 450,
               font=dict(size=10))
    fig_pie.update_layout( legend = {"xanchor": "left"})
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
                  font=dict(size=12),
                  #height=600,
                  )
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
    dataset_autores['autores']=dataset_autores['autores'].str.wrap(15,break_long_words=False).str.replace('\n','<br>')
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
                      font=dict(size=13))
    fig.update_layout(uniformtext=dict(minsize=16))
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
    title_label="<b>Publicaciones por Tipo</b>"
    if data.shape[0]==0:
        title_label="<b>No Hay Datos Disponibles</b>"
    data['tipo']=data['tipo'].str.wrap(15,break_long_words=False).str.replace('\n','<br>')
    fig_pie = px.pie(data, values=data['tipo'].value_counts(), 
                     names=data['tipo'].value_counts().index, color_discrete_sequence=px.colors.qualitative.Dark2,
                     hole=.3)
    fig_pie.update_layout(title={
               'text':title_label,
               'xanchor':'center',
               'x':0.5,
               'yanchor':'top',
               'automargin':True},
               font=dict(size=12))
    #fig_pie.update_layout( legend = {"xanchor": "right", "x": 1.08})
    return fig_pie

def pie_journal_element(datain): #solo para elementos con columna "revista" existente, se filtra a top 30 si hay mas
    data=datain.copy()
    data['revista']=data['revista'].str.wrap(20,break_long_words=False).str.replace('\n','<br>')
    print('pie_journal_element')
    if data['revista'].value_counts().shape[0]>30:
        data_aux=data['revista'].value_counts().iloc[:30]
        data_aux=data_aux.rename_axis('index').reset_index(name='values')
        data_aux['percents']=(data_aux['values']*100)/data_aux['values'].sum()
    else:
        data_aux=data['revista'].value_counts()
        data_aux=data_aux.rename_axis('index').reset_index(name='values')
        data_aux['percents']=data['revista'].value_counts(normalize=True).values*100
    
    fig_pie = px.pie(data_aux, values=data_aux['values'], 
                     names=data_aux['index'], color_discrete_sequence=px.colors.cyclical.Edge,
                     hole=.3, custom_data=['percents'])
    fig_pie.update_layout(title={
               'text':"<b>Publicaciones en Revistas</b>",
               'xanchor':'center',
               'x':0.5,
               'yanchor':'top'},
               font=dict(size=10))
    fig_pie.update_layout(legend=dict(
                orientation="v",
                xanchor="left",
                #x=0.02,
                #y=1.02,
                title='Revistas',
                font=dict(size=10),
                ))
    fig_pie.data[0].hovertemplate = '%{label}<br>'+'count'+':%{value}<br>%{customdata:.2f}%'
    fig_pie.update_traces(textposition='inside', textinfo='percent')
    return fig_pie

def pie_editorial_element(datain): #solo para elementos con columna "editorial" existente, se filtra a top 30 si hay mas
    data=datain.copy()
    data['editorial']=data['editorial'].str.wrap(20,break_long_words=False).str.replace('\n','<br>')
    if data['editorial'].value_counts().shape[0]>30:
        data_aux=data['editorial'].value_counts().iloc[:30]
        data_aux=data_aux.rename_axis('index').reset_index(name='values')
        data_aux['percents']=(data_aux['values']*100)/data_aux['values'].sum()
    else:
        data_aux=data['editorial'].value_counts()
        data_aux=data_aux.rename_axis('index').reset_index(name='values')
        data_aux['percents']=data['editorial'].value_counts(normalize=True).values*100
    fig_pie = px.pie(data_aux, values=data_aux['values'], 
                     names=data_aux['index'], color_discrete_sequence=px.colors.cyclical.Edge,
                     hole=.3,custom_data=['percents'])
    fig_pie.update_layout(title={
               'text':"<b>Publicaciones por Editoriales</b>",
               'xanchor':'center',
               'x':0.5,
               'yanchor':'top'},
               font=dict(size=12))
    fig_pie.update_layout(legend=dict(
                orientation="v",
                xanchor="left",
                #x=0.02,
                #y=1.02,
                title='Editoriales',
                font=dict(size=10),
                ))
    fig_pie.data[0].hovertemplate = '%{label}<br>'+'count'+':%{value}<br>%{customdata:.2f}%'
    fig_pie.update_traces(textposition='inside', textinfo='percent')
    return fig_pie

#GRUPLAC GENERAL: TODOS LOS PRODUCTOS
def time_series_all_general(series,grupos, elemento): #recibe time_series y grupos_nombres
    df=pd.DataFrame()
    if elemento=='Todos':
        title_label='<b>Productos Anuales Generados: Todos</b>'
    else:
        title_label='<b>Productos Anuales Generados: '+elemento+'</b>'
    for i,serie in enumerate(series):
        if i==0:
            df['fecha']=serie.index
            df[grupos[i]]=serie.values
        else:
            df_aux=pd.DataFrame(serie,columns=[grupos[i]])
            df_aux['fecha']=serie.index
            df=pd.merge(df, df_aux, on="fecha",how='outer').sort_values(by='fecha').fillna(0)
            df['fecha']=pd.to_datetime(df.fecha, format='%Y').dt.year
    fig = px.line(df, x="fecha", y=df.columns,
                  labels={
                          "fecha":"Años",
                          "value":'Cantidad de Productos'})
    fig.update_traces(line_width=1.5)
    fig.update_layout(
        title={
              'text':title_label,
              #'xanchor':'center',
              'xref':'paper',
              'x':0.5,
              'yanchor':'top',
              'automargin':True,
              },
        font=dict(size=12),
        margin=dict(t=1, b=1),
        legend=dict(
            orientation="h",
            y=1.02,
            yanchor="bottom",
            xanchor="left",
            x=0.01,
            title='Grupos',
            font=dict(size=11)),
        #height=650,
        )
    #fig.update_layout(height=600)#############
    return fig

def bar_general_all(codigos, nombres): #retorna dos graficas, recibe grupos_codigos y grupos_codigos
    df=pd.DataFrame(columns=['grupo','producto','count']).copy()
    for i,codigo in enumerate(codigos):
        dic={'grupo':[],'producto':[],'count':[]}
        for key in list(set(fuente_dic['GRUPLAC'].keys())-set(['Institución','Líneas de Investigación','Datos Básicos'])):
            data=fuente_dic['GRUPLAC'][key]
            dic['grupo'].append(nombres[i])
            dic['count'].append(data[data['idgruplac']==codigo]['idgruplac'].count())
            dic['producto'].append(key)
        df_aux=pd.DataFrame.from_dict(dic)
        df_aux=df_aux[df_aux['count']>0]
        df=pd.concat([df, df_aux], ignore_index=True)
    if df['grupo'].nunique()>1:
        df['grupo']=df['grupo'].str.wrap(20,break_long_words=False).str.replace('\n','<br>')
    fig = px.bar(df, x="grupo", y="count", color='producto',
                 labels={
                 "grupo":"Grupo de Investigación",
                 "count":"Cantidad de Productos"},color_discrete_sequence=px.colors.sequential.Viridis)#paleta de colores
    fig.update_layout(
                legend=dict(
                orientation="h",
                x=0.02,
                y=1.02,
                yanchor="bottom",
                xanchor="left",
                title='Productos',
                font=dict(size=10),
                #legend_itemclick="toggleothers",
                #legend_itemdoubleclick="toggle",
                #
                ),
                title={
                'text':"<b>Productos Generados por los Grupos de Investigación</b>",
                #'xanchor':'center',
                'x':0.5,
                #'xref':'paper',
                'yanchor':'top',
                'automargin':True,
                'font': {'size': 15},
                },
                yaxis={'categoryorder': 'total ascending'},
                font=dict(size=10),
                margin=dict(t=2, b=2),
                #height=650
                )
    if df['grupo'].nunique()>1:
        fig.update_xaxes(tickangle=90)
    #fig.update_layout(legend_x=0.02, legend_y=1.02)
    #fig.update_yaxes(automargin=True)
    #fig.update_traces(visible='legendonly')
    fig.update_layout(xaxis = dict(tickfont = dict(size=11)))
    return fig

def bar_consistencia(indicadores,grupos, elemento): #recibe df_indicadores y grupos_nombres
    df=indicadores.rename(columns={'idgruplac':'gruplac'}).copy()
    if elemento=='Todos':
        title_label="<b>Indicador de Consistencia para Todos los Productos</b>"
    else:
        title_label="<b>Indicador de Consistencia para "+elemento+"</b>"
    df['gruplac']=grupos
    locs=df[df['gruplac'].str.len()>65].index.tolist()
    locs_df=df['gruplac'].loc[locs].copy()
    df.loc[locs,'gruplac']=locs_df.str.slice(stop=65)+'...'
    
    categories_con=[]
    for i,name in enumerate(df['gruplac'].to_list()):
        categories_con.append({"name":name,"value":float(df['consistencia'].iloc[i])})
        
    fig_con = go.Figure(
        data=[go.Bar(
            x=[d.get('value') for d in categories_con], 
            y=[d.get('name') for d in categories_con],
            orientation='h',
            texttemplate="%{x:}",
            hovertemplate="%{x},%{y}<extra></extra>",
        ),
        go.Bar(
            x=[0] * len(categories_con), 
            y=[d.get('name') for d in categories_con],
            orientation='h',
            texttemplate="%{y}",
            textposition="outside"
        )],
        layout={
            'barmode': 'group',
            #'autosize':True,
            'height': 550,
            #'width':650,
            'yaxis':{'visible': False},
            'showlegend': False,
            'title':title_label
        }
    )
    fig_con.update_layout(
        title={
            #'y':0.8,
            'xref':'paper',#################
            'x':0.5,
            #'xanchor': 'center',
            #'yanchor': 'bottom',
            'font':{'size':12}},
        #font_size=14,
        )
    
    return fig_con

def bar_ppa(indicadores,grupos, elemento):  #recibe df_indicadores y grupos_nombres
    df=indicadores.rename(columns={'idgruplac':'gruplac'})
    if elemento=='Todos':
        title_label="<b>PPA Promedio de Productos por Año (Todos)</b>"
    else:
        title_label="<b>PPA Promedio de Productos por Año ("+elemento+")</b>"
    df['gruplac']=grupos
    
    locs=df[df['gruplac'].str.len()>65].index.tolist()
    locs_df=df['gruplac'].loc[locs].copy()
    df.loc[locs,'gruplac']=locs_df.str.slice(stop=65)+'...'
    
    
    categories_ppa=[]
    for i,name in enumerate(df['gruplac'].to_list()):
        categories_ppa.append({"name":name,"value":float(df['ppa'].iloc[i])})
    fig_ppa = go.Figure(
        data=[go.Bar(
            x=[d.get('value') for d in categories_ppa], 
            y=[d.get('name') for d in categories_ppa],
            orientation='h',
            texttemplate="%{x:}",
            hovertemplate="%{x},%{y}<extra></extra>"
        ),
        go.Bar(
            x=[0] * len(categories_ppa), 
            y=[d.get('name') for d in categories_ppa],
            orientation='h',
            texttemplate="%{y}",
            textposition="outside",

        )],
        layout={
            'barmode': 'group',
            #'autosize':True,
            'height': 550,
            #'width':650,
            'yaxis':{'visible': False},
            'showlegend': False,
            'title':title_label
        }
    )
    fig_ppa.update_layout(
        title={
            #'y':0.8,
            'xref':'paper',
            'x':0.5,
            #'xanchor': 'center',
            #'yanchor': 'bottom',
            'font':{'size':12}},
        #font_size=14,
        )
    fig_ppa.data[0].marker.color='orangered'

    return fig_ppa

def bar_ppua(indicadores,grupos, elemento):  #recibe df_indicadores y grupos_nombres
    df=indicadores.rename(columns={'idgruplac':'gruplac'})
    if elemento=='Todos':
        title_label="<b>PPUA Porcentaje de Productos en <br> los Ultimos Años (Todos)</b>"
    else:
        title_label="<b>PPUA Porcentaje de Productos en <br> los Ultimos Años ("+elemento+")</b>"
    df['gruplac']=grupos
    locs=df[df['gruplac'].str.len()>65].index.tolist()
    locs_df=df['gruplac'].loc[locs].copy()
    df.loc[locs,'gruplac']=locs_df.str.slice(stop=65)+'...'
    
    
    categories_ppua=[]
    for i,name in enumerate(df['gruplac'].to_list()):
        categories_ppua.append({"name":name,"value":float(df['ppua'].iloc[i])})
    fig_ppua = go.Figure(
        data=[go.Bar(
            x=[d.get('value') for d in categories_ppua], 
            y=[d.get('name') for d in categories_ppua],
            orientation='h',
            texttemplate="%{x}%",
            hovertemplate="%{x}%,%{y}<extra></extra>"
        ),
        go.Bar(
            x=[0] * len(categories_ppua), 
            y=[d.get('name') for d in categories_ppua],
            orientation='h',
            texttemplate="%{y}",
            textposition="outside",

        )],
        layout={
            'barmode': 'group',
            #'autosize':True,
            'height': 550,
            #'width':650,
            'yaxis':{'visible': False},
            'showlegend': False,
            'title':title_label
        }
    )
    fig_ppua.update_layout(
        title={
            #'y':0.8,
            'xref':'paper',
            'x':0,
            #'xanchor': 'center',
            #'yanchor': 'bottom',
            'font':{'size':12}},
        #font_size=14,
        )
    fig_ppua.data[0].marker.color='purple'

    return fig_ppua

def bar_pg(indicadores,grupos, elemento):  #recibe df_indicadores y grupos_nombres
    df=indicadores.rename(columns={'idgruplac':'gruplac'})
    if elemento=='Todos':
        title_label="<b>PG Productos Generados (Todos)</b>"
    else:
        title_label="<b>PG Productos Generados ("+elemento+")</b>"
    df['gruplac']=grupos
    locs=df[df['gruplac'].str.len()>65].index.tolist()
    locs_df=df['gruplac'].loc[locs].copy()
    df.loc[locs,'gruplac']=locs_df.str.slice(stop=65)+'...'
    
    
    categories_pg=[]
    for i,name in enumerate(df['gruplac'].to_list()):
        categories_pg.append({"name":name,"value":float(df['pg'].iloc[i])})
    fig_pg = go.Figure(
        data=[go.Bar(
            x=[d.get('value') for d in categories_pg], 
            y=[d.get('name') for d in categories_pg],
            orientation='h',
            texttemplate="%{x}",
            hovertemplate="%{x},%{y}<extra></extra>"
        ),
        go.Bar(
            x=[0] * len(categories_pg), 
            y=[d.get('name') for d in categories_pg],
            orientation='h',
            texttemplate="%{y}",
            textposition="outside",

        )],
        layout={
            'barmode': 'group',
            #'autosize':True,
            'height': 550,
            #'width':650,
            'yaxis':{'visible': False},
            'showlegend': False,
            'title':title_label
        }
    )
    fig_pg.update_layout(
        title={
            #'y':0.8,
            'xref':'paper',
            'x':0,
            #'xanchor': 'center',
            #'yanchor': 'bottom',
            'font':{'size':12}},
        #font_size=14,
        )
    fig_pg.data[0].marker.color='green'

    return fig_pg

#GRUPLAC GENERAL: ELEMENTO
def bar_general_element(data, elemento): #retorna dos graficas, recibe grupos_codigos y grupos_codigos
    df=data.rename(columns={'idgruplac':'grupo'}).copy()
    df['grupo']=df['grupo'].apply(lambda x: gruplac_basico[gruplac_basico['idgruplac']==x]['nombre'].iloc[0])
    if df['grupo'].nunique()>1:
        df['grupo']=df['grupo'].str.wrap(20,break_long_words=False).str.replace('\n','<br>')
    temp_df=df.copy()
    df=df['grupo'].value_counts()    

    fig = px.bar(df, x=df.index, y=df, color=df.index,
                 labels={
                 "index":"Grupo de Investigación",
                 "y":"Cantidad de Productos"},
                 orientation='v',color_discrete_sequence=px.colors.sequential.thermal)#paleta de colores
    fig.update_layout(
                font=dict(size=10),
                title={
                'text':"<b>Productos Generados por los Grupos de Investigación: "+elemento+"</b>",
                #'xanchor':'center',
                #'xref':'paper',
                #'x':0.5,
                'yanchor':'top',
                'automargin':True,
                'font': {'size': 14}},
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(t=10, b=2))
    fig.update(layout_showlegend=False)
    if temp_df['grupo'].nunique()>3:
        fig.update_xaxes(tickangle=90)
    #fig.update_layout(height='600')##############
    #fig.update_yaxes(automargin=True)
    #fig.update_xaxes(tickangle=0)
    fig.update_layout(xaxis = dict(tickfont = dict(size=11)))
    return fig

def pie_journal_element_general(datain,condition): #recibe dataset filtrado y ocndicion 'editorial' o 'revista'
    data=datain.copy()
    data[condition]=data[condition].str.wrap(20,break_long_words=False).str.replace('\n','<br>')
    if condition=='editorial':
        title_label="<b>Publicaciones por Editoriales</b>"
    else:
        title_label="<b>Publicaciones en Revistas</b>"
    print('pie_journal_element_general')
    if data[condition].value_counts().shape[0]>30:
        data_aux=data[condition].value_counts().iloc[:30]
        data_aux=data_aux.rename_axis('index').reset_index(name='values')
        data_aux['percents']=(data_aux['values']*100)/data_aux['values'].sum()
    else:
        data_aux=data[condition].value_counts()
        data_aux=data_aux.rename_axis('index').reset_index(name='values')
        data_aux['percents']=data[condition].value_counts(normalize=True).values*100
            
    fig_pie = px.pie(data_aux, values=data_aux['values'], 
                     names=data_aux['index'], color_discrete_sequence=px.colors.cyclical.Edge,
                     hole=.3, custom_data=['percents'])

    fig_pie.data[0].hovertemplate = '%{label}<br>'+'count'+':%{value}<br>%{customdata:.2f}%'
    
    fig_pie.update_layout(legend=dict(
                orientation="v",
                xanchor="left",
                #x=0.02,
                #y=1.02,
                title=condition.capitalize(),
                font=dict(size=10),
                ),
                title={
               'text':title_label,
               'xref':'paper',
               #'xanchor':'center',
               'x':0.5,
               'yanchor':'top',
               'automargin':True,
               },
               #margin=dict(r=1, l=1),
               font=dict(size=12))
    #fig_pie.update_yaxes(automargin=True)
    #fig_pie.update_layout(height=650)
    fig_pie.update_traces(textposition='inside', textinfo='percent')
    return fig_pie

def tree_author_element_general(data, elemento): #sólo para aquellos elementos con la columna 'autores' existente, se filtra a top 30 si hay mas
    warnings.filterwarnings(action='ignore', category=FutureWarning)#################
    dataset_autores=data[['idgruplac','autores']].copy()
    dataset_autores['autores']=dataset_autores['autores'].str.split(',')
    dataset_autores=dataset_autores.explode('autores')
    dataset_autores['autores']=dataset_autores['autores'].str.strip()
    dataset_autores=dataset_autores['autores'].value_counts().reset_index().rename(columns={'index':'autores','autores':'count'})
    dataset_autores['percents']=(dataset_autores['count']*100)/sum(dataset_autores['count'])
    dataset_autores['autores']=dataset_autores['autores'].str.wrap(15,break_long_words=False).str.replace('\n','<br>')
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
                      font=dict(size=12))
    #fig.update_layout(height='600')
    fig.update_layout(uniformtext=dict(minsize=16))
    warnings.filterwarnings(action='default', category=FutureWarning)##################
    return fig

def pie_type_element_general(datain): #solo elementos con columna "tipo" existente
    data=datain.copy()
    data['tipo']=data['tipo'].str.wrap(15,break_long_words=False).str.replace('\n','<br>')
    fig_pie = px.pie(data, values=data['tipo'].value_counts(), 
                     names=data['tipo'].value_counts().index, color_discrete_sequence=px.colors.qualitative.Dark2,
                     hole=.3)
    fig_pie.update_layout(title={
               'text':"<b>Publicaciones por Tipo</b>",
               #'xanchor':'center',
               'xref':'paper',
               'x':0.5,
               'yanchor':'top',
               'automargin':True},
               font=dict(size=12))
    return fig_pie

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
        value = [],  # Valor inicial seleccionado
        disabled= True,
        multi=True
    )
option_element_gruplac_general = dcc.Dropdown(
        id='filter_element_gruplac_general',
        options = options_general_element,
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
    [Output('filtro_individual', 'hidden'),Output('filtro_grupal', 'hidden')],
    Input('tabs_filter_scienti', 'value'))
def render_content(tab):
    if tab == 'tab_individual':
        return False, True
    else:
        return True, False

#----------------------individual
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
#-----------------grupal
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
    [State('filter_parameter', 'value'),
    State('filter_element_gruplac_general', 'value'),
    Input('filter_value', 'disabled'),
    Input('filter_value', 'value')])
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
    Output('kpi_all','style'),
    Output('indicators_group','children'),Output('products_element_group','children'),
    Output('url_group_grouplac','href'),Output('group_minciencias','href'),
    Output('kpi-1','children'),Output('kpi-2','children'),Output('kpi-3','children'),Output('kpi-4','children'),Output('kpi-5','children'),
    Output('dash_individual_graph1','figure'),Output('div_group_figure1','style'),
    Output('dash_individual_graph2','figure'),Output('div_group_figure2','style'),
    Output('dash_individual_graph3','figure'),Output('div_group_figure3','style'),
    Output('dash_individual_graph4','figure'),Output('div_group_figure4','style'),
    ],
    [State('filter_group', 'value'), State('filter_element_gruplac', 'value'),
    Input('button_group_filter_indiv','n_clicks')]
 )
def callback_filter_individual(grupo, elemento, boton):
    #print(boton)
    kpi_all = {'display':'none'}
    indicators_group = ''
    products_element_group = ''
    url_group_grouplac = ''
    group_minciencias = ''
    kpi1 = ''
    kpi2 = ''
    kpi3 = ''
    kpi4 = ''
    kpi5 = ''    
    dash_individual_graph1 = {}
    dash_individual_graph2 = {}
    dash_individual_graph3 = {}
    dash_individual_graph4 = {}
    div_group_figure1 = {'display':'none'}
    div_group_figure2 = {'display':'none'}
    div_group_figure3 = {'display':'none','width':'47%'}
    div_group_figure4 = {'display':'none'}
    if boton == 0 or elemento == None:
        return kpi_all, indicators_group, products_element_group, url_group_grouplac, group_minciencias, kpi1, kpi2, kpi3, kpi4, kpi5, dash_individual_graph1, div_group_figure1, dash_individual_graph2, div_group_figure2, dash_individual_graph3, div_group_figure3, dash_individual_graph4, div_group_figure4
    
    kpi_all = {'display':'block'}
    #indicadores    
    grupo_cod=get_codigo_grupo(grupo)
    ac=get_author_count(grupo_cod)  
    url_group_grouplac = 'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro='+grupo_cod
    group_minciencias = get_perfil_minciencias(grupo_cod)
    indicators_group = grupo
    products_element_group = elemento
    if elemento == 'Todos':
        consistencia, ppa,ppua,pc, series_gruplac = get_indicadores(grupo_cod)        
        kpi1 = str(consistencia)
        kpi2 = str(ppa)
        kpi3 = str(ppua)+'%'
        kpi4 = str(pc)
        kpi5 = str(ac)       
        dash_individual_graph1 = time_series_all(series_gruplac)
        dash_individual_graph2, dash_individual_graph3 = bar_pie_all(grupo_cod)
        div_group_figure1 = {'display':'block', 'height':'75vh', 'max-height':'85vh','margin-top':'10px','padding-bottom':'10px','padding-top':'15px'}
        div_group_figure2 = {'display':'inline-block', 'max-height':'75vh', 'margin-bottom':'10px','padding-bottom':'5px'}
        div_group_figure3 = {'display':'inline-block', 'max-height':'75vh','margin-top':'10px','padding-top':'10px','margin-bottom':'10px','padding-bottom':'5px'}
    else:
        consistencia, ppa,ppua,pc, series_gruplac = get_indicadores_relativos(grupo_cod, elemento)
        kpi1 = str(consistencia)
        kpi2 = str(ppa)
        kpi3 = str(ppua)+'%'
        kpi4 = str(pc)
        kpi5 = str(ac)
        dash_individual_graph1 = time_series_element(series_gruplac, elemento)
        div_group_figure1 = {'display':'block', 'height':'75vh', 'max-height':'85vh','margin-top':'10px','padding-bottom':'10px','padding-top':'15px'}
        data = filtro_gruplac_elemento_individual(grupo, elemento)
        if data.shape[0]==0:
            ###############################
            #HACER FUNCION DE MOSTRAR MENSAJE: NO HAY DATOS DISPONIBLES
            #############################
           return kpi_all, indicators_group, products_element_group, url_group_grouplac, group_minciencias, kpi1, kpi2, kpi3, kpi4, kpi5, dash_individual_graph1, div_group_figure1, dash_individual_graph2, div_group_figure2, dash_individual_graph3, div_group_figure3, dash_individual_graph4, div_group_figure4

        if ('revista' in data) and ('tipo' in data):
            dash_individual_graph2 = pie_journal_element(data)
            dash_individual_graph3 = pie_type_element(data)
            div_group_figure2 = {'display':'inline-block', 'max-height':'75vh', 'margin-bottom':'10px','padding-bottom':'5px'}
            div_group_figure3 = {'display':'inline-block', 'max-height':'75vh','margin-top':'10px','padding-top':'10px', 'margin-bottom':'10px','padding-bottom':'5px'}
        elif ('editorial' in data) and ('tipo' in data):
            dash_individual_graph2 = pie_editorial_element(data)
            dash_individual_graph3 = pie_type_element(data)
            div_group_figure2 = {'display':'inline-block', 'max-height':'75vh', 'margin-bottom':'10px','padding-bottom':'5px'}
            div_group_figure3 = {'display':'inline-block', 'max-height':'75vh','margin-top':'10px','padding-top':'10px', 'margin-bottom':'10px','padding-bottom':'5px'}
        elif ((('revista' in data) and ('editorial' in data)) != True) and ('tipo' in data):
            dash_individual_graph3 = pie_type_element(data)
            div_group_figure3 = {'display':'block', 'max-height':'75vh','margin-top':'10px','padding-top':'10px', 'margin-bottom':'10px','padding-bottom':'5px'}
        if 'autores' in data:
            dash_individual_graph4 = tree_author_element(data, elemento)        
            div_group_figure4 = {'display':'block','height':'75vh','max-height':'80vh','margin-bottom':'10px','margin-top':'10px','padding-top':'10px'}

    return kpi_all, indicators_group, products_element_group, url_group_grouplac, group_minciencias, kpi1, kpi2, kpi3, kpi4, kpi5, dash_individual_graph1, div_group_figure1, dash_individual_graph2, div_group_figure2, dash_individual_graph3, div_group_figure3, dash_individual_graph4, div_group_figure4

@callback(
    [    
    Output('dash_general_graph1','figure'),Output('div_general_figure1','style'),
    Output('dash_general_graph2','figure'),Output('div_general_figure2','style'),
    Output('dash_general_graph3','figure'),Output('div_general_figure3','style'),
    Output('dash_general_graph4','figure'),Output('div_general_figure4','style'),
    Output('dash_general_graph5','figure'),Output('div_general_figure5','style'),
    Output('dash_general_graph6','figure'),Output('div_general_figure6','style'),
    Output('dash_general_graph7','figure'),Output('div_general_figure7','style'),
    Output('dash_general_graph8','figure'),Output('div_general_figure8','style'),
    Output('dash_general_graph9','figure'),Output('div_general_figure9','style'),    
    ],
    [State('filter_parameter', 'value'), State('filter_value', 'value'), State('filter_element_gruplac_general', 'value'),
    Input('button_group_filter_group','n_clicks')]
 )
def callback_filter_grupal(parametro, valor, elemento, boton):
    dash_general_graph1 = {}
    dash_general_graph2 = {}
    dash_general_graph3 = {}
    dash_general_graph4 = {}
    dash_general_graph5 = {}
    dash_general_graph6 = {}
    dash_general_graph7 = {}
    dash_general_graph8 = {}
    dash_general_graph9 = {}
    div_general_figure1 = {'display':'none'}
    div_general_figure2 = {'display':'none'}
    div_general_figure3 = {'display':'none'}
    div_general_figure4 = {'display':'none'}
    div_general_figure5 = {'display':'none'}
    div_general_figure6 = {'display':'none'}
    div_general_figure7 = {'display':'none'}
    div_general_figure8 = {'display':'none'}
    div_general_figure9 = {'display':'none'}       
    if boton == 0 or elemento == None:
        return dash_general_graph1,div_general_figure1, dash_general_graph2, div_general_figure2, dash_general_graph3,div_general_figure3, dash_general_graph4, div_general_figure4, dash_general_graph5, div_general_figure5, dash_general_graph6, div_general_figure6, dash_general_graph7, div_general_figure7, dash_general_graph8, div_general_figure8, dash_general_graph9, div_general_figure9
    grupos_codigos, grupos_nombres=filtro_gruplac_valor_general(parametro,valor)
    
    if elemento == 'Todos':
        df_indicadores, time_series = get_indicadores_gruplac_general(grupos_codigos)
        if df_indicadores['idgruplac'].count()>10:
            df_indicadores=df_indicadores.sort_values(by='pg',ascending=False).iloc[:10].sort_index()
            indices_top=list(df_indicadores.index.astype('int64'))
            time_series=[time_series[x] for x in indices_top]
            grupos_codigos=df_indicadores['idgruplac'].to_list()
            grupos_nombres=[gruplac_basico[gruplac_basico['idgruplac'].str.contains(x)]['nombre'].iloc[0] for x in grupos_codigos]
            indices_top=0
        dash_general_graph1 = time_series_all_general(time_series,grupos_nombres,elemento)
        dash_general_graph2 = bar_general_all(grupos_codigos,grupos_nombres)
        dash_general_graph3 = bar_consistencia(df_indicadores,grupos_nombres,elemento)
        dash_general_graph4 = bar_ppa(df_indicadores,grupos_nombres,elemento)
        dash_general_graph5 = bar_ppua(df_indicadores,grupos_nombres,elemento)
        dash_general_graph6 = bar_pg(df_indicadores,grupos_nombres,elemento)
        div_general_figure1 = {'display':'block', 'height':'75vh', 'max-height':'85vh','margin-top':'10px','padding-bottom':'10px','padding-top':'15px'}
        wdg2=str(len(grupos_codigos)*7)+'vw'
        div_general_figure2 = {'display':'block', 'min-width':'40vw','width':wdg2, 'height':'75vh','max-height':'85vh','margin-top':'10px','padding-top':'15px','padding-bottom':'10px'}
        div_general_figure3 = {'display':'inline-block', 'max-height':'max-content'}
        div_general_figure4 = {'display':'inline-block', 'max-height':'max-content'}
        div_general_figure5 = {'display':'inline-block', 'max-height':'max-content'}
        div_general_figure6 = {'display':'inline-block', 'max-height':'max-content'}
    else:
        df_indicadores, time_series = get_indicadores_gruplac_relativo(grupos_codigos,elemento)
        if df_indicadores['idgruplac'].count()>10:
            print('slice?')
            df_indicadores=df_indicadores.sort_values(by='pg',ascending=False).iloc[:10].sort_index()
            indices_top=list(df_indicadores.index.astype('int64'))
            time_series=[time_series[x] for x in indices_top]
            grupos_codigos=df_indicadores['idgruplac'].to_list()
            grupos_nombres=[gruplac_basico[gruplac_basico['idgruplac'].str.contains(x)]['nombre'].iloc[0] for x in grupos_codigos]
            indices_top=0
        data=filtro_gruplac_elemento_general(grupos_codigos,elemento)
        if data.shape[0]==0:
            ###############################
            #HACER FUNCION DE MOSTRAR MENSAJE: NO HAY DATOS DISPONIBLES
            #############################
            return dash_general_graph1,div_general_figure1, dash_general_graph2, div_general_figure2, dash_general_graph3,div_general_figure3, dash_general_graph4, div_general_figure4, dash_general_graph5, div_general_figure5, dash_general_graph6, div_general_figure6, dash_general_graph7, div_general_figure7, dash_general_graph8, div_general_figure8, dash_general_graph9, div_general_figure9 
        dash_general_graph1 = time_series_all_general(time_series, grupos_nombres,elemento)
        div_general_figure1 = {'display':'block', 'height':'78vh','max-height':'83vh','margin-top':'10px','padding-bottom':'10px','padding-top':'15px'}
        dash_general_graph2 = bar_general_element(data,elemento)
        wdg2=str(len(grupos_codigos)*7)+'vw'
        div_general_figure2 = {'display':'block', 'min-width':'40vw','width':wdg2, 'height':'75vh','max-height':'85vh','margin-top':'10px','padding-top':'15px','padding-bottom':'10px'}
        dash_general_graph3 = bar_consistencia(df_indicadores,grupos_nombres,elemento)
        div_general_figure3 = {'display':'inline-block', 'max-height':'90vh'}
        dash_general_graph4 = bar_ppa(df_indicadores,grupos_nombres,elemento)
        div_general_figure4 = {'display':'inline-block', 'max-height':'90vh'}
        dash_general_graph5 = bar_ppua(df_indicadores,grupos_nombres,elemento)
        div_general_figure5 = {'display':'inline-block', 'max-height':'90vh'}
        dash_general_graph6 = bar_pg(df_indicadores,grupos_nombres,elemento)
        div_general_figure6 = {'display':'inline-block', 'max-height':'90vh'}
        if 'autores' in data:
            dash_general_graph7 = tree_author_element_general(data, elemento)
            div_general_figure7 = {'display':'block', 'height':'75vh','max-height':'80vh'}

        if ('revista' in data) and ('tipo' in data):
            dash_general_graph8 = pie_journal_element_general(data,'revista')
            dash_general_graph9 = pie_type_element_general(data)
            div_general_figure8 = {'display':'inline-block','max-height':'700px','padding-top':'10px'}
            div_general_figure9 = {'display':'inline-block','max-height':'700px','padding-top':'10px'}
        elif ('editorial' in data) and ('tipo' in data):
            dash_general_graph8 = pie_journal_element_general(data,'editorial')
            dash_general_graph9 = pie_type_element_general(data)
            div_general_figure8 = {'display':'inline-block','max-height':'700px','padding-top':'10px'}
            div_general_figure9 = {'display':'inline-block','max-height':'700px','padding-top':'10px'}
        elif ((('revista' in data) and ('editorial' in data)) != True) and ('tipo' in data):
            dash_general_graph9 = pie_type_element_general(data)
            div_general_figure9 = {'display':'block','width':'95%','max-height':'700px','padding-top':'10px'}       
    print(dash_general_graph3['layout']['title']['text'])
    return dash_general_graph1,div_general_figure1, dash_general_graph2, div_general_figure2, dash_general_graph3,div_general_figure3, dash_general_graph4, div_general_figure4, dash_general_graph5, div_general_figure5, dash_general_graph6, div_general_figure6, dash_general_graph7, div_general_figure7, dash_general_graph8, div_general_figure8, dash_general_graph9, div_general_figure9