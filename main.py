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
    create_scopus_db()
    
    ########################
    #CVLAC
    ########################
    
    
    Extractor=ExtractorGruplac()
    tablas=Extractor.get_cvs('https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160')
    
    articulos=ArticulosController()
    articulos.insert_df(tablas[1])
    
    actuacion = ActuacionController()
    actuacion.insert_df(tablas[2])
    
    basico=BasicoController()
    basico.insert_df(tablas[0])
    
    evaluador=EvaluadorController()
    evaluador.insert_df(tablas[6])
    
    identificadores=IdentificadoresController()
    identificadores.insert_df(tablas[8])
    
    idioma=IdiomaController()
    idioma.insert_df(tablas[3])
    
    investigacion=InvestigacionController()
    investigacion.insert_df(tablas[4])
    
    jurados=JuradosController()
    jurados.insert_df(tablas[10])
    
    libros=LibrosController()
    libros.insert_df(tablas[9])
    
    reconocimiento=ReconocimientoController()
    reconocimiento.insert_df(tablas[5])
    
    redes=RedesController()
    redes.insert_df(tablas[7])
    
    estancias=EstanciasController()
    estancias.insert_df(tablas[12])
    
    academica=AcademicaController()
    academica.insert_df(tablas[13])
    
    complementaria=ComplementariaController()
    complementaria.insert_df(tablas[11])
    
    
    ########################
    #SCOPUS
    ########################
    API_KEY=""
    INST_TOKEN=""
    API_KEY, INST_TOKEN = read_key()
    
    #Obtener lista de auid Unicauca
    #Obtener tabla de autores Unicauca
    ExtractorS = ExtractorScopus(API_KEY,INST_TOKEN)
    #df_autores=ExtractorS.get_authors_df(ExtractorS.get_auid_list(60051434)) 
    list=[8568805300,
        15135119500,
        22941628100,
        6507572648,
        6701647223,
        57195195220,
        22333375600,
        36603157500,
        57101084800,
        57214098924]
    df_articulos=ExtractorS.get_articles_df(list)
    
    autores = AutoresController()
    #autores.insert_df(df_autores)
    
    articulosSco = ArticulosScoController()
    articulosSco.insert_df(df_articulos)