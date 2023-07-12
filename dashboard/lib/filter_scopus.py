# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import pandas as pd
import numpy as np
import re


from dash import no_update
from dash.exceptions import PreventUpdate

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

#red colaboracion
from itertools import combinations
import networkx as nx
#pip install networkx
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('agg')
import os
import pathlib
import uuid


opciones_grupo_scopus_aux=[]
scopus_productos['nombre_grupo'].dropna().str.split(';').apply(lambda x: opciones_grupo_scopus_aux.extend(x)) #variable para opciones del filtro de grupo
opciones_grupo_scopus=list(map(str.strip, list(set(opciones_grupo_scopus_aux[:]))))

elementos_scopus_general=elementos_scopus_lista[:]
if 'Todos' in elementos_scopus_general:
    options_general_element_scopus=elementos_scopus_general[:]
else:
    options_general_element_scopus=[*elementos_scopus_general,'Todos']

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
    dic={'idgruplac':[],'cit_output':[],'citations':[],'h1_index':[],'h2_index':[],'pc':[]}
    list_series=[]
    for grup in grupos:
        dic['idgruplac'].append(grup)
        dic['cit_output'].append(citation_output_relativo(grup,elemento))
        dic['citations'].append(citation_count_relativo(grup,elemento))
        dic['h1_index'].append(get_h1_index_relativo(grup,elemento))
        dic['h2_index'].append(get_h2_index(grup))
        dic['pc'].append(products_count_relativo(grup,elemento))
        list_series.append(get_series_scopus(grup,elemento))
    indicadores_grupos_scopus= pd.DataFrame.from_dict(dic)#.sort_values(by='pc',ascending=False)
    return indicadores_grupos_scopus, list_series

#INDIVIDUAL

def filtro_scopus_grupo_individual(grupo):
    grupo=grupo.strip()
    idgruplac=gruplac_basico[gruplac_basico['nombre']==grupo]['idgruplac'].iloc[0]
    opc_elementos=[]
    for elemento in elementos_scopus_lista:        
        data=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac').copy()
        if data[data['idgruplac'].str.contains(idgruplac)].shape[0] >= 1:
            opc_elementos.append(elemento)
    # data=pd.DataFrame()
    return opc_elementos

def filtro_scopus_elemento_individual(grupo,elemento):
    grupo=grupo.strip()
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
    
    if 'Todos' in valor:
        idgruplacs=gruplac_basico['idgruplac'].drop_duplicates(keep='first').to_list()
    
    elif parametro=='Ingreso Manual':
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
    idgruplacs=[gruplac_basico[gruplac_basico['nombre']==nombre_grupo]['idgruplac'].iloc[0] for nombre_grupo in nombre_grupos]
    #data=pd.DataFrame()
    #elemento_general_seleccionado_scopus='Todos'
    return idgruplacs, nombre_grupos#, data

def filtro_scopus_elemento_general(idgruplacs, elemento):
    if elemento=='Todos':
        data=scopus_productos.copy() 
    else:
        data=fuente_dic['SCOPUS'][elemento].dropna(subset='idgruplac').copy()
    data_aux=data.copy()
    data_aux['id']=data_aux.index
    indexes=[]
    data_aux[['id','idgruplac']].dropna(subset='idgruplac').apply(lambda x: indexes.append(x['id']) if len(set(x['idgruplac'].split(';')).intersection(set(idgruplacs)))>=1 else None,axis=1)
    data=data.loc[indexes]#.astype(globals()[str(referencias['SCOPUS'][elemento])][data.columns.to_list()].dtypes.to_dict())
    return data

########## GRAFICAS INDIVIDUAL

##########TODOS

def time_series_all_scopus(series, elemento='Todos'):
    series=series.to_frame().reset_index()
    series.columns=['fecha','productos']
    #series['fecha']=series['fecha'].dt.to_timestamp(freq='M')
    series['fecha']=series['fecha'].dt.strftime('%Y-%m') 
    if elemento=='Todos':
        title_label="Productos Anuales Generados: Todos"
        axis_label="Conteo de Productos"
    else:
        title_label="Productos Anuales Generados: "+elemento
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
                  font=dict(size=10))
    fig.update_traces(line_color='#0000ff', line_width=2)
    return fig

def bar_all_scopus(grupo): #retorna dos graficas, recibe codigo de grupo
    dic={'producto':[],'count':[]}
    for key in list(set(fuente_dic['SCOPUS'].keys())):
        data=fuente_dic['SCOPUS'][key].dropna(subset='idgruplac').copy()
        dic['count'].append(data[data['idgruplac'].str.contains(grupo)]['idgruplac'].count())
        dic['producto'].append(key)
    df=pd.DataFrame.from_dict(dic)
    df=df[df['count']>0]
    fig = px.bar(df, x="producto", y="count", color='producto',color_discrete_sequence=px.colors.sequential.Turbo,
                 labels={
                 "producto":"Tipo de Producto",
                 "count":"Cantidad de Productos"})
    fig.update(layout_showlegend=False)
    fig.update_layout(title={
                'text':"Conteo de Productos",
                #'xanchor':'center',
                #'x':0.5,
                #'yanchor':'top'
                },
                xaxis={'categoryorder': 'total descending'},
               font=dict(size=10.5))
    return fig

def tree_author_all_scopus(data,elemento='Todos'): #sólo para aquellos elementos con la columna 'autores' existente, se filtra a top 30 si hay mas
    warnings.filterwarnings(action='ignore', category=FutureWarning)#################
    if elemento=='Todos':
        top_label="Top Autores: Todos los Productos"
    else:
        top_label="Top Autores: "+elemento
    dataset_autores=data[['idgruplac','autores']].copy()
    dataset_autores['autores']=dataset_autores['autores'].str.split(';')
    dataset_autores=dataset_autores.explode('autores')
    dataset_autores['autores']=dataset_autores['autores'].str.strip()
    dataset_autores=dataset_autores['autores'].value_counts().reset_index().rename(columns={'index':'autores','autores':'count'})
    dataset_autores['percents']=(dataset_autores['count']*100)/sum(dataset_autores['count'])
    dataset_autores['autores']=dataset_autores['autores'].str.wrap(15,break_long_words=False).str.replace('\n','<br>')
    if dataset_autores['autores'].count()>30:
        dataset_autores=dataset_autores.iloc[:30]
    fig = px.treemap(dataset_autores, path=[px.Constant(top_label),'autores'], values='count', 
                     custom_data=['percents'])
    fig.update_traces(root_color="white")
    fig.data[0].texttemplate = "%{label}<br>"+elemento+":%{value}<br>%{customdata:.2f}%"
    fig.data[0].hovertemplate = '%{label}<br>'+elemento+':%{value}<br>%{customdata:.2f}%'
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25),
                      title={
                      'text':'Participación de Autores',
                      #'xanchor':'center',
                      #'x':0.5,
                      #'yanchor':'top'
                      },
                      font=dict(size=14))
    fig.update_layout(uniformtext=dict(minsize=16))
    warnings.filterwarnings(action='default', category=FutureWarning)##################
    return fig

