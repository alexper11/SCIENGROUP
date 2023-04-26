from scopus.ExtractorScopus import ExtractorScopus
from scopus.Scientopy import Scientopy
# from scopus.readKey import read_key

import pandas as pd
import sys
import requests
import json
from requests.exceptions import ConnectionError

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
app.config['SESSION_COOKIE_NAME'] = 'session'

class FieldFormAutor(FlaskForm):
    #authorid de Gustavo Ramirez = 36603157500
    #authorid de Cristhian Figueroa = 7004506288
    id_autor = StringField('Digite el Author ID:', validators=[DataRequired()])
    submit_autor = SubmitField('Extraer Autor')
class FieldFormProducto(FlaskForm):
    #eid articulo de Cristhian Figueroa = 2-s2.0-84944176710
    #eid articulo de Cristhian Figueroa = 2-s2.0-85059990681
    id_producto = StringField('Digite el eid del Producto:', validators=[DataRequired()])
    submit_producto = SubmitField('Extraer Producto')

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
    return render_template('404_scopus.html',error=error)


@app.route('/logout')
def logout():
    session.clear()
    return make_response(redirect('/'))

@app.route('/')
def index():
    session.permanent = False
    user_ip = request.remote_addr
    response = make_response(redirect('/home_scopus'))
    session['user_ip'] = user_ip
    return response

@app.route('/home_scopus', methods=['GET', 'POST']) #ruta en que
def home():
    session.permanent = False
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
    field_form_autor = FieldFormAutor()
    field_form_producto = FieldFormProducto()
    #credential_form = CredentialForm()
    id_autor = session.get('id_autor')
    id_producto = session.get('id_producto')
    apikey = session.get('apikey')
    token = session.get('token')


    context_extractor = {
        'field_form_autor' : field_form_autor,
        'field_form_producto' : field_form_producto,
        'id_autor' : id_autor,
        'id_producto' : id_producto,
        # 'credential_form': credential_form,
        'apikey' : apikey,
        'token' : token
    }

    if field_form_autor.validate_on_submit():
        id_autor = field_form_autor.id_autor.data
        session['id_autor'] = id_autor
        apikey = session.get('apikey')
        token = session.get('token')
        try:
            sys.path.append(".")
            print('Inicializando prueba...')            
            print('api: ', apikey)
            print ('token: ',token)
            ExtractorS = ExtractorScopus(apikey,token)
            state_api = ExtractorS.get_credential_validator(id_autor)
            if state_api == 'APIKEY_INVALID':
                print('Credenciales invalidas')
                flash('Credenciales inválidas')
            else:
                #Inicio
                print('Credenciales validas')              
               
                df_autores=ExtractorS.get_authors_df([id_autor])                
                if isinstance(df_autores,str):                    
                    flash(df_autores)
                else:                                                           
                    autores = AutoresController()
                    print('Extracción del perfil de Scopus terminado')
                    flash('Extracción del perfil de Scopus terminado')
                    autores.delete_autor_id(id_autor)
                    autores.insert_df(df_autores)
                    print('Guardado exitósamente en la base de datos')                    
                    flash('Guardado exitósamente en la base de datos')
            del ExtractorS
        except ConnectionError:            
            print('Error de conexion')
            flash('Error de conexión')
            #make_response(redirect('/home'))
        
        except:
            print('Error de texto, verificar valor ingresado')
            flash('Error de texto, verificar valor ingresado')            

        return redirect(url_for('extractor'))
    
    if field_form_producto.validate_on_submit():
        id_producto = field_form_producto.id_producto.data
        session['id_producto'] = id_producto
        apikey = session.get('apikey')
        token = session.get('token')
        try:
            sys.path.append(".")
            print('Inicializando prueba...')            
            print('api: ', apikey)
            print ('token: ',token)
            ExtractorS = ExtractorScopus(apikey,token)
            state_api = ExtractorS.get_credential_validator(id_producto)
            if state_api == 'APIKEY_INVALID':
                print('Credenciales invalidas')
                flash('Credenciales inválidas')
            else:
                #Inicio
                print('Credenciales validas')                
               
                df_productos=ExtractorS.get_article(id_producto)#eid
                
                print('df_prodcutos:', df_productos)
                if isinstance(df_productos,str):                    
                    flash(df_productos)
                else:
                    #df_productos.to_csv('df_productos.csv',index=False)
                    print('Extracción del producto de Scopus terminado')
                    flash('Extracción del producto de Scopus terminado')
                    productos = ProductosController()
                    productos.delete_eid(id_producto)
                    productos.insert_df(df_productos)                    
                    print('Guardado exitósamente en la base de datos')                    
                    flash('Guardado exitósamente en la base de datos')
            del ExtractorS
                    

        except ConnectionError:            
            print('Error de conexion')
            flash('Error de conexión')
            #make_response(redirect('/home'))
        
        except:            
            print('Error de texto, verificar valor ingresado')

        return redirect(url_for('extractor'))

    return render_template('extractor_scopus.html', **context_extractor)

@app.route('/scopus', methods=['GET', 'POST'])
def scopus():
    return render_template('scopus.html')

#Cambia de puerto de flask siempre que se ejecute directamente el main y no se exporte como un módulo
if __name__ == "__main__":
    app.config['ENV'] = 'development'
    app.run(host='127.0.0.1', port=5005, threaded=True, debug=True)