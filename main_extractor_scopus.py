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

#############   Librerias para flask  #########
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
import unittest
###########   end librerias flask   ###########

#crea una nueva instancia de flask:
app= Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY']='SUPER SECRETO' #No es la mejor practica

    
class FieldFormScopus(FlaskForm):
    id_scopus = StringField('Digite el ID de la institución:', validators=[DataRequired()])    
    submit_scopus = SubmitField('Extraer productos')
    
class CredentialForm(FlaskForm):
    apikey = StringField('Digite el Apikey:', validators=[DataRequired()])
    token = StringField('Digite el Token:', validators=[DataRequired()])    
    submit_credential = SubmitField('Registrar')

#Creamos un decorador:
@app.cli.command()
def test():
    #Todo lo que encuentre unittest en el directorio tests:
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
    

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/home_scopus'))
    session['user_ip'] = user_ip

    return response

@app.route('/home_scopus', methods=['GET', 'POST']) #ruta en que
def home():
    user_ip = session.get('user_ip')
    credential_form = CredentialForm()
    apikey = session.get('apikey')
    token = session.get('token')
    
    context = {
        'user_ip' : user_ip,
        'login_form' : credential_form,
        'apikey' : apikey,
        'token' : token
    }
    
    if credential_form.validate_on_submit():#detecta cuando hay posy y valida la forma
        apikey = credential_form.apikey.data
        token = credential_form.token.data
        session['apikey'] = apikey
        session['token'] = token
        
        flash('Credenciales registradas con éxito')
        
        return redirect(url_for('extractor'))
    
    return render_template('home_scopus.html', **context)

@app.route('/extractor_scopus', methods=['GET', 'POST'])
def extractor():
    field_form_scopus = FieldFormScopus()
    credential_form = CredentialForm()
    id_scopus = session.get('id_scopus') 
    apikey = session.get('apikey')
    token = session.get('token')     
            
    context_extractor = {
        'field_form_scopus' : field_form_scopus,
        'id_scopus' : id_scopus,
        'apikey' : apikey,
        'token' : token
    }        
        
    if field_form_scopus.validate_on_submit():
        id_scopus = field_form_scopus.id_scopus.data
        session['id_scopus'] = id_scopus
        apikey = credential_form.apikey.data
        token = credential_form.token.data
        session['apikey'] = apikey
        session['token'] = token
        
        try:
            sys.path.append(".")                               
            create_scopus_db()
            print('Bases de datos creadas')
            
            # API_KEY=""
            # INST_TOKEN=""
            # API_KEY, INST_TOKEN = read_key()            
            # ExtractorS = ExtractorScopus(API_KEY,INST_TOKEN)
            print('api: ', apikey)
            print ('token: ',token)
            ExtractorS = ExtractorScopus(apikey,token)
            
            # authors_list=ExtractorS.get_auid_list(60051434)
            authors_list=ExtractorS.get_auid_list(id_scopus)
            
            df_autores=ExtractorS.get_authors_df(authors_list) 
            
            autores = AutoresController()
            autores.insert_df(df_autores)
            
            # df_productos=ExtractorS.get_articles_full([60051434])
            df_productos=ExtractorS.get_articles_full([id_scopus])
            
            #df_productos=pd.read_csv ('df_productos.csv')
            productos = ProductosController()
            try:
                productos.insert_df(df_productos)
            except:
                df_productos.to_csv('df_productos.csv',index=False)
                raise
            del ExtractorS
            
            flash('Extracción del perfil de Cvlac terminado')                
        except:
            flash('Error de conexion')
        #make_response(redirect('/home'))
                
        return redirect(url_for('extractor'))    

   
    return render_template('extractor_scopus.html', **context_extractor)

@app.route('/scopus', methods=['GET', 'POST']) 
def scopus():    
    return render_template('scopus.html')