def boxplot_individual(codigo_grupo,datain,elemento='Todos'):
    if elemento=='Todos':##########  
        title_label='Distribución de Citaciones: Todos los Productos'
    else:
        title_label='Distribución de Citaciones: '+elemento
    data=datain.dropna(subset='idgruplac')[['idgruplac','citado']].copy()
    data['citado']=data['citado'].astype('int64')
    data['idgruplac']=gruplac_basico[gruplac_basico['idgruplac']==codigo_grupo]['nombre'].iloc[0]
    data['idgruplac']=data['idgruplac'].str.wrap(20,break_long_words=False).str.replace('\n','<br>')
    fig = px.box(data, x="idgruplac", y="citado",color='idgruplac', points='all',hover_data = {'citado':True,'idgruplac':False})
    #if data['idgruplac'].nunique()>3:
    #    fig.update_xaxes(tickangle = 90)
    fig.update_layout(xaxis={'visible': False, 'showticklabels': False},yaxis_title="Citaciones",
                      legend_title='Grupos de Investigación')
    #fig.update_traces(orientation='h')
    fig.update_layout(title={'text':title_label})
    maxrange=data.groupby('idgruplac').quantile(0.93).max().iloc[0]
    fig['layout']['yaxis'].update(range=[-0.15,maxrange])
    return fig

def get_fig_title(fig):
    #fig.update_layout(title={'text':None})
    return fig['layout']['title']['text']

#ELEMENTO

def pie_journal_element_scopus(datain,condition): #recibe dataset filtrado y ocndicion 'editorial' o 'revista'
    data=datain.copy()
    data[condition]=data[condition].str.wrap(20,break_long_words=False).str.replace('\n','<br>')
    if condition=='editorial':
        title_label="Publicaciones por Editoriales"
        legend_label='Editorial'
    else:
        title_label="Publicaciones en Revistas"
        legend_label='Revista'
    
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
    fig_pie.update_layout(legend=dict(
                orientation="v",
                xanchor="left",
                #x=0.02,
                #y=1.02,
                title=legend_label,
                font=dict(size=10.5),
                ),
                title={
               'text':title_label,
               #'xanchor':'center',
               #'x':0.5,
               #'yanchor':'top',
               #'automargin':True
               },
               #margin=dict(r=10, l=10),
               font=dict(size=11))
    fig_pie.data[0].hovertemplate = '%{label}<br>'+'count'+':%{value}<br>%{customdata:.2f}%'
    fig_pie.update_traces(textposition='inside', textinfo='percent')
    return fig_pie

def tree_topic_element_scopus(data, elemento): #sólo para aquellos elementos con la columna 'autores' existente, se filtra a top 30 si hay mas
    warnings.filterwarnings(action='ignore', category=FutureWarning)#################
    dataset_tema=data[['idgruplac','tema']].copy()
    dataset_tema['tema']=dataset_tema['tema'].str.split(';')
    dataset_tema=dataset_tema.explode('tema')
    dataset_tema['tema']=dataset_tema['tema'].str.strip()
    dataset_tema=dataset_tema['tema'].value_counts().reset_index().rename(columns={'index':'tema','tema':'count'})
    dataset_tema['percents']=(dataset_tema['count']*100)/sum(dataset_tema['count'])
    dataset_tema['tema']=dataset_tema['tema'].str.wrap(15,break_long_words=False).str.replace('\n','<br>')
    if dataset_tema['tema'].count()>30:
        dataset_tema=dataset_tema.iloc[:30]
    fig = px.treemap(dataset_tema, path=[px.Constant('Top Temas'),'tema'], values='count', 
                     custom_data=['percents'])
    fig.update_traces(root_color="white")
    fig.data[0].texttemplate = "%{label}<br>"+elemento+":%{value}<br>%{customdata:.2f}%"
    fig.data[0].hovertemplate = '%{label}<br>'+elemento+':%{value}<br>%{customdata:.2f}%'
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25),
                      title={
                      'text':'Temas Trabajados',
                      #'xanchor':'center',
                      #'x':0.5,
                      #'yanchor':'top'
                      },
                      font=dict(size=14))
    fig.update_layout(uniformtext=dict(minsize=16))
    warnings.filterwarnings(action='default', category=FutureWarning)##################
    return fig

def collaboration_network(grupo_nombre,elemento='Todos'):
    def net_break(x):
        xlen=len(x)
        if xlen==2:
            return [x]
        else:
            return list(combinations(x, 2))
    def nudge(pos, x_shift, y_shift):
        return {n:(x + x_shift, y + y_shift) for n,(x,y) in pos.items()}
    grupo=gruplac_basico[gruplac_basico['nombre']==grupo_nombre]['idgruplac'].iloc[0]
    if elemento=='Todos':
        net=scopus_productos[['idgruplac']].dropna().copy()
    else:
        net=fuente_dic['SCOPUS'][elemento][['idgruplac']].dropna().copy()
    net=net[net['idgruplac'].str.contains(grupo)]
    net['idgruplac']=net['idgruplac'].str.split(';')
    net=net[net['idgruplac'].str.len()>1]
    net['idgruplac']=net['idgruplac'].apply(lambda x: net_break(x))
    net=net.explode('idgruplac')
    net['idgruplac']=net['idgruplac'].apply(lambda x: sorted(list(x)))
    net=net['idgruplac'].value_counts().reset_index(drop=False, name='count')
    net=net[net['index'].apply(lambda x: ','.join(map(str, x))).str.contains(grupo)]
    net["from"] = net['index'].apply(lambda t:t[0].strip() if t[0].strip()==grupo else t[1].strip())
    net["to"] = net['index'].apply(lambda t:t[1].strip() if t[1].strip()!=grupo else t[0].strip())
    net["weight"]=net['count']
    net.drop(columns=['index','count'], inplace=True)
    net['from']=net['from'].apply(lambda x: gruplac_basico[gruplac_basico['idgruplac']==x]['nombre'].iloc[0].strip())
    net['to']=net['to'].apply(lambda x: gruplac_basico[gruplac_basico['idgruplac']==x]['nombre'].iloc[0].strip())
    net['from']=net['from'].str.wrap(20,break_long_words=False).copy()
    net['to']=net['to'].str.wrap(20,break_long_words=False).copy()
    if net.shape[0]<1:
        network_image='None'
        return network_image
    ##net=net[(net['from']==grupo) | (net['to']==grupo)]
    #df = pd.DataFrame({ 'from':['DDDDDDDDDDDDDDDDDDDDD\nDDDDDDDDDDDDDDDDDDDDDD', 'A', 'B', 'C','A'], 'to':['A', 'DDDDDDDDDDDDDDDDDDDDD\nDDDDDDDDDDDDDDDDDDDDDD', 'A', 'E','C'], 'weight':['1', '5', '8', '3','20']})
    G=nx.from_pandas_edgelist(net, 'from', 'to', edge_attr='weight', create_using=nx.DiGraph() )
    widths = nx.get_edge_attributes(G, 'weight')
    nodelist = G.nodes()
    fig=plt.figure(figsize=(13,8))
    #pos = nx.shell_layout(G)
    pos=nx.spring_layout(G)
    pos_nodes = nudge(pos, 0, 0.15)
    nx.draw_networkx_nodes(G,pos,
                           nodelist=nodelist,
                           node_size=900,
                           node_color='black',
                           alpha=0.5)
    nx.draw_networkx_edges(G,pos,
                           edgelist = widths.keys(),
                           width=list(widths.values()),
                           edge_color='orange',
                           alpha=0.6)
    #pos=nx.spring_layout(G) # pos = nx.nx_agraph.graphviz_layout(G)
    #nx.draw_networkx(G,pos)
    nx.draw_networkx_labels(G, pos=pos_nodes,
                            labels=dict(zip(nodelist,nodelist)),
                            font_color='black',font_size=9)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, font_size=10)
    #plt.box(False)
    l,r = plt.xlim()
    b,t = plt.ylim()
    plt.xlim(l-0.07,r+0.07)
    plt.ylim(b,t+0.15)
    plt.close(fig)
    path = pathlib.Path('./assets/img/network_temp/').resolve() # Figures out the absolute path for you in case your working directory moves around.
    network_image = str(uuid.uuid4())+".PNG"
    fig.savefig(os.path.join(path, network_image), bbox_inches='tight', pad_inches=0.0)  #DEFINIR DIRECTORIO
    return network_image
