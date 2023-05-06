import base64
import io
import pandas as pd
from dash import dash_table, html
import requests
import dash_core_components as dcc
import json
import plotly.express as px

ip='http://3.90.183.244'

def read_archive():
    df = pd.read_csv('./assets/data/archivo_prueba.csv')
    return df

def data_validation(df):
    """
    This function receive the raw dataframe, and 
    check if it cointains the correct information,
    and it try to set the right format
    
    inputs:
        df= dataframe
        model= the model that define the columns and format
    output:
        df= dataframe with the cleaned data to send towards the backend

    """
    valid_columns=['Student_id','Parcial1','Parcial2']

    try:   

        if len(list(df.columns)) != 3:
            return "Error - your file must have 3 columns"

        untrained_columns = [column for column in list(df.columns) if column not in valid_columns]
        if len(untrained_columns) >0:
            return "There are some invalid columns, please check the template, it must contain some specifics column names."
    except:
        return "Please check your file, it can't be processed"

    
    try:
        df["Student_id"]= df["Student_id"].astype(str).replace(",",".")
        df["Student_id"]= df["Student_id"].astype(int)
        df["Parcial1"]= df["Parcial1"].astype(str).replace(",",".")
        df["Parcial1"]= df["Parcial1"].astype(float)
        df["Parcial2"]= df["Parcial2"].astype(str).replace(",",".")
        df["Parcial2"]= df["Parcial2"].astype(float)
        df.fillna(0,inplace=True)
    except:
        return "Please check your data types, it can't be processed, any column couldn't be parsed - Student_id (int), Parcial1(float), Parcial2(float) "
    
    return df


def data_prediction(df):
    """
    Send the dataframe to the backend, the endpoint depends on model
    input:
    df= dataframe to predict
    model= what model to use
    output:
    df= dataframe with the prediction
    """
    #parse the df to json format
    payload=df.to_json() 
    r = requests.post(ip+'/eaa', data=payload)
    return pd.read_json(json.loads(r.text))


def parse_contents(contents, filename, model):


    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return [html.Div([
            'There was an error processing this  file.'
        ]),pd.DataFrame()]
    #if the data frame contains any nan value it is filled with a zero

    df = data_validation(df)

    if(isinstance(df,str) ):
        return[html.H1(df), pd.DataFrame()]
    
    df = data_prediction(df)

 
    return [html.Div([
        
            dcc.Graph(figure=px.pie(df[["Estado","Student_id"]].groupby(["Estado"], as_index=False).count(), values="Student_id", 
                                names="Estado"), id="fig_prop", config={"displaylogo":False, "displayModeBar":False}),
            html.H1("Failed Students", style={"textAlign":"center", "fontSize":"3rem"}),  # horizontal line
            dash_table.DataTable(
                df[df["Estado"]=="Reprobado"].to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns],
                style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
                    } for c in ['Date', 'Region']
                ],
                style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'light blue',
            },
            {
                'if': {'column_id': 'Estado'},
                'backgroundColor': '#e56b6f',
            }
        ],
        style_cell={'textAlign': 'center'},
        filter_action="native",
        page_action="native",
            page_current= 0,
            page_size= 20,

            style_as_list_view=True,
            style_header={
            'backgroundColor': '#08469b',
            'color':'white',
            'fontWeight': 'bold'
        }
            ),

            html.Hr(),  # horizontal line
            html.Button("Download table", id="btn-download-table-alert", style={'backgroundColor':"#08469b", 'color':'white'}),
            html.H4("*If you want to review all the information, you can to download this table as csv.", style={ "fontSize":"2rem", "margin":"0"}),
            dcc.Download(id="download-dataframe-table"),
            dcc.Upload(id='upload_tool_early', style={'display':'None'})
                ], style={'width':'90%','padding':'2rem'}), df]

   