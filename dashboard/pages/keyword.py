import dash
from dash_labs.plugins import register_page

register_page(__name__, path="/keyword")

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px


layout = html.Div(
    [
        
    ]
)