###############GRAFICAS GENERAL

#TODOS

def time_series_all_general_scopus(series,grupos,elemento='Todos'): #recibe time_series y grupos_nombres
    df=pd.DataFrame()
    if elemento=='Todos':
        title_label='Productos Anuales Generados: Todos'
        axis_label='Cantidad de Productos'
    else:
        title_label='Productos Anuales Generados: '+elemento
        axis_label='Cantidad de '+elemento
    
    for i,serie in enumerate(series):
        serie=serie.to_frame().reset_index()
        serie.columns=['fecha','productos']
        #series['fecha']=series['fecha'].dt.to_timestamp(freq='M')
        serie['fecha']=serie['fecha'].dt.strftime('%Y-%m') 
        if i==0:
            df['fecha']=serie['fecha']
            df[grupos[i]]=serie['productos']
        else:
            df_aux=pd.DataFrame()
            df_aux['fecha']=serie['fecha']
            df_aux[grupos[i]]=serie['productos']
            df=pd.merge(df, df_aux, on="fecha",how='outer').sort_values(by='fecha').fillna(0)
            #df['fecha']=pd.to_datetime(df.fecha, format='%Y').dt.year
    fig = px.line(df, x='fecha', y=df.columns, 
                  labels={
                      "fecha":"Años",
                      "value":axis_label})
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0.01,
        title='Grupos',
        font=dict(size=10.5)),
        title={
              'text':title_label,
              #'xanchor':'center',
              #'x':0.5,
              #'yanchor':'top',
              #'automargin':True
              },
              font=dict(size=10))
              #margin=dict(t=20, b=20))
    fig.update_traces(line_width=1.5)
    #fig.update_layout(height=650)#############
    return fig

def bar_general_all_scopus(codigos, nombres): #retorna dos graficas, recibe grupos_codigos y grupos_codigos
    df=pd.DataFrame(columns=['grupo','producto','count'])
    for i,codigo in enumerate(codigos):
        dic={'grupo':[],'producto':[],'count':[]}
        for key in list(set(fuente_dic['SCOPUS'].keys())):
            data=fuente_dic['SCOPUS'][key].dropna(subset='idgruplac').copy()
            dic['grupo'].append(nombres[i])
            dic['count'].append(data[data['idgruplac'].str.contains(codigo)]['idgruplac'].count())
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
                'text':"Productos Generados por los Grupos de Investigación",
                #'xanchor':'center',
                #'x':0.5,
                #'xref':'paper',
                #'yanchor':'top',
                #'automargin':True,
                #'font': {'size': 15},
                },
                yaxis={'categoryorder': 'total ascending'},
                font=dict(size=10),
                margin=dict(t=2, b=2),
                #height=650
                )
    if df['grupo'].nunique()>3:
        fig.update_xaxes(tickangle=90)
    #fig.update_layout(legend_x=0.02, legend_y=1.02)
    #fig.update_yaxes(automargin=True)
    #fig.update_traces(visible='legendonly')
    fig.update_layout(xaxis = dict(tickfont = dict(size=10)))
    return fig

def radar_general_all(indicadores,elemento='Todos'):
    warnings.filterwarnings(action='ignore', category=FutureWarning)
    if elemento=='Todos':
        title_label='Radar de Indicadores: Todos los Productos'
    else:
        title_label='Radar de Indicadores: '+elemento
    aux_ind=indicadores[['idgruplac','cit_output','h1_index','h2_index']].copy()
    aux_ind.columns=['Grupos','Citaciones por<br>Producto','H1<br>Index','H2<br>Index']
    aux_ind['Grupos']=[gruplac_basico[gruplac_basico['idgruplac']==idg]['nombre'].iloc[0] for idg in aux_ind['Grupos'].to_list()]
    aux_ind['Grupos']=aux_ind['Grupos'].str.wrap(20,break_long_words=False).str.replace("\n","<br>")
    #aux_ind['id']=aux_ind.index
    aux_ind=pd.melt(aux_ind, id_vars='Grupos', value_vars=['Citaciones por<br>Producto','H1<br>Index','H2<br>Index']).sort_values(by='Grupos')
    fig = px.line_polar(aux_ind, r='value', color='Grupos', theta='variable', line_close=True)
    #fig.update_traces(fill='toself')
    fig.update_layout(title={'text':title_label},
                      legend=dict(font=dict(size=9.7)),
                      font=dict(size=10))
    fig.for_each_trace(lambda t: t.update(hoveron='points'))
    warnings.filterwarnings(action='default', category=FutureWarning)
    return fig

def heatmap_general(codigos,nombres):
    df=pd.DataFrame(columns=['grupo','tipo_producto','citaciones'])
    for i,codigo in enumerate(codigos):
        dic={'grupo':[],'tipo_producto':[],'citaciones':[]}
        for key in list(set(fuente_dic['SCOPUS'].keys())):
            data=fuente_dic['SCOPUS'][key].dropna(subset='idgruplac').copy()
            dic['grupo'].append(nombres[i])
            dic['citaciones'].append(data[data['idgruplac'].str.contains(codigo)]['citado'].astype('int64').sum())
            dic['tipo_producto'].append(key)
        df_aux=pd.DataFrame.from_dict(dic)
        df_aux['citaciones']=df_aux['citaciones'].astype('int64')
        if (df_aux['citaciones']==0).all(skipna=True):
            pass
        else:
            df_aux=df_aux[df_aux['citaciones']>0]
        df=pd.concat([df, df_aux], ignore_index=True)
    
    locs=df[df['grupo'].str.len()>40].index.tolist()
    locs_df=df['grupo'].loc[locs].copy()
    df.loc[locs,'grupo']=locs_df.str.slice(stop=40)+'...'
    df['grupo']=df['grupo'].str.wrap(25,break_long_words=False).str.replace('\n','<br>')
    df['tipo_producto']=df['tipo_producto'].str.wrap(15,break_long_words=False).str.replace('\n','<br>')
    df= df.pivot(index='grupo', columns='tipo_producto')['citaciones'].fillna(0)
    fig = px.imshow(df, x=df.columns, y=df.index, color_continuous_scale='RdBu_r',text_auto=True,
                   labels=dict(x="Tipo de Producto", y="Grupos de Investigación", color="Citaciones"))
    fig.update_layout(xaxis = dict(tickfont = dict(size=9.8)))
    fig.update_layout(yaxis = dict(tickfont = dict(size=9.6)),font=dict(size=10))
    #fig.update_layout(width=500,height=500)
    fig.update_layout(title={'text':'Grupos por Tipo de Producto: Citaciones'})
    if len(df.columns)>3:
        fig.update_xaxes(tickangle = 90)
    return fig

