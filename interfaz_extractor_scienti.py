from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.ExtractorGruplac import ExtractorGruplac
from cvlac.util import get_lxml

import pandas as pd
import sys
import requests
import json
from requests.exceptions import ConnectionError

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


#############   Librerias para flask  #########
from flask import Flask, request, make_response, redirect, render_template, url_for, flash, jsonify
from flask import Flask
from flask import session as session_flask
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
import unittest
###########   end librerias flask   ###########

#crea una nueva instancia de flask:
app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY']='SUPER SECRETO' #No es la mejor practica

    
class FieldFormCvlac(FlaskForm):
    enlace_cvlac = StringField('Digite enlace Cvlac:', validators=[DataRequired()])    
    submit_cvlac = SubmitField('Extraer cvlac')
    
class FieldFormGruplac(FlaskForm):
    enlace_gruplac = StringField('Digite enlace Gruplac:', validators=[DataRequired()])
    action_gruplac = RadioField('Elige una opción:', choices = ['Extraer datos del Gruplac', 'Extraer datos de los investigadores del Gruplac'], validators=[DataRequired()])
    submit_gruplac = SubmitField('Extraer gruplac')

#Creamos un decorador:
@app.cli.command()
def test():
    #Todo lo que encuentre unittest en el directorio tests:
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
    

