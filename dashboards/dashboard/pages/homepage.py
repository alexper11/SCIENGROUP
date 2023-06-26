from dash import html
from dash import dcc

#Homepage layout with the cards of modules

layout = html.Div(
    # style={
    #     'background-image': 'url(/assets/img/home.png)',
    #     'background-size': 'contain',
    #     'background-repeat': 'no-repeat',
    #     'background-position': 'center center',
    #     'background-origin': 'content-box',
    #     'height': '100vh'
    # },
    children=[
        html.Div(
            style={
                'background-color': 'rgba(255, 255, 255, 0.9)',
                'padding': '3em',
                'border-radius': '1em',
                'margin': '5vh auto',
                'max-width': '70%'
            },
            children=[
                html.H3(
                    'Herramienta de análisis y visualización bibliométrica dentro del ámbito de los grupos de investigación en el Cauca.',
                    style={
                        'color': 'black',
                        'text-align': 'center',
                        'font-size': '1.5em'
                    }
                ),
                html.P([
                    'Esta herramienta es un Dashboard para el análisis y visualización de datos bibliográficos de la producción científica de los grupos de investigación en el departamento del Cauca. Contiene una sección para la exploración de datos previamente obtenidos por medio de dos sistemas de extracción para las plataformas CvLAC y GrupLAC pertenecientes a ScienTI Colombia, y para la plataforma Scopus perteneciente a Elsevier.Se integra dos secciones para el análisis y visualización de los datos provenientes de GrupLAC y Scopus. El dashboard está desarrollado para en el contexto del trabajo de grado llamado “Dashboard para el análisis y visualización bibliométrica dentro del ámbito de los grupos de investigación en el departamento del Cauca” . ',
                    'Los usuarios sugeridos son los actores del SRCTI del Cauca, pertenecientes al Ecosistema de Ciencia, Tecnología e Innovación del Cauca, los cuales se muestran a continuación:'],
                    style={
                        'color': 'black',
                        'font-size': '1.3em',
                        'text-align': 'justify'
                    }
                ),
                html.Img(src='./assets/img/srcti.png', id='options_graph',style={'width':'auto', "height":'25rem', "padding-left":'auto',"padding-right":'auto', "position":"static"}),
            ]
        )
    ]
)