def boxplot_general_all_scopus(codigos,nombres):
    df=pd.DataFrame(columns=['idgruplac','citado'])
    for i,codigo in enumerate(codigos):
        data=scopus_productos.dropna(subset='idgruplac').copy()
        data=data[data['idgruplac'].str.contains(codigo)][['idgruplac','citado']]
        data['idgruplac']=nombres[i]
        df=pd.concat([df, data], ignore_index=True)
    df['idgruplac']=df['idgruplac'].str.wrap(20,break_long_words=False).str.replace('\n','<br>')
    df['citado']=df['citado'].astype('int64')
    fig = px.box(df, x="idgruplac", y="citado",color='idgruplac', points='all',hover_data = {'citado':True,'idgruplac':False})
    #if df['idgruplac'].nunique()>3:
    #    fig.update_xaxes(tickangle = 90)
    fig.update_layout(xaxis={'visible': False, 'showticklabels': False},yaxis_title="Citaciones",
                      legend_title='Grupos de Investigación')
    #fig.update_traces(orientation='h')
    fig.update_layout(title={'text':'Distribución de Citaciones: Todos los Productos'})
    maxrange=df.groupby('idgruplac').quantile(0.85).max().iloc[0]
    fig['layout']['yaxis'].update(range=[-0.2,maxrange])
    return fig

#ELEMENTO

def bar_general_element_scopus(data, grupos,elemento): #retorna dos graficas, recibe grupos_codigos y grupos_codigos
    df=data.rename(columns={'idgruplac':'grupo'}).copy()
    df=df[['grupo']]
    df['grupo']=df['grupo'].str.split(';')
    df=df.explode('grupo')
    df=df[df['grupo'].isin(grupos)]
    df['grupo']=df['grupo'].apply(lambda x: gruplac_basico[gruplac_basico['idgruplac']==x.strip()]['nombre'].iloc[0])
    if df['grupo'].nunique()>1:
        df['grupo']=df['grupo'].str.wrap(20,break_long_words=False).str.replace('\n','<br>')
    temp_df=df.copy()
    df=df['grupo'].value_counts()    
    fig = px.bar(df, x=df.index, y=df, color=df.index,
                 labels={
                 "index":"Grupo de Investigación",
                 "y":"Cantidad de "+elemento},
                 orientation='v',color_discrete_sequence=px.colors.sequential.thermal)#paleta de colores
    fig.update_layout(
                font=dict(size=10),
                title={
                'text':"Productos Generados por los Grupos de Investigación: "+elemento,
                #'xanchor':'center',
                #'xref':'paper',
                #'x':0.5,
                #'yanchor':'top',
                #'automargin':True,
                #'font': {'size': 14}
                },
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(t=10, b=2))
    fig.update(layout_showlegend=False)
    if temp_df['grupo'].nunique()>3:
        fig.update_xaxes(tickangle=90)
    #fig.update_layout(height='600')##############
    #fig.update_yaxes(automargin=True)
    #fig.update_xaxes(tickangle=0)
    fig.update_layout(xaxis = dict(tickfont = dict(size=10)))
    return fig

def boxplot_general_element_scopus(data,codigos,elemento):
    df=data[['idgruplac','citado']].copy()
    df['idgruplac']=df['idgruplac'].str.split(';')
    df=df.explode('idgruplac')
    df=df[df['idgruplac'].isin(codigos)]
    df['idgruplac']=df['idgruplac'].apply(lambda x: gruplac_basico[gruplac_basico['idgruplac']==x.strip()]['nombre'].iloc[0])
    df['idgruplac']=df['idgruplac'].str.wrap(20,break_long_words=False).str.replace('\n','<br>')
    df['citado']=df['citado'].astype('int64')
    fig = px.box(df, x="idgruplac", y="citado",color='idgruplac', points='all',hover_data = {'citado':True,'idgruplac':False})
    #if df['idgruplac'].nunique()>3:
    #    fig.update_xaxes(tickangle = 90)
    fig.update_layout(xaxis={'visible': False, 'showticklabels': False},yaxis_title="Citaciones",
                      legend_title='Grupos de Investigación')
    #fig.update_traces(orientation='h')
    fig.update_layout(title={'text':'Distribución de Citaciones: '+elemento})
    maxrange=df.groupby('idgruplac').quantile(0.85).max().iloc[0]
    fig['layout']['yaxis'].update(range=[-0.2,maxrange])
    return fig

#############################################################################
# State Dropdown
#############################################################################


option_group_scopus = dcc.Dropdown(
        id='filter_group_scopus',
        options = opciones_grupo_scopus,
        placeholder='Elija una opción',
        value = None  # Valor inicial seleccionado
    )
option_element_scopus = dcc.Dropdown(
        id='filter_element_scopus',
        options = [],
        placeholder='Grupo Requerido',
        clearable = False,
        disabled=True,
        value = None  # Valor inicial seleccionado
    )
option_parameter_scopus = dcc.Dropdown(
        id='filter_parameter_scopus',
        options = opciones_parametro_general,
        placeholder='Elija una opción',
        value = None  # Valor inicial seleccionado
    )
option_value_scopus = dcc.Dropdown(
        id='filter_value_scopus',
        options = [],
        value = [],  # Valor inicial seleccionado
        placeholder='Elija una opción',
        disabled= True,
        multi=True
    )
option_element_scopus_general = dcc.Dropdown(
        id='filter_element_scopus_general',
        options = options_general_element_scopus,        
        value = None,  # Valor inicial seleccionado
        placeholder='Valor Requerido',
        disabled=True,
        clearable = False,
        maxHeight=160
        # style = {"bottom": "100%", "transform": "translateY(-100%)"}
    )
