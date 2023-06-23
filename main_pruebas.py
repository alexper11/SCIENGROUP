from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.ExtractorGruplac import ExtractorGruplac
from cvlac.util import get_lxml
from scopus.ExtractorScopus import ExtractorScopus
from scopus.Scientopy import Scientopy
from scopus.readKey import read_key

import pandas as pd
import sys

from cvlac.cvlac_models.DBmodel import create_cvlac_db
from cvlac.cvlac_controllers.ActuacionController import ActuacionController
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
from cvlac.cvlac_controllers.EmpresaTecnologicaController import EmpresaTecnologicaController
from cvlac.cvlac_controllers.InnovacionEmpresarialController import InnovacionEmpresarialController
from cvlac.cvlac_controllers.CaplibrosController import CaplibrosController
from cvlac.cvlac_controllers.PrototipoController import PrototipoController
from cvlac.cvlac_controllers.SoftwareController import SoftwareController
from cvlac.cvlac_controllers.TecnologicosController import TecnologicosController
from cvlac.cvlac_controllers.MetaCvlacDBController import MetaCvlacDBController


from cvlac.gruplac_models.DBmodel import create_gruplac_db
from cvlac.gruplac_controllers.ArticulosGController import ArticulosGController
from cvlac.gruplac_controllers.BasicoGController import BasicoGController
from cvlac.gruplac_controllers.CaplibrosGController import CaplibrosGController
from cvlac.gruplac_controllers.CursoDoctoradoController import CursoDoctoradoController
from cvlac.gruplac_controllers.CursoMaestriaController import CursoMaestriaController
from cvlac.gruplac_controllers.DisenoIndustrialGController import DisenoIndustrialGController
from cvlac.gruplac_controllers.EmpresaTecnologicaGController import EmpresaTecnologicaGController
from cvlac.gruplac_controllers.InnovacionEmpresarialGController import InnovacionEmpresarialGController
from cvlac.gruplac_controllers.InstitucionesController import InstitucionesController
from cvlac.gruplac_controllers.IntegrantesController import IntegrantesController
from cvlac.gruplac_controllers.LibrosGController import LibrosGController
from cvlac.gruplac_controllers.LineasGController import LineasGController
from cvlac.gruplac_controllers.OtroProgramaController import OtroProgramaController
from cvlac.gruplac_controllers.OtrosArticulosController import OtrosArticulosController
from cvlac.gruplac_controllers.OtrosLibrosController import OtrosLibrosController
from cvlac.gruplac_controllers.OtrosTecnologicosController import OtrosTecnologicosController
from cvlac.gruplac_controllers.PlantaPilotoGController import PlantaPilotoGController
from cvlac.gruplac_controllers.ProgramaDoctoradoController import ProgramaDoctoradoController
from cvlac.gruplac_controllers.ProgramaMaestriaController import ProgramaMaestriaController
from cvlac.gruplac_controllers.PrototiposGController import PrototiposGController
from cvlac.gruplac_controllers.SoftwareGController import SoftwareGController
from cvlac.gruplac_controllers.MetaGruplacDBController import MetaGruplacDBController

from scopus.models.DBmodel import create_scopus_db
from scopus.controllers.AutoresController import AutoresController
from scopus.controllers.ProductosController import ProductosController  
from scopus.controllers.MetaDBScoController import MetaDBScoController                  


