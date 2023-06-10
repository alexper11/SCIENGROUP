# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import json
from datetime import datetime as dt
# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

#### cod alex
import pandas as pd
import numpy as np
import json
import re

# LOAD THE DIFFERENT FILES
from functions.csv_importer import fuente_dic, referencias, caracteristicas, caracteristicas_invertido#, elementos, elementos_cvlac, elementos_scopus
#from functions.csv_importer import gruplac_articulos, gruplac_basico, gruplac_caplibros, gruplac_integrantes,gruplac_libros, gruplac_oarticulos, gruplac_olibros, gruplac_cdoctorado, gruplac_cmaestria, gruplac_disenoind,gruplac_empresatec,gruplac_innovaempresa,gruplac_instituciones,gruplac_lineas,gruplac_otecnologicos,gruplac_pdoctorado,gruplac_plantapiloto,gruplac_pmaestria,gruplac_prototipos,gruplac_software,scopus_autores,scopus_productos,cvlac_articulos,cvlac_basico,cvlac_caplibros,cvlac_libros,cvlac_empresatec,cvlac_innovaempresa,cvlac_lineas,cvlac_tecnologicos,cvlac_prototipos,cvlac_software,cvlac_areas,cvlac_reconocimiento,cvlac_identificadores


####################################################################################
# Add the dash_Img
####################################################################################

#################################################################################
#Inicialización de parametros necesarios para filtros de explorador del dashboard
#################################################################################

#Opciones de fuentes a mostrar...
opciones_fuente=list(fuente_dic.keys())

#Opciones de elementos a mostrar...
opciones_elemento=[] #Esto solo debe ocurrir al iniciar el dashboard

#Opciones de caracteristicas a mostrar....
opciones_caracteristica=[] #Esto solo debe ocurrir al iniciar el dashboard
#Si opciones_caracteristica=['Todos']: entrada desaparece

#Estado del filtro de entrada del usuario
opciones_entrada=None
valor_entrada=None

#Selecciones o datos ingresados a los campos de los filtros
fuente_seleccionada='CVLAC'
#
caracteristica_seleccionada=None
entrada_seleccionada=None

dataset=pd.DataFrame()


def filtrar_fuente(fuente, condicion):
    data=fuente_dic[fuente]
    #Opciones de elementos a mostrar...
    if condicion=='option':
        opc_elemento=list(data.keys())#El cambio de esta variable debe afectar directamente el filtro elemento
        return opc_elemento
    elif condicion=='data':
        data=pd.DataFrame()
        return data

def filtrar_elemento(elemento,fuente):
    data=fuente_dic[fuente]  
    data=data[elemento]#############
    #Opciones de caracteristicas a mostrar....
    opc_caracteristica=pd.Series(data.columns).replace(caracteristicas).to_list()
    opc_caracteristica.append('Todos')
    #opc_caracteristica.append('Contador')
    entrada_new=None
    return data, opc_caracteristica, entrada_new

def filtrar_caracteristica(caracteristica,elemento,fuente):
    data=fuente_dic[fuente][elemento]    
        
    if caracteristica=='Todos':
        #campo de entrada desaparece
        entrada_new=None
        opc_entrada=None
    #tags, en este caso la entrada es una lista de elementos
    elif caracteristica in ['Tipo','Lugar','Revista','ISSN','Editorial','Disponibilidad',
                          'Mercado','Aval','Programas','Idioma','Agencia Fundadora','País',
                          'Verificado','Certificación','Clasificación','Categoría','Sexo',
                          'Área']:  
        entrada_new=[]
        opc_entrada=data[caracteristicas_invertido[caracteristica]].drop_duplicates(keep='first').to_list()
        
    elif caracteristica in ['Áreas','Temáticas','Palabras Clave de Autor','Palabras Clave Indizadas',
                           'Líneas de Investigación','Institución','Palabras Clave','Sectores',
                           'Palabras Clave']:
    
        entrada_new=[]
        new_list=[]
        data.dropna(subset=caracteristicas_invertido[caracteristica])[caracteristicas_invertido[caracteristica]].astype('object').str.split(';').apply(lambda x: new_list.extend(x))
        opc_entrada=list(filter(None,list(set(new_list))))
    #text, tipo string
    elif caracteristica in ['Código de GrupLAC','Nombre','Nombre del Capítulo','Libro','Nombre del Curso',
                            'Nombre del Programa','Nombre Comercial','Título','Código de CVLAC','Plataforma',
                            'Ambiente']:
        entrada_new=''
        opc_entrada=None
    #date(years), tipo tuple con dos int
    else:
        
        entrada_new=()
        opc_entrada=None
        #Las opciones de entrada en este caso son para dos campos, ya sea dos años fecha o dos valores count
        #se debe asegurar que el primer campo reciba una fecha o numero y que el segundo campo valide que el valor
        #ingresado sea mayor que el del campo anterior, si no ocurriran errores internos en el filtrado de 
        #dataframes por inconsistencia lógica.
        
    return entrada_new, opc_entrada