#############################################################################
# Sidebar Layout
#############################################################################
sidebar_scopus = html.Div([
    # html.H1('Opciones de filtrado',className="text_filter_scopus"),
    html.Hr(),  # Add an horizontal line
    html.H5("Los datos analizados reflejan únicamente la informacion emparejada entre GrupLAC y Scopus.",className="text_filter_scopus"),
    dcc.Tabs(id="tabs_filter_scopus", value='tab_individual', 
    children=[dcc.Tab(label='Individual', value='tab_individual',selected_style={'color':'white','background-color':'#c65721','border-top': '2px solid #93330E'}),
        dcc.Tab(label='General', value='tab_general',selected_style={'color':'white','background-color':'#c65721','border-top': '2px solid #93330E'}),
    ]),       
    html.Div([
        html.H4("Elija un grupo de investigación:",className="text_filter_scopus"),
        option_group_scopus,
        html.H4("Elija el tipo de producto:",className="text_filter_scopus"),
        option_element_scopus,
        html.Button('Filtrar', id='button_scopus_filter_indiv', n_clicks=0),
    ],id="filtro_individual_scopus"),
    html.Div([
        html.H4("Filtrar grupos por:",className="text_filter_scopus"),
        option_parameter_scopus,
        html.H4("Ingrese el valor:",className="text_filter_scopus"),
        option_value_scopus,
        html.H4("Elija el tipo de producto:",className="text_filter_scopus"),
        option_element_scopus_general,
        html.Button('Filtrar', id='button_scopus_filter_group', n_clicks=0),
    ],id="filtro_general_scopus", hidden=True),        
],id="menu_filter_flex_scopus",className="dash-sidebar-graph",style={'background-color':'#A8AAAC'},    
)

#  ---------------------callback---------------
@callback(
    [Output('filtro_individual_scopus', 'hidden'),Output('filtro_general_scopus', 'hidden')],
    Input('tabs_filter_scopus', 'value'), prevent_initial_call=True)
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
        #option_elements= filtro_scopus_grupo_individual(grupo)
        option_elements= [*filtro_scopus_grupo_individual(grupo),'Todos']
        #option_elements.append('Todos')
        return 'Todos', False, option_elements
#-----------------general
@callback(
    [Output('filter_value_scopus', 'value'),Output('filter_value_scopus', 'disabled'),Output('filter_value_scopus', 'options')],
    Input('filter_parameter_scopus', 'value'))
def callback_parameter(parametro):
    if parametro == None:
        return None, True, []
    else:
        option_elements= [*filtro_scopus_parametro_general(parametro),'Todos']
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
    Output('dash_individual_scopus_graph5','figure'),Output('div_group_scopus_figure5','style'),
    Output('dash_individual_scopus_graph6','children'),Output('div_group_scopus_figure6','style'),
    #titulo
    Output('title_individual_scopus_graph1','children'),
    Output('title_individual_scopus_graph2','children'),
    Output('title_individual_scopus_graph3','children'),
    Output('title_individual_scopus_graph4','children'),
    Output('title_individual_scopus_graph5','children'),
    #
    Output('msj_alert_individual_scopus','children'),Output('fade-alert-individual-scopus','is_open'),
    ],
    [State('filter_group_scopus', 'value'), State('filter_element_scopus', 'value'),
    Input('button_scopus_filter_indiv','n_clicks'),State('image_network_path', 'src')]
 , prevent_initial_call=True)
