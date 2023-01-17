from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.ExtractorGruplac import ExtractorGruplac
from cvlac.util import get_lxml
from scopus.ExtractorScopus import ExtractorScopus
from scopus.Scientopy import Scientopy
# from scopus.readKey import read_key

import pandas as pd
import sys
import requests
import json
from requests.exceptions import ConnectionError

# from scopus.models.DBmodel import create_scopus_db
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

#############
import threading
import time
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

    if credential_form.validate_on_submit():#detecta cuando hay post y valida la forma
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
        # 'credential_form': credential_form,
        'apikey' : apikey,
        'token' : token
    }

    if field_form_scopus.validate_on_submit():
        id_scopus = field_form_scopus.id_scopus.data
        session['id_scopus'] = id_scopus
        apikey = session.get('apikey')
        token = session.get('token')
        # apikey = credential_form.apikey.data
        # token = credential_form.token.data
        # session['apikey'] = apikey
        # session['token'] = token

        try:
            sys.path.append(".")
            # create_scopus_db()
            print('Inicializando prueba...')

            # API_KEY=""
            # INST_TOKEN=""
            # API_KEY, INST_TOKEN = read_key()
            # ExtractorS = ExtractorScopus(API_KEY,INST_TOKEN)
            print('api: ', apikey)
            print ('token: ',token)
            ExtractorS = ExtractorScopus(apikey,token)
            state_api = ExtractorS.get_credential_validator(id_scopus)
            if state_api == 'APIKEY_INVALID':
                print('Credenciales invalidas')
                flash('Credenciales inválidas')
            else:
                #Inicio
                print('Credenciales validas')
                # authors_list=ExtractorS.get_auid_list(id_scopus)
                # df_autores=ExtractorS.get_authors_df(authors_list)

                # autores = AutoresController()
                # autores.insert_df(df_autores)
                # Fin

                # Lo siguiente es para id_institucion
                # hacerlo para solo producto
                url = f'https://api.elsevier.com/content/author/author_id/a?view=ENHANCED'
                response = requests.get(url,
                                        headers={'Accept':'application/json',
                                                 'X-ELS-APIKey': apikey,
                                                 'X-ELS-Insttoken': token})
                print(response.headers)
                result = response.json()
                print(result)
                print(response.headers['X-RateLimit-Remaining'])
                df_autores=ExtractorS.get_authors_df([id_scopus])
                if isinstance(df_autores,str):
                    print('aqui')
                    print(df_autores)
                    flash(df_autores)
                else:
                    df_autores.to_csv('df_autores.csv',index=False)
                    # df_productos=ExtractorS.get_articles_full([id_scopus])
                    # ###
                    # productos = ProductosController()
                    # try:
                    #     productos.insert_df(df_productos)
                    # except:
                    #     df_productos.to_csv('df_productos.csv',index=False)
                    #     raise
                    # del ExtractorS
                    flash('Extracción del perfil de Scopus terminado')

        except ConnectionError:            
            print('no entro a nada')
            flash('Error de conexión')
        #make_response(redirect('/home'))
        
        except:
            raise
            print('Error de texto, verificar valor ingresado')

        return redirect(url_for('extractor'))


    return render_template('extractor_scopus.html', **context_extractor)

@app.route('/scopus', methods=['GET', 'POST'])
def scopus():
    return render_template('scopus.html')