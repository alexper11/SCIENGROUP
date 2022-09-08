from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.ExtractorGruplac import ExtractorGruplac
from cvlac.util import get_gruplacList, get_lxml
from scopus.ExtractorScopus import ExtractorScopus
from scopus.Scientopy import Scientopy

import pandas as pd
import sys
from scopus.readKey import read_key
'''
from cvlac.cvlac_models.DBmodel import create_db
from cvlac.controllers.ActuacionController import ActuacionController
from cvlac.cvlac_controllers.ArticulosController import ArticulosController
from cvlac.cvlac_controllers.BasicoController import BasicoController
from cvlac.cvlac_controllers.EvaluadorController import EvaluadorController
from cvlac.cvlac_controllers.IdentificadoresController import IdentificadoresController
from cvlac.cvlac_controllers.IdiomaController import IdiomaController
from cvlac.cvlac_controllers.InvestigacionController import InvestigacionController
from cvlac.cvlac_controllers.JuradosController import JuradosController
from cvlac.cvlac_controllers.LibrosController import LibrosController
from cvlac.cvlac_controllers.ReconocimientoController import ReconocimientoController
from cvlac.cvlac_controllers.RedesController import RedesController
from cvlac.cvlac_controllers.EstanciasController import EstanciasController
from cvlac.cvlac_controllers.AcademicaController import AcademicaController
from cvlac.cvlac_controllers.ComplementariaController import ComplementariaController
from cvlac.cvlac_controllers.MetaDBController import MetaDBController


from scopus.models.DBmodel import create_scopus_db
from scopus.controllers.AutoresController import AutoresController
from scopus.controllers.ProductosController import ProductosController  
from scopus.controllers.MetaDBScoController import MetaDBScoController                     


if __name__ == '__main__':
    
    #######################
    sys.path.append(".")
    #######################
    
    #create_db()
    #create_scopus_db()
    
    ########################
    #CVLAC
    ########################
    """
    Extractor=ExtractorGruplac()
    Extractor.set_gruplac_attrs(get_gruplacList('UNIVERSIDAD DEL CAUCA'))
    print('supo')
    
    articulos=ArticulosController()
    articulos.insert_df(Extractor.grup_articulos.reset_index(drop=True))
    
    actuacion = ActuacionController()
    actuacion.insert_df(Extractor.grup_actuacion.reset_index(drop=True))
    
    basico=BasicoController()
    basico.insert_df(Extractor.grup_basico.reset_index(drop=True))
    
    evaluador=EvaluadorController()
    evaluador.insert_df(Extractor.grup_evaluador.reset_index(drop=True))
    
    identificadores=IdentificadoresController()
    identificadores.insert_df(Extractor.grup_identificadores.reset_index(drop=True))
    
    idioma=IdiomaController()
    idioma.insert_df(Extractor.grup_idioma.reset_index(drop=True))
    
    investigacion=InvestigacionController()
    investigacion.insert_df(Extractor.grup_investiga.reset_index(drop=True))
    
    jurados=JuradosController()
    jurados.insert_df(Extractor.grup_jurado.reset_index(drop=True))
    
    libros=LibrosController()
    libros.insert_df(Extractor.grup_libros.reset_index(drop=True))
    
    reconocimiento=ReconocimientoController()
    reconocimiento.insert_df(Extractor.grup_reconocimiento.reset_index(drop=True))
    
    redes=RedesController()
    redes.insert_df(Extractor.grup_redes.reset_index(drop=True))
    
    estancias=EstanciasController()
    estancias.insert_df(Extractor.grup_estancias.reset_index(drop=True))
    
    academica=AcademicaController()
    academica.insert_df(Extractor.grup_academica.reset_index(drop=True))
    
    complementaria=ComplementariaController()
    complementaria.insert_df(Extractor.grup_complementaria.reset_index(drop=True))
    
    del Extractor
   
   """
    ########################
    #SCOPUS
    ########################
    """
    
    API_KEY=""
    INST_TOKEN=""
    API_KEY, INST_TOKEN = read_key()
    
    #Obtener lista de auid Unicauca
    #Obtener autores Unicauca
    
    ExtractorS = ExtractorScopus(API_KEY,INST_TOKEN)
    authors_list=ExtractorS.get_auid_list(60051434)
    
    df_autores=ExtractorS.get_authors_df(authors_list) 
    
    autores = AutoresController()
    autores.insert_df(df_autores)
    
    df_productos=ExtractorS.get_articles_full(authors_list)
    #df_productos=pd.read_csv ('df_productos.csv')
    
    productos = ProductosController()
    try:
        productos.insert_df(df_productos)
    except:
        df_productos.to_csv('df_productos.csv',index=False)
        raise
    del ExtractorS
    
    """
    
    #########################################
    #Insertar fecha de extracción de los datos en ambos modulos
    #########################################
    
    #metadb= MetaDBController()
    #metadb.insert_datetime()
    
    #metadbsco=MetaDBScoController()
    #metadbsco.insert_datetime()

    ###############################
    #SCIENTOPY
    #################################
    """
    API_KEY=""
    INST_TOKEN=""
    API_KEY, INST_TOKEN = read_key()
    scientopy = Scientopy(API_KEY,INST_TOKEN)
    input_df = scientopy.scopus_preprocessed_df('"linked open data"')
    input_df.to_csv('papersPreprocessed.csv',index=False)
    """
    
'''   

##Pruebas para tablas individuales
if __name__ == '__main__':

    #prueba a tablas individuales.. dentro del main
    Extractor=ExtractorGruplac()
    
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000626252'
    #perfil de cristian figueroa:
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001239368'
    #perfil de gustavo ramirtez:
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000523496'
    #perfil gruplac telematica:
    url='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160'
    #url="https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160"

    #empresa abse tec:
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000373770'
    #innovacion empresarial:
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000523496'
    #prototipo
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000373770'
  
    dom=get_lxml(url)    
    df_prueba=Extractor.get_perfil_articulos(dom,url)
   
    df_prueba.to_csv('prueba.csv',index=False)

'''

if __name__ == '__main__':
    from IPython.display import display
    ############################
    #DEMO CVLAC
    ############################
    print('Ejecutando Demo cvlac...')
    Extractor=ExtractorGruplac()
    url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000013056'
    dom=get_lxml(url)
    df=Extractor.get_articulo(dom,url)
    display(df['nombre'].head(10).to_string())

    ###########################
    #DEMO SCOPUS
    ###########################
    
    API_KEY=""
    INST_TOKEN=""
    API_KEY, INST_TOKEN = read_key()
    print('Ejecutando Demo Scopus...')
    ExtractorS = ExtractorScopus(API_KEY,INST_TOKEN)
    df_productos=ExtractorS.get_articles_full([7004506288])
    display(df_productos['titulo'].to_string())
'''