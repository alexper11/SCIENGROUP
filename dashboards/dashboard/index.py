from dash.dependencies import Input, Output
from dash import  html
from dash import dcc
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



APP_LOGO = "/assets/img/logo_dash.png"


app.layout = html.Div([
    html.Header(        
            [html.Div([dcc.Link(html.Img(src=APP_LOGO, id='logo-icon'), href='/')]),
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
                        dcc.Link("GrupLAC", href='/scienti', className='nav-link'),
                    ], className='nav-item'),
                    html.Li([
                        dcc.Link("Scopus", href='/scopus', className='nav-link')
                    ], className='nav-item')
                ], className='navbar-nav mr-auto')
            ], className='headerRight'),
            html.Div([
                html.Img(src='/assets/img/info.png',id='info-icon'),  
                html.Aside([
                    html.Div([
                        # Información sobre el dash
                        html.H1('Instrucciones'),
                        html.Hr(),
                        html.H3('Explorador de datos'),
                        html.P('Para hacer uso del explorador de datos, utilice el filtro en el que puede elegir la fuente de los datos, de acuerdo a su elección puede seleccionar el producto a analizar y filtrar los datos con el botón filtrar. Si quiere realizar un nivel más profundo en el filtrado, elija la caracteristica del producto y su valor. La opción General permite realizar un análisis de datos de un conjunto de grupos de investigación, permite elejir entre filtrar por intituciones, por la clasificación, las áreas, y las líneas de investigación de los grupos, o ingreso manual para elejir los grupos de investigación a analizar manualmente por nombre'),
                        html.Hr(),
                        html.H3('Análisis GrupLAC'),
                        html.P('Para realizar el análisis de los datos de GrupLAC, utilice el filtro de acuerdo a sus necesidades, la opción "Individual" permite realizar un análisis de un único grupo de investigación, elija el grupo y el producto científico.'),
                        html.Hr(),
                        html.H3('Siglas utilizadas'),
                        html.P('PPA= Productos Por Año, PPUA= Porcentaje de productos  PG= Productos Generados'),

                        dcc.Link("Desarroladores", href='/about_us', className='nav-link')
                    ],className='asideMenu-content')
                ], className='asideMenu')
                ], className='asideMenuActivator'),
        ], className='row'
    ) 
    #Here in main contet will be displayed all the different pages
    ,html.Main(
       id='main-content',
    ),
    #defaul footer    
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
    app.run_server(host='localhost', port=8051,debug=True)