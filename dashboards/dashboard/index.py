from dash.dependencies import Input, Output
from dash import  html
import dash_core_components as dcc
import dash
import os
import flask


server = flask.Flask(__name__) # flask server creation

#Dash app instantiation
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True,meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
app.title = "Dashboard Scienti - Scopus"


#Here I Import the pages, I can´t do it above because the app must be created because 
# this pages need it
from pages import about_us, scopus, homepage, explorer, scienti, page404


#Url to use the same logo than Dashboard
APP_LOGO = "/assets/img/logo_dash.png"

#Basic an static template for all the dah application
app.layout = html.Div([
    #The header contains the hamburguer menu, the sidebar menu and the logo
    html.Header(        
            [html.Div([dcc.Link(html.Img(src=APP_LOGO, id='logo-icon'), href='/', id='logo-home')]),
            html.Div("Dashboard Analytics", className="rightOptions"),
            html.Div([
                html.Ul([
                    html.Li([
                        dcc.Link("Home", href='/', className='nav-link'),
                    ], className='nav-item'),
                    html.Li([
                        dcc.Link("Explorar datos", href='/exploration', className='nav-link'),
                    ], className='nav-item'),
                    html.Li([
                        dcc.Link("Scienti", href='/scienti', className='nav-link'),
                    ], className='nav-item'),
                    html.Li([
                        dcc.Link("Scopus", href='/scopus', className='nav-link')
                    ], className='nav-item')
                ], className='navbar-nav mr-auto')
            ], className='headerRight'),
            html.Div([
                html.Img(src='/assets/img/info.png', className='headerIcon'),  
                html.Aside([
                    html.Div([
                        # Información sobre el dash
                        html.H1('Este dashboard es una herramienta muy útil que permite presentar y analizar métricas clave,como el número de publicaciones, citas, índices de impacto, colaboraciones, etc.'),
                        html.H1('Permite Visualización clara de los datos, Fácil identificación de áreas de mejora, Seguimiento del progreso a lo largo del tiempo, Identificación de oportunidades de colaboración'),
                        dcc.Link("Desarroladores", href='/about_us', className='nav-link')
                    ],className='asideMenu-content')
                ], className='asideMenu')
                ], className='asideMenuActivator'),
        ], className='row'
    ) 
    #Here in main contet will be displayed all the different pages
    ,html.Main(
       id='main-content',
    )
    #defaul footer
     ,
     html.Footer(
         [
             html.H2(
                 "Dashboard para el análisis de de la producción científica"
             )
         ],
       id='footer',
       className='footer'
    ),
    dcc.Location(id='url', refresh=False),     
], className='grid-container')

#-----------------------------------Callbacks ---------------------------------

#This callback controls the paths to show every module
@app.callback(
    Output('main-content','children'),
    [Input('url', 'pathname')],
)
def loadpage(path_route):
    """
    Input: route in the path
    output: page to render
    """
    
    if path_route == '/'  :
        return homepage.layout
    elif path_route == '/exploration':
        return explorer.layout
    elif path_route == '/scienti':
        return scienti.layout
    elif path_route == '/scopus':
        return scopus.layout
    elif path_route == '/about_us':
        return about_us.layout
    else:
        return page404.layout

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8051,debug=True)