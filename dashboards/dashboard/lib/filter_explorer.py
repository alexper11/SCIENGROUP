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

def filtrar_elemento(elemento,fuente,condicion):
    data=fuente_dic[fuente].copy()
    data=data[elemento]
    opc_caracteristica=pd.Series(data.columns).replace(caracteristicas).to_list()
    opc_caracteristica.append('Todos')
    if condicion=='option':
        return opc_caracteristica
    elif condicion=='data':
        return data

def filtrar_caracteristica(caracteristica,elemento,fuente):
    data=fuente_dic[fuente][elemento].fillna('No Aplica').copy()
    #sectores borrar
    if caracteristica=='Sectores':
        data=data.replace(to_replace={',':';'},regex=True)
    ####
    if caracteristica=='Todos':
        #campo de entrada desaparece
        entrada_new=None
        opc_entrada=[]
    #tags, en este caso la entrada es una lista de elementos
    elif caracteristica in ['Tipo','Lugar','Revista','ISSN','Editorial','Disponibilidad',
                          'Mercado','Aval','Programas','Idioma','Agencia Fundadora',
                          'Verificado','Certificación','Clasificación','Categoría','Sexo',
                          'Área']:  
        entrada_new=[]
        opc_entrada=data[caracteristicas_invertido[caracteristica]].drop_duplicates(keep='first').to_list()
        print(opc_entrada)
        
    elif caracteristica in ['Áreas','Temáticas','Palabras Clave de Autor','Palabras Clave Indizadas',
                           'Líneas de Investigación','Institución','Palabras Clave','Sectores','País',
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
        opc_entrada=[]
    #date(years), tipo tuple con dos int
    else:
        
        entrada_new=()
        opc_entrada=[]
        #Las opciones de entrada en este caso son para dos campos, ya sea dos años fecha o dos valores count
        #se debe asegurar que el primer campo reciba una fecha o numero y que el segundo campo valide que el valor
        #ingresado sea mayor que el del campo anterior, si no ocurriran errores internos en el filtrado de 
        #dataframes por inconsistencia lógica.
    return entrada_new, opc_entrada

def filtrar_entrada(entrada,caracteristica,elemento,fuente):
    data=fuente_dic[fuente][elemento].copy()
    if type(entrada) == list:
        data = data.fillna('No Aplica')
        data=data.replace(to_replace={'\(':'','\)':''},regex=True)
        if caracteristica in ['Áreas','Temáticas','Palabras Clave de Autor','Palabras Clave Indizadas',
                             'Líneas de Investigación','Institución','Palabras Clave','Sectores',
                             'Palabras Clave','Código de GrupLAC']:
            if len(entrada)>1:
                regex_entrada=re.compile('|'.join(entrada)).pattern
            else:
                regex_entrada=entrada[0].strip()
        else:
            if len(entrada)>1:
                regex_entrada='^'+re.compile('$|^'.join(entrada)).pattern+'$'
            else:
                regex_entrada=entrada[0].strip()
        #grupos=dataset[dataset[caracteristicas_invertido[caracteristica_seleccionada]].str.contains(regex_entrada,regex=True)]['idgruplac'].drop_duplicates(keep='first').to_list()
        data=data.dropna(subset=caracteristicas_invertido[caracteristica])
        data=data[data[caracteristicas_invertido[caracteristica]].str.strip().str.contains(regex_entrada,regex=True)]
        
    elif type(entrada) == str:
        data = data.fillna('No Aplica')
        #grupos=dataset[dataset[caracteristicas_invertido[caracteristica_seleccionada]].str.contains(entrada)]['idgruplac'].drop_duplicates(keep='first').to_list()
        data=data.dropna(subset=caracteristicas_invertido[caracteristica])
        data=data[data[caracteristicas_invertido[caracteristica]].str.contains(entrada)]
    
    else:
        data = data.dropna(subset=caracteristicas_invertido[caracteristica])
        data=data[(data[caracteristicas_invertido[caracteristica]].dt.year >= entrada[0]) & (data[caracteristicas_invertido[caracteristica]].dt.year <= entrada[1])]
        data = data.sort_values(by=caracteristicas_invertido[caracteristica])

    return data



##############################################################################
# key Picker
##############################################################################
# palabras=pd.Series([x.strip() for item in df_articulos.palabras.str.split(',') for x in item if x.strip() != '']).value_counts()
# key_picker = dcc.Dropdown(id="key_dropdown", options=[{"label": palabra, "value": palabra} for palabra in palabras.index], multi=True)

# Define las opciones del Dropdown
option_source = dcc.Dropdown(
    id='filter_fuente',
    options = opciones_fuente,
    value = 'CVLAC',  # Valor inicial seleccionado
    clearable = False
)
option_element = dcc.Dropdown(
    id='filter_element',
    options = opciones_elemento,
    value = None  # Valor inicial seleccionado
)
component_filters= html.Div(children=[html.H5("Caracteristica:",className="title_white",style={"color":"white"}),
        html.Div(
            dcc.Dropdown(
                id='filter_feature',
                options = [],
                disabled =True,
                value = None
            ),
        id='div_feature'),
        html.H5("Entrada:",className="title_white",style={"color":"white"}),
        html.Div(children=[
            dcc.Input(
                id='filter_input',
                placeholder='Inactivo',
                disabled =True,
                value = None
            )],
        id='div_input')],
id='component_filters')

#############################################################################
# Sidebar Layout
#############################################################################
sidebar_explorer = html.Div(
    [
        html.P("Filtros para explorar los datos.",style={"color":"white"} ),   
        html.Hr(),  
        ####################################################
        # Layout static here
        ####################################################
        html.H5("Fuente:",className="title_white",style={"color":"white"}),
        option_source,
        html.H5("Elemento:",className="title_white",style={"color":"white"}),
        option_element,
        ####################################################
        # Layout dynamic here
        ####################################################
        component_filters,
        html.Button('Filtrar', id='button_state', n_clicks=0),
    ],
    className="dash-sidebar",    
)
def dataset_explorer (dataset_base,elemento,fuente):
    #dataset_explorador=globals()[str(referencias[fuente][elemento])].iloc[list(dataset_base.index)]
    dataset_explorador=dataset_base
    return dataset_explorador