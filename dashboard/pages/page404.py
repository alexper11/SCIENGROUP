from dash import  html

#this page us showed when someona try to reach any page that doesn't exist.
layout = html.Div([    
    html.H1("La página solicitada no ha sido encontrada.")
], 
style={
    "color": "black",
    "display": "flex",
    "align-items": "center",
    "justify-content": "center",
    "height": "50vh"
})