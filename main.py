from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.ExtractorGruplac import ExtractorGruplac
from scopus.ExtractorScopus import ExtractorScopus

import pandas as pd
import sys
from scopus.readKey import read_key

from cvlac.models.DBmodel import create_db
from cvlac.controllers.ActuacionController import ActuacionController
from cvlac.controllers.ArticulosController import ArticulosController
from cvlac.controllers.BasicoController import BasicoController
from cvlac.controllers.EvaluadorController import EvaluadorController
from cvlac.controllers.IdentificadoresController import IdentificadoresController
from cvlac.controllers.IdiomaController import IdiomaController
from cvlac.controllers.InvestigacionController import InvestigacionController
from cvlac.controllers.JuradosController import JuradosController
from cvlac.controllers.LibrosController import LibrosController
from cvlac.controllers.ReconocimientoController import ReconocimientoController
from cvlac.controllers.RedesController import RedesController
from cvlac.controllers.EstanciasController import EstanciasController
from cvlac.controllers.AcademicaController import AcademicaController
from cvlac.controllers.ComplementariaController import ComplementariaController

from scopus.models.DBmodel import create_scopus_db
from scopus.controllers.AutoresController import AutoresController
from scopus.controllers.ArticulosScoController import ArticulosScoController                       


if __name__ == '__main__':
    
    #######################
    sys.path.append(".")
    #######################
    
    #create_db()
    #create_scopus_db()
    
    ########################
    #CVLAC
    ########################
    
    '''
    Extractor=ExtractorGruplac()
    dfs=Extractor.get_cvs('https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160')
    
    articulos=ArticulosController()
    articulos.insert_df(dfs['articulos'])
    
    actuacion = ActuacionController(dfs['actuacion'])
    actuacion.insert_df()
    
    basico=BasicoController()
    basico.insert_df(dfs['basico'])
    
    evaluador=EvaluadorController()
    evaluador.insert_df(dfs['evaluador'])
    
    identificadores=IdentificadoresController()
    identificadores.insert_df(dfs['identificadores'])
    
    idioma=IdiomaController()
    idioma.insert_df(dfs['idioma'])
    
    investigacion=InvestigacionController()
    investigacion.insert_df(dfs['investigacion'])
    
    jurados=JuradosController()
    jurados.insert_df(dfs['jurado'])
    
    libros=LibrosController()
    libros.insert_df(dfs['libros'])
    
    reconocimiento=ReconocimientoController()
    reconocimiento.insert_df(dfs['reconocimiento'])
    
    redes=RedesController()
    redes.insert_df(dfs['redes'])
    
    estancias=EstanciasController()
    estancias.insert_df(dfs['estancias'])
    
    academica=AcademicaController()
    academica.insert_df(dfs['academica'])
    
    complementaria=ComplementariaController()
    complementaria.insert_df(dfs['complementaria'])
    '''
    
    ########################
    #SCOPUS
    ########################
    API_KEY=""
    INST_TOKEN=""
    API_KEY, INST_TOKEN = read_key()
    
    #Obtener lista de auid Unicauca
    #Obtener tabla de autores Unicauca
    ExtractorS = ExtractorScopus(API_KEY,INST_TOKEN)
    df_autores=ExtractorS.get_authors_df(ExtractorS.get_auid_list(60051434)) 

    #df_articulos=ExtractorS.get_articles_df(ExtractorS.get_auid_list(60051434))
    
    autores = AutoresController()
    autores.insert_df(df_autores)
    
    articulosSco = ArticulosScoController()
    #articulosSco.insert_df(df_articulos)
    
    
    