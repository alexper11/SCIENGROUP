#libraries
from tkinter.ttk import Style
import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
import os
#from callbacks import register_callbacks
import dash_html_components as html
"""
request_path_prefix = None

#only for workspace in dash
workspace_user = os.getenv('JUPYTERHUB_USER')  # Get dash Workspace user name
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'
"""
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
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=True)