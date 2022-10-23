import unittest

import numpy as np
import pandas as pd

from cvlac.ExtractorGruplac import ExtractorGruplac
from cvlac.util import get_lxml

#las url de testing son tomadas de manera aleatoria con SQL desde la base de datos generada
"""
SQL QUERY:

SELECT idgruplac FROM <table>
ORDER BY RANDOM( )
LIMIT 3;

"""

class prueba_unitaria(unittest.TestCase):
    def test_dfs(self, df_auto, df_manu):
        pd.testing.assert_frame_equal(df_auto,df_manu, check_column_type=False, check_dtype=False)


def run_unittests_gruplac():
    
    Extractor=ExtractorGruplac()
    test=prueba_unitaria()
    
    ##########################
    #Prueba tabla software
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000003792'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000011727'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000006175'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_software(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/software1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_software = Extractor.perfil_software.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_software(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/software2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_software = Extractor.perfil_software.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_software(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/software3.csv', dtype='object', keep_default_na=False)

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
    #Prueba tabla prototipos
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000018223'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000014080'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000005833'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_prototipos(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/prototipos1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_prototipos = Extractor.perfil_prototipos.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_prototipos(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/prototipos2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_prototipos = Extractor.perfil_prototipos.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_prototipos(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/prototipos3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: prototipos')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    

    ##########################
    #Prueba tabla programa_maestria
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002142'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002191'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_programa_maestria(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/programa_maestria1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_programa_maestria = Extractor.perfil_programa_maestria.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_programa_maestria(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/programa_maestria2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_programa_maestria = Extractor.perfil_programa_maestria.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_programa_maestria(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/programa_maestria3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: programa_maestria')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla programa_doctorado
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002192'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008159'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_programa_doctorado(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/programa_doctorado1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_programa_doctorado = Extractor.perfil_programa_doctorado.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_programa_doctorado(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/programa_doctorado2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_programa_doctorado = Extractor.perfil_programa_doctorado.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_programa_doctorado(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/programa_doctorado3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: programa_doctorado')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla planta_piloto
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000015901'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000000592'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000005833'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_planta_piloto(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/planta_piloto1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_planta_piloto = Extractor.perfil_planta_piloto.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_planta_piloto(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/planta_piloto2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_planta_piloto = Extractor.perfil_planta_piloto.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_planta_piloto(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/planta_piloto3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: planta_piloto')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla otros_tecnologicos
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000006312'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002192'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000010829'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_otros_tecnologicos(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/otros_tecnologicos1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_otros_tecnologicos = Extractor.perfil_otros_tecnologicos.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_otros_tecnologicos(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/otros_tecnologicos2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_otros_tecnologicos = Extractor.perfil_otros_tecnologicos.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_otros_tecnologicos(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/otros_tecnologicos3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: otros_tecnologicos')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla otros_libros
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000000694'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008156'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002146'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_otros_libros(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/otros_libros1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_otros_libros = Extractor.perfil_otros_libros.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_otros_libros(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/otros_libros2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_otros_libros = Extractor.perfil_otros_libros.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_otros_libros(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/otros_libros3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: otros_libros')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla otros_articulos
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000000316'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000001155'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000016547'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_otros_articulos(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/otros_articulos1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_otros_articulos = Extractor.perfil_otros_articulos.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_otros_articulos(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/otros_articulos2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_otros_articulos = Extractor.perfil_otros_articulos.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_otros_articulos(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/otros_articulos3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: otros_articulos')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla otro_programa
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000000668'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000007827'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002153'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_otro_programa(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/otro_programa1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_otro_programa = Extractor.perfil_otro_programa.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_otro_programa(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/otro_programa2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_otro_programa = Extractor.perfil_otro_programa.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_otro_programa(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/otro_programa3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: otro_programa')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)