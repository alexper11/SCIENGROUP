import dash
from dash import html , dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page


register_page(__name__, path="/")
home_image = html.Img(src = "assets/home.png", className = "home_image")

layout=  dbc.Container(
    [
        html.Div(home_image)       
        
    ]
)  