from flask_testing import TestCase
from flask import current_app, url_for

from main import app

class Maintest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        #Desactivar token de sesion activa para probar las formas ( se puede inyectar scripts ):
        app.config['WTF_CSRF_ENABLED'] = False
        
        return app
    
    #Prueba para ver si la app existe:
    def test_app_exists(self):
        self.assertIsNotNone(current_app)
        
    #Prueba para saber si la app esta en modo test:
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])
    
    #Prueba que index redirecciona a hello:
    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        
        self.assertRedirects(response, url_for('hello'))
    
    #Prueba que hello regresa un 200 cuando se hace un get:
    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        
        self.assert200(response)
    
    #Prueba que el al hacer un POST se obtiene el redirect index
    def test_hello_post(self):
        fake_form = {
            'username' : 'fake',
            'password' : 'fake-password'
        }
        response = self.client.post(url_for('hello'), data=fake_form)
        
        self.assertRedirects(response, url_for('index'))