def callback_filter_individual_scopus(grupo, elemento, boton, image_url):
    #print('prueba filtro scopus individual')
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
    dash_individual_scopus_graph5 = {}
    dash_individual_scopus_graph6 = ''
    div_scopus_figure1 = {'display':'none'}
    div_scopus_figure2 = {'display':'none'}
    div_scopus_figure3 = {'display':'none'}
    div_scopus_figure4 = {'display':'none'}
    div_scopus_figure5 = {'display':'none'}
    div_scopus_figure6 = {'display':'none'}
    titulo_individual_scopus1=''
    titulo_individual_scopus2=''
    titulo_individual_scopus3=''
    titulo_individual_scopus4=''
    titulo_individual_scopus5=''   
    msj_alert_individual_scopus = ''
    fade_alert_individual_scopus = False
    
    if boton == 0 or elemento == None or grupo == None:
        return kpi_all_scopus, indicators_group_scopus, products_element_group_scopus, kpi_scopus1, kpi_scopus2, kpi_scopus3, kpi_scopus4, kpi_scopus5, kpi_scopus6, dash_individual_scopus_graph1, div_scopus_figure1, dash_individual_scopus_graph2, div_scopus_figure2, dash_individual_scopus_graph3, div_scopus_figure3, dash_individual_scopus_graph4, div_scopus_figure4, dash_individual_scopus_graph5, div_scopus_figure5, dash_individual_scopus_graph6, div_scopus_figure6, titulo_individual_scopus1, titulo_individual_scopus2, titulo_individual_scopus3, titulo_individual_scopus4, titulo_individual_scopus5, msj_alert_individual_scopus, fade_alert_individual_scopus
    
    
    #indicadores    
    grupo_cod_scopus=get_codigo_grupo(grupo)    
    indicators_group_scopus = 'Grupo: '+grupo
    products_element_group_scopus ='Indicadores analizados para: '+elemento
    data = filtro_scopus_elemento_individual(grupo,elemento) #corroborar
    
    if elemento == 'Todos':
        kpi_all_scopus = {'display':'block','width':'80vw', 'marginLeft':'auto', 'marginRight':'auto'}
        series_scopus=get_series_scopus(grupo_cod_scopus)             
        kpi_scopus1 = str(get_h1_index(grupo_cod_scopus))
        kpi_scopus2 = str(get_h2_index(grupo_cod_scopus))
        kpi_scopus3 = str(authors_count(grupo_cod_scopus))
        kpi_scopus4 = str(products_count(grupo_cod_scopus))
        kpi_scopus5 = str(citation_count(grupo_cod_scopus))  
        kpi_scopus6 = str(citation_output(grupo_cod_scopus) )     
        dash_individual_scopus_graph1 = time_series_all_scopus(series_scopus)
        titulo_individual_scopus1 = get_fig_title(dash_individual_scopus_graph1)
        dash_individual_scopus_graph1.update_layout(title={'text':None})
        dash_individual_scopus_graph2 = bar_all_scopus(grupo_cod_scopus)
        titulo_individual_scopus2 = get_fig_title(dash_individual_scopus_graph2)
        dash_individual_scopus_graph2.update_layout(title={'text':None})
        dash_individual_scopus_graph3 = boxplot_individual(grupo_cod_scopus,data)  #corroborar        
        titulo_individual_scopus3 = get_fig_title(dash_individual_scopus_graph3)
        dash_individual_scopus_graph3.update_layout(title={'text':None})
        dash_individual_scopus_graph4 = tree_author_all_scopus(data)    #corroborar     
        titulo_individual_scopus4 = get_fig_title(dash_individual_scopus_graph4)
        dash_individual_scopus_graph4.update_layout(title={'text':None})
        url_red = './assets/img/network_temp/'+str(collaboration_network(grupo))    
        if url_red=='./assets/img/network_temp/None':
            dash_individual_scopus_graph6=html.Img(src='./assets/img/None.png', id='image_network_path',style={'width':'auto', "height":'90%', 'object-fit': 'contain', 'cursor': 'zoom-in'})
            div_scopus_figure6 = {'display':'block', 'height':'40vh','width':'40vw','marginTop':'3vh','paddingTop':'5px','marginLeft':'auto','marginRight':'auto', 'marginBottom':'7px','textAlign':'center'}
        else:
            dash_individual_scopus_graph6 = html.Img(src=url_red, id='image_network_path',style={'width':'auto', "height":'95%', 'object-fit': 'contain', 'cursor': 'zoom-in'})
            #div_scopus_figure6 = {'display':'block', 'height':'70vh', 'maxHeight':'80vh','marginTop':'5px','paddingTop':'5px','marginLeft':'auto','marginRight':'auto','maxWidth':'80vw', 'marginBottom':'7px','textAlign':'center'}
            div_scopus_figure6 = {'display':'block', 'height':'max-content','marginTop':'3vh','paddingTop':'5px','marginLeft':'auto','marginRight':'auto', 'marginBottom':'7px','textAlign':'center'}
        
        div_scopus_figure1 = {'display':'block', 'height':'70vh', 'maxHeight':'80vh','marginTop':'5px','paddingTop':'5px','marginLeft':'auto','marginRight':'auto','maxWidth':'80vw', 'marginBottom':'7px'}
        div_scopus_figure2 = {'display':'inline-block', 'height':'70vh','maxHeight':'75vh', 'marginBottom':'5px','paddingBottom':'5px', 'marginTop':'7px'}
        div_scopus_figure3 = {'display':'inline-block', 'height':'70vh','maxHeight':'75vh', 'marginBottom':'5px','paddingBottom':'5px', 'marginTop':'7px'}
        div_scopus_figure4 = {'display':'block', 'height':'82vh','maxHeight':'85vh', 'marginTop':'5px', 'marginBottom':'5vh'}
    else:
        if data.shape[0]==0:
            #arreglar
            msj_alert_individual_scopus = 'No existen datos'
            fade_alert_individual_scopus = True
            return kpi_all_scopus, indicators_group_scopus, products_element_group_scopus, kpi_scopus1, kpi_scopus2, kpi_scopus3, kpi_scopus4, kpi_scopus5, kpi_scopus6, dash_individual_scopus_graph1, div_scopus_figure1, dash_individual_scopus_graph2, div_scopus_figure2, dash_individual_scopus_graph3, div_scopus_figure3, dash_individual_scopus_graph4, div_scopus_figure4, dash_individual_scopus_graph5, div_scopus_figure5, dash_individual_scopus_graph6, div_scopus_figure6, titulo_individual_scopus1, titulo_individual_scopus2, titulo_individual_scopus3, titulo_individual_scopus4, titulo_individual_scopus5, msj_alert_individual_scopus, fade_alert_individual_scopus
    
        kpi_all_scopus = {'display':'block','width':'80vw', 'margin-left':'auto', 'margin-right':'auto'}
        series_scopus=get_series_scopus(grupo_cod_scopus,elemento) #OBTIENE LA SERIE RELATIVA AL ELEMENTO
        kpi_scopus1 = str(get_h1_index_relativo(grupo_cod_scopus,elemento))
        kpi_scopus2 = str(get_h2_index(grupo_cod_scopus))
        kpi_scopus3 = str(authors_count(grupo_cod_scopus))
        kpi_scopus4 = str(products_count_relativo(grupo_cod_scopus,elemento))
        kpi_scopus5 = str(citation_count_relativo(grupo_cod_scopus,elemento))
        kpi_scopus6 = str(citation_output_relativo(grupo_cod_scopus,elemento))
        dash_individual_scopus_graph1 = time_series_all_scopus(series_scopus,elemento)
        titulo_individual_scopus1 = get_fig_title(dash_individual_scopus_graph1)
        dash_individual_scopus_graph1.update_layout(title={'text':None})
        div_scopus_figure1 = {'display':'block', 'height':'70vh', 'maxHeight':'80vh','marginTop':'5px','paddingTop':'5px','marginLeft':'auto','marginRight':'auto','maxWidth':'80vw', 'marginBottom':'7px'}
        
        dash_individual_scopus_graph5 = tree_topic_element_scopus(data,elemento)
        titulo_individual_scopus5 = get_fig_title(dash_individual_scopus_graph5)
        dash_individual_scopus_graph5.update_layout(title={'text':None})
        div_scopus_figure5 = {'display':'block', 'height':'70vh', 'maxHeight':'80vh','marginTop':'5px','paddingTop':'5px','marginLeft':'auto','marginRight':'auto','maxWidth':'80vw', 'marginBottom':'7px'}
        if (elemento == 'Libros') or elemento == 'Capítulos':
            dash_individual_scopus_graph2 = pie_journal_element_scopus(data,'nombre_publicacion')
        else:
            dash_individual_scopus_graph2 = pie_journal_element_scopus(data,'editorial')
        titulo_individual_scopus2 = get_fig_title(dash_individual_scopus_graph2)
        dash_individual_scopus_graph2.update_layout(title={'text':None})
        div_scopus_figure2 = {'display':'inline-block', 'height':'70vh','maxHeight':'75vh', 'marginBottom':'5px','paddingBottom':'5px', 'marginTop':'7px'}

        dash_individual_scopus_graph3 = boxplot_individual(grupo_cod_scopus,data,elemento)
        titulo_individual_scopus3 = get_fig_title(dash_individual_scopus_graph3)
        dash_individual_scopus_graph3.update_layout(title={'text':None})
        div_scopus_figure3 = {'display':'inline-block', 'height':'70vh','maxHeight':'75vh', 'marginBottom':'5px','paddingBottom':'5px', 'marginTop':'7px'}

        dash_individual_scopus_graph4 = tree_author_all_scopus(data,elemento) 
        titulo_individual_scopus4 = get_fig_title(dash_individual_scopus_graph4)
        dash_individual_scopus_graph4.update_layout(title={'text':None})      
        div_scopus_figure4 = {'display':'block', 'height':'82vh','maxHeight':'85vh', 'marginTop':'5px', 'marginBottom':'5vh'}

        url_red = './assets/img/network_temp/'+str(collaboration_network(grupo, elemento))    
        if url_red=='./assets/img/network_temp/None':
            dash_individual_scopus_graph6=html.Img(src='./assets/img/None.png', id='image_network_path',style={'width':'auto', "height":'95%', 'object-fit': 'contain', 'cursor': 'zoom-in'})
            div_scopus_figure6 = {'display':'block', 'height':'40vh','width':'40vw','marginTop':'3vh','paddingTop':'5px','marginLeft':'auto','marginRight':'auto', 'marginBottom':'7px','textAlign':'center'}
        else:
            dash_individual_scopus_graph6 = html.Img(src=url_red, id='image_network_path',style={'width':'auto', "height":'95%', 'object-fit': 'contain', 'cursor': 'zoom-in'})
            #div_scopus_figure6 = {'display':'block', 'height':'70vh', 'maxHeight':'80vh','marginTop':'5px','paddingTop':'5px','marginLeft':'auto','marginRight':'auto','maxWidth':'80vw', 'marginBottom':'7px','textAlign':'center'}
            div_scopus_figure6 = {'display':'block', 'height':'max-content','marginTop':'3vh','paddingTop':'5px','marginLeft':'auto','marginRight':'auto', 'marginBottom':'7px','textAlign':'center'}
    
    return kpi_all_scopus, indicators_group_scopus, products_element_group_scopus, kpi_scopus1, kpi_scopus2, kpi_scopus3, kpi_scopus4, kpi_scopus5, kpi_scopus6, dash_individual_scopus_graph1, div_scopus_figure1, dash_individual_scopus_graph2, div_scopus_figure2, dash_individual_scopus_graph3, div_scopus_figure3, dash_individual_scopus_graph4, div_scopus_figure4, dash_individual_scopus_graph5, div_scopus_figure5, dash_individual_scopus_graph6, div_scopus_figure6, titulo_individual_scopus1, titulo_individual_scopus2, titulo_individual_scopus3, titulo_individual_scopus4, titulo_individual_scopus5, msj_alert_individual_scopus, fade_alert_individual_scopus
    