if __name__ == '__main__':
    
    ########################
    #MODULO CVLAC
    ########################
    """
    sys.path.append(".")
    #create_cvlac_db()
    create_gruplac_db()
    #create_scopus_db()
    print('Bases de datos creadas')
    
    Extractor=ExtractorGruplac()
    #para este caso el parametro de entrada es la url del buscador scienti para el departamento del Cauca
    lista_gruplac=Extractor.get_gruplac_list('https://scienti.minciencias.gov.co/ciencia-war/busquedaGrupoXDepartamentoGrupo.do?codInst=&sglPais=COL&sgDepartamento=CA&maxRows=15&grupos_tr_=true&grupos_p_=1&grupos_mr_=130')
    """
    ######################
    #Extraccion de tablas CVLAC
    ######################
    
    """print('setting grup attributes...')
    Extractor.set_grup_attrs(lista_gruplac)
    
    print('updating cvlacdb...')
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
    
    caplibros=CaplibrosController()
    caplibros.insert_df(Extractor.grup_caplibros.reset_index(drop=True))
    
    empresatec=EmpresaTecnologicaController()
    empresatec.insert_df(Extractor.grup_empresa_tecnologica.reset_index(drop=True))
    
    innovaempresa=InnovacionEmpresarialController()
    innovaempresa.insert_df(Extractor.grup_innovacion_empresarial.reset_index(drop=True))
    
    prototipo=PrototipoController()
    prototipo.insert_df(Extractor.grup_prototipo.reset_index(drop=True))
    
    software=SoftwareController()
    software.insert_df(Extractor.grup_software.reset_index(drop=True))
    
    tecnologicos=TecnologicosController()
    tecnologicos.insert_df(Extractor.grup_tecnologicos.reset_index(drop=True))
    """
    ######################
    #Extraccion de tablas GRUPLAC
    ######################
    
    """print('setting perfil attributes')
    Extractor.set_perfil_attrs(lista_gruplac)
    
    print('updating gruplacdb...')
    articulosg=ArticulosGController()
    articulosg.insert_df(Extractor.perfil_articulos)
    
    basicog=BasicoGController()
    basicog.insert_df(Extractor.perfil_basico)
    
    instituciones=InstitucionesController()
    instituciones.insert_df(Extractor.perfil_instituciones)
    
    lineasg=LineasGController()
    lineasg.insert_df(Extractor.perfil_lineas)
    
    integrantes=IntegrantesController()
    integrantes.insert_df(Extractor.perfil_integrantes)
    
    pdoctorado=ProgramaDoctoradoController()
    pdoctorado.insert_df(Extractor.perfil_programa_doctorado)
    
    pmaestria=ProgramaMaestriaController()
    pmaestria.insert_df(Extractor.perfil_programa_maestria)
    
    oprograma=OtroProgramaController()
    oprograma.insert_df(Extractor.perfil_otro_programa)
    
    cdoctorado=CursoDoctoradoController()
    cdoctorado.insert_df(Extractor.perfil_curso_doctorado)
    
    cmaestria=CursoMaestriaController()
    cmaestria.insert_df(Extractor.perfil_curso_maestria)
    
    librosg=LibrosGController()
    librosg.insert_df(Extractor.perfil_libros)
    
    caplibrosg=CaplibrosGController()
    caplibrosg.insert_df(Extractor.perfil_caplibros)
    
    oarticulos=OtrosArticulosController()
    oarticulos.insert_df(Extractor.perfil_otros_articulos)
    
    olibros=OtrosLibrosController()
    olibros.insert_df(Extractor.perfil_otros_libros)
    
    disenoind=DisenoIndustrialGController()
    disenoind.insert_df(Extractor.perfil_diseno_industrial)
    
    otecnologicos=OtrosTecnologicosController()
    otecnologicos.insert_df(Extractor.perfil_otros_tecnologicos)
    
    prototiposg=PrototiposGController()
    prototiposg.insert_df(Extractor.perfil_prototipos)
    
    softwareg=SoftwareGController()
    softwareg.insert_df(Extractor.perfil_software)
    
    empresatecg=EmpresaTecnologicaGController()
    empresatecg.insert_df(Extractor.perfil_empresa_tecnologica)
    
    innovaempresag=InnovacionEmpresarialGController()
    innovaempresag.insert_df(Extractor.perfil_innovacion_empresarial)
    
    plantapilotog=PlantaPilotoGController()
    plantapilotog.insert_df(Extractor.perfil_planta_piloto)
    
    del Extractor"""
    
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
    
    #metadb= MetaCvlacDBController()
    #metadb.insert_datetime()
    
    #metadb1= MetaGruplacDBController()
    #metadb1.insert_datetime()
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


 
    ##Pruebas para tablas individuales

    #prueba a tablas individuales.. dentro del main
    Extractor=ExtractorGruplac()
    
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000626252'
    #perfil de cristian figueroa:
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001239368'
    #perfil de gustavo ramirtez:
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000523496'
    #perfil gruplac telematica:
    #url='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160'
    #url='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002153'

    #empresa abse tec:
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000373770'
    #innovacion empresarial:
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000523496'
    #prototipo
    #url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000373770'
    #urls cvlac:
    list_url=['https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000013021',
    'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001427333',
    'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001239368',
    'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000013056',
    'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000012963',
    'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000004900']
    #urls gruplac:
    
    list_url=['https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160',
    'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000015570']
    
    list_url=['https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000004672',
    'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002153',
    'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000001014',
    'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000002726',
    'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000001162',
    'https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000008160']
    list_url=['https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001239368']
    list_url=['https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000013021']
    for url in list_url:
        dom=get_lxml(url)
        df_prueba=Extractor.get_caplibro(dom,url)  
    
    df_prueba.to_csv('prueba.csv',index=False)

   








    ##############
    #DEMOS PARA PRUEBAS
    ##############
    """
    from cvlac.cvlac_models.DBmodel import create_db
    from cvlac.cvlac_controllers.ArticulosController import ArticulosController
    ############################
    #DEMO CVLAC
    ############################
    print('Ejecutando Demo cvlac...')
    Extractor=ExtractorGruplac()
    url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000013056'
    dom=get_lxml(url)
    df=Extractor.get_articulo(dom,url)
    print("Extracción supo")
    ######################
    sys.path.append(".")
    #######################  
    create_db()
    print("Creacion db supo")
    articulos=ArticulosController()
    articulos.insert_df(df)
    print("Inserción supo")
    
    #articulos.delete_idcvlac('0000013056')
    #print('borrado supo')
    
    del Extractor
    
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
    """