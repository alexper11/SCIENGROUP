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

logo = html.Img(src = "assets/escudo_Unicauca.png", className = "logo")

#Top menu, items get from all pages registered with plugin.pages

navbar = dbc.NavbarSimple([
    html.Div(
        dbc.Row(
            (                
                dbc.Col(dbc.NavItem(dbc.NavLink( "Inicio", href="/")),),
                dbc.Col(dbc.NavItem(dbc.NavLink("Cvlac", href="/cvlac")),),
                dbc.Col(dbc.NavItem(dbc.NavLink("Scopus", href="/scopus")),),
                dbc.Col(
                    dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem("Keyword", href="/keyword"),
                        dbc.DropdownMenuItem("Titulo", href="/filter_title")
                        #dbc.DropdownMenuItem(page["name"], href=page["path"])
                        #for page in dash.page_registry.values()
                        #if page["module"] != "pages.not_found_404"
                    ],
                    nav=True,
                    label="Filtros",
                ),
                ),                          
            )
        )
        
    ),        
    ],
    brand="Dashboard Unicauca",
    color="#082066",
    dark=True,
    className="mb-2",         
)
dash_header=html.Header([
    dbc.Row(
        dbc.Col([logo,navbar]),
        className="g-0"       
    ),
    dbc.Row(
        dbc.Col(html.P(" "),className="header_red"),
        className="g-0"
    ),    
],
)

#Main layout
app.layout = dbc.Container(
    [        
        html.Div([
            dbc.Row(
                dbc.Col(dash_header,className="header")
            ),
            dbc.Row(
                dbc.Col(dl.plugins.page_container,className="container")
            )
        ])
        
    ],
    className="dbc",
    fluid=True,
)

# Call to external function to register all callbacks
#register_callbacks(app)


# This call will be used with Gunicorn server
server = app.server

# Testing server, don't use in production, host
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=True)