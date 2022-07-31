import dash
from dash_labs.plugins import register_page
# LOAD THE DIFFERENT FILES
from lib import sider_key

register_page(__name__, path="/keyword")

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px


layout = html.Div(
    [
        sider_key.sidebar_key,
    ]
)