@callback(
    [    
    Output('dash_general_scopus_graph1','figure'),Output('div_general_scopus_figure1','style'),
    Output('dash_general_scopus_graph2','figure'),Output('div_general_scopus_figure2','style'),
    Output('dash_general_scopus_graph3','figure'),Output('div_general_scopus_figure3','style'),
    Output('dash_general_scopus_graph4','figure'),Output('div_general_scopus_figure4','style'),
    Output('dash_general_scopus_graph5','figure'),Output('div_general_scopus_figure5','style'),
    Output('dash_general_scopus_graph6','figure'),Output('div_general_scopus_figure6','style'),
   
    #titulos
    Output('title_general_scopus_graph1','children'),
    Output('title_general_scopus_graph2','children'),
    Output('title_general_scopus_graph3','children'),
    Output('title_general_scopus_graph4','children'),
    Output('title_general_scopus_graph5','children'),
    Output('title_general_scopus_graph6','children'),   
    #
    Output('msj_alert_general_scopus','children'),Output('fade-alert-general-scopus','is_open'),   
    ],
    [State('filter_parameter_scopus', 'value'), State('filter_value_scopus', 'value'), State('filter_element_scopus_general', 'value'),
    Input('button_scopus_filter_group','n_clicks')]
 , prevent_initial_call=True)
