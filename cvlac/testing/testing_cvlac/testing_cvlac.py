import unittest

import numpy as np
import pandas as pd

from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.util import get_lxml


#las url de testing son tomadas de manera aleatoria con SQL desde la base de datos generada
"""
SQL QUERY:

SELECT idcvlac FROM <table>
ORDER BY RANDOM( )
LIMIT 3;

"""

class prueba_unitaria(unittest.TestCase):
    def test_dfs(self, df_auto, df_manu):
        pd.testing.assert_frame_equal(df_auto,df_manu, check_column_type=False, check_dtype=False)


def run_unittests_cvlac():
    
    Extractor=ExtractorCvlac()
    test=prueba_unitaria()
    
    ##########################
    #Prueba tabla tecnologicos
    ##########################
    
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000331589'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001380950'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000881040'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_tecnologicos(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/tecnologicos1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.tecnologicos = Extractor.tecnologicos.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_tecnologicos(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/tecnologicos2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.tecnologicos = Extractor.tecnologicos.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_tecnologicos(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/tecnologicos3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: tecnologicos')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla software
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001388030'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000012947'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001425138'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_software(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/software1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.software = Extractor.software.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_software(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/software2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.software = Extractor.software.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_software(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/software3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: software')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla redes
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001403787'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001474779'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000103547'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_redes(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/redes1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.redes = Extractor.redes.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_redes(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/redes2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.redes = Extractor.redes.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_redes(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/redes3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: redes')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla reconocimiento
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001239368'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001566534'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000652636'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_reconocimiento(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/reconocimiento1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.reconocimiento = Extractor.reconocimiento.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_reconocimiento(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/reconocimiento2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.reconocimiento = Extractor.reconocimiento.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_reconocimiento(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/reconocimiento3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: reconocimiento')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla prototipo
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001562582'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000000555'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001433528'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_prototipo(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/prototipo1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.prototipo = Extractor.prototipo.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_prototipo(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/prototipo2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.prototipo = Extractor.prototipo.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_prototipo(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/prototipo3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: prototipo')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla libros
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000011606'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000470252'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000561460'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_libro(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/libros1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.libros = Extractor.libros.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_libro(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/libros2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.libros = Extractor.libros.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_libro(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/libros3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: libros')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla jurados
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001430742'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001348276'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001565693'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_jurado(lxml_url1,url1).sort_values('titulo',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/jurado1.csv', dtype='object', keep_default_na=False).sort_values('titulo',ignore_index=True)
    Extractor.jurados = Extractor.jurados.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_jurado(lxml_url2,url2).sort_values('titulo',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/jurado2.csv', dtype='object', keep_default_na=False).sort_values('titulo',ignore_index=True)
    Extractor.jurados = Extractor.jurados.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_jurado(lxml_url3,url3).sort_values('titulo',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/jurado3.csv', dtype='object', keep_default_na=False).sort_values('titulo',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: jurados')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla investigacion
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000013323'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000063130'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000350028'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_investiga(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/investiga1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.investigacion = Extractor.investigacion.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_investiga(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/investiga2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.investigacion = Extractor.investigacion.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_investiga(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/investiga3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: investigacion')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla innovacion_empresarial
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000215899'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001424171'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000870994'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_innovacion(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/innova1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.innovacion_empresarial = Extractor.innovacion_empresarial.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_innovacion(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/innova2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.innovacion_empresarial = Extractor.innovacion_empresarial.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_innovacion(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/innova3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: innovacion_empresarial')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla idioma
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000011720'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000185997'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000676446'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_idioma(lxml_url1,url1).sort_values('idioma',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/idioma1.csv', dtype='object', keep_default_na=False).sort_values('idioma',ignore_index=True)
    Extractor.idioma = Extractor.idioma.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_idioma(lxml_url2,url2).sort_values('idioma',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/idioma2.csv', dtype='object', keep_default_na=False).sort_values('idioma',ignore_index=True)
    Extractor.idioma = Extractor.idioma.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_idioma(lxml_url3,url3).sort_values('idioma',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/idioma3.csv', dtype='object', keep_default_na=False).sort_values('idioma',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: idioma')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla identificadores
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001239368'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001787051'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001343159'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_identificadores(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/identificadores1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.identificadores = Extractor.identificadores.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_identificadores(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/identificadores2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.identificadores = Extractor.identificadores.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_identificadores(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/identificadores3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: identificadores')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla evaluador
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001378453'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000491012'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000011410'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_evaluador(lxml_url1,url1).sort_values(['ambito','fecha'],ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/evaluador1.csv', dtype='object', keep_default_na=False).sort_values(['ambito','fecha'],ignore_index=True)
    Extractor.evaluador = Extractor.evaluador.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_evaluador(lxml_url2,url2).sort_values(['ambito','fecha'],ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/evaluador2.csv', dtype='object', keep_default_na=False).sort_values(['ambito','fecha'],ignore_index=True)
    Extractor.evaluador = Extractor.evaluador.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_evaluador(lxml_url3,url3).sort_values(['ambito','fecha'],ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/evaluador3.csv', dtype='object', keep_default_na=False).sort_values(['ambito','fecha'],ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: evaluador')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla estancias
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000399213'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001721573'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000524492'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_estancias(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/estancias1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.estancias = Extractor.estancias.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_estancias(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/estancias2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.estancias = Extractor.estancias.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_estancias(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/estancias3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: estancias')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla empresa_tecnologica
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000031614'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001364033'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001380834'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_empresa_tecnologica(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/empresa_tecnologica1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.empresa_tecnologica = Extractor.empresa_tecnologica.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_empresa_tecnologica(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/empresa_tecnologica2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.empresa_tecnologica = Extractor.empresa_tecnologica.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_empresa_tecnologica(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/empresa_tecnologica3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: empresa_tecnologica')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla complementaria
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000674460'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000205087'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000028625'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_complementaria(lxml_url1,url1).sort_values(['titulo','fecha'],ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/complementaria1.csv', dtype='object', keep_default_na=False).sort_values(['titulo','fecha'],ignore_index=True)
    Extractor.complementaria = Extractor.complementaria.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_complementaria(lxml_url2,url2).sort_values(['titulo','fecha'],ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/complementaria2.csv', dtype='object', keep_default_na=False).sort_values(['titulo','fecha'],ignore_index=True)
    Extractor.complementaria = Extractor.complementaria.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_complementaria(lxml_url3,url3).sort_values(['titulo','fecha'],ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/complementaria3.csv', dtype='object', keep_default_na=False).sort_values(['titulo','fecha'],ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: complementaria')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla caplibros
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001368052'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001436146'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001602134'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_caplibro(lxml_url1,url1).sort_values('capitulo',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/caplibros1.csv', dtype='object', keep_default_na=False).sort_values('capitulo',ignore_index=True)
    Extractor.caplibros = Extractor.caplibros.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_caplibro(lxml_url2,url2).sort_values('capitulo',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/caplibros2.csv', dtype='object', keep_default_na=False).sort_values('capitulo',ignore_index=True)
    Extractor.caplibros = Extractor.caplibros.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_caplibro(lxml_url3,url3).sort_values('capitulo',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/caplibros3.csv', dtype='object', keep_default_na=False).sort_values('capitulo',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: caplibros')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla basico
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001452311'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001412764'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001471317'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_basico(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/basico1.csv', dtype='object', keep_default_na=False)
    Extractor.basico = Extractor.basico.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_basico(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/basico2.csv', dtype='object', keep_default_na=False)
    Extractor.basico = Extractor.basico.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_basico(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/basico3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: basico')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla articulos
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001625568'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000317535'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000013030'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_articulo(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/articulos1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.articulos = Extractor.articulos.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_articulo(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/articulos2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.articulos = Extractor.articulos.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_articulo(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/articulos3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: articulos')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)

    ##########################
    #Prueba tabla actuacion
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000431974'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001674093'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001380980'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_actuacion(lxml_url1,url1).sort_values('areas',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/actuacion1.csv', dtype='object', keep_default_na=False).sort_values('areas',ignore_index=True)
    Extractor.actuacion = Extractor.actuacion.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_actuacion(lxml_url2,url2).sort_values('areas',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/actuacion2.csv', dtype='object', keep_default_na=False).sort_values('areas',ignore_index=True)
    Extractor.actuacion = Extractor.actuacion.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_actuacion(lxml_url3,url3).sort_values('areas',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/actuacion3.csv', dtype='object', keep_default_na=False).sort_values('areas',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: actuacion')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla academica
    ##########################
    url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001538712'
    url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000101188'
    url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001672586'
    
    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_academica(lxml_url1,url1).sort_values('titulo',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_cvlac/academica1.csv', dtype='object', keep_default_na=False).sort_values('titulo',ignore_index=True)
    Extractor.academica = Extractor.academica.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_academica(lxml_url2,url2).sort_values('titulo',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_cvlac/academica2.csv', dtype='object', keep_default_na=False).sort_values('titulo',ignore_index=True)
    Extractor.academica = Extractor.academica.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_academica(lxml_url3,url3).sort_values('titulo',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_cvlac/academica3.csv', dtype='object', keep_default_na=False).sort_values('titulo',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: academica')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)