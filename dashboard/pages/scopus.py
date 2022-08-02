import dash
from dash_labs.plugins import register_page

register_page(__name__, path="/scopus")

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from lib import title, sidebar


layout = html.Div(
    [
        sidebar.sidebar,
    ]
)

