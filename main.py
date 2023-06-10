from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.ExtractorGruplac import ExtractorGruplac
from cvlac.util import get_lxml
from scopus.ExtractorScopus import ExtractorScopus
from scopus.Scientopy import Scientopy
from scopus.readKey import read_key
from scopus.integracion import integrar

import pandas as pd
import numpy as np
import os
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
    
    sys.path.append(".")
    create_cvlac_db()
    #create_gruplac_db()
    #create_scopus_db()
    print('Bases de datos creadas')
    
    ########################
    #MODULO CVLAC
    ########################
    
    Extractor=ExtractorGruplac()
    #para este caso el parametro de entrada es la url del buscador scienti para el departamento del Cauca
    lista_gruplac=Extractor.get_gruplac_list('https://scienti.minciencias.gov.co/ciencia-war/busquedaGrupoXDepartamentoGrupo.do?codInst=&sglPais=COL&sgDepartamento=CA&maxRows=15&grupos_tr_=true&grupos_p_=1&grupos_mr_=130')
    
    try:
        os.mkdir('extracted_data')
    except:
        pass
    
    ######################
    #Extraccion de tablas CVLAC
    ######################
    
    print('setting grup attributes...')
    Extractor.set_grup_attrs(lista_gruplac)
    
    print('updating cvlacdb...')
    
    basico=BasicoController()
    aux_basico=Extractor.grup_basico.drop_duplicates(ignore_index=True)
    aux_basico.to_csv('extracted_data/aux_basico.csv',index=False)
    basico.insert_df(aux_basico)
    del basico
    
    articulos=ArticulosController()
    aux_articulos=Extractor.grup_articulos.drop_duplicates(ignore_index=True)
    aux_articulos.to_csv('extracted_data/aux_articulos.csv',index=False)
    articulos.insert_df(aux_articulos)
    del articulos
    
    actuacion = ActuacionController()
    aux_actuacion=Extractor.grup_actuacion.drop_duplicates(ignore_index=True)
    aux_actuacion.to_csv('extracted_data/aux_actuacion.csv',index=False)
    actuacion.insert_df(aux_actuacion)
    del actuacion
    
    evaluador=EvaluadorController()
    evaluador.insert_df(Extractor.grup_evaluador.drop_duplicates(ignore_index=True))
    del evaluador
    
    identificadores=IdentificadoresController()
    aux_identificadores=Extractor.grup_identificadores.drop_duplicates(ignore_index=True)
    aux_identificadores.to_csv('extracted_data/aux_identificadores.csv',index=False)
    identificadores.insert_df(aux_identificadores)
    del identificadores
    
    idioma=IdiomaController()
    idioma.insert_df(Extractor.grup_idioma.drop_duplicates(ignore_index=True))
    del idioma
    
    investigacion=InvestigacionController()
    aux_investigacion=Extractor.grup_investiga.drop_duplicates(ignore_index=True)
    aux_investigacion.to_csv('extracted_data/aux_investigacion.csv',index=False)
    investigacion.insert_df(aux_investigacion)
    del investigacion
    
    jurados=JuradosController()
    jurados.insert_df(Extractor.grup_jurado.drop_duplicates(ignore_index=True))
    del jurados
    
    libros=LibrosController()
    aux_libros=Extractor.grup_libros.drop_duplicates(ignore_index=True)
    aux_libros.to_csv('extracted_data/aux_libros.csv',index=False)
    libros.insert_df(aux_libros)
    del libros
    
    reconocimiento=ReconocimientoController()
    aux_reconocimiento=Extractor.grup_reconocimiento.drop_duplicates(ignore_index=True)
    aux_reconocimiento.to_csv('extracted_data/aux_reconocimiento.csv',index=False)
    reconocimiento.insert_df(aux_reconocimiento)
    del reconocimiento
    
    redes=RedesController()
    aux_redes=Extractor.grup_redes.drop_duplicates(ignore_index=True)
    aux_redes.to_csv('extracted_data/aux_redes.csv',index=False)
    redes.insert_df(aux_redes)
    del redes
    
    estancias=EstanciasController()
    estancias.insert_df(Extractor.grup_estancias.drop_duplicates(ignore_index=True))
    del estancias
    
    academica=AcademicaController()
    academica.insert_df(Extractor.grup_academica.drop_duplicates(ignore_index=True))
    del academica
    
    complementaria=ComplementariaController()
    complementaria.insert_df(Extractor.grup_complementaria.drop_duplicates(ignore_index=True))
    del complementaria
    
    caplibros=CaplibrosController()
    aux_caplibros=Extractor.grup_caplibros.drop_duplicates(ignore_index=True)
    aux_caplibros.to_csv('extracted_data/aux_caplibros.csv',index=False)
    caplibros.insert_df(aux_caplibros)
    del caplibros
    
    empresatec=EmpresaTecnologicaController()
    aux_empresatec=Extractor.grup_empresa_tecnologica.drop_duplicates(ignore_index=True)
    aux_empresatec.to_csv('extracted_data/aux_empresatec.csv',index=False)
    empresatec.insert_df(aux_empresatec)
    del empresatec
    
    innovaempresa=InnovacionEmpresarialController()
    aux_innovaempresa=Extractor.grup_innovacion_empresarial.drop_duplicates(ignore_index=True)
    aux_innovaempresa.to_csv('extracted_data/aux_innovaempresa.csv',index=False)
    innovaempresa.insert_df(aux_innovaempresa)
    del innovaempresa
    
    prototipo=PrototipoController()
    aux_prototipo=Extractor.grup_prototipo.drop_duplicates(ignore_index=True)
    aux_prototipo.to_csv('extracted_data/aux_prototipo.csv',index=False)
    prototipo.insert_df(aux_prototipo)
    del prototipo
    
    software=SoftwareController()
    aux_software=Extractor.grup_software.drop_duplicates(ignore_index=True)
    aux_software.to_csv('extracted_data/aux_software.csv',index=False)
    software.insert_df(aux_software)
    del software
    
    tecnologicos=TecnologicosController()
    aux_tecnologicos=Extractor.grup_tecnologicos.drop_duplicates(ignore_index=True)
    aux_tecnologicos.to_csv('extracted_data/aux_tecnologicos.csv',index=False)
    tecnologicos.insert_df(aux_tecnologicos)
    del tecnologicos
    
    print('Extracción Cvlac Finalizada')
    
    ######################
    #Extraccion de tablas GRUPLAC
    ######################
    
    print('setting perfil attributes')
    Extractor.set_perfil_attrs(lista_gruplac)
    
    print('updating gruplacdb...')
    
    basicog=BasicoGController()
    aux_basicog=Extractor.perfil_basico
    aux_basicog.to_csv('extracted_data/aux_basicog.csv',index=False)
    basicog.insert_df(aux_basicog)
    del basicog
    
    articulosg=ArticulosGController()
    aux_articulosg=Extractor.perfil_articulos
    aux_articulosg.to_csv('extracted_data/aux_articulosg.csv',index=False)
    articulosg.insert_df(aux_articulosg)
    del articulosg
    
    instituciones=InstitucionesController()
    aux_instituciones=Extractor.perfil_instituciones
    aux_instituciones.to_csv('extracted_data/aux_instituciones.csv',index=False)
    instituciones.insert_df(aux_instituciones)
    del instituciones
    
    lineasg=LineasGController()
    aux_lineas=Extractor.perfil_lineas
    aux_lineas.to_csv('extracted_data/aux_lineas.csv',index=False)
    lineasg.insert_df(Extractor.perfil_lineas)
    del lineasg
    
    integrantes=IntegrantesController()
    aux_integrantes=Extractor.perfil_integrantes
    aux_integrantes.to_csv('extracted_data/aux_integrantes.csv',index=False)
    integrantes.insert_df(aux_integrantes)
    del integrantes
    
    pdoctorado=ProgramaDoctoradoController()
    aux_pdoctorado=Extractor.perfil_programa_doctorado
    aux_pdoctorado.to_csv('extracted_data/aux_pdoctorado.csv',index=False)
    pdoctorado.insert_df(aux_pdoctorado)
    del pdoctorado
    
    pmaestria=ProgramaMaestriaController()
    aux_pmaestria=Extractor.perfil_programa_maestria
    aux_pmaestria.to_csv('extracted_data/aux_pmaestria.csv',index=False)
    pmaestria.insert_df(aux_pmaestria)
    del pmaestria
    
    oprograma=OtroProgramaController()
    oprograma.insert_df(Extractor.perfil_otro_programa)
    del oprograma
    
    cdoctorado=CursoDoctoradoController()
    aux_cdoctorado=Extractor.perfil_curso_doctorado
    aux_cdoctorado.to_csv('extracted_data/aux_cdoctorado.csv',index=False)
    cdoctorado.insert_df(aux_cdoctorado)
    del cdoctorado
    
    cmaestria=CursoMaestriaController()
    aux_cmaestria=Extractor.perfil_curso_maestria
    aux_cmaestria.to_csv('extracted_data/aux_cmaestria.csv',index=False)
    cmaestria.insert_df(aux_cmaestria)
    del cmaestria
    
    librosg=LibrosGController()
    aux_librosg=Extractor.perfil_libros
    aux_librosg.to_csv('extracted_data/aux_librosg.csv',index=False)
    librosg.insert_df(aux_librosg)
    del librosg
    
    caplibrosg=CaplibrosGController()
    aux_caplibrosg=Extractor.perfil_caplibros
    aux_caplibrosg.to_csv('extracted_data/aux_caplibrosg.csv',index=False)
    caplibrosg.insert_df(aux_caplibrosg)
    del caplibrosg
    
    oarticulos=OtrosArticulosController()
    aux_oarticulos=Extractor.perfil_otros_articulos
    aux_oarticulos.to_csv('extracted_data/aux_oarticulos.csv',index=False)
    oarticulos.insert_df(aux_oarticulos)
    del oarticulos
    
    olibros=OtrosLibrosController()
    aux_olibros=Extractor.perfil_otros_libros
    aux_olibros.to_csv('extracted_data/aux_olibros.csv',index=False)
    olibros.insert_df(aux_olibros)
    del olibros
    
    disenoind=DisenoIndustrialGController()
    aux_disenoind=Extractor.perfil_diseno_industrial
    aux_disenoind.to_csv('extracted_data/aux_disenoind.csv',index=False)
    disenoind.insert_df(aux_disenoind)
    del disenoind
    
    otecnologicos=OtrosTecnologicosController()
    aux_otecnologicos=Extractor.perfil_otros_tecnologicos
    aux_otecnologicos.to_csv('extracted_data/aux_otecnologicos.csv',index=False)
    otecnologicos.insert_df(aux_otecnologicos)
    del otecnologicos
    
    prototiposg=PrototiposGController()
    aux_prototiposg=Extractor.perfil_prototipos
    aux_prototiposg.to_csv('extracted_data/aux_prototiposg.csv',index=False)
    prototiposg.insert_df(aux_prototiposg)
    del prototiposg
    
    softwareg=SoftwareGController()
    aux_softwareg=Extractor.perfil_software
    aux_softwareg.to_csv('extracted_data/aux_softwareg.csv',index=False)
    softwareg.insert_df(aux_softwareg)
    del softwareg
    
    empresatecg=EmpresaTecnologicaGController()
    aux_empresatecg=Extractor.perfil_empresa_tecnologica
    aux_empresatecg.to_csv('extracted_data/aux_empresatecg.csv',index=False)
    empresatecg.insert_df(aux_empresatecg)
    del empresatecg
    
    innovaempresag=InnovacionEmpresarialGController()
    aux_innovaempresag=Extractor.perfil_innovacion_empresarial
    aux_innovaempresag.to_csv('extracted_data/aux_innovaempresag.csv',index=False)
    innovaempresag.insert_df(aux_innovaempresag)
    del innovaempresag
    
    plantapilotog=PlantaPilotoGController()
    aux_plantapilotog=Extractor.perfil_planta_piloto
    aux_plantapilotog.to_csv('extracted_data/aux_plantapilotog.csv',index=False)
    plantapilotog.insert_df(aux_plantapilotog)
    del plantapilotog
    
    print('Extracción Gruplac Finalizada')
    
    del Extractor
    
    ########################
    #SCOPUS
    ########################
    API_KEY=""
    INST_TOKEN=""
    API_KEY, INST_TOKEN = read_key()
    
    #Obtener lista de auid Unicauca
    #Obtener autores Unicauca
    
    ExtractorS = ExtractorScopus(API_KEY,INST_TOKEN)
    authors_set=set()
    
    #La siguiente lista de id de afiliciones se obtuvo tras un proceso de selección y filtrado de datos desde la
    #base de datos de scopus para recopilar las afiliciones de los municipios y la capital del Cauca.
    """
    cauca_affiliations=['60051434','113372863','117688708','117795037','126338541','128447346','128268840',
                  '127081273','126489416','128778365','128309743','128482659','117008946','126682182',
                  '128105349','126290034','126174357','112818394','125811395',
                  '127752672','127622090','127564855','127405489','127405461','127381524','115900332',
                  '126777846','126186631','126173286','60108709','101775869','119181814','128840430',
                  '114698614','116513678','117723547','117305237','113883714','114526629','114791601',
                  '123885595','122628633','119043818','115563645','101726347','125032749','121970185',
                  '116735865','101514240','125785463','125750906','124804790','116456976','127190801',
                  '113900343','112191830','60077382','128549532','128171945','128105012','128814956',
                  '128024009','126051165','125818633','125750802','125632933','127586953','126802821',
                  '125632538','125632187','125252062','125251921','124411847','124133827','128828376',
                  '123994672','123836332','122819512','126682198','127781039','123689024','128812265',
                  '122309488','121977650','121967890','121824461','121318460','127656911','128778956',
                  '120708272','120314658','119159252','118786435','118690331','127128201','128620548',
                  '116086835','115060744','114832182','114293784','113845992','126803577','128573517',
                  '109407507','101852916','101836579','101193438','100890026','123046459','128401012',
                  '127577880','125880059','127342961','126722732','117676389','122213398','128178397',
                  '128132135','127180877','127175281','126426661','126369148','126220579','126220389',
                  '116477105','112246667','109475450'] 
    """
    cauca_affiliations=['60051434','113372863','117795037','128447346','128268840','60276620','129051230',
                  '127081273','126489416','128778365','128309743','128482659','117008946','126682182',
                  '128105349','126290034','126174357','125811395','114526610','129393749','129252659',
                  '127752672','127622090','127564855','127405489','127405461','127381524','115900332',
                  '126777846','126186631','126173286','60108709','101775869','119181814','129182092',
                  '114698614','116513678','117723547','117305237','113883714','114526629','129138504',
                  '123885595','122628633','119043818','115563645','101726347','125032749','121970185',
                  '116735865','101514240','125785463','125750906','124804790','116456976','127190801',
                  '113900343','60077382','128549532','128171945','128105012','128814956','128957167',
                  '128024009','126051165','125750802','125632933','127586953','126802821','128956909',
                  '125632538','125632187','125252062','125251921','124411847','124133827','128828376',
                  '123994672','123836332','122819512','126682198','127781039','123689024','128812265',
                  '122309488','121977650','121967890','121824461','121318460','127656911','128778956',
                  '120708272','120314658','119159252','118786435','118690331','127128201','128620548',
                  '116086835','115060744','114832182','114293784','113845992','126803577','128573517',
                  '109407507','101852916','101836579','101193438','100890026','123046459','128401012',
                  '127577880','125880059','127342961','126722732','117676389','122213398','128178397',
                  '128132135','127180877','127175281','126426661','126369148','126220579','126220389',
                  '116477105','112246667','109475450','122755339','128956705']
        
    for affiliation in cauca_affiliations:
        authors_set.update(ExtractorS.get_auid_list(affiliation))

    df_autores=ExtractorS.get_authors_df(authors_set)
    
    try:
        df_autores.to_csv('extracted_data/aux_autores.csv',index=False)
    except:
        print(df_autores)
    
    df_productos=ExtractorS.get_articles_full(cauca_affiliations)
    df_productos = df_productos.astype(str)
    df_productos.to_csv('extracted_data/aux_productos.csv',index=False)
    
    print('Extracción Scopus finalizada')
    
    del ExtractorS

    #########################################
    #Insertar fecha de extracción de los datos en ambos modulos
    #########################################
    
    metadb= MetaCvlacDBController()
    metadb.insert_datetime()
    
    metadb1= MetaGruplacDBController()
    metadb1.insert_datetime()
    
    metadbsco=MetaDBScoController()
    metadbsco.insert_datetime()

    ###############################
    #INTEGRACIÓN DE MODULOS PARA DATOS DE GRUPOS DE INVESTIGACIÓN
    #################################
    
    aux_articulosg = pd.read_csv('extracted_data/aux_articulosg.csv', dtype = str)
    aux_basicog = pd.read_csv('extracted_data/aux_basicog.csv', dtype = str)
    aux_caplibrosg = pd.read_csv('extracted_data/aux_caplibrosg.csv', dtype = str)
    aux_identificadores = pd.read_csv('extracted_data/aux_identificadores.csv', dtype = str)
    aux_integrantes = pd.read_csv('extracted_data/aux_integrantes.csv', dtype = str)
    aux_librosg = pd.read_csv('extracted_data/aux_librosg.csv', dtype = str) #pendiente de remplazo
    aux_oarticulos = pd.read_csv('extracted_data/aux_oarticulos.csv', dtype = str)
    aux_olibros = pd.read_csv('extracted_data/aux_olibros.csv', dtype = str)
    df_autores = pd.read_csv('extracted_data/aux_autores.csv', dtype = str).drop(['idgruplac','nombre_grupo','idcvlac'], axis=1)
    df_productos = pd.read_csv('extracted_data/aux_productos.csv', dtype = str).drop(['idgruplac','nombre_grupo'], axis=1)

    df_productos, df_autores=integrar(aux_articulosg,aux_basicog,aux_caplibrosg,aux_identificadores,aux_integrantes,aux_librosg,aux_oarticulos,aux_olibros,df_autores,df_productos)
    
    #Inserción a base de datos de SCOPUS
    productos = ProductosController()
    try:
        print('insertando productos')
        productos.insert_df(df_productos)
        df_productos.to_csv('extracted_data/aux_productos.csv',index=False)
    except:
        print('error en inserción de datos para productos de scopus')
        raise
        
    del productos
    
    autores = AutoresController()
    autores.insert_df(df_autores)
    df_autores.to_csv('extracted_data/aux_autores.csv',index=False)
    
    """
    try:
        os.remove('aux_articulosg.csv')
        os.remove('aux_basicog.csv')
        os.remove('aux_caplibrosg.csv')
        os.remove('aux_identificadores.csv')
        os.remove('aux_integrantes.csv')
        os.remove('aux_librosg.csv')
        os.remove('aux_oarticulos.csv')
        os.remove('aux_olibros.csv')
        os.remove('aux_autores.csv')
        os.remove('aux_productos.csv')
        os.remove(aux_instituciones.csv)
        os.remove(aux_lineas.csv)
        os.remove(aux_pdoctorado.csv)
        os.remove(aux_pmaestria.csv)
        os.remove(aux_cdoctorado.csv)
        os.remove(aux_cmaestria.csv)
        os.remove(aux_disenoind.csv)
        os.remove(aux_otecnologicos.csv)
        os.remove(aux_prototiposg.csv)
        os.remove(aux_softwareg.csv)
        os.remove(aux_empresatecg.csv)
        os.remove(aux_innovaempresag.csv)
        os.remove(aux_plantapilotog.csv)
        os.remove(aux_autores_integrado.csv)
        os.remove(aux_productos_integrado.csv)
        
        print('aux csv files deleted')
        
    except:
        print('Error deleting csv files')
    """
    
    print('Integración finalizada')
    
    
    
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
