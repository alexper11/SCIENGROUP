
from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.util import get_lxml
import pandas as pd
import unittest
import numpy as np
    
class prueba_unitaria(unittest.TestCase):
    def test_dfs(self, df_auto, df_manu):
        pd.testing.assert_frame_equal(df_auto,df_manu, check_column_type=False, check_dtype=False)

Extractor=ExtractorCvlac()
##########################
#Prueba tabla tecnologicos
##########################
#las url de testing son tomadas de manera aleatoria con SQL desde la base de datos generada
url1='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000331589'
url2='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001380950'
url3='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000881040'

lxml_url1 = get_lxml(url1)
df_auto1=Extractor.get_tecnologicos(lxml_url1,url1).astype(str)
df_manu1=pd.read_csv('tecnologicos1.csv', dtype='object', keep_default_na=False)
Extractor.tecnologicos = Extractor.tecnologicos.iloc[0:0]

lxml_url2 = get_lxml(url2)
df_auto2=Extractor.get_tecnologicos(lxml_url2,url2).astype(str)
df_manu2=pd.read_csv('tecnologicos2.csv', dtype='object', keep_default_na=False)
Extractor.tecnologicos = Extractor.tecnologicos.iloc[0:0]

lxml_url3 = get_lxml(url3)
df_auto3=Extractor.get_tecnologicos(lxml_url3,url3).astype(str)
df_manu3=pd.read_csv('tecnologicos3.csv', dtype='object', keep_default_na=False)

