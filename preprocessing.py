from cvlac.db_cvlac import session as cvlac_session
from cvlac.db_gruplac import session as gruplac_session
from scopus.scopusdb import session as scopus_session

import pandas as pd
import numpy as np
import json
import re
import shutil
import os

try:
    print("######### INICIO DE PREPROCESAMIENTO ############")
    shutil.rmtree('dashboard/assets/data/preprocessed_data')
    os.mkdir('dashboard/assets/data/preprocessed_data')
    print('preprocessed folder created')
except Exception as e:
    os.mkdir('dashboard/assets/data/preprocessed_data')
    print(e)
    pass

try:
    ############################################
    #SELECCIÓN DE TABLAS EN BASES DE DATOS: OPCIÓN 1
    ###########################################
    print("")
    print("RECUPERANDO TABLAS DE BASES DE DATOS...")
    #cvlac
    gruplac_articulos = pd.read_sql_query('SELECT * FROM articulos', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_articulos=gruplac_articulos.drop('id',axis=1)
    gruplac_basico = pd.read_sql_query('SELECT * FROM basico', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    #gruplac_basico=gruplac_basico.drop('id',axis=1)
    gruplac_caplibros = pd.read_sql_query('SELECT * FROM caplibros', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_caplibros=gruplac_caplibros.drop('id',axis=1)
    gruplac_integrantes = pd.read_sql_query('SELECT * FROM integrantes', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_integrantes=gruplac_integrantes.drop('id',axis=1)
    gruplac_libros = pd.read_sql_query('SELECT * FROM libros', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_libros=gruplac_libros.drop('id',axis=1)
    gruplac_oarticulos = pd.read_sql_query('SELECT * FROM otros_articulos', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_oarticulos=gruplac_oarticulos.drop('id',axis=1)
    gruplac_olibros = pd.read_sql_query('SELECT * FROM otros_libros', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_olibros=gruplac_olibros.drop('id',axis=1)
    gruplac_cdoctorado= pd.read_sql_query('SELECT * FROM curso_doctorado', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_cdoctorado=gruplac_cdoctorado.drop('id',axis=1)
    gruplac_cmaestria= pd.read_sql_query('SELECT * FROM curso_maestria', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_cmaestria=gruplac_cmaestria.drop('id',axis=1)
    gruplac_disenoind= pd.read_sql_query('SELECT * FROM diseno_industrial', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_disenoind=gruplac_disenoind.drop('id',axis=1)
    gruplac_empresatec= pd.read_sql_query('SELECT * FROM empresa_tecnologica', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_empresatec=gruplac_empresatec.drop('id',axis=1)
    gruplac_innovaempresa= pd.read_sql_query('SELECT * FROM innovacion_empresarial', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_innovaempresa=gruplac_innovaempresa.drop('id',axis=1)
    gruplac_instituciones= pd.read_sql_query('SELECT * FROM instituciones', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_instituciones=gruplac_instituciones.drop('id',axis=1)
    gruplac_lineas= pd.read_sql_query('SELECT * FROM lineas', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_lineas=gruplac_lineas.drop('id',axis=1)
    gruplac_otecnologicos= pd.read_sql_query('SELECT * FROM otros_tecnologicos', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_otecnologicos=gruplac_otecnologicos.drop('id',axis=1)
    gruplac_pdoctorado= pd.read_sql_query('SELECT * FROM programa_doctorado', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_pdoctorado=gruplac_pdoctorado.drop('id',axis=1)
    gruplac_plantapiloto= pd.read_sql_query('SELECT * FROM planta_piloto', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_plantapiloto=gruplac_plantapiloto.drop('id',axis=1)
    gruplac_pmaestria= pd.read_sql_query('SELECT * FROM programa_maestria', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_pmaestria=gruplac_pmaestria.drop('id',axis=1)
    gruplac_prototipos= pd.read_sql_query('SELECT * FROM prototipos', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_prototipos=gruplac_prototipos.drop('id',axis=1)
    gruplac_software= pd.read_sql_query('SELECT * FROM software', gruplac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    gruplac_software=gruplac_software.drop('id',axis=1)
    scopus_autores= pd.read_sql_query('SELECT * FROM autores', scopus_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    scopus_autores=scopus_autores.drop('id',axis=1)
    scopus_productos=pd.read_sql_query('SELECT * FROM productos', scopus_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    scopus_productos=scopus_productos.drop('id',axis=1)
    cvlac_areas=pd.read_sql_query('SELECT * FROM actuacion', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_areas=cvlac_areas.drop('id',axis=1)
    cvlac_articulos=pd.read_sql_query('SELECT * FROM articulos', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_articulos=cvlac_articulos.drop('id',axis=1)
    cvlac_basico=pd.read_sql_query('SELECT * FROM basico', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    #cvlac_basico=cvlac_basico.drop('id',axis=1)
    cvlac_lineas=pd.read_sql_query('SELECT * FROM investigacion', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_lineas=cvlac_lineas.drop('id',axis=1)
    cvlac_libros=pd.read_sql_query('SELECT * FROM libros', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_libros=cvlac_libros.drop('id',axis=1)
    cvlac_reconocimiento=pd.read_sql_query('SELECT * FROM reconocimiento', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_reconocimiento=cvlac_reconocimiento.drop('id',axis=1)
    cvlac_caplibros=pd.read_sql_query('SELECT * FROM caplibros', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_caplibros=cvlac_caplibros.drop('id',axis=1)
    cvlac_empresatec=pd.read_sql_query('SELECT * FROM empresa_tecnologica', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_empresatec=cvlac_empresatec.drop('id',axis=1)
    cvlac_innovaempresa=pd.read_sql_query('SELECT * FROM innovacion_empresarial', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_innovaempresa=cvlac_innovaempresa.drop('id',axis=1)
    cvlac_prototipos=pd.read_sql_query('SELECT * FROM prototipo', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_prototipos=cvlac_prototipos.drop('id',axis=1)
    cvlac_software=pd.read_sql_query('SELECT * FROM software', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_software=cvlac_software.drop('id',axis=1)
    cvlac_tecnologicos=pd.read_sql_query('SELECT * FROM tecnologicos', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_tecnologicos=cvlac_tecnologicos.drop('id',axis=1)
    cvlac_identificadores=pd.read_sql_query('SELECT * FROM identificadores', cvlac_session.bind, dtype = str).replace({'NaN':np.nan,'N.A':np.nan, '':np.nan, 'N/A':np.nan})
    cvlac_identificadores=cvlac_identificadores.drop('id',axis=1)
    gruplac_duplicados={'articulos':[],'libros':[],'oarticulos':[],'libros':[],'olibros':[],'caplibros':[],'otecnologicos':[],'software':[],'prototipos':[]}
except Exception as e:
    #raise
    print(e)
    ############################################
    #ENTRADA DE DATOS EXTRAIDOS: OPCION 2
    ############################################
    print("")
    print("RECUPERANDO TABLAS LOCALES EXTRAIDAS...")
    gruplac_articulos = pd.read_csv('dashboard/assets/data/extracted_data/aux_articulosg.csv', dtype = str)
    gruplac_basico = pd.read_csv('dashboard/assets/data/extracted_data/aux_basicog.csv', dtype = str)
    gruplac_caplibros = pd.read_csv('dashboard/assets/data/extracted_data/aux_caplibrosg.csv', dtype = str)
    gruplac_integrantes = pd.read_csv('dashboard/assets/data/extracted_data/aux_integrantes.csv', dtype = str)
    gruplac_libros = pd.read_csv('dashboard/assets/data/extracted_data/aux_librosg.csv', dtype = str) 
    gruplac_oarticulos = pd.read_csv('dashboard/assets/data/extracted_data/aux_oarticulos.csv', dtype = str)
    gruplac_olibros = pd.read_csv('dashboard/assets/data/extracted_data/aux_olibros.csv', dtype = str)
    gruplac_cdoctorado= pd.read_csv('dashboard/assets/data/extracted_data/aux_cdoctorado.csv', dtype = str)
    gruplac_cmaestria= pd.read_csv('dashboard/assets/data/extracted_data/aux_cmaestria.csv', dtype = str)
    gruplac_disenoind= pd.read_csv('dashboard/assets/data/extracted_data/aux_disenoind.csv', dtype = str)
    gruplac_empresatec= pd.read_csv('dashboard/assets/data/extracted_data/aux_empresatecg.csv', dtype = str)
    gruplac_innovaempresa= pd.read_csv('dashboard/assets/data/extracted_data/aux_innovaempresag.csv', dtype = str)
    gruplac_instituciones= pd.read_csv('dashboard/assets/data/extracted_data/aux_instituciones.csv', dtype = str)
    gruplac_lineas= pd.read_csv('dashboard/assets/data/extracted_data/aux_lineas.csv', dtype = str)
    gruplac_otecnologicos= pd.read_csv('dashboard/assets/data/extracted_data/aux_otecnologicos.csv', dtype = str)
    gruplac_pdoctorado= pd.read_csv('dashboard/assets/data/extracted_data/aux_pdoctorado.csv', dtype = str)
    gruplac_plantapiloto= pd.read_csv('dashboard/assets/data/extracted_data/aux_plantapilotog.csv', dtype = str)
    gruplac_pmaestria= pd.read_csv('dashboard/assets/data/extracted_data/aux_pmaestria.csv', dtype = str)
    gruplac_prototipos= pd.read_csv('dashboard/assets/data/extracted_data/aux_prototiposg.csv', dtype = str)
    gruplac_software= pd.read_csv('dashboard/assets/data/extracted_data/aux_softwareg.csv', dtype = str)
    scopus_autores= pd.read_csv('dashboard/assets/data/extracted_data/aux_autores.csv', dtype = str)
    scopus_productos=pd.read_csv('dashboard/assets/data/extracted_data/aux_productos.csv', dtype = str)
    cvlac_areas=pd.read_csv('dashboard/assets/data/extracted_data/aux_actuacion.csv', dtype = str)
    cvlac_articulos=pd.read_csv('dashboard/assets/data/extracted_data/aux_articulos.csv', dtype = str)
    cvlac_basico=pd.read_csv('dashboard/assets/data/extracted_data/aux_basico.csv', dtype = str)
    cvlac_lineas=pd.read_csv('dashboard/assets/data/extracted_data/aux_investigacion.csv', dtype = str)
    cvlac_libros=pd.read_csv('dashboard/assets/data/extracted_data/aux_libros.csv', dtype = str)
    cvlac_reconocimiento=pd.read_csv('dashboard/assets/data/extracted_data/aux_reconocimiento.csv', dtype = str)
    cvlac_caplibros=pd.read_csv('dashboard/assets/data/extracted_data/aux_caplibros.csv', dtype = str)
    cvlac_empresatec=pd.read_csv('dashboard/assets/data/extracted_data/aux_empresatec.csv', dtype = str)
    cvlac_innovaempresa=pd.read_csv('dashboard/assets/data/extracted_data/aux_innovaempresa.csv', dtype = str)
    cvlac_prototipos=pd.read_csv('dashboard/assets/data/extracted_data/aux_prototipo.csv', dtype = str)
    cvlac_software=pd.read_csv('dashboard/assets/data/extracted_data/aux_software.csv', dtype = str)
    cvlac_tecnologicos=pd.read_csv('dashboard/assets/data/extracted_data/aux_tecnologicos.csv', dtype = str)
    cvlac_identificadores=pd.read_csv('dashboard/assets/data/extracted_data/aux_identificadores.csv', dtype = str)
    gruplac_duplicados={'articulos':[],'libros':[],'oarticulos':[],'libros':[],'olibros':[],'caplibros':[],'otecnologicos':[],'software':[],'prototipos':[]}

###########################################
#PREPROCESSING
##########################################
print("Limpiando datos...")
#LIMPIEZA DE TABLAS CVLAC

cvlac_basico['categoria']=cvlac_basico['categoria'].fillna('No Aplica').astype(str).str.extract(r'(^[^(]*)',expand=False).replace('','No Aplica')
cvlac_basico['sexo']=cvlac_basico['sexo'].replace('','No Aplica').fillna('No Aplica')
cvlac_areas['areas']=cvlac_areas['areas'].astype(str).replace(' -- ',';',regex=True)
cvlac_articulos['tipo']=cvlac_articulos['tipo'].fillna('No Aplica').astype(str).str.extract(r'([^-]*$)',expand=False).replace('','No Aplica').str.strip()
cvlac_articulos['sectores']=cvlac_articulos['sectores'].fillna('No Aplica').astype(str).str.extract(r'(^[^-]*)',expand=False).replace('','No Aplica').str.strip()
cvlac_articulos['lugar']=cvlac_articulos['lugar'].fillna('No Aplica')
#remover duplicados por doi,idgruplac y mantener el registro con mas columnas rellenadas
cvlac_articulos['issn']=cvlac_articulos['issn'].replace('','No Aplica',regex=True).fillna('No Aplica')
cvlac_articulos['fecha']=pd.to_datetime(cvlac_articulos['fecha']).dt.to_period('Y')
cvlac_articulos['palabras']=cvlac_articulos['palabras'].fillna('No Aplica').astype(str).replace(', ',';',regex=True)
cvlac_articulos['revista']=cvlac_articulos['revista'].fillna('No Aplica')
col=cvlac_articulos.copy()
col['revista']=col['revista'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
byrevi_normalized=col.groupby('revista')
for key in list(byrevi_normalized.groups.keys()):  
    cvlac_articulos.iloc[list(byrevi_normalized.get_group(key).index),6]=cvlac_articulos.iloc[list(byrevi_normalized.get_group(key).index)]['revista'].value_counts().index[0]
byrevi_normalized=0
col['editorial']=col['editorial'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('editorial')
col=0
for key in list(bydept_normalized.groups.keys()):  
    cvlac_articulos.iloc[list(bydept_normalized.get_group(key).index),8]=cvlac_articulos.iloc[list(bydept_normalized.get_group(key).index)]['editorial'].value_counts().index[0]
bydept_normalized=0
cvlac_lineas['nombre']=cvlac_lineas['nombre'].replace('','No Aplica')
cvlac_libros['tipo']=cvlac_libros['tipo'].fillna('No Aplica').astype(str).str.extract(r'([^-]*$)',expand=False).replace('','No Aplica').str.strip()
cvlac_libros['lugar']=cvlac_libros['lugar'].fillna('No Aplica')
#remover  duplicados por (isbn limpio),idgruplac mantener el registro con mas columnas rellenas
cvlac_libros['fecha']=pd.to_datetime(cvlac_libros['fecha']).dt.to_period('Y')
cvlac_libros['editorial']=cvlac_libros['editorial'].fillna('No Aplica')
cvlac_libros['palabras']=cvlac_libros['palabras'].fillna('No Aplica').astype(str).replace(', ',';',regex=True)
cvlac_libros['areas']=cvlac_libros['areas'].fillna('No Aplica').astype(str).replace(' -- ',';',regex=True)
cvlac_libros['sectores']=cvlac_libros['sectores'].fillna('No Aplica').astype(str).str.extract(r'(^[^-]*)',expand=False).replace('','No Aplica').str.strip()
col=cvlac_libros.copy()
col['editorial']=col['editorial'].str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9]','', regex=True).str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip() 
byedit_normalized=col.groupby('editorial')
for key in list(byedit_normalized.groups.keys()):  
    cvlac_libros.iloc[list(byedit_normalized.get_group(key).index),7]=cvlac_libros.iloc[list(byedit_normalized.get_group(key).index)]['editorial'].value_counts().index[0]
byedit_normalized=0
col=0
cvlac_reconocimiento['fecha']=pd.to_datetime(cvlac_reconocimiento['fecha'].astype(str).str.extract(r'([^ ]*$)',expand=False).str.strip()).dt.to_period('Y')
cvlac_caplibros['libro']=cvlac_caplibros['libro'].replace('&gt;','',regex=True)
cvlac_caplibros['lugar']=cvlac_caplibros['lugar'].fillna('No Aplica')
#remover duplicados por capitulo,idgruplac,paginas y matener el de mas columnas rellenadas
cvlac_caplibros['fecha']=pd.to_datetime(cvlac_caplibros['fecha']).dt.to_period('Y')
cvlac_caplibros['editorial']=cvlac_caplibros['editorial'].fillna('No Aplica')
cvlac_caplibros['areas']=cvlac_caplibros['areas'].fillna('No Aplica').astype(str).replace(' -- ',';',regex=True)
cvlac_caplibros['palabras']=cvlac_caplibros['palabras'].fillna('No Aplica').astype(str).replace(', ',';',regex=True)
cvlac_caplibros['sectores']=cvlac_caplibros['sectores'].fillna('No Aplica').astype(str).str.extract(r'(^[^-]*)',expand=False).replace('','No Aplica').str.strip()
col=cvlac_caplibros.copy()
col['editorial']=col['editorial'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
byedit_normalized=col.groupby('editorial')
for key in list(byedit_normalized.groups.keys()):  
    cvlac_caplibros.iloc[list(byedit_normalized.get_group(key).index),6]=cvlac_caplibros.iloc[list(byedit_normalized.get_group(key).index)]['editorial'].value_counts().index[0]
byedit_normalized=0
col['capitulo']=col['capitulo'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
bydept_normalized=col.groupby('capitulo')
for key in list(bydept_normalized.groups.keys()):  
    cvlac_caplibros.iloc[list(bydept_normalized.get_group(key).index),13]=cvlac_caplibros.iloc[list(bydept_normalized.get_group(key).index)]['capitulo'].value_counts().index[0]
bydept_normalized=0
cvlac_caplibros['nombre']=cvlac_caplibros['capitulo'].copy()
col['libro']=col['libro'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('libro')
col=0
for key in list(bydept_normalized.groups.keys()):  
    cvlac_caplibros.iloc[list(bydept_normalized.get_group(key).index),14]=cvlac_caplibros.iloc[list(bydept_normalized.get_group(key).index)]['libro'].value_counts().index[0]
bydept_normalized=0
cvlac_empresatec['registro_camara']=pd.to_datetime(cvlac_empresatec['registro_camara']).dt.to_period('M')
cvlac_empresatec['tipo']=cvlac_empresatec['tipo'].fillna('No Aplica').astype(str).str.extract(r'([^ - ]*$)',expand=False).replace('','No Aplica').str.strip()
cvlac_empresatec['palabras']=cvlac_empresatec['palabras'].fillna('No Aplica').astype(str).replace(', ',';',regex=True)
cvlac_empresatec['areas']=cvlac_empresatec['areas'].fillna('No Aplica').astype(str).replace(' -- ',';',regex=True)
cvlac_empresatec['sectores']=cvlac_empresatec['sectores'].fillna('No Aplica').astype(str).str.extract(r'(^[^-]*)',expand=False).replace('','No Aplica').str.strip()
cvlac_innovaempresa['tipo']=cvlac_innovaempresa['tipo'].fillna('No Aplica').astype(str).str.extract(r'([^-]*$)',expand=False).replace('','No Aplica').str.strip()
cvlac_innovaempresa['lugar']=cvlac_innovaempresa['lugar'].fillna('No Aplica')
cvlac_innovaempresa['fecha']=pd.to_datetime(cvlac_innovaempresa['fecha']).dt.to_period('Y')
cvlac_innovaempresa['palabras']=cvlac_innovaempresa['palabras'].fillna('No Aplica').astype(str).replace(', ',';',regex=True)
cvlac_innovaempresa['areas']=cvlac_innovaempresa['areas'].fillna('No Aplica').astype(str).replace(' -- ',';',regex=True)
cvlac_innovaempresa['sectores']=cvlac_innovaempresa['sectores'].fillna('No Aplica').astype(str).str.extract(r'(^[^-]*)',expand=False).replace('','No Aplica').str.strip()
cvlac_prototipos['tipo']=cvlac_prototipos['tipo'].fillna('No Aplica').astype(str).str.extract(r'([^-]*$)',expand=False).replace('','No Aplica').str.strip()
cvlac_prototipos['lugar']=cvlac_prototipos['lugar'].fillna('No Aplica')
cvlac_prototipos['fecha']=pd.to_datetime(cvlac_prototipos['fecha']).dt.to_period('Y')
cvlac_prototipos['palabras']=cvlac_prototipos['palabras'].fillna('No Aplica').astype(str).replace(', ',';',regex=True)
cvlac_prototipos['areas']=cvlac_prototipos['areas'].fillna('No Aplica').astype(str).replace(' -- ',';',regex=True)
cvlac_prototipos['sectores']=cvlac_prototipos['sectores'].fillna('No Aplica').astype(str).str.extract(r'(^[^-]*)',expand=False).replace('','No Aplica').str.strip()
cvlac_software['tipo']=cvlac_software['tipo'].fillna('No Aplica').astype(str).str.extract(r'([^-]*$)',expand=False).replace('','No Aplica').str.strip()
cvlac_software['lugar']=cvlac_software['lugar'].fillna('No Aplica')
cvlac_software['fecha']=pd.to_datetime(cvlac_software['fecha']).dt.to_period('Y')
cvlac_software['palabras']=cvlac_software['palabras'].fillna('No Aplica').astype(str).replace(', ',';',regex=True)
cvlac_software['areas']=cvlac_software['areas'].fillna('No Aplica').astype(str).replace(' -- ',';',regex=True)
cvlac_software['sectores']=cvlac_software['sectores'].fillna('No Aplica').astype(str).str.extract(r'(^[^-]*)',expand=False).replace('','No Aplica').str.strip()
cvlac_tecnologicos['tipo']=cvlac_tecnologicos['tipo'].fillna('No Aplica').astype(str).str.extract(r'([^-]*$)',expand=False).replace('','No Aplica').str.strip()
cvlac_tecnologicos['lugar']=cvlac_tecnologicos['lugar'].fillna('No Aplica')
cvlac_tecnologicos['fecha']=pd.to_datetime(cvlac_tecnologicos['fecha']).dt.to_period('Y')
cvlac_tecnologicos['palabras']=cvlac_tecnologicos['palabras'].fillna('No Aplica').astype(str).replace(', ',';',regex=True)
cvlac_tecnologicos['areas']=cvlac_tecnologicos['areas'].fillna('No Aplica').astype(str).replace(' -- ',';',regex=True)
cvlac_tecnologicos['sectores']=cvlac_tecnologicos['sectores'].fillna('No Aplica').astype(str).str.extract(r'(^[^-]*)',expand=False).replace('','No Aplica').str.strip()

cvlac_articulos.to_csv('dashboard/assets/data/preprocessed_data/cvlac_articulos.csv',index=False)
cvlac_basico.to_csv('dashboard/assets/data/preprocessed_data/cvlac_basico.csv',index=False)
cvlac_caplibros.to_csv('dashboard/assets/data/preprocessed_data/cvlac_caplibros.csv',index=False)
cvlac_libros.to_csv('dashboard/assets/data/preprocessed_data/cvlac_libros.csv',index=False)
cvlac_empresatec.to_csv('dashboard/assets/data/preprocessed_data/cvlac_empresatec.csv',index=False)
cvlac_innovaempresa.to_csv('dashboard/assets/data/preprocessed_data/cvlac_innovaempresa.csv',index=False)
cvlac_lineas.to_csv('dashboard/assets/data/preprocessed_data/cvlac_lineas.csv',index=False)
cvlac_tecnologicos.to_csv('dashboard/assets/data/preprocessed_data/cvlac_otecnologicos.csv',index=False)
cvlac_prototipos.to_csv('dashboard/assets/data/preprocessed_data/cvlac_prototipos.csv',index=False)
cvlac_software.to_csv('dashboard/assets/data/preprocessed_data/cvlac_software.csv',index=False)
cvlac_areas.to_csv('dashboard/assets/data/preprocessed_data/cvlac_areas.csv',index=False)
cvlac_reconocimiento.to_csv('dashboard/assets/data/preprocessed_data/cvlac_reconocimiento.csv',index=False)
cvlac_identificadores.to_csv('dashboard/assets/data/preprocessed_data/cvlac_identificadores.csv',index=False)

#LIMPIEZA DE TABLAS GRUPLAC

gruplac_basico['fecha_formacion']=pd.to_datetime(gruplac_basico['fecha_formacion']).dt.to_period('M')#DTYPE: period[M]
gruplac_basico['clasificacion']=gruplac_basico['clasificacion'].fillna('No Aplica').astype(str).str.extract(r'([^\s]+)',expand=False).replace('','No Aplica')
gruplac_basico['areas']=gruplac_basico['areas'].astype(str).replace(' -- ',';',regex=True)
gruplac_basico['nombre']=gruplac_basico['nombre'].str.strip()
col=gruplac_basico.copy()
col['programas']=col['programas'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('programas')
for key in list(bydept_normalized.groups.keys()):  
    gruplac_basico.iloc[list(bydept_normalized.get_group(key).index),10]=gruplac_basico.iloc[list(bydept_normalized.get_group(key).index)]['programas'].value_counts().index[0]
bydept_normalized=0
col['programas_secundario']=col['programas_secundario'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('programas_secundario')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_basico.iloc[list(bydept_normalized.get_group(key).index),11]=gruplac_basico.iloc[list(bydept_normalized.get_group(key).index)]['programas_secundario'].value_counts().index[0]
bydept_normalized=0
#CREAR VALORES UNICOS PARA FILTROS
#set_areas=set()
#gruplac_basico['areas'].apply(lambda x: set_areas.update(x.split(';')))
col=gruplac_instituciones.copy()
col['nombre']=col['nombre'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('nombre')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_instituciones.iloc[list(bydept_normalized.get_group(key).index),1]=gruplac_instituciones.iloc[list(bydept_normalized.get_group(key).index)]['nombre'].value_counts().index[0]
bydept_normalized=0
gruplac_articulos['lugar']=gruplac_articulos['lugar'].fillna('No Aplica')
#remover duplicados por doi,idgruplac y mantener el registro con mas columnas rellenadas
gruplac_articulos['issn']=gruplac_articulos['issn'].replace('^0$','No Aplica',regex=True).fillna('No Aplica')
gruplac_articulos['fecha']=pd.to_datetime(gruplac_articulos['fecha']).dt.to_period('Y')
gruplac_articulos['revista']=gruplac_articulos['revista'].fillna('No Aplica')
col=gruplac_articulos.copy()
col['revista']=col['revista'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
byrevi_normalized=col.groupby('revista')
for key in list(byrevi_normalized.groups.keys()):  
    gruplac_articulos.iloc[list(byrevi_normalized.get_group(key).index),5]=gruplac_articulos.iloc[list(byrevi_normalized.get_group(key).index)]['revista'].value_counts().index[0]
byrevi_normalized=0
col['nombre']=col['nombre'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('nombre')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_articulos.iloc[list(bydept_normalized.get_group(key).index),3]=gruplac_articulos.iloc[list(bydept_normalized.get_group(key).index)]['nombre'].value_counts().index[0]
bydept_normalized=0
gruplac_caplibros['lugar']=gruplac_caplibros['lugar'].fillna('No Aplica')
#remover duplicados por capitulo,idgruplac,paginas y matener el de mas columnas rellenadas
gruplac_caplibros['fecha']=pd.to_datetime(gruplac_caplibros['fecha']).dt.to_period('Y')
gruplac_caplibros['editorial']=gruplac_caplibros['editorial'].fillna('No Aplica')
col=gruplac_caplibros.copy()
col['editorial']=col['editorial'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
byedit_normalized=col.groupby('editorial')
for key in list(byedit_normalized.groups.keys()):  
    gruplac_caplibros.iloc[list(byedit_normalized.get_group(key).index),10]=gruplac_caplibros.iloc[list(byedit_normalized.get_group(key).index)]['editorial'].value_counts().index[0]
byedit_normalized=0
col['capitulo']=col['capitulo'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
bydept_normalized=col.groupby('capitulo')
for key in list(bydept_normalized.groups.keys()):  
    gruplac_caplibros.iloc[list(bydept_normalized.get_group(key).index),3]=gruplac_caplibros.iloc[list(bydept_normalized.get_group(key).index)]['capitulo'].value_counts().index[0]
bydept_normalized=0
col['libro']=col['libro'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('libro')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_caplibros.iloc[list(bydept_normalized.get_group(key).index),6]=gruplac_caplibros.iloc[list(bydept_normalized.get_group(key).index)]['libro'].value_counts().index[0]
bydept_normalized=0
pattern='|'.join(['Universidad del Cauca','Editorial Universidad Del Cauca','Ediorial Universidad Del Cauca','Sello Editorial Universidad del Cauca','Taller Editorial Universidad Del Cauca','Editorial De La Universidad Del Cauca','Univesidad Del Cauca','Talleres de impresión de la Universidad del Cauca','Talleres de Impresión la Universidad el Cauca','Centro De Publicaciones Universidad Del Cauca'])
gruplac_caplibros['editorial']=gruplac_caplibros['editorial'].str.replace(pattern, 'Editorial Universidad del Cauca',regex=True)
pattern='|'.join(['Sello editorial Uniautónoma del Cauca','Editorial de la Corporación Universitaria Autónoma del Cauca','Uniautónoma del Cauca','Uniatónoma del Cauca','Editorial Uniautónoma del Cauca','Sello Editorial Uniatónoma del Cauca'])
gruplac_caplibros['editorial']=gruplac_caplibros['editorial'].str.replace(pattern, 'Corporación Universitaria Autónoma del Cauca',regex=True)
pattern='|'.join(['SERVICIO NACIONAL DE APRENDIZAJE - SENA (Regional Cauca)'])
gruplac_caplibros['editorial']=gruplac_caplibros['editorial'].str.replace(pattern, 'SENA',regex=True)
gruplac_lineas['lineas']=gruplac_lineas['lineas'].replace({"1.\t":"","2.\t":"","^L.NEA .. ":""},regex=True)
gruplac_pdoctorado['fecha']=pd.to_datetime(gruplac_pdoctorado['fecha'])#Tiene valores nulos!
gruplac_pdoctorado['institucion']=gruplac_pdoctorado['institucion'].fillna('No Aplica')
col=gruplac_pdoctorado.copy()
col['institucion']=col['institucion'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
byinst_normalized=col.groupby('institucion')
for key in list(byinst_normalized.groups.keys()):  
    gruplac_pdoctorado.iloc[list(byinst_normalized.get_group(key).index),4]=gruplac_pdoctorado.iloc[list(byinst_normalized.get_group(key).index)]['institucion'].value_counts().index[0]
byinst_normalized=0
col['programa']=col['programa'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
bydept_normalized=col.groupby('programa')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_pdoctorado.iloc[list(bydept_normalized.get_group(key).index),1]=gruplac_pdoctorado.iloc[list(bydept_normalized.get_group(key).index)]['programa'].value_counts().index[0]
bydept_normalized=0
gruplac_pmaestria['fecha']=pd.to_datetime(gruplac_pmaestria['fecha'])#Tiene valores nulos!
gruplac_pmaestria['institucion']=gruplac_pmaestria['institucion'].fillna('No Aplica')
col=gruplac_pmaestria.copy()
col['institucion']=col['institucion'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
byinst_normalized=col.groupby('institucion')
for key in list(byinst_normalized.groups.keys()):  
    gruplac_pmaestria.iloc[list(byinst_normalized.get_group(key).index),4]=gruplac_pmaestria.iloc[list(byinst_normalized.get_group(key).index)]['institucion'].value_counts().index[0]
byinst_normalized=0
col['programa']=col['programa'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('programa')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_pmaestria.iloc[list(bydept_normalized.get_group(key).index),1]=gruplac_pmaestria.iloc[list(bydept_normalized.get_group(key).index)]['programa'].value_counts().index[0]
bydept_normalized=0
gruplac_cdoctorado['fecha']=pd.to_datetime(gruplac_cdoctorado['fecha'])#Tiene valores nulos![^a-zA-Z0-9]
col=gruplac_cdoctorado.copy()
col['programa']=col['programa'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
byprog_normalized=col.groupby('programa')
for key in list(byprog_normalized.groups.keys()):  
    gruplac_cdoctorado.iloc[list(byprog_normalized.get_group(key).index),4]=gruplac_cdoctorado.iloc[list(byprog_normalized.get_group(key).index)]['programa'].value_counts().index[0]
byprog_normalized=0
col['curso']=col['curso'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('curso')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_cdoctorado.iloc[list(bydept_normalized.get_group(key).index),1]=gruplac_cdoctorado.iloc[list(bydept_normalized.get_group(key).index)]['curso'].value_counts().index[0]
bydept_normalized=0
gruplac_cmaestria['fecha']=pd.to_datetime(gruplac_cmaestria['fecha'])#Tiene valores nulos!
col=gruplac_cmaestria.copy()
col['programa']=col['programa'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
byprog_normalized=col.groupby('programa')
for key in list(byprog_normalized.groups.keys()):  
    gruplac_cmaestria.iloc[list(byprog_normalized.get_group(key).index),4]=gruplac_cmaestria.iloc[list(byprog_normalized.get_group(key).index)]['programa'].value_counts().index[0]
byprog_normalized=0
col['curso']=col['curso'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('curso')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_cmaestria.iloc[list(bydept_normalized.get_group(key).index),1]=gruplac_cmaestria.iloc[list(bydept_normalized.get_group(key).index)]['curso'].value_counts().index[0]
bydept_normalized=0
gruplac_libros['lugar']=gruplac_libros['lugar'].fillna('No Aplica')
#remover  duplicados por (isbn limpio),idgruplac mantener el registro con mas columnas rellenas
gruplac_libros['fecha']=pd.to_datetime(gruplac_libros['fecha']).dt.to_period('Y')
gruplac_libros['editorial']=gruplac_libros['editorial'].fillna('No Aplica')
col=gruplac_libros.copy()
col['editorial']=col['editorial'].str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9]','', regex=True).str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip() 
byedit_normalized=col.groupby('editorial')
for key in list(byedit_normalized.groups.keys()):  
    gruplac_libros.iloc[list(byedit_normalized.get_group(key).index),7]=gruplac_libros.iloc[list(byedit_normalized.get_group(key).index)]['editorial'].value_counts().index[0]
byedit_normalized=0
col['nombre']=col['nombre'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('nombre')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_libros.iloc[list(bydept_normalized.get_group(key).index),3]=gruplac_libros.iloc[list(bydept_normalized.get_group(key).index)]['nombre'].value_counts().index[0]
bydept_normalized=0
pattern='|'.join(['Universidad del Cauca','Editorial Universidad Del Cauca','Ediorial Universidad Del Cauca','Sello Editorial Universidad del Cauca','Taller Editorial Universidad Del Cauca','Editorial De La Universidad Del Cauca','Univesidad Del Cauca','Talleres de impresión de la Universidad del Cauca','Talleres de Impresión la Universidad el Cauca','Centro De Publicaciones Universidad Del Cauca'])
gruplac_libros['editorial']=gruplac_libros['editorial'].str.replace(pattern, 'Editorial Universidad del Cauca',regex=True)
pattern='|'.join(['Sello editorial Uniautónoma del Cauca','Editorial de la Corporación Universitaria Autónoma del Cauca','Uniautónoma del Cauca','Uniatónoma del Cauca','Editorial Uniautónoma del Cauca','Sello Editorial Uniatónoma del Cauca'])
gruplac_libros['editorial']=gruplac_libros['editorial'].str.replace(pattern, 'Corporación Universitaria Autónoma del Cauca',regex=True)
pattern='|'.join(['SERVICIO NACIONAL DE APRENDIZAJE - SENA (Regional Cauca)'])
gruplac_libros['editorial']=gruplac_libros['editorial'].str.replace(pattern, 'SENA',regex=True)
gruplac_oarticulos['issn']=gruplac_oarticulos['issn'].replace('^0$','No Aplica',regex=True).fillna('No Aplica')
gruplac_oarticulos['fecha']=pd.to_datetime(gruplac_oarticulos['fecha']).dt.to_period('Y')
#remover duplicados por idgruplac,nombre,(paginas?) mantener el de mas columnas rellenas
gruplac_oarticulos['revista']=gruplac_oarticulos['revista'].fillna('No Aplica')
col=gruplac_oarticulos.copy()
col['revista']=col['revista'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
byrevi_normalized=col.groupby('revista')
for key in list(byrevi_normalized.groups.keys()):  
    gruplac_oarticulos.iloc[list(byrevi_normalized.get_group(key).index),5]=gruplac_oarticulos.iloc[list(byrevi_normalized.get_group(key).index)]['revista'].value_counts().index[0]
byrevi_normalized=0
col['nombre']=col['nombre'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('nombre')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_oarticulos.iloc[list(bydept_normalized.get_group(key).index),3]=gruplac_oarticulos.iloc[list(bydept_normalized.get_group(key).index)]['nombre'].value_counts().index[0]
bydept_normalized=0
gruplac_olibros['lugar']=gruplac_olibros['lugar'].fillna('No Aplica')
gruplac_olibros['fecha']=pd.to_datetime(gruplac_olibros['fecha']).dt.to_period('Y')
#remover duplicados por idgruplac,(isbn limpio) y mantener eld e mas columnas rellenas
gruplac_olibros['editorial']=gruplac_olibros['editorial'].fillna('No Aplica')
col=gruplac_olibros.copy()
col['editorial']=col['editorial'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
byedit_normalized=col.groupby('editorial')
for key in list(byedit_normalized.groups.keys()):  
    gruplac_olibros.iloc[list(byedit_normalized.get_group(key).index),9]=gruplac_olibros.iloc[list(byedit_normalized.get_group(key).index)]['editorial'].value_counts().index[0]
byedit_normalized=0
col['nombre']=col['nombre'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('nombre')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_olibros.iloc[list(bydept_normalized.get_group(key).index),3]=gruplac_olibros.iloc[list(bydept_normalized.get_group(key).index)]['nombre'].value_counts().index[0]
bydept_normalized=0
pattern='|'.join(['Universidad del Cauca','Editorial Universidad Del Cauca','Ediorial Universidad Del Cauca','Sello Editorial Universidad del Cauca','Taller Editorial Universidad Del Cauca','Editorial De La Universidad Del Cauca','Univesidad Del Cauca','Talleres de impresión de la Universidad del Cauca','Talleres de Impresión la Universidad el Cauca','Centro De Publicaciones Universidad Del Cauca'])
gruplac_olibros['editorial']=gruplac_olibros['editorial'].str.replace(pattern, 'Editorial Universidad del Cauca',regex=True)
pattern='|'.join(['Sello editorial Uniautónoma del Cauca','Editorial de la Corporación Universitaria Autónoma del Cauca','Uniautónoma del Cauca','Uniatónoma del Cauca','Editorial Uniautónoma del Cauca','Sello Editorial Uniatónoma del Cauca'])
gruplac_olibros['editorial']=gruplac_olibros['editorial'].str.replace(pattern, 'Corporación Universitaria Autónoma del Cauca',regex=True)
pattern='|'.join(['SERVICIO NACIONAL DE APRENDIZAJE - SENA (Regional Cauca)'])
gruplac_olibros['editorial']=gruplac_olibros['editorial'].str.replace(pattern, 'SENA',regex=True)
gruplac_disenoind['fecha']=pd.to_datetime(gruplac_disenoind['fecha']).dt.to_period('Y')
gruplac_innovaempresa['fecha']=pd.to_datetime(gruplac_innovaempresa['fecha']).dt.to_period('Y')
gruplac_innovaempresa['institucion']=gruplac_innovaempresa['institucion'].fillna('No Aplica')
col=gruplac_innovaempresa.copy()
col['institucion']=col['institucion'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
byinst_normalized=col.groupby('institucion')
for key in list(byinst_normalized.groups.keys()):  
    gruplac_innovaempresa.iloc[list(byinst_normalized.get_group(key).index),7]=gruplac_innovaempresa.iloc[list(byinst_normalized.get_group(key).index)]['institucion'].value_counts().index[0]
byinst_normalized=0
col['nombre']=col['nombre'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('nombre')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_innovaempresa.iloc[list(bydept_normalized.get_group(key).index),3]=gruplac_innovaempresa.iloc[list(bydept_normalized.get_group(key).index)]['nombre'].value_counts().index[0]
bydept_normalized=0
gruplac_plantapiloto['fecha']=pd.to_datetime(gruplac_plantapiloto['fecha']).dt.to_period('Y')
gruplac_plantapiloto['institucion']=gruplac_plantapiloto['institucion'].fillna('No Aplica')
col=gruplac_plantapiloto.copy()
col['institucion']=col['institucion'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
byinst_normalized=col.groupby('institucion')
for key in list(byinst_normalized.groups.keys()):  
    gruplac_plantapiloto.iloc[list(byinst_normalized.get_group(key).index),8]=gruplac_plantapiloto.iloc[list(byinst_normalized.get_group(key).index)]['institucion'].value_counts().index[0]
byinst_normalized=0
col['nombre']=col['nombre'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('nombre')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_plantapiloto.iloc[list(bydept_normalized.get_group(key).index),3]=gruplac_plantapiloto.iloc[list(bydept_normalized.get_group(key).index)]['nombre'].value_counts().index[0]
bydept_normalized=0
gruplac_otecnologicos['fecha']=pd.to_datetime(gruplac_otecnologicos['fecha']).dt.to_period('Y')
gruplac_otecnologicos['institucion']=gruplac_otecnologicos['institucion'].fillna('No Aplica')
col=gruplac_otecnologicos.copy()
col['institucion']=col['institucion'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
byinst_normalized=col.groupby('institucion')
for key in list(byinst_normalized.groups.keys()):  
    gruplac_otecnologicos.iloc[list(byinst_normalized.get_group(key).index),8]=gruplac_otecnologicos.iloc[list(byinst_normalized.get_group(key).index)]['institucion'].value_counts().index[0]
byinst_normalized=0
col['nombre']=col['nombre'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('nombre')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_otecnologicos.iloc[list(bydept_normalized.get_group(key).index),3]=gruplac_otecnologicos.iloc[list(bydept_normalized.get_group(key).index)]['nombre'].value_counts().index[0]
bydept_normalized=0
gruplac_prototipos['fecha']=pd.to_datetime(gruplac_prototipos['fecha']).dt.to_period('Y')
gruplac_prototipos['institucion']=gruplac_prototipos['institucion'].fillna('No Aplica')
col=gruplac_prototipos.copy()
col['institucion']=col['institucion'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
byinst_normalized=col.groupby('institucion')
for key in list(byinst_normalized.groups.keys()):  
    gruplac_prototipos.iloc[list(byinst_normalized.get_group(key).index),7]=gruplac_prototipos.iloc[list(byinst_normalized.get_group(key).index)]['institucion'].value_counts().index[0]
byinst_normalized=0
col['nombre']=col['nombre'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('nombre')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_prototipos.iloc[list(bydept_normalized.get_group(key).index),3]=gruplac_prototipos.iloc[list(bydept_normalized.get_group(key).index)]['nombre'].value_counts().index[0]
bydept_normalized=0
gruplac_software['disponibilidad']=gruplac_software['disponibilidad'].replace('Restrita','Restricta')
gruplac_software['fecha']=pd.to_datetime(gruplac_software['fecha']).dt.to_period('Y')
gruplac_software['institucion']=gruplac_software['institucion'].fillna('No Aplica')
col=gruplac_software.copy()
col['institucion']=col['institucion'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
byinst_normalized=col.groupby('institucion')
for key in list(byinst_normalized.groups.keys()):  
    gruplac_software.iloc[list(byinst_normalized.get_group(key).index),7]=gruplac_software.iloc[list(byinst_normalized.get_group(key).index)]['institucion'].value_counts().index[0]
byinst_normalized=0
col['nombre']=col['nombre'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('nombre')
col=0
for key in list(bydept_normalized.groups.keys()):  
    gruplac_software.iloc[list(bydept_normalized.get_group(key).index),3]=gruplac_software.iloc[list(bydept_normalized.get_group(key).index)]['nombre'].value_counts().index[0]
bydept_normalized=0
gruplac_empresatec['fecha_registro']=pd.to_datetime(gruplac_empresatec['fecha_registro'])

#MANEJO DE DUPLICADOS
c=gruplac_articulos.groupby(['idgruplac','nombre','doi']).size().reset_index(name="size").sort_values('size',ascending=False)
d=gruplac_articulos.groupby(['idgruplac','nombre','revista','fecha']).size().reset_index(name="size").sort_values('size',ascending=False)
l=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
l.extend(d[d['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist())
gruplac_duplicados['articulos']=list(set(l))
d=0
l=0
#ARTICULOS DUPLICADOS EN GRUPLAC POR NOMBRE Y DOI
print("")
print("****PERFILES EN GRUPLAC CON ARTÍCULOS DUPLICADOS****")
print("Grupos con artículos duplicados en general: ",c[c['size']>1].drop_duplicates('idgruplac').shape[0])
c=gruplac_articulos[gruplac_articulos['verificado']=='True'].groupby(['idgruplac','nombre','doi']).size().reset_index(name="size").sort_values('size',ascending=False)
print("Grupos con artículos verificados duplicados: ",c[c['size']>1].drop_duplicates('idgruplac').shape[0])
articulos_totales=gruplac_articulos.shape[0]

gruplac_articulos=gruplac_articulos.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','nombre','doi'],keep='first')
gruplac_articulos=gruplac_articulos.drop_duplicates(['idgruplac','nombre','revista','fecha'],keep='first')

dup_arts=articulos_totales-gruplac_articulos.shape[0]
print("Artículos duplicados en los grupos del Cauca: ",dup_arts)

c=gruplac_oarticulos.groupby(['idgruplac','nombre','revista','fecha']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['oarticulos']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_oarticulos=gruplac_oarticulos.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','nombre','revista','fecha'],keep='first')
c=gruplac_libros.groupby(['idgruplac','isbn']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['libros']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_libros=gruplac_libros.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','isbn'],keep='first')
c=gruplac_olibros.groupby(['idgruplac','isbn']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['olibros']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_olibros=gruplac_olibros.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','isbn'],keep='first')
c=gruplac_caplibros.groupby(['idgruplac','capitulo','libro']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['caplibros']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_caplibros=gruplac_caplibros.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','capitulo','libro'],keep='first')
c=gruplac_otecnologicos.groupby(['idgruplac','nombre','fecha','institucion']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['otecnologicos']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_otecnologicos=gruplac_otecnologicos.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','nombre','fecha','institucion'],keep='first')
c=gruplac_software.groupby(['idgruplac','nombre','institucion']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['software']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_software=gruplac_software.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','nombre','institucion'],keep='first')
c=gruplac_prototipos.groupby(['idgruplac','nombre','institucion']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['prototipos']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_prototipos=gruplac_prototipos.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','nombre','institucion'],keep='first')
c=gruplac_cdoctorado.groupby(['idgruplac','curso','fecha']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['cdoctorado']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_cdoctorado=gruplac_cdoctorado.drop_duplicates(['idgruplac','curso','fecha'],keep='first')
c=gruplac_cmaestria.groupby(['idgruplac','curso','fecha']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['cmaestria']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_cmaestria=gruplac_cmaestria.drop_duplicates(['idgruplac','curso','fecha'],keep='first')
c=gruplac_innovaempresa.groupby(['idgruplac','nombre','fecha']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['innovaempresa']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_innovaempresa=gruplac_innovaempresa.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','nombre','fecha'],keep='first')
c=gruplac_empresatec.groupby(['idgruplac','nombre','fecha']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['empresatec']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_empresatec=gruplac_empresatec.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','nombre','fecha'],keep='first')
c=gruplac_plantapiloto.groupby(['idgruplac','nombre','fecha']).size().reset_index(name="size").sort_values('size',ascending=False)
gruplac_duplicados['empresatec']=c[c['size']>1].drop_duplicates('idgruplac')['idgruplac'].tolist()
gruplac_plantapiloto=gruplac_plantapiloto.sort_values(['verificado'],ascending=False).drop_duplicates(['idgruplac','nombre','fecha'],keep='first')

gruplac_articulos.to_csv('dashboard/assets/data/preprocessed_data/gruplac_articulos.csv',index=False)
gruplac_basico.to_csv('dashboard/assets/data/preprocessed_data/gruplac_basico.csv',index=False)
gruplac_caplibros.to_csv('dashboard/assets/data/preprocessed_data/gruplac_caplibros.csv',index=False)
gruplac_integrantes.to_csv('dashboard/assets/data/preprocessed_data/gruplac_integrantes.csv',index=False)
gruplac_libros.to_csv('dashboard/assets/data/preprocessed_data/gruplac_libros.csv',index=False)
gruplac_oarticulos.to_csv('dashboard/assets/data/preprocessed_data/gruplac_oarticulos.csv',index=False)
gruplac_olibros.to_csv('dashboard/assets/data/preprocessed_data/gruplac_olibros.csv',index=False)
gruplac_cdoctorado.to_csv('dashboard/assets/data/preprocessed_data/gruplac_cdoctorado.csv',index=False)
gruplac_cmaestria.to_csv('dashboard/assets/data/preprocessed_data/gruplac_cmaestria.csv',index=False)
gruplac_disenoind.to_csv('dashboard/assets/data/preprocessed_data/gruplac_disenoind.csv',index=False)
gruplac_empresatec.to_csv('dashboard/assets/data/preprocessed_data/gruplac_empresatec.csv',index=False)
gruplac_innovaempresa.to_csv('dashboard/assets/data/preprocessed_data/gruplac_innovaempresa.csv',index=False)
gruplac_instituciones.to_csv('dashboard/assets/data/preprocessed_data/gruplac_instituciones.csv',index=False)
gruplac_lineas.to_csv('dashboard/assets/data/preprocessed_data/gruplac_lineas.csv',index=False)
gruplac_otecnologicos.to_csv('dashboard/assets/data/preprocessed_data/gruplac_otecnologicos.csv',index=False)
gruplac_pdoctorado.to_csv('dashboard/assets/data/preprocessed_data/gruplac_pdoctorado.csv',index=False)
gruplac_plantapiloto.to_csv('dashboard/assets/data/preprocessed_data/gruplac_plantapiloto.csv',index=False)
gruplac_pmaestria.to_csv('dashboard/assets/data/preprocessed_data/gruplac_pmaestria.csv',index=False)
gruplac_prototipos.to_csv('dashboard/assets/data/preprocessed_data/gruplac_prototipos.csv',index=False)
gruplac_software.to_csv('dashboard/assets/data/preprocessed_data/gruplac_software.csv',index=False)
#gruplac_duplicados
#gruplac_duplicados=json.dumps(gruplac_duplicados)
#with open('dashboard/assets/data/preprocessed_data/gruplac_duplicados.json','w') as file:
#    file.write(gruplac_duplicados)


#LIMPIEZA DE TABLAS SCOPUS

scopus_autores['documentos']=scopus_autores['documentos'].astype('int')
scopus_autores['documentos_citados']=scopus_autores['documentos_citados'].astype('int')
scopus_autores['h_index']=scopus_autores['h_index'].astype('int')
scopus_autores['co_autores']=scopus_autores['co_autores'].astype('int')
scopus_autores['citaciones']=scopus_autores['citaciones'].astype('int')
#scopus_autores.rename(columns={'documentos_citados':'citado_por'},inplace=True)
scopus_autores['fecha_creacion']=pd.to_datetime(scopus_autores['fecha_creacion'], format='%d/%m/%Y')
#scopus_autores['departamento']=scopus_autores['departamento'].str.lstrip(' ,.-').str.rstrip(' ,.-').fillna('No Aplica')
scopus_autores['departamento']=scopus_autores['departamento'].fillna('No Aplica')
col=scopus_autores.copy()
col['departamento']=col['departamento'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip() 
bydept_normalized=col.groupby('departamento')
col=0
for key in list(bydept_normalized.groups.keys()):  
    scopus_autores.iloc[list(bydept_normalized.get_group(key).index),16]=scopus_autores.iloc[list(bydept_normalized.get_group(key).index)]['departamento'].value_counts().index[0]
bydept_normalized=0
scopus_autores['departamento']=scopus_autores['departamento'].replace('^and Control$','No Aplica',regex=True)              
scopus_autores['institucion']=scopus_autores['institucion'].fillna('No Aplica')
col=scopus_autores.copy()
col['institucion']=col['institucion'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
bydept_normalized=col.groupby('institucion')
col=0
for key in list(bydept_normalized.groups.keys()):  
    scopus_autores.iloc[list(bydept_normalized.get_group(key).index),14]=scopus_autores.iloc[list(bydept_normalized.get_group(key).index)]['institucion'].value_counts().index[0]
bydept_normalized=0
scopus_autores['institucion']=scopus_autores['institucion'].replace({'Médico general':'No Aplica','^Colombia$':'No Aplica','':'No Aplica','^and Control$':'No Aplica','^IU Colegio Mayor del Cauca$':'Institución Universitaria Colegio Mayor del Cauca',
                                                                    'Hospital Universitario San José de Popayán':'Hospital Universitario San José','InnovaGen Foundation':'Fundación InnovaGen','Fundacion EcoHabitats':'Fundación Ecohabitats',
                                                                    '^TECNICAFE$':'Parque Tecnológico de Innovación del Café - TECNICAFÉ','Vejarano Ophthalmological Foundation':'Fundación Oftalmológica Vejarano',
                                                                    'Fundación Ecohábitats':'Fundación Ecohabitats','Efigenia Aerospace Robotics Autonomous Unmanned Aerial Vehicles Research, Colombia':'EFIGENIA Aerospace Robotics Research',
                                                                    'Efigenia Aerospace Robotics Autonomous Unmanned Aerial Vehicles Research, Colombia, EFIGENIA Aerospace Robotics Research':'EFIGENIA Aerospace Robotics Research',
                                                                    'Grupo de Investigación en Diseño y Arte \(D&A\)':'Universidad Mayor','\(CYTBIA\)':'CYTBIA','Hospital Universitário San José':'Hospital Universitario San José',
                                                                    'Investigador Adscrito al Centro Regional de Productividad e Innovación del Cauca-CREPIC':'Centro Regional de Productividad e Innovación del Cauca-CREPIC',
                                                                    'Faculty of Health Sciences':'Universidad del Cauca','Bachiller Comunero del Resguardo de Puracé':'Resguardo de Puracé','^CGS$':'Colombian Geological Service',
                                                                    'Tecnólogo Ambiental Comunero del Resguardo de Puracé':'Resguardo de Puracé','Hospital Universitário':'Hospital Universitario San José',
                                                                    '^IVSI$':'Synthetic Vaccine and New Drug Research Institute – IVSI','University of Cauca–CREPIC':'Centro Regional de Productividad e Innovación del Cauca-CREPIC',
                                                                    'Environmental Division Acueducto y Alcantarillado de Popayán S\.A\. E\.S\.P\. \(Popayán Water and Sewage Company\)':'Division Acueducto y Alcantarillado de Popayán S.A. E.S.P.',
                                                                    'Sena':'SENA','SENNOVA':'SENA','Health Specialists Center-Renacer Ltda.':'Centro de Especialistas en Salud Integral Renacer Ltda'}, regex=True)

pattern='|'.join(['Facultad de Ingeniería Electrónica y Telecomunicaciones Universidad del Cacuca','U. de Toxicol. Genet. Y Citogenetica','Systems Engineering Program University of Cauca Popayán','ECCO','^FIET$','Grupo de investigación de Ingeniería Telemática','Umversidad Del Cauca-DCE','University of Cauca at Tulcán'])
scopus_autores['institucion']=scopus_autores['institucion'].str.replace(pattern, 'Universidad del Cauca',regex=True)
pattern = '|'.join(['University Foundation of Popayán','^Universitaria de Popayán$','^Fundación Universitaria de$','Fundacion Universitaria de Popayán','Popayán University Foundation'])
scopus_autores['institucion']=scopus_autores['institucion'].str.replace(pattern, 'Fundación Universitaria de Popayán',regex=True)
pattern = '|'.join(['Programa de Ingeniería de Sistemas Unicomfacauca','Corporación Universitaria Comfacauca \- Unicomfacauca','Corporación Universitaria Comfacauca \-\- Unicomfacauca','Comfacauca University Corporation','Corporación Universitaria Comfacauca\—Unicomfacauca','Unicomfacauca University',
                    'Unicomfacauca Grupode Investigation en Sistemaslnteligentes','Grupo de Investigación en Sistemas Inteligentes GISI, Corporación Universitaria Comfacauca','^Grupo de Investigation en Sistemas Inteligentes$'])
scopus_autores['institucion']=scopus_autores['institucion'].str.replace(pattern, 'Corporación Universitaria Comfacauca',regex=True)
pattern = '|'.join(['Technology Development Center, Corporation Cluster CreaTIC','^Grupo de Investigación CreaTIC$'])
scopus_autores['institucion']=scopus_autores['institucion'].str.replace(pattern, 'Centro de desarrollo tecnológico CREATIC',regex=True)
pattern = '|'.join(['Intensive Care Unit La Estancia Clinic','^Clínica La Estancia$'])
scopus_autores['institucion']=scopus_autores['institucion'].str.replace(pattern, 'Clínica la Estancia',regex=True)
pattern = '|'.join(['National Open and Distance University','^UNAD$','^Universidad Nacional Abierta y a Distancia - UNAD$','Open and Distance National University'])
scopus_autores['institucion']=scopus_autores['institucion'].str.replace(pattern, 'Universidad Nacional Abierta y a Distancia',regex=True)
pattern = '|'.join(['^Corporación Del Laboratorio al Campo$','Del Laboratorio al Campo-Grupo de Investigación en Biotecnología y Biomedicina \(BIOTECMED\)'])
scopus_autores['institucion']=scopus_autores['institucion'].str.replace(pattern, 'Corporación del Laboratorio al Campo',regex=True)
pattern = '|'.join(['Clínica de Rehabilitación Integral Fisiocenter-Área de Fonoaudiología','Fisioterapeuta Fisiocenter'])
scopus_autores['institucion']=scopus_autores['institucion'].str.replace(pattern, 'Clínica de Rehabilitación Integral Fisiocenter',regex=True)

#Afiliaciones unicas de tabla autores
set_institucion_scopus1=set()
scopus_autores['institucion'].apply(lambda x: set_institucion_scopus1.update(x.split(';'))) #cambiar por ';'

#Afiliaciones de la lista a nivel Cauca generada en Anexo B
affilnames=['Universidad del Cauca', 'Institución Universitaria Colegio Mayor del Cauca', 'Institución Universitaria Colegio Mayor del Cauca', 'Institución Universitaria Colegio Mayor del Cauca', 'INNOVATEC', 'Corporación Universitaria Autónoma del Cauca', 
            'Popayán University Foundation', 'Corporación Universitaria Comfacauca', 'Hospital Universitario San José', 'Corporación Universitaria Comfacauca—Unicomfacauca', 'Médico general', 'Hospital Universitario San José', 'Institución Universitaria Colegio Mayor del Cauca', 
            'Comunicadora Social en la radio comunitaria Namuy Wam', 'Hospital Susana López de Valencia', 'Corporación Universitaria Comfacauca', 'IU Colegio Mayor del Cauca', 'Grupo de Investigación en Diseño y Arte (D&A)', 'Hospital Piloto de Popayan', 
            'TECNICAFE', 'Bachiller Comunero del Resguardo de Puracé', 'Tecnólogo Ambiental Comunero del Resguardo de Puracé', 'Centro de Estudios Urbanos', 'University Foundation of Popayán', 'Asociación Campesina de Inzá Tierradentro (ACIT)', 'Fundación Biotellus', 
            'Latin American School for Youth Social Actory Popayán', 'Fundacion Universitaria de Popayán', 'Hospital Universitario San José', 'Corporación Universitaria Comfacauca', 'University Foundation of Popayán', 'University Foundation of Popayán', 
            'Hospital Susana López de Valencia', 'Corporación Universitaria Comfacauca - Unicomfacauca', 'Secretaría Departamental de Salud del Cauca', 'Fundación InnovaGen', 'Comfacauca University Corporation', 'Fundación Oftalmológica Vejarano', 'SENA', 
            'InnovaGen Foundation', 'Fundación Ecohabitats', 'Clínica la Estancia', 'Universitaria de Popayán', 'Secretaría de Salud Municipal', 'Fundación Universitaria de', 'Wildlife Conservation Society', 'Parque Nacional Natural Puracé', 'FIET', 
            'Technology Development Center, Corporation Cluster CreaTIC', 'Fundación Ecohabitats', 'Intensive Care Unit La Estancia Clinic', 'Efigenia Aerospace Robotics Autonomous Unmanned Aerial Vehicles Research, Colombia', 'Regional Autonomous Corporation of Cauca', 
            'Faculty of Health Sciences', 'Systems Engineering Program University of Cauca Popayán', 'Asociación Indígena del Cauca', 'Red de Mujeres Del Cauca-REDEMUC', 'Ganadería "Ernesto González Caicedo"', 'Fundación Biotellus', 'Grupo de Investigation en Sistemas Inteligentes', 
            'Comfacauca University Corporation', 'Parque Tecnológico de Innovación del Café - TECNICAFÉ', 'Umversidad Del Cauca-DCE', 'Unicomfacauca Grupode Investigation en Sistemaslnteligentes', 'Empresa Social del Estado Suroccidente.', 'Centro de Salud María Oriente.', 
            'Centro de Estudios Urbanos', 'Unicomfacauca University', 'Parque Nacional Natural Puracé', 'Facultad de Ingeniería Electrónica y Telecomunicaciones Universidad del Cacuca', 'Fundación José María Delgado-Paredes para Promover la Investigación en Medicina', 
            'Clínica de Rehabilitación Integral Fisiocenter-Área de Fonoaudiología', 'Sunset Software House S.A.S', 'Corporación Universitaria Comfacauca—Unicomfacauca', 'Ecotecma SAS', 'Wildlife Conservation Society', 'Grupo de Investigación en Sistemas Inteligentes GISI, Corporación Universitaria Comfacauca', 
            'Programa de Ingeniería de Sistemas Unicomfacauca', 'Observatorio Vulcanológico y Sismológico', 'Open and Distance National University', 'Environmental Division Acueducto y Alcantarillado de Popayán S.A. E.S.P. (Popayán Water and Sewage Company)', 'Clínica La Estancia', 
            'Clínica Santa Gracia', 'Corporación Del Laboratorio al Campo', 'Fisioterapeuta Fisiocenter', 'Bit Bang Company', 'Ecología y Conservación GECO', 'IVSI', 'Secretaría Departamental de Salud del Cauca', 'National Open and Distance University', 'CGS', 'Fundacion EcoHabitats', 
            'Conjunto Mallorca', 'Vejarano Ophthalmological Foundation', 'CRIC - Consejo Regional Indígena del Cauca', 'University of Cauca at Tulcán', 'Health Specialists Center-Renacer Ltda.', 'Hospital Universitário', 'U. de Toxicol. Genet. Y Citogenetica', 'ICOBANDAS S. A.', 
            'FUNCOP - Fundacion para la Comunicacion popular', 'Centro Medico Sigma', 'Centro de desarrollo tecnológico CREATIC', 'UNAD', 'Corporación Universitaria Comfacauca', 'Movimiento de Mujeres por la Vida Cajibío-Cauca', 'Paediatric Ophthalmology', 
            'Institución Educativa Agroindustrial Monterilla', 'Guapi Regional Hospital', 'Municipio de San Sebastián', 'University of Cauca–CREPIC', 'IPS Horisoes', '(CYTBIA)', 'Hospital Universitario San José de Popayán', 'Fundación Oftalmológica Vejarano', 
            'Synthetic Vaccine and New Drug Research Institute – IVSI', 'Totems Ltda', 'Investigador Adscrito al Centro Regional de Productividad e Innovación del Cauca-CREPIC', 'Investigador Adscrito al Centro Regional de Productividad e Innovación del Cauca-CREPIC', 'ECCO', 
            'ECOBAMBOO','No Aplica']
#Limpieza de la lista cruda a nivel Cauca
df = pd.DataFrame(affilnames,columns=['0'])

df['0']=df['0'].replace({'Médico general':'No Aplica','^Colombia$':'No Aplica','':'No Aplica','^and Control$':'No Aplica','^IU Colegio Mayor del Cauca$':'Institución Universitaria Colegio Mayor del Cauca',
                        'Hospital Universitario San José de Popayán':'Hospital Universitario San José','InnovaGen Foundation':'Fundación InnovaGen','Fundacion EcoHabitats':'Fundación Ecohabitats',
                        '^TECNICAFE$':'Parque Tecnológico de Innovación del Café - TECNICAFÉ','Vejarano Ophthalmological Foundation':'Fundación Oftalmológica Vejarano',
                        'Fundación Ecohábitats':'Fundación Ecohabitats','Efigenia Aerospace Robotics Autonomous Unmanned Aerial Vehicles Research, Colombia':'EFIGENIA Aerospace Robotics Research',
                        'Efigenia Aerospace Robotics Autonomous Unmanned Aerial Vehicles Research, Colombia, EFIGENIA Aerospace Robotics Research':'EFIGENIA Aerospace Robotics Research',
                        'Grupo de Investigación en Diseño y Arte \(D&A\)':'Universidad Mayor','\(CYTBIA\)':'CYTBIA','Hospital Universitário San José':'Hospital Universitario San José',
                        'Investigador Adscrito al Centro Regional de Productividad e Innovación del Cauca-CREPIC':'Centro Regional de Productividad e Innovación del Cauca-CREPIC',
                        'Faculty of Health Sciences':'Universidad del Cauca','Bachiller Comunero del Resguardo de Puracé':'Resguardo de Puracé','^CGS$':'Colombian Geological Service',
                        'Tecnólogo Ambiental Comunero del Resguardo de Puracé':'Resguardo de Puracé','Hospital Universitário':'Hospital Universitario San José',
                        '^IVSI$':'Synthetic Vaccine and New Drug Research Institute – IVSI','University of Cauca–CREPIC':'Centro Regional de Productividad e Innovación del Cauca-CREPIC',
                        'Environmental Division Acueducto y Alcantarillado de Popayán S\.A\. E\.S\.P\. \(Popayán Water and Sewage Company\)':'Division Acueducto y Alcantarillado de Popayán S.A. E.S.P.',
                        'Sena':'SENA','SENNOVA':'SENA','Health Specialists Center-Renacer Ltda.':'Centro de Especialistas en Salud Integral Renacer Ltda'}, regex=True)

pattern='|'.join(['Facultad de Ingeniería Electrónica y Telecomunicaciones Universidad del Cacuca','U. de Toxicol. Genet. Y Citogenetica','Systems Engineering Program University of Cauca Popayán','ECCO','^FIET$','Grupo de investigación de Ingeniería Telemática','Umversidad Del Cauca-DCE','University of Cauca at Tulcán'])
df['0']=df['0'].str.replace(pattern, 'Universidad del Cauca',regex=True)
pattern = '|'.join(['University Foundation of Popayán','^Universitaria de Popayán$','^Fundación Universitaria de$','Fundacion Universitaria de Popayán','Popayán University Foundation'])
df['0']=df['0'].str.replace(pattern, 'Fundación Universitaria de Popayán',regex=True)
pattern = '|'.join(['Programa de Ingeniería de Sistemas Unicomfacauca','Corporación Universitaria Comfacauca \- Unicomfacauca','Corporación Universitaria Comfacauca \-\- Unicomfacauca','Comfacauca University Corporation','Corporación Universitaria Comfacauca\—Unicomfacauca','Unicomfacauca University',
                    'Unicomfacauca Grupode Investigation en Sistemaslnteligentes','Grupo de Investigación en Sistemas Inteligentes GISI, Corporación Universitaria Comfacauca','^Grupo de Investigation en Sistemas Inteligentes$'])
df['0']=df['0'].str.replace(pattern, 'Corporación Universitaria Comfacauca',regex=True)
pattern = '|'.join(['Technology Development Center, Corporation Cluster CreaTIC','^Grupo de Investigación CreaTIC$'])
df['0']=df['0'].str.replace(pattern, 'Centro de desarrollo tecnológico CREATIC',regex=True)
pattern = '|'.join(['Intensive Care Unit La Estancia Clinic','^Clínica La Estancia$'])
df['0']=df['0'].str.replace(pattern, 'Clínica la Estancia',regex=True)
pattern = '|'.join(['National Open and Distance University','^UNAD$','^Universidad Nacional Abierta y a Distancia - UNAD$','Open and Distance National University'])
df['0']=df['0'].str.replace(pattern, 'Universidad Nacional Abierta y a Distancia',regex=True)
pattern = '|'.join(['^Corporación Del Laboratorio al Campo$','Del Laboratorio al Campo-Grupo de Investigación en Biotecnología y Biomedicina \(BIOTECMED\)'])
df['0']=df['0'].str.replace(pattern, 'Corporación del Laboratorio al Campo',regex=True)
pattern = '|'.join(['Clínica de Rehabilitación Integral Fisiocenter-Área de Fonoaudiología','Fisioterapeuta Fisiocenter'])
df['0']=df['0'].str.replace(pattern, 'Clínica de Rehabilitación Integral Fisiocenter',regex=True)

#Se emparejan afiliaciones unicas identificadas en los registros de autores con las identificadas 
#por la lista creada a nivel Cauca
a1=list(set_institucion_scopus1)
a1=[s.strip() for s in a1] #comentar a futuro
b1=df['0'].tolist()
c1 = [i for i in b1 if i in a1]

afiliaciones_emparejadas_a=c1
print("")
print("**** MÁS ESTADÍSTICAS ****")
print('Afiliaciones emparejadas en Scopus por autores: ',len(set(afiliaciones_emparejadas_a)))
#print('Total de afiliaciones de Scopus en el Cauca: ',len(set(b1)))
a1=0
b1=0
c1=0
set_institucion_scopus1=0

#editorial,pag_count,fecha_publicacion,citado,institucion,tema,palabras_clave_autor,palabras_clave_index,agencia_fundadora, 
#scopus_productos=scopus_productos.fillna('')
#scopus_productos['pag_count']=scopus_productos['pag_count'].astype('int')
scopus_productos['citado']=scopus_productos['citado'].astype('int')
scopus_productos['fecha_publicacion']=pd.to_datetime(scopus_productos['fecha_publicacion'])
scopus_productos['agencia_fundadora']=scopus_productos['agencia_fundadora'].replace('','No Aplica').fillna('No Aplica')
scopus_productos['agencia_fundadora']=scopus_productos['agencia_fundadora'].replace({'Ministerio de Ciencia e InnovaciÃ³n':'Ministerio de Ciencia e Innovación','Ministerio de Ciencia, Innovación y Universidades':'Ministerio de Ciencia e Innovación','Ministerio de Economía y Competitividad':'Ministerio de Economía, Industria y Competitividad, Gobierno de España'},regex=True)
scopus_productos['editorial']=scopus_productos['editorial'].fillna('No Aplica')
scopus_productos['editorial']=scopus_productos['editorial'].replace({'':'No Aplica','Springer Verlagservice@springer.de':'Springer Verlag','Associacao Iberica de Sistemas e Tecnologias de Informacaoaisti@aisti.eu':'Associacao Iberica de Sistemas e Tecnologias de Informacao','IEEE Computer Societyhelp@computer.org':'IEEE Computer Society','Sociedad Colombiana de Anestesiologia y ReanimacionB9, Kanara Business Centre, off Link Road, Ghatkopar \(E\)Mumbai400 075':'Sociedad Colombiana de Anestesiologia y Reanimacion',
                                                                    'Association for Computing Machineryacmhelp@acm.org':'Association for Computing Machinery','IOS PressNieuwe Hemweg 6BAmsterdam1013 BG':'IOS PressNieuwe Hemweg','Centro de Informacion TecnologicaLarrain Alcalde 1120La Serena':'Centro de Informacion Tecnologica','Universidad de Chile, Facultad de Ciencias Sociales':'Universidad de Chile','Universidad de Chile, Facultad de Filosofia y Humanidades, Departamento de Literatura':'Universidad de Chile',
                                                                    'Institute of Physics Publishinghelen.craven@iop.org':'Institute of Physics Publishing','Education Society of IEEE \(Spanish Chapter\)martin.Llamas@det.uvigo.es':'Education Society of IEEE (Spanish Chapter)','Springer New York LLCbarbara.b.bertram@gsk.com':'Springer New York LLC','^Universidad de Chile, Facultad de Ciencias Sociales$':'Universidad de Chile',
                                                                    'Universidad Nacional de Colombiafchumana@unalmed.edu.co':'Universidad Nacional de Colombia','Universidad de Caldasucaldas@ucaldas.edu.co':'Universidad de Caldas','Revista Espaciosvaldiviesor@cantv.net':'Revista Espacios','Instituto Nacional de Saludbiomedica@ins.gov.co':'Instituto Nacional de Salud','Universidad de Chilemanuel.loyola@usach.cl':'Universidad de Chile',
                                                                    'Federacion Colombiana de Asociaciones de Obstetricia y Ginecologia \(FECOLSOG\)fecolsog@fecolsog\.org':'Federacion Colombiana de Asociaciones de Obstetricia y Ginecologia (FECOLSOG)','Sociedad Mexicana de Ingenieria Biomedicasecretariado@somib.org.mx':'Sociedad Mexicana de Ingenieria Biomedica','Instituto Nacional de Salud Publicaspm@insp.mx':'Instituto Nacional de Salud',
                                                                     'Universidad de Antioquiarevista.ingenieria@udea.edu.co':'Universidad de Antioquia','Trans Tech Publications Ltdttp@transtec.ch':'Trans Tech Publications Ltd','Sociedad Colombiana de Anestesiologia y Reanimacion SCAREB9, Kanara Business Centre, off Link Road, Ghatkopar \(E\)Mumbai400 075':'Sociedad Colombiana de Anestesiologia y Reanimacion',
                                                                    'Sociedad Colombiana de Anestesiologia y Reanimacion SCARE':'Sociedad Colombiana de Anestesiologia y Reanimacion','Universidad de Tarapacainfo@uta.cl':'Universidad de Tarapaca','Academic Press Inc.apjcs@harcourt.com':'Academic Press Inc.','^Academic Press$':'Academic Press Inc.','Academic Press Inc.Journals_subscriptions@cup.cam.ac.uk':'Academic Press Inc.',
                                                                    'Springer-Verlag Italia s.r.l.':'Springer Verlag','Springer \(India\) Private Ltd.':'Springer','Springereditorial@springerplus.com':'Springer','Springer Healthcarekathleen.burke@springer.com':'Springer Healthcare','^Springer-Verlag Wien$':'Springer Verlag','Maik Nauka Publishing / Springer SBMcompmg@maik.ru':'Springer','^Universidad de Chilepablo.lopez@uv.cl$':'Universidad de Chile',
                                                                     'Springer-Verlag Wienmichaela.bolli@springer.at':'Springer Verlag','Springer Netherlandsrbk@louisiana.edu':'Springer Netherlands','^Springer Science\+Business Media$':'Springer Science and Business Media','Springer Science and Business Media Deutschland GmbHinfo@springer-sbm.com':'Springer Science and Business Media Deutschland GmbH',
                                                                    '^Springer International Publishing$':'Springer','^Springer Science and Business Media, LLC$':'Springer Science and Business Media','^Springer New York$':'Springer New York LLC','Springer New York LLCjournals@springer-sbm.com':'Springer New York LLC','^Springer Berlin Heidelberg$':'Springer','^Springer Nature$':'Springer',
                                                                    'Elsevier Doymaeditorial@elsevier.com':'Elfsevier Doyma','Elsevier DoymaB9, Kanara Business Centre, off Link Road, Ghatkopar \(E\)Mumbai400 075':'Elsevier Doyma','Elsevier B.V.publicaciones@scc.org.co':'Elsevier B.V.','Elsevier Masson SAS62 rue Camille DesmoulinsIssy les Moulineaux Cedex92442':'Elsevier Masson','Blackwell Publishing Inc.subscrip@blackwellpub.com':'Blackwell Publishing Inc.',
                                                                    'Elsevier Inc.usjcs@elsevier.com':'Elsevier Inc.','Elsevier Masson s.r.l.':'Elsevier Masson','^Elsevier S.A.$':'Elsevier','Elsevier USAsupport@ubiquitypress.com':'Elsevier','Elsevier Doymapublicaciones@scare.org.co':'Elsevier Doyma','^Elsevier Editora Ltda$':'Elsevier','^MDPI AG$':'MDPI','Medknow PublicationsB9, Kanara Business Centre, off Link Road, Ghatkopar \(E\)Mumbai400 075':'Medknow Publications',
                                                                    'MDPI AGPostfachBaselCH-4005':'MDPI','MDPI AGmembranes@mdpi.com':'MDPI','^MDPI AGindexing@mdpi.com$':'MDPI','MDPI AGPostfachBaselCH-4005rasetti@mdpi.com':'MDPI','MDPI AGPostfachBaselCH-4005indexing@mdpi.com':'MDPI','MDPI AGdiversity@mdpi.com':'MDPI','MDPI Multidisciplinary Digital Publishing Instituterasetti@mdpi.com':'MDPI',
                                                                     'Universidad Nacional de Colombiafchumana@unalmed.edu.co':'Universidad Nacional de Colombia','Universidad Nacional de Colombiaactagronomica_pal@unal.edu.co':'Universidad Nacional de Colombia','Universidad Nacional de Colombia1agrocol_fabog@unal.edu.co':'Universidad Nacional de Colombia','Universidad Nacional de Colombiarevcuaeco_bog@unal.edu.co':'Universidad Nacional de Colombia',
                                                                    'Universidad Nacional de Colombiarevcolamt@scm.org.co':'Universidad Nacional de Colombia','Universidad Nacional de Colombiaanuhisto@gmail.com':'Universidad Nacional de Colombia','Universidad Nacional de Colombiarevideva_fchbog@unal.edu.co':'Universidad Nacional de Colombia','IEEE Computer Societyhelp@computer.org':'IEEE Computer Society',
                                                                    'Association for Computing Machineryacmhelpacm.org':'Association for Computing Machinery','Universidad de Antioquiarevista.ingenieria@udea.edu.co':'Universidad de Antioquia','Universidad de Antioquiaiatreia@medicina.udea.ed.co':'Universidad de Antioquia','Universidad de Antioquiarmutatismutandis@gmail.com':'Universidad de Antioquia',
                                                                    'Universidad de AntioquiaBloque 18 Oficina 141 Ciudad UniversitariaMedellin':'Universidad de Antioquia','John Wiley and Sons Inc.P.O.Box 18667NewarkNJ 07191-8667':'John Wiley and Sons Inc.','John Wiley and Sons Ltdvgorayska@wiley.com':'John Wiley and Sons Ltd','^MDPIindexing@mdpi.com$':'MDPI','^MDPIrasetti@mdpi.com$':'MDPI',
                                                                    'John Wiley and Sons LtdSouthern GateChichester, West SussexPO19 8SQvgorayska@wiley.com':'John Wiley and Sons Ltd','John Wiley and Sons Ltdcs-journals@wiley.co.uk':'John Wiley and Sons Ltd','John Wiley and Sons LtdSouthern GateChichester, West SussexPO19 8SQ':'John Wiley and Sons Ltd','Escola de Ciencia da Informacao da UFMGeci@eci.ufmg.br':'Escola de Ciencia da Informacao da UFMG',
                                                                    'Universidad del Zuliapublicaciones.fecs@luz.edu.ve':'Universidad del Zulia','Universidad del Zulialvivanco99@hotmail.com':'Universidad del Zulia','BioMed Central Ltd.info@biomedcentral.com':'BioMed Central Ltd','BioMed Central Ltdinfo@biomedcentral.com':'BioMed Central Ltd','Wolters Kluwer Medknow PublicationsB9, Kanara Business Centre, off Link Road, Ghatkopar \(E\)Mumbai400 075':'Medknow Publications',
                                                                    'Pontificia Universidad Javerianaoocampo@javeriana.edu.co':'Pontificia Universidad Javeriana','Pontificia Universidad Javerianacuadernos.mavae@javeriana.edu.co':'Pontificia Universidad Javeriana','Pontificia Universidad Javeriana 1articulosmagis@javeriana.edu.co':'Pontificia Universidad Javeriana',
                                                                    'Pontificia Universidad Javerianaflorez.f@javeriana.edu.co':'Pontificia Universidad Javeriana','Pontificia Universidad Javerianarevistascientificasjaveriana@gmail.com':'Pontificia Universidad Javeriana','Pontificia Universidad JaverianaCalle 40 N 6-23, Piso 8, Edificio Gabriel GiraldoS.J. Santa Fe de Bogota':'Pontificia Universidad Javeriana',
                                                                    'Taylor and Francis Ltd.michael.wagreich@univie.ac.at':'Taylor and Francis Ltd.','Taylor and Francis Inc.325 Chestnut St, Suite 800PhiladelphiaPA 19106':'Taylor and Francis Ltd.','Taylor and Francis Ltdhealthcare.enquiries@informa.com':'Taylor and Francis Ltd.','^Taylor and Francis$':'Taylor and Francis Ltd.',
                                                                    'Sociedad Espanola de Ceramica y VidrioVitruvio 8MadridE-28006':'Sociedad Espanola de Ceramica y Vidrio','Hindawi Limited410 Park Avenue, 15th Floor, 287 pmbNew YorkNY 10022':'Hindawi Limited','IGI Globalcust@igi-global.com':'IGI Global','Sociedad Mexicana de Ingenieria Biomedicasecretariado@somib.org.mx':'Sociedad Mexicana de Ingenieria Biomedica',
                                                                    'Inderscience Publishers29, route de Pre-BoisCase Postale 856, CH-1215 Geneva 15CH-1215editor@inderscience.com':'Inderscience Publishers','Corporacion Colombiana de Investigacion Agropecuaria Corpoicarevista_corpoica@corpoica.org.co':'Corporacion Colombiana de Investigacion Agropecuaria Corpoica','Public Library of Scienceplos@plos.org':'Public Library of Science',
                                                                    'Universidad de Tarapacacsantoro@uta.cl':'Universidad de Tarapaca','De Gruyter Open Ltdkasia@cesj.com':'De Gruyter Open Ltd','IOS PressNieuwe Hemweg 6BAmsterdam1013 B':'IOS PressNieuwe Hemweg','Revista Ingenieria e Investigacion - Editorial BoardCalle 44 No. 45-67. Unidad Camilo Torres.Bloque B5. OficinaBogota401':'Revista Ingenieria e Investigacion - Editorial Board',
                                                                    'Sociedade Brasileira de Quimicaquimicanova@sbq.org.br':'Sociedade Brasileira de Quimica','Sociedade Brasileira de Quimicasbqsp@quim.ip.usp.br':'Sociedade Brasileira de Quimica','Lippincott Williams and Wilkinsagents@lww.com':'Lippincott Williams and Wilkins','Blackwell Publishing Ltdcustomerservices@oxonblackwellpublishing.com':'Blackwell Publishing Ltd',
                                                                    'CEUR-WSceurws@sunsite.informatik.rwth-aachen.de':'CEUR-WS','Wiley-VCH Verlaginfo@wiley-vch.de':'Wiley-VCH Verlag','Routledgeinfo@tandf.co.uk':'Routledge','Universidad de los Andes, Bogota ColombiaCalle 1 No. 18 A-12 Edificio Franco GB-417BogotaAU106res@uniandes.edu.co':'Universidad de los Andes','Universidad de los Andes, Bogota ColombiaCalle 1 No. 18 A-12 Edificio Franco GB-417BogotaAU106publicacionestaciso@uniandos.edu.co':'Universidad de los Andes',
                                                                    'Universidad de los Andes, Bogota Colombiares@uniandes.edu.co':'Universidad de los Andes','^Universidad de Los Andes$':'Universidad de los Andes','Universidad de Los Andesantipoda@uniandes.edu.co':'Universidad de los Andes','Universidad de los Andes, Bogota Colombia':'Universidad de los Andes','Sociedad Mexicana de Fisicarmf@hp.fciencias.unam.mx':'Sociedad Mexicana de Fisica',
                                                                    'Asociacion Colombiana de Reumatologiaasoreuma@epm.net.co':'Asociacion Colombiana de Reumatologia','Corporacion Universitaria Lasallistacomunicaciones@lasallista.edu.co':'Corporacion Universitaria Lasallista','Frontiers Media S.A.info@frontiersin.org':'Frontiers Media S.A.','SAGE Publications Ltdinfo@sagepub.co.uk':'SAGE Publications Ltd',
                                                                    'American Chemical Societyservice@acs.org':'American Chemical Society','Kluwer Academic Publishersbarbara.b.bertram@gsk.com':'Kluwer Academic Publishers','Facultad de Salud de la Universidad del Vallecomedica@univalle.edu.co':'Facultad de Salud de la Universidad del Valle','Current Science Inc.info@current-reports.com':'Current Science Inc.',
                                                                    'Dove Medical Press Ltd.PO Box 300-008, AlbanyAuckland':'Dove Medical Press Ltd.','Mary Ann Liebert Inc.info@liebertpub.com':'Mary Ann Liebert Inc.','American Institute of Physics Inc.subs@aip.org':'American Institute of Physics Inc.','Fed. Colombiana de Asoc. de Obstetricia y Ginecologia':'Federacion Colombiana de Asociaciones de Obstetricia y Ginecologia (FECOLSOG)',
                                                                    'Sociedad Chilena de Obstetricia y GinecologiaRoman Diaz 205, Officina 205':'Sociedad Chilena de Obstetricia y Ginecologia','Nature Publishing GroupHoundmillsBasingstoke, HampshireRG21 6XS':'Nature Publishing Group','Universitat Politecnica de ValenciaDISA\-Universitat Politècnica de València, C\. Vera, s\/n\.Valencia \(España\)46022informacion@upv.es':'Universitat Politecnica de Valencia',
                                                                    'Wolters Kluwer Medknow PublicationsB9, Kanara Business Centre, off Link Road, Ghatkopar \(E\)Mumbai400 075':'Wolters Kluwer Medknow Publications','Universidad de Costa Ricacristina.moreno@ucr.ac.cr':'Universidad de Costa Rica','Asociacion Espanola de Dietistas-Nutricionistasj.manager@renhyd.org':'Asociacion Espanola de Dietistas-Nutricionistas',
                                                                    '^Institute of Physics$':'Institute of Physics Publishing','University of Waterloosubscriptions@alternativesjournal.ca; editor@alternativesjournal.ca':'University of Waterloo','University of Waterloosubscription@alternativesjournal.ca':'University of Waterloo','PeerJ Inc.pete@peerj.com':'PeerJ Inc.','Sociedad Iberoamericana de Informacion Cientificaatencionallector@siicsalud.com':'Sociedad Iberoamericana de Informacion Cientifica',
                                                                    'Walter de Gruyter GmbHinfo@degruyter.com':'Walter de Gruyter GmbH','Cambridge University PressJournals_subscriptions@cup.cam.ac.uk':'Cambridge University Press','Korean Mathematical Societykms@kms.or.kr':'Korean Mathematical Society','Centar for Qualitycqm@kg.ac.rs':'Centar for Quality','Open Medicineinfo@openmedicine.ca':'Open Medicine',
                                                                    'Bentham Science PublishersP.O. Box 294Bussum1400 AG':'Bentham Science Publishers','Hindawi Publishing Corporation410 Park Avenue, 15th Floor, 287 pmbNew YorkNY 10022':'Hindawi Publishing Corporation','Publicaciones Dyna Slc/ Alameda Mazarredo 69 - 3BilbaoE48009':'Publicaciones Dyna Slc','Instituto Politecnico Nacionalrevista@cic.ipn.mx':'Instituto Politecnico Nacional','Universidad Complutense de Madridrcha@ghis.ucm.es':'Universidad Complutense de Madrid',
                                                                    'Universidad Complutense de Madridmaitgarc@pas.ucm.es':'Universidad Complutense de Madrid','Centro de Referencia em Informacao AmbientalAv. Romeu Tortima, 388, Barao Geraldo.Campinas, SPCEP 13084-791checklistjournal@yahoo.com':'Centro de Referencia em Informacao Ambiental','Centro de Referencia em Informacao AmbientalAv. Romeu Tortima, 388, Barao Geraldo.Campinas, SPCEP 13084-791':'Centro de Referencia em Informacao Ambiental',
                                                                    'Universidade Estadual Paulista \(UNESP\)dfil@marilia\.unesp\.br':'Universidade Estadual Paulista','Hikari Ltd.HIKARI LTD, P.O. Box 15Ruse7005hikaripublishers@m-hikari.com':'Hikari Ltd.','Hikari Ltd.HIKARI LTD, P.O. Box 15Ruse7005':'Hikari Ltd.','Universidad Nacional de Lanos29 de SeptiembreLanus,Buenos Aires,3901':'Universidad Nacional de Lanos','Mathematical Research Publisherstdiagana@howard.edu':'Mathematical Research Publisher',
                                                                    'Pushpa Publishing HouseVijaya Niwas, 198, MumfordganjAllahabad211002arun@pphmj.com':'Pushpa Publishing HouseVijaya','Group Psychology Campus Univalle - GEPUgepu@univalle.edu.co':'Group Psychology Campus Univalle - GEPU','Mathematical Society of the Rep. of Chinaalicef@math.nthu.edu.tw':'Mathematical Society of the Rep. of China','Science and Engineering Research Support Societyijbsbt@sersc.org':'Science and Engineering Research Support Society',
                                                                    'Ovidius UniversityMamaia Bd. 124Constanta900527':'Ovidius UniversityMamaia','American Geophysical Unioncustomerservices@oxonblackwellpublishing.com':'American Geophysical Union','Medwell Journalsmedwellonline@gmail.com':'Medwell Journals','Politechnika Wroclawskaoficwyd@pwr.wroc.pl':'Politechnika Wroclawska','International Press of Boston, Inc.P.O. Box 502387 Somerville AvenueMA 02143ipb-mgmt@intlpress.com':'International Press of Boston',
                                                                    'Centro de Ciencias de la Atmosfera, UNAMclaudio.amescua@atmosfera.unam.mx':'Centro de Ciencias de la Atmosfera, UNAM','Sociedad Quimica de Mexico A.C.delgado@servidor.unam.mx':'Sociedad Quimica de Mexico','Wiley-Blackwellinfo@wiley.com':'Wiley-Blackwell','University of Miskolcmatronto@uni-miskolc.hu':'University of Miskolc','Sociedad Colombiana de Cardiologia y Cirugia Cardiovascularpublicaciones@scc.org.co':'Sociedad Colombiana de Cardiologia y Cirugia Cardiovascular',
                                                                    'Universidad Distrital Francisco Jose de Caldascolombiaforestal.ud@correo.udistrital.edu.co':'Universidad Distrital Francisco Jose de Caldas','Sociedad Chilena de Nutricion Bromatologia y Toxilogicasochinut@chilesat.net':'Sociedad Chilena de Nutricion Bromatologia y Toxilogicas','Universidade do Vale do Rio dos SinosAv. Unisinos, 950 - Caixa Postal 275Sao Leopoldo - RSCEP 93022-000':'Universidade do Vale do Rio dos Sinos',
                                                                    'Fundacao de Pesquisas Cientificas de Ribeirao Pretofunpecrp@uol.com.br':'Fundacao de Pesquisas Cientificas de Ribeirao Preto','Spanish Research Councilredc@cindoc.csic.es':'Spanish Research Council','American Society of Agricultural and Biological Engineers2950 Niles RoadSt. JosephMI 49085-9659':'American Society of Agricultural and Biological Engineers','Sello editorial Universidad del Atlanticorhistoria@ocaribe.org':'Sello editorial Universidad del Atlantico',
                                                                    'Public Health Services, US Dept of Health and Human Servicesehp@jjeditorial.com':'Public Health Services, US Dept of Health and Human Services','Universidad Austral de Chileeped@uach.cl':'Universidad Austral de Chile','European Centre for Disease Prevention and Control \(ECDC\)ECDCStockholm171 83eurosutveiliance@eecdc.europa.eu':'European Centre for Disease Prevention and Control','Elsevier DoymaB9, Kanara Business Centre, off Link Road, Ghatkopar \(E\)Mumbai400 075':'Elsevier Doyma',
                                                                    'Universidad Autonoma del Estado de Mexicorevistaconvergencia@yahoo.com.mx':'Universidad Autonoma del Estado de Mexico','A.D.A.C.C.P. 39, 57 rue CuvierParis Cedex 05F-75231':'A.D.A.C.C.P.','Asociacion Espanola de la Carreteraaec@aecarretera.com':'Asociacion Espanola de la Carretera','Comite Latinoamericano de Matematica Educativarelime@clame.org.mx':'Comite Latinoamericano de Matematica Educativa',
                                                                    'Universidade de Minas Geraiskriterion@fafich.ufmg.br':'Universidade de Minas Gerais','IADISsecretariat@iadis.org':'IADIS','Association Quimica Argentinaanales@inifta.unlp.edu.ar':'Association Quimica Argentina','Informa Healthcarehealthcare.enquiries@informa.com':'Informa Healthcare','AGH University of Science and Technologyopuscula@agh.edu.pl':'AGH University of Science and Technology','Ediciones Universidad de SalamancaPlaza de San Benito, 2':'Ediciones Universidad de Salamanca',
                                                                    'Universidad de CordobaKilometro 28 Via Monteria -Cienaga de OroMonteria Cordoba':'Universidad de Cordoba','Asociacion Colombiana de OrnitologiaTransversal 18A BIS No. 37-92Bogotaornitologiacolombiana@yahoo.com':'Asociacion Colombiana de Ornitologia','American Association for Cancer Research Inc.helen.atkins@aacr.org':'American Association for Cancer Research Inc.','Texas State University - San Marcoseditor@ejde.math.txstate.edu':'Texas State University - San Marcos',
                                                                    'Pensoft Publishersinfo@pensoft.net':'Pensoft Publishers','IEOM Societyieom-society@iieom.org':'IEOM Society','Asociacion Iberica de LimnologiaPorche 2.1Mislata46920':'Asociacion Iberica de Limnologia','Polska Akademia Naukpubl@impan.gov.pl':'Polska Akademia Nauk','Fibonacci Associationsolsaap@itctel.com':'Fibonacci Association','Interamerican Society for Electron Microscopy \(CIASEM\)Carretera PanamericanaKm\. 11\. Apartado Postal 20632,Caracas1020\-A':'Interamerican Society for Electron Microscopy (CIASEM)',
                                                                    'American Academy of Pediatricscsc@aap.org':'American Academy of Pediatrics','Carl Hanser VerlagKolbergerstrasse 22MunchenD-81679':'Carl Hanser Verlag','Sociedad Chilena de Pediatriarevistachilenadepediatria@gmail.com':'Sociedad Chilena de Pediatria','Complex Systems Publications, Incinfo@complex-systems.com':'Complex Systems Publications, Inc','wiley':'Wiley','^Universidad de Chile, Facultad de Ciencias Socialesmanuel.loyola@usach.cl$':'Universidad de Chile',
                                                                    'Ecological Society of America1900 M Street NW, Suite 700WashingtonDC 20036':'Ecological Society of America','Universidad Pedagogica y Tecnologica de Colombia, Instituto de Investigaciones y Formacion Avanzada':'Universidad Pedagogica y Tecnologica de Colombia','IWA Publishing12 Caxton StreetLondonSW1H 0QS':'IWA Publishing','Annual Reviews Inc.4139 El Camino Way, P.O. Box 10139Palo AltoCA 94306':'Annual Reviews Inc.','Universidad de Magallanesmagallania@umag.cl':'Universidad de Magallanes',
                                                                    'Escuela Interamericana de Bibliotecologiarevistabibliotecologia@udea.edu.co':'Escuela Interamericana de Bibliotecologia','Ministry Education and ScienceSan Fernando Del Jarama 14Madrid28002':'Ministry Education and ScienceSan Fernando Del Jarama','Universidade Federal de Campina Grandecmci@ccsa.ufpb.br':'Universidade Federal de Campina Grande','Bridgewater State Collegejbodi@bridgew.edu':'Bridgewater State College','Sociedade Brasileira de Medicina Tropicalcarlos@rsbmt.uftm.edu.br':'Sociedade Brasileira de Medicina Tropical',
                                                                    'Universidad Nacional Autonoma de Mexicoiieanales@gmail.com':'Universidad Nacional Autonoma de Mexico','King Saud Universityinfo@ksu.edu.sa':'King Saud University','American Scientific Publishersorder@aspbs.com':'American Scientific Publishers','BMJ Publishing Groupsubscriptions@bmjgroup.com':'BMJ Publishing Group','Universidad del NorteKm 5 Via PuertoBarranquilla,':'Universidad del Norte',
                                                                    'Sociedad Espanola de Nutricion Comunitariainfo@nutricioncomunitaria.org':'Sociedad Espanola de Nutricion Comunitaria','Societas Europaea Herpetologicaherpetologynoteseditor@gmail.com':'Societas Europaea Herpetologica','Institute of Mathematics. Polish Academy of SciencesZADROZNY@IMPAN.PL':'Institute of Mathematics. Polish Academy of Sciences','Sociedad Mexicana de Pediatriaemyc@medigraphic.com':'Sociedad Mexicana de Pediatria','Science Publishing Corporation Incijet@sciencepubco.com':'Science Publishing Corporation Inc',
                                                                    'Sociedad espanola de dieteticaGuadiana, 7Pozuelo, Madrid28224revista@nutricion.org':'Sociedad espanola de dietetica','University of Novi Sad, Faculty of TechnologyBul. Cara Lazara 1,21000 Novi Sad,21000sanya@uns.ac.rs':'University of Novi Sad, Faculty of Technology','Universidad Austral de Chilerevider@uach.cl':'Universidad Austral de Chile','KKS FLU AV CRlf@ics.cas.cz':'KKS FLU AV CR','Pontificia Universidade Catolica de Campinascleo@acad.puccamp.br':'Pontificia Universidade Catolica de Campinas',
                                                                    'American Institute of Mathematical SciencesPO Box 2604SpringfieldMO 65801-2604':'American Institute of Mathematical Sciences','Informing Science Institute131 Brookhill CourtSanta RosaCA 95409-2464':'Informing Science Institute131 Brookhill Court','Editora UFLACaixa Postal 3037Lavras, MG37200-000coffeescience@dag.ufla.br':'Editora UFLACaixa','Universidad Alberto Hurtadorae@uahurtado.cl':'Universidad Alberto Hurtado','EDIMES Edizioni Medico Scientificheinfezmed@libero.it':'EDIMES Edizioni Medico Scientific',
                                                                    'Universidad de Alicantejose.perez@ua.es':'Universidad de Alicante','Inter-Researchmarita@int-res.com':'Inter-Research','Institution of Engineering and Technologykvukmirovic@theiet.org':'Institution of Engineering and Technology','^Universidad de Chile, Facultad de Ciencias Socialespablo.lopez@uv.cl$':'Universidad de Chile','SPIEspie@spie.org':'SPIE','TUBITAKerdin@metu.edu.tr':'TUBITAK',
                                                                    'Asociacion Colombiana de OrnitologiaTransversal 18A BIS No. 37-92Bogotarevista.ornitologia.colombiana@gmail.com':'Asociacion Colombiana de Ornitologia','Akademiai Kiado Rt.info@akkrt.hu':'Akademiai Kiado','Edipucrscivitas@pucrs.br':'No Aplica','Universidad de Alicanterevistaobets@ua.es':'Universidad de Alicante','ASERS Publishing HouseNo 5, Sabba Stefanescu Street, 200145':'ASERS Publishing','Asociacion Mexicana de Gastroenterologialtorres@gastro.org.mx':'Asociacion Mexicana de Gastroenterologia',
                                                                    'Sciendomacvetrev@fvm.ukim.edu.mk':'No Aplica','ICE Publishingsubscriptions@icepublishing.com':'ICE Publishing','Universidad del RosarioCalle 14, 4-69Bogota':'Universidad del Rosario','Universidad Simon Bolivarrlmm@usb.ve':'Universidad Simon Bolivar','Sociedad de Anestesiologia de Chileinfo@biomedcentral.com':'Sociedad de Anestesiologia de Chile'}, regex=True)
scopus_productos['editorial']=scopus_productos['editorial'].replace({'MDPIrasetti@mdpi.com':'MDPI','Universidad de Chilepablo.lopez@uv.cl':'Universidad de Chile','MDPIindexing@mdpi.com':'MDPI','Universidad de Chilemanuel.loyola@usach.cl':'Universidad de Chile'},regex=True)
scopus_productos['institucion']=scopus_productos['institucion'].fillna('No Aplica')
col=scopus_productos.copy()
col['institucion']=col['institucion'].str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace(r'/\s+/g',' ',regex=True).str.replace(r'[^a-zA-Z0-9 ]','', regex=True).str.strip()
byinst_normalized=col.groupby('institucion')
col=0
for key in list(byinst_normalized.groups.keys()):  
    scopus_productos.iloc[list(byinst_normalized.get_group(key).index),19]=scopus_productos.iloc[list(byinst_normalized.get_group(key).index)]['institucion'].value_counts().index[0]
byinst_normalized=0
scopus_productos['institucion']=scopus_productos['institucion'].replace({'Médico general':'No Aplica','^Colombia$':'No Aplica','':'No Aplica','^and Control$':'No Aplica','^IU Colegio Mayor del Cauca$':'Institución Universitaria Colegio Mayor del Cauca',
                                                                      'Hospital Universitario San José de Popayán':'Hospital Universitario San José','InnovaGen Foundation':'Fundación InnovaGen','Fundacion EcoHabitats':'Fundación Ecohabitats',
                                                                      '^TECNICAFE$':'Parque Tecnológico de Innovación del Café - TECNICAFÉ','Vejarano Ophthalmological Foundation':'Fundación Oftalmológica Vejarano',
                                                                      'Fundación Ecohábitats':'Fundación Ecohabitats','Efigenia Aerospace Robotics Autonomous Unmanned Aerial Vehicles Research, Colombia':'EFIGENIA Aerospace Robotics Research',
                                                                       'Efigenia Aerospace Robotics Autonomous Unmanned Aerial Vehicles Research, Colombia, EFIGENIA Aerospace Robotics Research':'EFIGENIA Aerospace Robotics Research',
                                                                      'Grupo de Investigación en Diseño y Arte \(D&A\)':'Universidad Mayor','\(CYTBIA\)':'CYTBIA','Hospital Universitário San José':'Hospital Universitario San José',
                                                                       'Investigador Adscrito al Centro Regional de Productividad e Innovación del Cauca-CREPIC':'Centro Regional de Productividad e Innovación del Cauca-CREPIC',
                                                                        'Faculty of Health Sciences':'Universidad del Cauca','^CGS$':'Colombian Geological Service','Bachiller Comunero del Resguardo de Puracé':'Resguardo de Puracé',
                                                                        'Tecnólogo Ambiental Comunero del Resguardo de Puracé':'Resguardo de Puracé','Hospital Universitário':'Hospital Universitário San José',
                                                                        '^IVSI$':'Synthetic Vaccine and New Drug Research Institute \– IVSI','University of Cauca–CREPIC':'Centro Regional de Productividad e Innovación del Cauca-CREPIC',
                                                                        'Environmental Division Acueducto y Alcantarillado de Popayán S\.A\. E\.S\.P\. \(Popayán Water and Sewage Company\)':'Division Acueducto y Alcantarillado de Popayán S.A. E.S.P.',
                                                                        'Sena':'SENA','SENNOVA':'SENA','Health Specialists Center-Renacer Ltda.':'Centro de Especialistas en Salud Integral Renacer Ltda'}, regex=True)

pattern='|'.join(['Facultad de Ingeniería Electrónica y Telecomunicaciones Universidad del Cacuca','U. de Toxicol. Genet. Y Citogenetica','Systems Engineering Program University of Cauca Popayán','\(CYTBIA\)','ECCO','^FIET$','Grupo de investigación de Ingeniería Telemática','Umversidad Del Cauca-DCE','University of Cauca at Tulcán'])
scopus_productos['institucion']=scopus_productos['institucion'].str.replace(pattern, 'Universidad del Cauca',regex=True)
pattern = '|'.join(['University Foundation of Popayán','^Universitaria de Popayán$','^Fundación Universitaria de$','Fundacion Universitaria de Popayán','Popayán University Foundation'])
scopus_productos['institucion']=scopus_productos['institucion'].str.replace(pattern, 'Fundación Universitaria de Popayán',regex=True)
pattern = '|'.join(['Programa de Ingeniería de Sistemas Unicomfacauca','Corporación Universitaria Comfacauca \- Unicomfacauca','Corporación Universitaria Comfacauca \-\- Unicomfacauca','Comfacauca University Corporation','Corporación Universitaria Comfacauca\—Unicomfacauca','Unicomfacauca University',
                    'Unicomfacauca Grupode Investigation en Sistemaslnteligentes','Grupo de Investigación en Sistemas Inteligentes GISI, Corporación Universitaria Comfacauca','^Grupo de Investigation en Sistemas Inteligentes$'])
scopus_productos['institucion']=scopus_productos['institucion'].str.replace(pattern, 'Corporación Universitaria Comfacauca',regex=True)
pattern = '|'.join(['Technology Development Center, Corporation Cluster CreaTIC','^Grupo de Investigación CreaTIC$'])
scopus_productos['institucion']=scopus_productos['institucion'].str.replace(pattern, 'Centro de desarrollo tecnológico CREATIC',regex=True)
pattern = '|'.join(['Intensive Care Unit La Estancia Clinic','^Clínica La Estancia$'])
scopus_productos['institucion']=scopus_productos['institucion'].str.replace(pattern, 'Clínica la Estancia',regex=True)
pattern = '|'.join(['National Open and Distance University','^UNAD$','^Universidad Nacional Abierta y a Distancia - UNAD$','Open and Distance National University'])
scopus_productos['institucion']=scopus_productos['institucion'].str.replace(pattern, 'Universidad Nacional Abierta y a Distancia',regex=True)
pattern = '|'.join(['^Corporación Del Laboratorio al Campo$','Del Laboratorio al Campo-Grupo de Investigación en Biotecnología y Biomedicina \(BIOTECMED\)'])
scopus_productos['institucion']=scopus_productos['institucion'].str.replace(pattern, 'Corporación del Laboratorio al Campo',regex=True)
pattern = '|'.join(['Clínica de Rehabilitación Integral Fisiocenter-Área de Fonoaudiología','Fisioterapeuta Fisiocenter'])
scopus_productos['institucion']=scopus_productos['institucion'].str.replace(pattern, 'Clínica de Rehabilitación Integral Fisiocenter',regex=True)

set_institucion_scopus=set()
scopus_productos['institucion'].apply(lambda x: set_institucion_scopus.update(x.split(';'))) #cambiar por ';'

a=list(set_institucion_scopus)
a=[s.strip() for s in a] # comentar a futuro
b=df['0'].tolist()
c = [i for i in b if i in a]
afiliaciones_emparejadas_p=c

print('Total de afiliaciones en productos de Scopus: ',len(set(afiliaciones_emparejadas_p)))
print('Total de afiliaciones identificadas en Scopus tras limpieza: ',len(set(b)))
print("Total de afiliaciones en Gruplac para el Cauca: ",gruplac_instituciones['nombre'].drop_duplicates().shape[0])
a=0
b=0
c=0
df=0
pattern=0
set_institucion_scopus=0

#MANEJO DE DUPLICADOS

scopus_autores=scopus_autores.sort_values(['documentos','citaciones'],ascending=False).drop_duplicates(['nombre','institucion'],keep='first')
scopus_autores=scopus_autores[scopus_autores['autor_id'].isin(['57534159600','57210376968','57614233300'])==False]
scopus_productos=scopus_productos.sort_values(['citado'],ascending=False).drop_duplicates(['institucion','editorial','titulo','doi'],keep='first')
scopus_productos=scopus_productos.drop_duplicates(['editorial','titulo','fecha_publicacion','autores'],keep='first')
scopus_productos=scopus_productos.drop_duplicates(['institucion','editorial','doi','autores'],keep='first')

scopus_autores.to_csv('dashboard/assets/data/preprocessed_data/scopus_autores.csv',index=False)
scopus_productos.to_csv('dashboard/assets/data/preprocessed_data/scopus_productos.csv',index=False)

#ESTADÍSTICAS
print("")
print("Total de autores en Scopus para el Cauca: ",scopus_autores.shape[0])
print("Grupos visibles en Scopus a partir de autores: ",scopus_autores['idgruplac'].dropna().drop_duplicates(keep='first').shape[0])
set_grupos=[]
scopus_productos['idgruplac'].dropna().str.split(';').apply(lambda x: set_grupos.extend(x))
set_grupos=set(set_grupos)
print("Grupos visibles en Scopus a partir de productos: ",len(set_grupos))
print("")
print("Total de autores en Scopus emparejados con grupos: ",scopus_autores[~scopus_autores['idgruplac'].isna()].shape[0], " de ",scopus_autores.shape[0])
print("Total de productos en Scopus emparejados con grupos: ",scopus_productos[~scopus_productos['idgruplac'].isna()].shape[0], " de ",scopus_productos.shape[0])
print("")
print("Total de autores en Gruplac para el Cauca: ",gruplac_integrantes['url'].drop_duplicates().shape[0])
print("Grupos en Gruplac: ",gruplac_basico.shape[0])
print("")
gruplac_lineas_copy=gruplac_lineas.copy()
gruplac_lineas_copy['lineas']=gruplac_lineas_copy['lineas'].str.split(';')
gruplac_lineas_copy=gruplac_lineas_copy.explode('lineas')
gruplac_lineas_copy=gruplac_lineas_copy.groupby('lineas').size().reset_index(name='count').sort_values(by='count',ascending=False)
print('Total de líneas de investigación entre los grupos del Cauca: ',gruplac_lineas_copy.shape[0])
gruplac_lineas_copy=gruplac_lineas_copy[gruplac_lineas_copy['count']>1]
print('Total de líneas de investigación compartidas entre los grupos: ',gruplac_lineas_copy.shape[0])
print("**************PREPROCESAMIENTO FINALIZADO***************")



