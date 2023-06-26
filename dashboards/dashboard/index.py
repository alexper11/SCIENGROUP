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
                        html.P('Para hacer uso del explorador de datos, utilice el filtro en el que puede elegir la fuente de los datos, de acuerdo a su elección puede seleccionar el producto a analizar y filtrar los datos con el botón filtrar. Si quiere realizar un nivel más profundo en el filtrado, elija la caracteristica del producto y su valor. La opción General permite realizar un análisis de datos de un conjunto de grupos de investigación, permite elejir entre filtrar por intituciones, por la clasificación, las áreas, y las líneas de investigación de los grupos, o ingreso manual para elejir los grupos de investigación a analizar manualmente por nombre',style={"text-align": "justify"}),
                        html.Hr(),
                        html.H3('Análisis GrupLAC'),
                        html.P('Para realizar el análisis de los datos de GrupLAC, utilice el filtro de acuerdo a sus necesidades, la opción "Individual" permite realizar un análisis de un único grupo de investigación, elija el grupo y el producto científico.',style={"text-align": "justify"}),
                        html.Hr(),
                        html.H3('Análisis Scopus'),
                        html.P('Para realizar el análisis de los datos de Scopus, utilice el filtro de acuerdo a sus necesidades, la opción "Individual" permite realizar un análisis de un único grupo de investigación, elija el grupo y el producto científico.',style={"text-align": "justify"}),
                        html.Hr(),
                        html.H3('Indicadores GrupLAC'),
                        html.P([html.Span('Consistencia: ', style={'font-weight': 'bold'}),'Mide la actividad de un grupo de investigación según su consistencia generando productos nuevos a lo largo de un periodo de tiempo.'],style={"text-align": "justify"}),
                        html.P([html.Span('PPA (Promedio de productos por año): ', style={'font-weight': 'bold'}),'Indicador absoluto que representa la media de documentos publicados en un periodo de tiempo para un tema específico.'],style={"text-align": "justify"}),
                        html.P([html.Span('PPUA (Porcentaje de productos en los últimos años): ', style={'font-weight': 'bold'}),'Representa el porcentaje de la producción cientifica de un grupo en los últimos 3 años con respecto a la producción general de todos los grupos del departamento.'],style={"text-align": "justify"}),
                        html.P([html.Span('Productos generados: ', style={'font-weight': 'bold'}),'Muestra el número total de productos publicados en GrupLAC por un grupo de investigación.'],style={"text-align": "justify"}),
                        html.P([html.Span('Autores: ', style={'font-weight': 'bold'}),'Representa el número total de autores registrados en un grupo de investigación.'],style={"text-align": "justify"}),
                        html.Hr(),
                        html.H3('Indicadores Scopus'),
                        html.P([html.Span('H1 index: ', style={'font-weight': 'bold'}),'H index de primer orden, indica que el grupo ha publicado H1 productos con al menos H1 citaciones. '],style={"text-align": "justify"}),
                        html.P([html.Span('H2 index: ', style={'font-weight': 'bold'}),'H index de segundo orden, indica que el grupo tiene H2 investigadores, cada uno con al menos un registro H2 en Scopus.'],style={"text-align": "justify"}),
                        html.P([html.Span('Autores: ', style={'font-weight': 'bold'}),'Representa el número de autores de un grupo de investigación que fueron emparejados de GrupLAC y Scopus.'],style={"text-align": "justify"}),
                        html.P([html.Span('Conteo Productos: ', style={'font-weight': 'bold'}),'Muestra el número total de productos publicados en Scopus por un grupo de investigación.'],style={"text-align": "justify"}),
                        html.P([html.Span('Conteo Citaciones: ', style={'font-weight': 'bold'}),'Suma total de citas de los productos del grupo de investigación analizado.'],style={"text-align": "justify"}),
                        html.P([html.Span('CO (Citations per Output): ', style={'font-weight': 'bold'}),'Promedio de citas que ha recibido una entidad hasta la fecha por cada salida. Una entidad puede ser una institución, un grupo de investigación o un investigador.'],style={"text-align": "justify"}),
                        html.Hr(),
                        html.H3('Herramientas para manipulación de gráficas'),
                        html.P('1. Descargar gráfica en formato PNG.',style={"text-align": "left"}),
                        html.P('2. Realizar zoom selectivo a la gráfica.',style={"text-align": "left"}),
                        html.P('3. Mover la gráfica.',style={"text-align": "left"}),
                        html.P('4. Selección de múltiples datos en forma rectangular',style={"text-align": "left"}),
                        html.P('5. Selección de múltiples datos de manera libre',style={"text-align": "left"}),
                        html.P('6. Aumentar zoom a la gráfica.',style={"text-align": "left"}),
                        html.P('7. Disminuir zoom a la gráfica.',style={"text-align": "left"}),
                        html.P('8. Autoescalar la gráfica para ver el total de los datos.',style={"text-align": "left"}),
                        html.P('9. Resetear los ejes de la gráfica',style={"text-align": "left"}),                        
                        html.Img(src='./assets/img/options_graph.png', id='options_graph',style={'width':'auto', "height":'8rem', "position":"static","padding-left":"27px"}),
                        dcc.Link("Información sobre los desarrolladores", href='/about_us', className='nav-link')
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
                 "Dashboard para el análisis de la producción científica"
             )
         ],
       id='footer',
       className='footer'
    ),
    dcc.Location(id='url', refresh='callback-nav'),     
], className='grid-container')

#-----------------------------------Callbacks ---------------------------------

#This callback controls the paths to show every module
@app.callback(
    Output('main-content','children'),
    [Input('url', 'pathname')]
, prevent_initial_call=True)
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
    #app.run_server(host='10.55.4.73', port=8051,debug=True)
    app.run_server(host='localhost', port=8051,debug=True)