def filtrar_entrada(entrada,elemento_sel):
    try:
        if len(entrada_seleccionada)>1:
            data=fuente_dic[fuente_seleccionada][elemento_sel]
        else:
            data=dataset.copy()
    except:
        data=dataset.copy()
    if type(entrada) == list:
        if caracteristica_seleccionada in ['Áreas','Temáticas','Palabras Clave de Autor','Palabras Clave Indizadas',
                                           'Líneas de Investigación','Institución','Palabras Clave','Sectores',
                                           'Palabras Clave','Código de GrupLAC']:
            if len(entrada)>1:
                regex_entrada=re.compile('|'.join(entrada)).pattern
            else:
                regex_entrada=entrada[0]
        else:
            if len(entrada)>1:
                regex_entrada='^'+re.compile('$|^'.join(entrada)).pattern+'$'
            else:
                regex_entrada=entrada[0]
        #grupos=dataset[dataset[caracteristicas_invertido[caracteristica_seleccionada]].str.contains(regex_entrada,regex=True)]['idgruplac'].drop_duplicates(keep='first').to_list()
        data=data.dropna(subset=caracteristicas_invertido[caracteristica_seleccionada])
        data=data[data[caracteristicas_invertido[caracteristica_seleccionada]].str.contains(regex_entrada,regex=True)]

    elif type(entrada) == str:
        #grupos=dataset[dataset[caracteristicas_invertido[caracteristica_seleccionada]].str.contains(entrada)]['idgruplac'].drop_duplicates(keep='first').to_list()
        data=data.dropna(subset=caracteristicas_invertido[caracteristica_seleccionada])
        data=data[data[caracteristicas_invertido[caracteristica_seleccionada]].str.contains(entrada)]
    
    else:
        if caracteristica_seleccionada=='Citaciones':
            #grupos...
            data=data.dropna(subset=caracteristicas_invertido[caracteristica_seleccionada])
            data=data[(data[caracteristicas_invertido[caracteristica_seleccionada]] >= entrada[0]) & (data[caracteristicas_invertido[caracteristica_seleccionada]] <= entrada[1])]

        else:
            #grupos=dataset[(dataset[caracteristicas_invertido[caracteristica_seleccionada]].dropna().dt.year >= entrada[0]) & (dataset[caracteristicas_invertido[caracteristica_seleccionada]].dropna().dt.year <= entrada[1])]['idgruplac'].drop_duplicates(keep='first').to_list()
            data=data.dropna(subset=caracteristicas_invertido[caracteristica_seleccionada])
            data=data[(data[caracteristicas_invertido[caracteristica_seleccionada]].dt.year >= entrada[0]) & (data[caracteristicas_invertido[caracteristica_seleccionada]].dt.year <= entrada[1])]

    return data#,grupos



##############################################################################
# key Picker
##############################################################################
# palabras=pd.Series([x.strip() for item in df_articulos.palabras.str.split(',') for x in item if x.strip() != '']).value_counts()
# key_picker = dcc.Dropdown(id="key_dropdown", options=[{"label": palabra, "value": palabra} for palabra in palabras.index], multi=True)

# Define las opciones del Dropdown
option_source = dcc.Dropdown(
    id='filter_fuente',
    options = opciones_fuente,
    value = 'CVLAC'  # Valor inicial seleccionado
    )

option_input= html.Div(
    id='option_inputs'
)
option_element = dcc.Dropdown(
    id='filter_element',
    options = opciones_elemento,
    #value = ''  # Valor inicial seleccionado
)
option_feature = dcc.Dropdown(
    id='filter_feature',
    options = opciones_caracteristica,
    #value = None  # Valor inicial seleccionado
)
value_input = dcc.Input(
    id='input_value',
    placeholder='Digite el filtro',
    type='text',
    #value=''
)
# key_picker = dcc.Dropdown(
#     id="input_tags",
#     # options=[{"label": tags, "value": tags} for tags in opciones_entrada.index],
#     options= opciones_entrada,
#     multi=True
# )
#############################################################################
# Sidebar Layout
#############################################################################
sidebar_explorer = html.Div(
    [
        html.P("Filtros para explorar los datos.",style={"color":"white"} ),   
        html.Hr(),  # Add an horizontal line
        ####################################################
        # Place the rest of Layout here
        ####################################################
        html.H5("Elija la fuente:",className="title_white",style={"color":"white"}),
        option_source,
        html.H5("Elija el elemento:",className="title_white",style={"color":"white"}),
        option_element,
        html.H5("Elija una caracteristica:",className="title_white",style={"color":"white"}),
        option_feature,
        html.H5("Entrada:",className="title_white",style={"color":"white"}),
        option_input,
    ],
    className="dash-sidebar",    
)
def dataset_explorer (dataset_base,elemento,fuente):
    #dataset_explorador=globals()[str(referencias[fuente][elemento])].iloc[list(dataset_base.index)]
    dataset_explorador=dataset_base
    return dataset_explorador