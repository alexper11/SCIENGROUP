from dash import html
from dash import dcc

#Homepage layout with the cards of modules

layout = html.Div(
    style={
        'background-image': 'url(/assets/img/home.png)',
        'background-size': 'contain',
        'background-repeat': 'no-repeat',
        'background-position': 'center center',
        'background-origin': 'content-box',
        'height': '100vh'
    },
    children=[
        html.Div(
            style={
                'background-color': 'rgba(255, 255, 255, 0.93)',
                'padding': '3em',
                'border-radius': '1em',
                'margin': '5vh auto',
                'max-width': '85%'
            },
            children=[
                html.H3(
                    'Research Groups Analytics Dashboard',
                    style={
                        'color': 'black',
                        'text-align': 'center',
                        'font-size': '1.5em'
                    }
                ),
                html.P(
                    'Esta herramienta es un Dashboard para el análisis y visualización bibliométrica de la producción científica de los grupos de investigación en el departamento del Cauca. ',                    
                    style={
                        'color': 'black',
                        'font-size': '1.3em',
                        'text-align': 'justify'
                    }
                ),
                html.P(
                    'Se integra una sección llamada “Explorar datos” con el objetivo de inspeccionar los datos previamente obtenidos y preprocesados por medio de dos sistemas de extracción, uno para las plataformas CvLAC y GrupLAC pertenecientes a ScienTI Colombia, y otro para la plataforma Scopus perteneciente a Elsevier. ',                    
                    style={
                        'color': 'black',
                        'font-size': '1.3em',
                        'text-align': 'justify'
                    }
                ),
                html.P(
                    'Se integran dos secciones para el análisis y visualización de los datos provenientes de GrupLAC y Scopus. El dashboard está desarrollado dentro del marco del trabajo de grado titulado “Dashboard para el análisis y visualización bibliométrica dentro del ámbito de los grupos de investigación en el departamento del Cauca” desarrollado en la Universidad del Cauca por los estudiantes Jarby Daniel Salazar Galindez y Edison Alexander Mosquera Perdomo. El dashboard busca ser un asistente para los actores del Sistema Regional de Ciencia, Tecnología e Innovación del Cauca.',                    
                    style={
                        'color': 'black',
                        'font-size': '1.3em',
                        'text-align': 'justify'
                    }
                ),
                html.Img(src='./assets/img/srcti.png', id='srcti',style={'width':'auto', "height":'30vh', "marginLeft":'auto',"marginRight":'auto', "display":"grid"}),
            ]
        )
    ]
)