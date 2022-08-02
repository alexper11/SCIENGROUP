# Basics Requirements
import pathlib
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

# Dash Bootstrap Components
import dash_bootstrap_components as dbc
logo = html.Img(src = "assets/escudo_Unicauca.png", className = "logo")

#Top menu, items get from all pages registered with plugin.pages
title = dbc.NavbarSimple([
            html.Div(
                dbc.Row(
                    (                
                        dbc.Col(dbc.NavItem(dbc.NavLink("Inicio", href="/")),),
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
        dbc.Col([logo,title]),
        className="g-0"       
    ),
    dbc.Row(
        dbc.Col(html.P(" "),className="header_red"),
        className="g-0"
    ),    
    ],               
    className="dash-title",
    id="title",
)
