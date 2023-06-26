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
                'background-color': 'rgba(255, 255, 255, 0.8)',
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
                    'Este dashboard es una herramienta muy útil que permite presentar y analizar métricas clave, como el número de publicaciones, citas, índices de impacto, colaboraciones, etc. Permite Visualización clara de los datos, Fácil identificación de áreas de mejora, Seguimiento del progreso a lo largo del tiempo, Identificación de oportunidades de colaboración. Este dashboard es una herramienta muy útil que permite presentar y analizar métricas clave,como el número de publicaciones, citas, índices de impacto, colaboraciones, etc. Permite Visualización clara de los datos, Fácil identificación de áreas de mejora, Seguimiento del progreso a lo largo del tiempo, Identificación de oportunidades de colaboración. Este dashboard es una herramienta muy útil que permite presentar y analizar métricas clave,como el número de publicaciones, citas, índices de impacto, colaboraciones, etc. Permite Visualización clara de los datos, Fácil identificación de áreas de mejora, Seguimiento del progreso a lo largo del tiempo, Identificación de oportunidades de colaboración ',
                    'Ecosistema de Ciencia, Tecnología e Innovación del Cauca” reúnen actores del SRCTI del Cauca para aportar valor a la sociedad a partir del conocimiento'],
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