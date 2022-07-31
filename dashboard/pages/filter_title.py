import dash
from dash_labs.plugins import register_page

register_page(__name__, path="/filter_title")

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px


layout = html.Div(
    [
        
    ]
)

