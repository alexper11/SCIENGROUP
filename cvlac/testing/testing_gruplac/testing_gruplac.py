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
    df_auto1=Extractor.get_perfil_software(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/software1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_software = Extractor.perfil_software.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_software(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/software2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_software = Extractor.perfil_software.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_software(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/software3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

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
    df_auto1=Extractor.get_perfil_prototipos(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/prototipos1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_prototipos = Extractor.perfil_prototipos.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_prototipos(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/prototipos2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_prototipos = Extractor.perfil_prototipos.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_prototipos(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/prototipos3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

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
    df_auto1=Extractor.get_perfil_programa_maestria(lxml_url1,url1).sort_values('programa',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/programa_maestria1.csv', dtype='object', keep_default_na=False).sort_values('programa',ignore_index=True)
    Extractor.perfil_programa_maestria = Extractor.perfil_programa_maestria.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_programa_maestria(lxml_url2,url2).sort_values('programa',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/programa_maestria2.csv', dtype='object', keep_default_na=False).sort_values('programa',ignore_index=True)
    Extractor.perfil_programa_maestria = Extractor.perfil_programa_maestria.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_programa_maestria(lxml_url3,url3).sort_values('programa',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/programa_maestria3.csv', dtype='object', keep_default_na=False).sort_values('programa',ignore_index=True)

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
    df_auto1=Extractor.get_perfil_programa_doctorado(lxml_url1,url1).sort_values('programa',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/programa_doctorado1.csv', dtype='object', keep_default_na=False).sort_values('programa',ignore_index=True)
    Extractor.perfil_programa_doctorado = Extractor.perfil_programa_doctorado.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_programa_doctorado(lxml_url2,url2).sort_values('programa',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/programa_doctorado2.csv', dtype='object', keep_default_na=False).sort_values('programa',ignore_index=True)
    Extractor.perfil_programa_doctorado = Extractor.perfil_programa_doctorado.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_programa_doctorado(lxml_url3,url3).sort_values('programa',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/programa_doctorado3.csv', dtype='object', keep_default_na=False).sort_values('programa',ignore_index=True)

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
    df_auto1=Extractor.get_perfil_planta_piloto(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/planta_piloto1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_planta_piloto = Extractor.perfil_planta_piloto.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_planta_piloto(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/planta_piloto2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_planta_piloto = Extractor.perfil_planta_piloto.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_planta_piloto(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/planta_piloto3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

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
    df_auto1=Extractor.get_perfil_otros_tecnologicos(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/otros_tecnologicos1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_otros_tecnologicos = Extractor.perfil_otros_tecnologicos.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_otros_tecnologicos(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/otros_tecnologicos2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_otros_tecnologicos = Extractor.perfil_otros_tecnologicos.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_otros_tecnologicos(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/otros_tecnologicos3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

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
    df_auto1=Extractor.get_perfil_otros_libros(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/otros_libros1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_otros_libros = Extractor.perfil_otros_libros.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_otros_libros(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/otros_libros2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_otros_libros = Extractor.perfil_otros_libros.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_otros_libros(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/otros_libros3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

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
    df_auto1=Extractor.get_perfil_otros_articulos(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/otros_articulos1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_otros_articulos = Extractor.perfil_otros_articulos.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_otros_articulos(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/otros_articulos2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_otros_articulos = Extractor.perfil_otros_articulos.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_otros_articulos(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/otros_articulos3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

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
    df_auto1=Extractor.get_perfil_otro_programa(lxml_url1,url1).sort_values('programa',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/otro_programa1.csv', dtype='object', keep_default_na=False).sort_values('programa',ignore_index=True)
    Extractor.perfil_otro_programa = Extractor.perfil_otro_programa.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_otro_programa(lxml_url2,url2).sort_values('programa',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/otro_programa2.csv', dtype='object', keep_default_na=False).sort_values('programa',ignore_index=True)
    Extractor.perfil_otro_programa = Extractor.perfil_otro_programa.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_otro_programa(lxml_url3,url3).sort_values('programa',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/otro_programa3.csv', dtype='object', keep_default_na=False).sort_values('programa',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: otro_programa')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla lineas
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002157'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000019510'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_lineas(lxml_url1,url1).sort_values('lineas',ignore_index=True).astype(str)
    #print(df_auto1.iloc[0,1].split(';').sort())
    df_auto1.iloc[0,1]=';'.join(sorted(df_auto1.iloc[0,1].split(';')))
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/lineas1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_lineas = Extractor.perfil_lineas.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_lineas(lxml_url2,url2).astype(str)
    df_auto2.iloc[0,1]=';'.join(sorted(df_auto2.iloc[0,1].split(';')))
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/lineas2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_lineas = Extractor.perfil_lineas.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_lineas(lxml_url3,url3).astype(str)
    df_auto3.iloc[0,1]=';'.join(sorted(df_auto3.iloc[0,1].split(';')))
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/lineas3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: lineas')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla integrantes
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000020815'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000021902'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000017266'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_integrantes(lxml_url1,url1).sort_values('integrante',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/integrantes1.csv', dtype='object', keep_default_na=False).sort_values('integrante',ignore_index=True)
    Extractor.perfil_integrantes = Extractor.perfil_integrantes.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_integrantes(lxml_url2,url2).sort_values('integrante',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/integrantes2.csv', dtype='object', keep_default_na=False).sort_values('integrante',ignore_index=True)
    Extractor.perfil_integrantes = Extractor.perfil_integrantes.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_integrantes(lxml_url3,url3).sort_values('integrante',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/integrantes3.csv', dtype='object', keep_default_na=False).sort_values('integrante',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: integrantes')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla instituciones
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000003625'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002141'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000020932'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_instituciones(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/instituciones1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_instituciones = Extractor.perfil_instituciones.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_instituciones(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/instituciones2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_instituciones = Extractor.perfil_instituciones.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_instituciones(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/instituciones3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: instituciones')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
        
    ##########################
    #Prueba tabla innovacion_empresarial
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000007096'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000005833'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000007276'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_innovacion_empresarial(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/innovacion_empresarial1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_innovacion_empresarial = Extractor.perfil_innovacion_empresarial.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_innovacion_empresarial(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/innovacion_empresarial2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_innovacion_empresarial = Extractor.perfil_innovacion_empresarial.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_innovacion_empresarial(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/innovacion_empresarial3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

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
    #Prueba tabla empresa_tecnologica
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000001995'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000007827'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_empresa_tecnologica(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/empresa_tecnologica1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_empresa_tecnologica = Extractor.perfil_empresa_tecnologica.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_empresa_tecnologica(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/empresa_tecnologica2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_empresa_tecnologica = Extractor.perfil_empresa_tecnologica.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_empresa_tecnologica(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/empresa_tecnologica3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

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
    #Prueba tabla diseno_industrial
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002191'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000005833'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000000694'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_diseno_industrial(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/diseno_industrial1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_diseno_industrial = Extractor.perfil_diseno_industrial.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_diseno_industrial(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/diseno_industrial2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_diseno_industrial = Extractor.perfil_diseno_industrial.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_diseno_industrial(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/diseno_industrial3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: diseno_industrial')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla curso_maestria
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000018223'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000012288'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000003792'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_curso_maestria(lxml_url1,url1).sort_values('curso',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/curso_maestria1.csv', dtype='object', keep_default_na=False).sort_values('curso',ignore_index=True)
    Extractor.perfil_curso_maestria = Extractor.perfil_curso_maestria.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_curso_maestria(lxml_url2,url2).sort_values('curso',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/curso_maestria2.csv', dtype='object', keep_default_na=False).sort_values('curso',ignore_index=True)
    Extractor.perfil_curso_maestria = Extractor.perfil_curso_maestria.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_curso_maestria(lxml_url3,url3).sort_values('curso',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/curso_maestria3.csv', dtype='object', keep_default_na=False).sort_values('curso',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: curso_maestria')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla curso_doctorado
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000000592'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000012079'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002175'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_curso_doctorado(lxml_url1,url1).sort_values('curso',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/curso_doctorado1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_curso_doctorado = Extractor.perfil_curso_doctorado.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_curso_doctorado(lxml_url2,url2).sort_values('curso',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/curso_doctorado2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_curso_doctorado = Extractor.perfil_curso_doctorado.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_curso_doctorado(lxml_url3,url3).sort_values('curso',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/curso_doctorado3.csv', dtype='object', keep_default_na=False)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: curso_doctorado')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    ##########################
    #Prueba tabla caplibros
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000006693'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000005833'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002127'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_caplibros(lxml_url1,url1).sort_values('capitulo',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/caplibros1.csv', dtype='object', keep_default_na=False).sort_values('capitulo',ignore_index=True)
    Extractor.perfil_caplibros = Extractor.perfil_caplibros.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_caplibros(lxml_url2,url2).sort_values('capitulo',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/caplibros2.csv', dtype='object', keep_default_na=False).sort_values('capitulo',ignore_index=True)
    Extractor.perfil_caplibros = Extractor.perfil_caplibros.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_caplibros(lxml_url3,url3).sort_values('capitulo',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/caplibros3.csv', dtype='object', keep_default_na=False).sort_values('capitulo',ignore_index=True)

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
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002126'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000001155'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000000316'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_basico(lxml_url1,url1).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/basico1.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_basico = Extractor.perfil_basico.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_basico(lxml_url2,url2).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/basico2.csv', dtype='object', keep_default_na=False)
    Extractor.perfil_basico = Extractor.perfil_basico.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_basico(lxml_url3,url3).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/basico3.csv', dtype='object', keep_default_na=False)

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
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000015254'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000005361'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002156'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_articulos(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/articulos1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_articulos = Extractor.perfil_articulos.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_articulos(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/articulos2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_articulos = Extractor.perfil_articulos.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_articulos(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/articulos3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

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
    #Prueba tabla libros
    ##########################
    url1='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000001995'
    url2='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008372'
    url3='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002141'

    lxml_url1 = get_lxml(url1)
    df_auto1=Extractor.get_perfil_libros(lxml_url1,url1).sort_values('nombre',ignore_index=True).astype(str)
    df_manu1=pd.read_csv('cvlac/testing/testing_gruplac/libros1.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_libros = Extractor.perfil_libros.iloc[0:0]

    lxml_url2 = get_lxml(url2)
    df_auto2=Extractor.get_perfil_libros(lxml_url2,url2).sort_values('nombre',ignore_index=True).astype(str)
    df_manu2=pd.read_csv('cvlac/testing/testing_gruplac/libros2.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)
    Extractor.perfil_libros = Extractor.perfil_libros.iloc[0:0]

    lxml_url3 = get_lxml(url3)
    df_auto3=Extractor.get_perfil_libros(lxml_url3,url3).sort_values('nombre',ignore_index=True).astype(str)
    df_manu3=pd.read_csv('cvlac/testing/testing_gruplac/libros3.csv', dtype='object', keep_default_na=False).sort_values('nombre',ignore_index=True)

    try:
        print('******************************************')
        print('Pruebas unitarias para tabla: libros')
        print('Prueba 1:',test.test_dfs(df_auto1,df_manu1))
        print('Prueba 2:',test.test_dfs(df_auto2,df_manu2))
        print('Prueba 3:',test.test_dfs(df_auto3,df_manu3))
    except Exception as e:
        print('Reporte: ')
        print(e)
    
    