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