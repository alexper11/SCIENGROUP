#libraries
from tkinter.ttk import Style
import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
import os
#from callbacks import register_callbacks
import dash_html_components as html

# Recall app
from app import app
from lib import tittle_menu

#Main layout
app.layout = html.Div(
    [        
        tittle_menu.dash_header,
        dl.plugins.page_container,
        
    ])

# Call to external function to register all callbacks
#register_callbacks(app)


# This call will be used with Gunicorn server
server = app.server

# Testing server, don't use in production, host
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8052,debug=True)