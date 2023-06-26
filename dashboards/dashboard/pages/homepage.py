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
                'max-width': '50%'
            },
            children=[
                html.H3(
                    'Analizador de producción científica de investigadores',
                    style={
                        'color': 'black',
                        'text-align': 'center',
                        'font-size': '1.5em'
                    }
                ),
                html.H3(
                    'Este dashboard es una herramienta muy útil que permite presentar y analizar métricas clave,como el número de publicaciones, citas, índices de impacto, colaboraciones, etc. Permite Visualización clara de los datos, Fácil identificación de áreas de mejora, Seguimiento del progreso a lo largo del tiempo, Identificación de oportunidades de colaboración. Este dashboard es una herramienta muy útil que permite presentar y analizar métricas clave,como el número de publicaciones, citas, índices de impacto, colaboraciones, etc. Permite Visualización clara de los datos, Fácil identificación de áreas de mejora, Seguimiento del progreso a lo largo del tiempo, Identificación de oportunidades de colaboración. Este dashboard es una herramienta muy útil que permite presentar y analizar métricas clave,como el número de publicaciones, citas, índices de impacto, colaboraciones, etc. Permite Visualización clara de los datos, Fácil identificación de áreas de mejora, Seguimiento del progreso a lo largo del tiempo, Identificación de oportunidades de colaboración',
                    style={
                        'color': 'black',
                        'text-align': 'center',
                        'font-size': '1.2em',
                        'text-align': 'justify'
                    }
                )
            ]
        )
    ]
)