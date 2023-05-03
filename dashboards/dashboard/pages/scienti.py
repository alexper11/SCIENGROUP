from dash.dependencies import Input, Output, State
from dash import dash_table, html
import dash_core_components as dcc
import plotly.express as px
from index import app
import pandas as pd
from queries.queries import get_subject_options, run_arima
color = '#08469b'


layout= html.Div([
    #Header 
    html.Div(
        [
            html.H1("Occupancy prediction", className='title' ),
            html.P('Please select the subject to make a prediction about the next period.')
        ] ,  style={'textAlign':'center'}
    ),

    #Filters
    html.Div(
        [
            dcc.Loading([html.P('Choose the Schedule: '),dcc.RadioItems(["Day","Night"],  id='sub_drop_1', inline=True, value="Day")],parent_className='dropdown',  className='dropdown-loading', color=color, type='dot'),
            dcc.Loading(dcc.Dropdown([], placeholder="Choose Subject", id='sub_drop'),parent_className='dropdown', className='dropdown-loading',color=color, type='dot')
        ] ,  style={'textAlign':'center', 'display':'flex', 'justifyContent':'space-around'}
    ),

    #Dynamic Content
    dcc.Loading(
                    id="loading-7",
                    children=[
                        html.Div(
                        dcc.Graph(id='time-line',  config={"displaylogo":False, "displayModeBar":False})
                        , className="card"),
                        html.Div([],id='forecast-table'),
                        dcc.Download(id="download-dataframe-csv_fore"),
                        html.Button("Download  table", id="btn-download-csv-alert_fore", style={'backgroundColor':"#08469b", 'color':'white'}),
                         html.A([
            html.Img(src='/assets/img/reload.png',className='whatsappIcon', )
            ], id='reload-button_early_time'),
                    ],
                    type="cube", fullscreen=True,color='#08469b', style={'height':'100%'}
                ), 
    dcc.Store(id='store-table')
   
    
    

    
], className='col-1',style={"color":"black", 'textAlign':'center'})

#-----------------------------------Callbacks ---------------------------------


@app.callback(
    Output('sub_drop','options'),
    Input('reload-button_early_time','n_clicks'),
    Input('sub_drop','value'),
    Input('sub_drop_1','value'),
)
def get_filt_opt(n,subj,sch):

    """
    Inputs:
        (1) Reload button clicks to launch a reload
        (2) Subject value - Dropdown
        (3) Schedule value - Dropdown
    Outputs:
        (1) subjects Dropdown List  based on Schedule

    Description:
        Every time that the user click on reload or change any option,
        the option list will update to avoid to make a disjoint query.
    """
    # In the database doesn't exist Day or Night values, only 1 or two.
    #So we tranform it before to send to the backend.
    if(sch=='Day'):
        sch='1'
    elif(sch=='Night'):
        sch ='2'
    else:
        sch='None'


    options_df= get_subject_options(sch,'%','%',subj)

    fil2= options_df["Subject"].drop_duplicates().tolist()
    fil2.sort()
    return  fil2

@app.callback(  Output('time-line', 'figure'),
                Output('forecast-table', 'children'),
                Output('store-table','data'),
                Input('reload-button_early_time','n_clicks'),
                State('sub_drop', 'value'),
                State('sub_drop_1', 'value'),
                )
def initial_state(n, subject,sch):

    """
    Inputs:
        (1) Reload button clicks to launch a reload
    State:
        (1) Subject value - Dropdown
        (2) Schedule value - Dropdown
    Outputs:
        (1) subjects Dropdown List  based on Schedule

    Description:
        (1) Time serie chart
        (2) Dash table with the data
        (3) Dataframe to be saved in the user session
    """

    if(sch=='Day'):
        sch='1'
    elif(sch=='Night'):
        sch ='2'
    else:
        sch='None'

    #Here the data is send to backend server to run the model
    data_time = run_arima(subject, sch)

    
    #Creating the chart  with the  new data
    fig=px.line(data_time,x='Period',y="Quotas", color='Type', template='seaborn')

    # customize font and legend orientation & position
    fig.update_layout( 
    legend=dict(
        title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
    )
)
    #The table is created and to make an efect of continuos line in the prediction
    #we create an artificial row pf prediction in the last real value, with the same 
    #value, and here it is removed for the data an table
    data_time = data_time[~((data_time['Period']=='I PERIODO DE 2022')&(data_time['Type']=="Prediction"))]
    table = dash_table.DataTable(
                data_time.to_dict('records'),
                [{'name': i, 'id': i} for i in data_time.columns],
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
                'if': {'column_id': 'Type', 'filter_query':'{Type} =Historical' },
                'backgroundColor': '#a2d2ff',
            },
            {
                'if': {'column_id': 'Type', 'filter_query':'{Type} =Prediction' },
                'backgroundColor': '#d4e09b',
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



    return fig, table, data_time.to_dict()

   
# Allow to download the table with the prediction
@app.callback(
    Output("download-dataframe-csv_fore", "data"),
    Input("btn-download-csv-alert_fore", "n_clicks"),
    State("store-table", "data"),
    prevent_initial_call=True)
def download_data_forec(n_clicks, data):
    """
    Input:
        (1) Click event, to save the table as csv.
    State:
        (1) Data saved in the session
    Output:
        (1): Component that qownload the table
    """
    temp_df = pd.DataFrame(data)
    return dcc.send_data_frame(temp_df.to_csv, "arima_forecast.csv")