def callback_filter_general(parametro, valor, elemento, boton):
    #print('prueba filtro scopus general')
    dash_general_scopus_graph1 = {}
    dash_general_scopus_graph2 = {}
    dash_general_scopus_graph3 = {}
    dash_general_scopus_graph4 = {}
    dash_general_scopus_graph5 = {}
    dash_general_scopus_graph6 = {}
    div_general_scopus_figure1 = {'display':'none'}
    div_general_scopus_figure2 = {'display':'none'}
    div_general_scopus_figure3 = {'display':'none'}
    div_general_scopus_figure4 = {'display':'none'}
    div_general_scopus_figure5 = {'display':'none'}
    div_general_scopus_figure6 = {'display':'none'}
    titulo_general_scopus1=''
    titulo_general_scopus2=''
    titulo_general_scopus3=''
    titulo_general_scopus4=''
    titulo_general_scopus5=''
    titulo_general_scopus6=''
    
    msj_alert_general_scopus = ''
    fade_alert_general_scopus = False      
    if boton == 0 or elemento == None:
        return dash_general_scopus_graph1,div_general_scopus_figure1, dash_general_scopus_graph2, div_general_scopus_figure2, dash_general_scopus_graph3,div_general_scopus_figure3, dash_general_scopus_graph4, div_general_scopus_figure4, dash_general_scopus_graph5, div_general_scopus_figure5, dash_general_scopus_graph6, div_general_scopus_figure6,titulo_general_scopus1,titulo_general_scopus2,titulo_general_scopus3,titulo_general_scopus4,titulo_general_scopus5,titulo_general_scopus6, msj_alert_general_scopus, fade_alert_general_scopus
    
    grupos_codigos_scopus, grupos_nombres_scopus=filtro_scopus_valor_general(parametro,valor)
    cantidad_grupos=len(grupos_codigos_scopus)
    if cantidad_grupos <= 10:
        msj_alert_general_scopus = f'Para el análisis se filtraron {cantidad_grupos} grupos de investigación.'
    else:
        msj_alert_general_scopus = f'Para el análisis se filtraron {cantidad_grupos} grupos de investigación, para la visualización de datos se tiene en cuenta los 10 grupos con mayor cantidad de de datos, si desea analizar grupos específicos elija filtrar grupos por "Ingreso Manual".'
    fade_alert_general_scopus = True
    if elemento == 'Todos':
        df_indicadores, series_scopus = get_indicadores_scopus_general(grupos_codigos_scopus)
        if df_indicadores['idgruplac'].count()>10:
            df_indicadores=df_indicadores.sort_values(by='PC',ascending=False).iloc[:10].sort_index()
            indices_top=list(df_indicadores.index.astype('int64'))
            series_scopus=[series_scopus[x] for x in indices_top]
            grupos_codigos_scopus=df_indicadores['idgruplac'].to_list()
            grupos_nombres_scopus=[gruplac_basico[gruplac_basico['idgruplac'].str.contains(x)]['nombre'].iloc[0] for x in grupos_codigos_scopus]
            indices_top=0
        dash_general_scopus_graph1 = time_series_all_general_scopus(series_scopus,grupos_nombres_scopus)
        titulo_general_scopus1 = get_fig_title(dash_general_scopus_graph1)
        dash_general_scopus_graph1.update_layout(title={'text':None})
        dash_general_scopus_graph2 = bar_general_all_scopus(grupos_codigos_scopus, grupos_nombres_scopus)
        titulo_general_scopus2 = get_fig_title(dash_general_scopus_graph2)
        dash_general_scopus_graph2.update_layout(title={'text':None})
        dash_general_scopus_graph3 = radar_general_all(df_indicadores,elemento='Todos')
        titulo_general_scopus3 = get_fig_title(dash_general_scopus_graph3)
        dash_general_scopus_graph3.update_layout(title={'text':None})
        dash_general_scopus_graph4 = heatmap_general(grupos_codigos_scopus,grupos_nombres_scopus)
        titulo_general_scopus4 = get_fig_title(dash_general_scopus_graph4)
        dash_general_scopus_graph4.update_layout(title={'text':None})
        dash_general_scopus_graph5 = boxplot_general_all_scopus(grupos_codigos_scopus,grupos_nombres_scopus)
        titulo_general_scopus5 = get_fig_title(dash_general_scopus_graph5)
        dash_general_scopus_graph5.update_layout(title={'text':None})
        data=filtro_scopus_elemento_general(grupos_codigos_scopus,elemento) #corroborar
        dash_general_scopus_graph6 = tree_author_all_scopus(data,elemento)
        titulo_general_scopus6 = get_fig_title(dash_general_scopus_graph6)
        dash_general_scopus_graph6.update_layout(title={'text':None})
        div_general_scopus_figure1 = {'display':'block', 'height':'83vh', 'maxHeight':'85vh','marginTop':'5px','paddingBottom':'5px','paddingTop':'5px','marginLeft':'auto','marginRight':'auto','maxWidth':'80vw', 'marginBottom':'7px'}
        #wdg2=str(len(grupos_codigos_scopus)*7.5)+'vw'
        wdg2=len(grupos_codigos_scopus)
        if wdg2 >= 5:
            widthdiv='90vw'
        else:
            widthdiv='50vw'
        div_general_scopus_figure2 = {'display':'block', 'marginLeft':'auto', 'marginRight':'auto','minWidth':'50vw','width':widthdiv, 'height':'83vh','maxHeight':'83vh','marginTop':'8px','paddingTop':'5px','paddingBottom':'5px','marginBottom':'7px'}
        div_general_scopus_figure3 = {'display':'inline-block', 'height':'82vh','maxHeight':'83vh', 'marginTop':'8px', 'marginBottom':'8px'}
        div_general_scopus_figure4 = {'display':'inline-block', 'height':'82vh','maxHeight':'83vh', 'marginTop':'8px', 'marginBottom':'8px'}
        div_general_scopus_figure5 = {'display':'block', 'height':'82vh','maxHeight':'85vh', 'marginTop':'8px', 'marginBottom':'8px'}
        div_general_scopus_figure6 = {'display':'block', 'height':'82vh','maxHeight':'85vh', 'marginTop':'8px', 'marginBottom':'5vh'}
    else:
        df_indicadores, series_scopus = get_indicadores_scopus_relativo(grupos_codigos_scopus,elemento)
        if df_indicadores['idgruplac'].count()>10:
            df_indicadores=df_indicadores.sort_values(by='pc',ascending=False).iloc[:10].sort_index()
            indices_top=list(df_indicadores.index.astype('int64'))
            series_scopus=[series_scopus[x] for x in indices_top]
            grupos_codigos_scopus=df_indicadores['idgruplac'].to_list()
            grupos_nombres_scopus=[gruplac_basico[gruplac_basico['idgruplac'].str.contains(x)]['nombre'].iloc[0] for x in grupos_codigos_scopus]
            indices_top=0
        data=filtro_scopus_elemento_general(grupos_codigos_scopus,elemento)
        if data.shape[0]==0:
            msj_alert_general_scopus = 'No existen datos'
            fade_alert_general_scopus = True
            return dash_general_scopus_graph1,div_general_scopus_figure1, dash_general_scopus_graph2, div_general_scopus_figure2, dash_general_scopus_graph3,div_general_scopus_figure3, dash_general_scopus_graph4, div_general_scopus_figure4, dash_general_scopus_graph5, div_general_scopus_figure5, dash_general_scopus_graph6, div_general_scopus_figure6,titulo_general_scopus1,titulo_general_scopus2,titulo_general_scopus3,titulo_general_scopus4,titulo_general_scopus5,titulo_general_scopus6, msj_alert_general_scopus, fade_alert_general_scopus
    
        dash_general_scopus_graph1 = time_series_all_general_scopus(series_scopus,grupos_nombres_scopus,elemento)
        titulo_general_scopus1 = get_fig_title(dash_general_scopus_graph1)
        dash_general_scopus_graph1.update_layout(title={'text':None})
        div_general_scopus_figure1 = {'display':'block', 'height':'81vh','maxHeight':'83vh','marginTop':'8px','paddingBottom':'8px','paddingTop':'5px','marginLeft':'auto','marginRight':'auto','maxWidth':'80vw', 'marginBottom':'8px'}
        dash_general_scopus_graph2 = bar_general_element_scopus(data, grupos_codigos_scopus,elemento)
        titulo_general_scopus2 = get_fig_title(dash_general_scopus_graph2)
        dash_general_scopus_graph2.update_layout(title={'text':None})
        #wdg2=str(len(grupos_codigos_scopus)*7)+'vw'
        wdg2=len(grupos_codigos_scopus)
        if wdg2 >= 5:
            widthdiv='90vw'
        else:
            widthdiv='50vw'
        div_general_scopus_figure2 = {'display':'block', 'marginLeft':'auto', 'marginRight':'auto', 'minWidth':'50vw','width':widthdiv, 'height':'81vh','maxHeight':'90vh','marginTop':'8px','paddingTop':'5px','paddingBottom':'5px','marginBottom':'8px'}
        dash_general_scopus_graph3 = radar_general_all(df_indicadores,elemento)
        titulo_general_scopus3 = get_fig_title(dash_general_scopus_graph3)
        dash_general_scopus_graph3.update_layout(title={'text':None})
        div_general_scopus_figure3 = {'display':'inline-block', 'height':'82vh','maxHeight':'83vh', 'marginTop':'8px', 'marginBottom':'8px'}
        if (elemento == 'Libros') or elemento == 'Capítulos':
            dash_general_scopus_graph4 = pie_journal_element_scopus(data,'nombre_publicacion')
        else:
            dash_general_scopus_graph4 = pie_journal_element_scopus(data,'editorial')
        titulo_general_scopus4 = get_fig_title(dash_general_scopus_graph4)
        dash_general_scopus_graph4.update_layout(title={'text':None})
        div_general_scopus_figure4 = {'display':'inline-block', 'height':'82vh','maxHeight':'83vh', 'marginTop':'8px', 'marginBottom':'8px'}
        
        dash_general_scopus_graph5 = boxplot_general_element_scopus(data,grupos_codigos_scopus,elemento)
        titulo_general_scopus5 = get_fig_title(dash_general_scopus_graph5)
        dash_general_scopus_graph5.update_layout(title={'text':None})
        div_general_scopus_figure5 = {'display':'block', 'height':'82vh','maxHeight':'85vh', 'marginTop':'8px', 'marginBottom':'8px'}

        dash_general_scopus_graph6 = tree_author_all_scopus(data,elemento)
        titulo_general_scopus6 = get_fig_title(dash_general_scopus_graph6)
        dash_general_scopus_graph6.update_layout(title={'text':None})
        div_general_scopus_figure6 = {'display':'block', 'height':'82vh','maxHeight':'85vh', 'marginTop':'8px', 'marginBottom':'5vh'}
              
    return dash_general_scopus_graph1,div_general_scopus_figure1, dash_general_scopus_graph2, div_general_scopus_figure2, dash_general_scopus_graph3,div_general_scopus_figure3, dash_general_scopus_graph4, div_general_scopus_figure4, dash_general_scopus_graph5, div_general_scopus_figure5, dash_general_scopus_graph6, div_general_scopus_figure6,titulo_general_scopus1,titulo_general_scopus2,titulo_general_scopus3,titulo_general_scopus4,titulo_general_scopus5,titulo_general_scopus6, msj_alert_general_scopus, fade_alert_general_scopus

# @callback(
#      Output('title_individual_scopus_graph6', 'children'),
#      Input('image_network_path', 'src'))
# def remove_image_network(image_url):
#     print(image_url)
#     try:
#         if image_url != './assets/img/init.png':
#             if image_url != './assets/img/None.png':
#                 os.remove(image_url)
#     except:
#         pass
#     return no_update