@app.errorhandler(404)
def not_found(error):
    return render_template('404_scienti.html',error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/extractor_scienti'))
    session_flask['user_ip'] = user_ip

    return response

@app.route('/home_scienti', methods=['GET', 'POST']) #ruta en que
def home():
    user_ip = session_flask.get('user_ip')    
    context = {
        'user_ip' : user_ip
    }        
    return render_template('home_scienti.html', **context)

@app.route('/extractor_scienti', methods=['GET', 'POST'])
def extractor():
    field_form_cvlac = FieldFormCvlac()
    enlace_cvlac = session_flask.get('enlace_cvlac')
        
    field_form_gruplac = FieldFormGruplac()
    enlace_gruplac = session_flask.get('enlace_gruplac')
    action_gruplac = session_flask.get('action_gruplac')
        
    context_extractor = {
        'field_form_cvlac' : field_form_cvlac,
        'enlace_cvlac' : enlace_cvlac,
        'field_form_gruplac' : field_form_gruplac,
        'action_gruplac' : action_gruplac,
        'enlace_gruplac' : enlace_gruplac
    }        
        
    if field_form_cvlac.validate_on_submit():
        enlace_cvlac = field_form_cvlac.enlace_cvlac.data
        session_flask['enlace_cvlac'] = enlace_cvlac
        if 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=' in enlace_cvlac:
            try:
                Extractor=ExtractorCvlac()
                #urls cvlac:                    
                dom = get_lxml(enlace_cvlac)
                id_cvlac = enlace_cvlac[enlace_cvlac.find('=')+1:]
                
                df_basico = Extractor.get_basico(dom,enlace_cvlac)
                print(df_basico['nombre'].loc[0])
                if str(df_basico['nombre'].loc[0]) == '':
                    print('IdCvlac inválido')
                    flash('Lo sentimos, url inválida')
                else: 
                    #Genera dataframe por cada tabla de informacion
                    df_academica = Extractor.get_academica(dom,enlace_cvlac)
                    df_actuacion = Extractor.get_actuacion(dom,enlace_cvlac)
                    df_articulo = Extractor.get_articulo(dom,enlace_cvlac)
                    #df_basico = Extractor.get_basico(dom,enlace_cvlac)
                    df_complementaria = Extractor.get_complementaria(dom,enlace_cvlac)
                    df_estancias = Extractor.get_estancias(dom,enlace_cvlac)
                    df_evaluador = Extractor.get_evaluador(dom,enlace_cvlac)
                    df_idioma = Extractor.get_idioma(dom,enlace_cvlac)
                    df_investiga = Extractor.get_investiga(dom,enlace_cvlac)
                    df_jurado = Extractor.get_jurado(dom,enlace_cvlac)
                    df_libro = Extractor.get_libro(dom,enlace_cvlac)
                    df_reconocimiento = Extractor.get_reconocimiento(dom,enlace_cvlac)
                    df_redes = Extractor.get_redes(dom,enlace_cvlac)
                    df_identificadores = Extractor.get_identificadores(dom,enlace_cvlac)
                    df_caplibro = Extractor.get_caplibro(dom,enlace_cvlac)
                    df_software = Extractor.get_software(dom,enlace_cvlac)
                    df_prototipo = Extractor.get_prototipo(dom,enlace_cvlac)
                    df_tecnologicos = Extractor.get_tecnologicos(dom,enlace_cvlac)
                    df_empresa_tecnologica = Extractor.get_empresa_tecnologica(dom,enlace_cvlac)
                    df_innovacion = Extractor.get_innovacion(dom,enlace_cvlac) 
                    
                    print('Extracción del perfil de Cvlac terminado')
                    flash('Extracción del perfil de Cvlac terminado')
                    
                    #Crea objeto controlador para cada tabla              
                    actuacionObj = ActuacionController()
                    articuloObj = ArticulosController()
                    basicoObj = BasicoController()
                    evaluadorObj = EvaluadorController()
                    identificadoresObj = IdentificadoresController()
                    idiomaObj = IdiomaController()
                    investigacionObj = InvestigacionController()
                    juradosObj = JuradosController()
                    librosObj = LibrosController()
                    reconocimientoObj = ReconocimientoController()
                    redesObj = RedesController()
                    estanciasObj = EstanciasController()
                    academicaObj = AcademicaController()
                    complementariaObj = ComplementariaController()
                    empresaTecnologicaObj = EmpresaTecnologicaController()
                    innovacionEmpresarialObj = InnovacionEmpresarialController()
                    capLibrosObj = CaplibrosController()
                    prototipoObj = PrototipoController()
                    softwareObj = SoftwareController()
                    tecnologicosObj = TecnologicosController()
                    
                    #Con cada objeto, elimina los datos para no guardar duplicados
                    actuacionObj.delete_idcvlac(id_cvlac)
                    articuloObj.delete_idcvlac(id_cvlac)
                    evaluadorObj.delete_idcvlac(id_cvlac)
                    identificadoresObj.delete_idcvlac(id_cvlac)
                    idiomaObj.delete_idcvlac(id_cvlac)
                    investigacionObj.delete_idcvlac(id_cvlac)
                    juradosObj.delete_idcvlac(id_cvlac)
                    librosObj.delete_idcvlac(id_cvlac)
                    reconocimientoObj.delete_idcvlac(id_cvlac)
                    redesObj.delete_idcvlac(id_cvlac)
                    estanciasObj.delete_idcvlac(id_cvlac)
                    academicaObj.delete_idcvlac(id_cvlac)
                    complementariaObj.delete_idcvlac(id_cvlac)
                    empresaTecnologicaObj.delete_idcvlac(id_cvlac)
                    innovacionEmpresarialObj.delete_idcvlac(id_cvlac)
                    capLibrosObj.delete_idcvlac(id_cvlac)
                    prototipoObj.delete_idcvlac(id_cvlac)
                    softwareObj.delete_idcvlac(id_cvlac)
                    tecnologicosObj.delete_idcvlac(id_cvlac)
                    basicoObj.delete_idcvlac(id_cvlac)
                    
                    #inserta los dataframes extraidos anteriormente y los almacena
                    basicoObj.insert_df(df_basico)
                    actuacionObj.insert_df(df_actuacion)
                    articuloObj.insert_df(df_articulo)
                    evaluadorObj.insert_df(df_evaluador)
                    identificadoresObj.insert_df(df_identificadores)
                    idiomaObj.insert_df(df_idioma)
                    investigacionObj.insert_df(df_investiga)
                    juradosObj.insert_df(df_jurado)
                    librosObj.insert_df(df_libro)
                    reconocimientoObj.insert_df(df_reconocimiento)
                    redesObj.insert_df(df_redes)
                    estanciasObj.insert_df(df_estancias)
                    academicaObj.insert_df(df_academica)
                    complementariaObj.insert_df(df_complementaria)
                    empresaTecnologicaObj.insert_df(df_empresa_tecnologica)
                    innovacionEmpresarialObj.insert_df(df_innovacion)
                    capLibrosObj.insert_df(df_caplibro)
                    prototipoObj.insert_df(df_prototipo)
                    softwareObj.insert_df(df_software)
                    tecnologicosObj.insert_df(df_tecnologicos)
                    
                    print('Guardado exitósamente en la base de datos')                               
                    flash('Guardado exitósamente en la base de datos')
                                
            except ConnectionError:            
                print('Error de conexion')
                flash('Lo sentimos, error de conexión')
            except:
                print('Error interno')
                flash('Lo sentimos, error interno')
                raise
            
            del Extractor
            #make_response(redirect('/home_scienti'))
        else:
            print('link incorrecto')
            flash('Lo sentimos, link incorrecto')
        
        return redirect(url_for('extractor'))        
    
    if field_form_gruplac.validate_on_submit():#detecta cuando hay post y valida la forma
        enlace_gruplac = field_form_gruplac.enlace_gruplac.data
        action_gruplac = field_form_gruplac.action_gruplac.data
        session_flask['enlace_gruplac'] = enlace_gruplac
        session_flask['action_gruplac'] = action_gruplac
        if 'https://scienti.minciencias.gov.co/gruplac/jsp/' in enlace_gruplac:
            try:       
                ExtractorG = ExtractorGruplac()
                id_gruplac = enlace_gruplac[enlace_gruplac.find('=')+1:]      
                
                #Extrae datos de un gruplac:
                if action_gruplac == 'Extraer datos del Gruplac':
                    dom = get_lxml(enlace_gruplac)
                    
                    df_perfil_basico = ExtractorG.get_perfil_basico(dom,enlace_gruplac)
                    print(df_perfil_basico['nombre'].shape[0])
                    if str(df_perfil_basico['nombre'].shape[0]) == '0':
                        print('IdGruplac inválido')
                        flash('Lo sentimos, url inválida')
                    else:                    
                        #Genera dataframes de tablas de información de un gruplac
                        #df_perfil_basico = ExtractorG.get_perfil_basico(dom,enlace_gruplac)
                        df_perfil_instituciones = ExtractorG.get_perfil_instituciones(dom,enlace_gruplac)
                        df_perfil_lineas = ExtractorG.get_perfil_lineas(dom,enlace_gruplac)
                        df_perfil_integrantes = ExtractorG.get_perfil_integrantes(dom,enlace_gruplac)
                        df_perfil_programa_doctorado = ExtractorG.get_perfil_programa_doctorado(dom,enlace_gruplac)
                        df_perfil_programa_maestria = ExtractorG.get_perfil_programa_maestria(dom,enlace_gruplac)
                        df_perfil_otro_programa = ExtractorG.get_perfil_otro_programa(dom,enlace_gruplac)
                        df_perfil_curso_doctorado = ExtractorG.get_perfil_curso_doctorado(dom,enlace_gruplac)
                        df_perfil_curso_maestria = ExtractorG.get_perfil_curso_maestria(dom,enlace_gruplac)
                        df_perfil_articulos = ExtractorG.get_perfil_articulos(dom,enlace_gruplac)
                        df_perfil_libros = ExtractorG.get_perfil_libros(dom,enlace_gruplac)
                        df_perfil_caplibros = ExtractorG.get_perfil_caplibros(dom,enlace_gruplac)
                        df_perfil_otros_articulos = ExtractorG.get_perfil_otros_articulos(dom,enlace_gruplac)
                        df_perfil_otros_libros = ExtractorG.get_perfil_otros_libros(dom,enlace_gruplac)
                        df_perfil_diseno_industrial = ExtractorG.get_perfil_diseno_industrial(dom,enlace_gruplac)
                        df_perfil_otros_tecnologicos = ExtractorG.get_perfil_otros_tecnologicos(dom,enlace_gruplac)
                        df_perfil_prototipos = ExtractorG.get_perfil_prototipos(dom,enlace_gruplac)
                        df_perfil_software = ExtractorG.get_perfil_software(dom,enlace_gruplac)
                        df_perfil_empresa_tecnologica = ExtractorG.get_perfil_empresa_tecnologica(dom,enlace_gruplac)
                        df_perfil_innovacion_empresarial = ExtractorG.get_perfil_innovacion_empresarial(dom,enlace_gruplac)
                        df_perfil_planta_piloto = ExtractorG.get_perfil_planta_piloto(dom,enlace_gruplac)
                        
                        print('Extracción del perfil de Gruplac terminado')
                        flash('Extracción del perfil de Gruplac terminado')
                        
                        # creo objetos controller_grup para cada tabla de gruplac     
                        perfilBasicoObj = BasicoGController()
                                           
                        perfilArticulosObj = ArticulosGController()
                        perfilArticulosObj.delete_idgruplac(id_gruplac)
                                              
                        perfilCapLibrosObj = CaplibrosGController()
                        perfilCapLibrosObj.delete_idgruplac(id_gruplac)
                        
                        perfilCursoDoctoradoObj = CursoDoctoradoController()
                        perfilCursoDoctoradoObj.delete_idgruplac(id_gruplac)
                        
                        perfilCursoMaestriaObj = CursoMaestriaController()
                        perfilCursoMaestriaObj.delete_idgruplac(id_gruplac)
                        
                        perfilDisenoIndustrialObj = DisenoIndustrialGController()
                        perfilDisenoIndustrialObj.delete_idgruplac(id_gruplac)
                        
                        perfilEmpresaTecnologicaObj = EmpresaTecnologicaGController()
                        perfilEmpresaTecnologicaObj.delete_idgruplac(id_gruplac)
                        
                        perfilInnovacionEmpresarialObj = InnovacionEmpresarialGController()
                        perfilInnovacionEmpresarialObj.delete_idgruplac(id_gruplac)
                        
                        perfilInstitucionesObj = InstitucionesController()
                        perfilInstitucionesObj.delete_idgruplac(id_gruplac)
                        
                        perfilIntegrantesObj = IntegrantesController()
                        perfilIntegrantesObj.delete_idgruplac(id_gruplac)
                        
                        perfilLibrosObj = LibrosGController()
                        perfilLibrosObj.delete_idgruplac(id_gruplac)
                        
                        perfilLineasObj = LineasGController()
                        perfilLineasObj.delete_idgruplac(id_gruplac)
                        
                        perfilOtroProgramaObj = OtroProgramaController()
                        perfilOtroProgramaObj.delete_idgruplac(id_gruplac)
                        
                        perfilOtrosArticulosObj = OtrosArticulosController()
                        perfilOtrosArticulosObj.delete_idgruplac(id_gruplac)
                        
                        perfilOtrosLibrosObj = OtrosLibrosController()
                        perfilOtrosLibrosObj.delete_idgruplac(id_gruplac)
                        
                        perfilOtrosTecnologicosObj = OtrosTecnologicosController()
                        perfilOtrosTecnologicosObj.delete_idgruplac(id_gruplac)
                        
                        perfilPlantaPilotoObj = PlantaPilotoGController()
                        perfilPlantaPilotoObj.delete_idgruplac(id_gruplac)
                        
                        perfilProgramaDoctoradoObj = ProgramaDoctoradoController()
                        perfilProgramaDoctoradoObj.delete_idgruplac(id_gruplac)
                        
                        perfilProgramaMaestriaObj = ProgramaMaestriaController()
                        perfilProgramaMaestriaObj.delete_idgruplac(id_gruplac)
                        
                        perfilPrototiposObj = PrototiposGController()
                        perfilPrototiposObj.delete_idgruplac(id_gruplac)
                        
                        perfilSoftwareObj = SoftwareGController()
                        perfilSoftwareObj.delete_idgruplac(id_gruplac)
                        
                        perfilBasicoObj.delete_idgruplac(id_gruplac) 
                        
                        perfilBasicoObj.insert_df(df_perfil_basico)
                        perfilArticulosObj.insert_df(df_perfil_articulos)
                        perfilCapLibrosObj.insert_df(df_perfil_caplibros)
                        perfilCursoDoctoradoObj.insert_df(df_perfil_curso_doctorado)
                        perfilCursoMaestriaObj.insert_df(df_perfil_curso_maestria)
                        perfilDisenoIndustrialObj.insert_df(df_perfil_diseno_industrial)
                        perfilEmpresaTecnologicaObj.insert_df(df_perfil_empresa_tecnologica)
                        perfilInnovacionEmpresarialObj.insert_df(df_perfil_innovacion_empresarial)
                        perfilInstitucionesObj.insert_df(df_perfil_instituciones)
                        perfilIntegrantesObj.insert_df(df_perfil_integrantes)
                        perfilLibrosObj.insert_df(df_perfil_libros)
                        perfilLineasObj.insert_df(df_perfil_lineas)
                        perfilOtroProgramaObj.insert_df(df_perfil_otro_programa)
                        perfilOtrosArticulosObj.insert_df(df_perfil_otros_articulos)
                        perfilOtrosLibrosObj.insert_df(df_perfil_otros_libros)
                        perfilOtrosTecnologicosObj.insert_df(df_perfil_otros_tecnologicos)
                        perfilPlantaPilotoObj.insert_df(df_perfil_planta_piloto)
                        perfilProgramaDoctoradoObj.insert_df(df_perfil_programa_doctorado)
                        perfilProgramaMaestriaObj.insert_df(df_perfil_programa_maestria)
                        perfilPrototiposObj.insert_df(df_perfil_prototipos)
                        perfilSoftwareObj.insert_df(df_perfil_software)
                                                
                        print('Guardado exitósamente en la base de datos')                               
                        flash('Guardado exitósamente en la base de datos')
                    
                #Extrae datos de investigadores de gruplac:
                elif action_gruplac == 'Extraer datos de los investigadores del Gruplac':            
                    # llamo get_cvs mando url del gruplac y recibo un diccionario de df de todas las tablas acumuladas
                    dom = get_lxml(enlace_gruplac)                                        
                    df_perfil_basico = ExtractorG.get_perfil_basico(dom,enlace_gruplac)
                    print(df_perfil_basico['nombre'].shape[0])
                    if str(df_perfil_basico['nombre'].shape[0]) == '0':
                        print('IdGruplac inválido')
                        flash('Lo sentimos, url inválida')
                    else:
                        dic_data = ExtractorG.get_cvs(enlace_gruplac)                                                                                   
                        #datag=dic_data.value_counts()                        
                        print('Extracción de los Cvlacs del perfil de Gruplac terminado')
                        flash('Extracción de los Cvlacs del perfil de Gruplac terminado')
                       
                        #Crea objeto controlador para cada tabla              
                        actuacionObj = ActuacionController()
                        articuloObj = ArticulosController()
                        basicoObj = BasicoController()
                        evaluadorObj = EvaluadorController()
                        identificadoresObj = IdentificadoresController()
                        idiomaObj = IdiomaController()
                        investigacionObj = InvestigacionController()
                        juradosObj = JuradosController()
                        librosObj = LibrosController()
                        reconocimientoObj = ReconocimientoController()
                        redesObj = RedesController()
                        estanciasObj = EstanciasController()
                        academicaObj = AcademicaController()
                        complementariaObj = ComplementariaController()
                        empresaTecnologicaObj = EmpresaTecnologicaController()
                        innovacionEmpresarialObj = InnovacionEmpresarialController()
                        capLibrosObj = CaplibrosController()
                        prototipoObj = PrototipoController()
                        softwareObj = SoftwareController()
                        tecnologicosObj = TecnologicosController()
                        
                        #Con cada objeto, elimina los datos para no guardar duplicados
                        list_idcvlac=dic_data['basico']['idcvlac'].tolist()
                        for id_cvlac in list_idcvlac:
                            
                            actuacionObj.delete_idcvlac(id_cvlac)
                            articuloObj.delete_idcvlac(id_cvlac)
                            evaluadorObj.delete_idcvlac(id_cvlac)
                            identificadoresObj.delete_idcvlac(id_cvlac)
                            idiomaObj.delete_idcvlac(id_cvlac)
                            investigacionObj.delete_idcvlac(id_cvlac)
                            juradosObj.delete_idcvlac(id_cvlac)
                            librosObj.delete_idcvlac(id_cvlac)
                            reconocimientoObj.delete_idcvlac(id_cvlac)
                            redesObj.delete_idcvlac(id_cvlac)
                            estanciasObj.delete_idcvlac(id_cvlac)
                            academicaObj.delete_idcvlac(id_cvlac)
                            complementariaObj.delete_idcvlac(id_cvlac)
                            empresaTecnologicaObj.delete_idcvlac(id_cvlac)
                            innovacionEmpresarialObj.delete_idcvlac(id_cvlac)
                            capLibrosObj.delete_idcvlac(id_cvlac)
                            prototipoObj.delete_idcvlac(id_cvlac)
                            softwareObj.delete_idcvlac(id_cvlac)
                            tecnologicosObj.delete_idcvlac(id_cvlac)   
                            basicoObj.delete_idcvlac(id_cvlac)                           
                                        
                        #inserta los dataframes extraidos anteriormente y los almacena
                        basicoObj.insert_df(dic_data['basico'])
                        actuacionObj.insert_df(dic_data['actuacion'])
                        articuloObj.insert_df(dic_data['articulos'])
                        evaluadorObj.insert_df(dic_data['evaluador'])
                        identificadoresObj.insert_df(dic_data['identificadores'])
                        idiomaObj.insert_df(dic_data['idioma'])
                        investigacionObj.insert_df(dic_data['investigacion'])
                        juradosObj.insert_df(dic_data['jurado'])
                        librosObj.insert_df(dic_data['libros'])
                        reconocimientoObj.insert_df(dic_data['reconocimiento'])
                        redesObj.insert_df(dic_data['redes'])
                        estanciasObj.insert_df(dic_data['estancias'])
                        academicaObj.insert_df(dic_data['academica'])
                        complementariaObj.insert_df(dic_data['complementaria'])
                        empresaTecnologicaObj.insert_df(dic_data['empresa_tecnologica'])
                        innovacionEmpresarialObj.insert_df(dic_data['innovacion_empresarial'])
                        capLibrosObj.insert_df(dic_data['caplibros'])
                        prototipoObj.insert_df(dic_data['prototipo'])
                        softwareObj.insert_df(dic_data['software'])
                        tecnologicosObj.insert_df(dic_data['tecnologicos'])
                        
                        print('Guardado exitósamente en la base de datos')                               
                        flash('Guardado exitósamente en la base de datos')
                                        
                else:
                    #make_response(redirect('/home_scienti'))
                    pass  
            except ConnectionError:            
                print('Error de conexion')
                flash('Lo sentimos, error de conexión')
            except:
                print('Error interno 1')
                flash('Lo sentimos, error interno')
                raise
            
            del ExtractorG           
        else:
            print('link incorrecto')
            flash('Lo sentimos, link incorrecto')
            
        return redirect(url_for('extractor'))
   
    return render_template('extractor_scienti.html', **context_extractor)

@app.route('/scopus', methods=['GET', 'POST']) 
def scopus():    
    return render_template('scopus.html')

#Cambia de puerto de flask siempre que se ejecute directamente el main y no se exporte como un módulo
if __name__ == "__main__":
    app.config['ENV'] = 'development'
    app.run(host='127.0.0.1', port=5006, threaded=True, debug=True)