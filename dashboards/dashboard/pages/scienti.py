
from dash.dependencies import Input, Output, State
from dash import  html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from index import app
import numpy as np
import plotly.graph_objects as go
from queries.queries import get_periods,get_programs,get_schedules,get_subject_options, get_grades, get_quotas, get_resume, get_st_path
from functions.sorter import sort_periods
from functions.classifier import grade_classif

# LOAD THE DIFFERENT FILES
from lib.filter_graph import sidebar_graph


data_col = {"0":"codigo_programa","1":"codigo_sede_municipio","2":"codigo_materia_estudiante","3":"codigo_plan_materia",
            "4":"codigo_materia_grupos","5":"codigo_jornada","6":"codigo_materia","7":"codigo_salon","8":"codigo_periodo",
            "9":"Parcial1","10":"Parcial2","11":"Final","12":"definitiva","13":"codigo_estado","14":"estado","15":"periodo"}
template='seaborn'
color = '#08469b'

Graficas= html.Div([
    #Header
    html.Div([
        html.H1("Análisis de la producción científica"),
    ] ,
    className='col-12',
    style={'textAlign':'center'}
    ),

    #Dropdwon options, this configuration doesn't allow to change two filters at a time
   
    #Dynamic Content
    html.Div([
        dcc.Loading(
            id="loading-2",
            children=[
            html.Div([
            #Scorecards
                html.Div([
                    html.Div([
                        html.Div(
                            html.Div([html.P("Indicador 1", style={'fontSize':'2rem'}),html.P('0',style={'fontSize':'6rem'}, id='badge-1')], className='score-card') , style={'margin':'2rem','height':'10rem'}),
                            html.Div(html.Div([html.P("Indicador 2", style={'fontSize':'2rem'}),html.P('0',style={'fontSize':'6rem'}, id='badge-2')], className='score-card') , style={'margin':'2rem','height':'10rem'}),
                            html.Div(html.Div([html.P("Indicador 3", style={'fontSize':'2rem'}),html.P('0',style={'fontSize':'6rem'}, id='badge-3')], className='score-card') , style={'margin':'2rem','height':'10rem'}),
                            html.Div(html.Div([html.P("Indicador 4", style={'fontSize':'2rem'}),html.P('0',style={'fontSize':'6rem'}, id='badge-4')], className='score-card') , style={'margin':'2rem','height':'10rem'})
                    ],className='card-score-container')
                ], className='col-graph'),
            
                #Charts
                html.Div([html.Div([html.H1("Grafica 1"),dcc.Graph(id='violin-plot',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})],className='card-graph card-body')], className='col-graph-big'),
                html.Div([html.Div([html.H1("Grafica 2"),dcc.Graph(id='pie-1',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})],className='card-graph card-body')], className='col-graph-big'),
                html.Div([html.Div([html.H1("Grafica 3 media pantalla"),dcc.Graph(id='histogram',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph_50'),
                html.Div([html.Div([html.H1("Grafica 4 pantalla completa"),dcc.Graph(id='path',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph_100'),
                html.Div([html.Div([html.H1("Grafica 5"),dcc.Graph(id='radial',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph'),
                html.Div([html.Div([html.H1("Grafica 6"),dcc.Graph(id='radial',style={'Width':'100%', "height":'100%'}, config={"displaylogo":False, "displayModeBar":False})], className='card-graph card-body')], className='col-graph'),  
            ],),            
            ],type="cube", fullscreen=False, color=color, style={'height':'100%', 'marginTop':'15rem'}
        ),
    ] , 
    className='col-6',
    style={'textAlign':'center', 'display':'flex', 'justifyContent':'space-around'}
    ),    
],
style={"color":"black"}
)
layout= html.Div([    
    html.Div([
                dbc.Col(
                    Graficas
                    )
                ],className="dash-body-graph"),
        sidebar_graph,
],
style={"color":"black"}
)


#-----------------------------------Callbacks ---------------------------------

@app.callback(
    # Output('filter-1','options'),
    # Output('filter-2','options'),
    # Output('filter-3','options'),
    Output('filters-container', 'children'),
    Output('filter-4','options'),
    Input('filter-1','value'),
    # Input('filter-2','value'),
    # Input('filter-3','value'),
    Input('filter-4','value'),
)
def get_filt_opt(sch,prog,peri,subj):
    """
    Input:
        (1) Schedule value
        (2) Program Value
        (3) Period  value
        (4) Subject Value
    Outputs:
        (1) Schedule list 
        (2) Program list
        (3) Period  list
        (4) Subject list

    Description:  The filters are updated based on the other filters
    """
    # In the database doesn't exist Day or Night values, only 1 or two.
    #So we tranform it before to send to the backend.
    if(sch=='Day'):
        sch='1'
    elif(sch=='Night'):
        sch ='2'

    #getting the data drom backend
    df_schedule = get_schedules(sch,prog,peri,subj)
    options_df = get_subject_options(sch,prog,peri,subj)
    df_period = get_periods(sch,prog,peri,subj)
    df_program = get_programs(sch,prog,peri,subj)

    df_schedule["schedule"] = df_schedule["schedule"].replace({1:'Day',2:'Night'})
    
    fil1= df_schedule["schedule"].drop_duplicates().tolist()
    fil2= df_program ["Program"].drop_duplicates().tolist()
    fil3= df_period ["Period"].drop_duplicates().tolist()
    fil4= options_df["Subject"].drop_duplicates().tolist()

    fil2.sort()
    fil4.sort()

    return  fil1, fil2, fil3, fil4

def update_filters(filter1_value):
    if filter1_value == 'opcion1':
        options_2 = [
            {'label': 'Opción 3', 'value': 'opcion3'},
            {'label': 'Opción 4', 'value': 'opcion4'}
        ]
        options_3 = [
            {'label': 'Opción 5', 'value': 'opcion5'},
            {'label': 'Opción 6', 'value': 'opcion6'}
        ]
        # options_4 = [
        #     {'label': 'Opción 7', 'value': 'opcion7'},
        #     {'label': 'Opción 8', 'value': 'opcion8'}
        # ]
    else:
        options_2 = [
            {'label': 'Opción A', 'value': 'opcionA'},
            {'label': 'Opción B', 'value': 'opcionB'}
        ]
        options_3 = [
            {'label': 'Opción C', 'value': 'opcionC'},
            {'label': 'Opción D', 'value': 'opcionD'}
        ]
        # options_4 = [
        #     {'label': 'Opción E', 'value': 'opcionE'},
        #     {'label': 'Opción F', 'value': 'opcionF'}
        # ]
        
    return html.Div([
        dcc.Dropdown(
            id='filter-2',
            options=options_2,
            placeholder="Elija segundo filtro"
        ),
        dcc.Dropdown(
            id='filter-3',
            options=options_3,
            placeholder="Elija tercer filtro"
        ),
        # dcc.Dropdown(
        #     id='filter-4',
        #     options=options_4,
        #     placeholder="Elija cuarto filtro"
        # )
    ])

@app.callback(
    Output('violin-plot','figure'),
    Output('pie-1','figure'),
    Output('histogram','figure'),
    Output('path','figure'),
    Output('radial','figure'),
    Output('badge-1','children'),
    Output('badge-2','children'),
    Output('badge-3','children'),
    Output('badge-4','children'),
    Input('reload-button','n_clicks'),
    State('filter-1','value'),
    State('filter-2','value'),
    State('filter-3','value'),
    State('filter-4','value'),
)
def magic_maker(n,sch, prog, peri, subj):

    """
    Inputs:
        (1) Reload button, this trigger the reload the content in this specific section
    State:
        (1) Schedule value
        (2) Program Value
        (3) Period  value
        (4) Subject Value
    Output:
        (1) Violin plot with the data retorned from queries
        (2) Pie Chart with the data retorned from queries
        (3) Histogram with the data retorned from queries
        (4) Parallel coordinates with the data retorned from queries
        (5) timeseries with the data retorned from queries
        (6) Total of Quotas
        (7) Average grade
        (8) Standard Deviation
        (9) Average Students for every subject
     Description : This function creates al the chartas and score cards based on the data filtered by the user  
        
    """

    if(sch=='Day'):
        sch='1'
    elif(sch=='Night'):
        sch ='2'

    #Fetching data from backend server
    df = get_grades(sch,prog,peri,subj) # Grades for every student
    df_timeline = get_quotas(sch,prog,peri,subj) # number of quotas per period
    df_parallel = get_st_path(sch,prog,peri,subj) #Every studen clasified for every grade an his result
    df_insights = get_resume(sch,prog,peri,subj) #  Data about mean, standard deviation and students per subject
    df_timeline = sort_periods(df_timeline) # this function parse period column as sorted category

    #Charts generation
    df['Grade Range']= df.apply(grade_classif, axis=1) # function that create a range from note to make an artifitial histogram based on resumed data
    df.rename(columns={'Cantidad':'qty'}, inplace=True)
    fig1 = px.line(df_timeline.sort_values(by="Period"), x="Period", y="Quotas", markers=True,template=template)
    fig2 = px.violin(df.reindex(df.index.repeat(df['qty'])), y="Grade", x="State", box=True, template=template, )
    fig3 = px.pie(df[["State","qty"]].groupby('State', as_index=False).sum(), values="qty", names="State", template=template, )
    fig4 = px.bar(df[['Grade Range','qty', 'State']].groupby(['Grade Range','State'], as_index=False).sum(), x="Grade Range", y="qty", color='State' )
    fig5 = px.parallel_categories(df_parallel.reindex(df_parallel.index.repeat(df_parallel['freq'])), dimensions=["Parcial1","Parcial2","final","definitiva",'estado'])

    #Scorecards generation
    badge_1 = '{:,}'.format(df.qty.sum())
    badge_2 = '{:,}'.format(round(np.average(df_insights['avg']),2))
    badge_3 = '{:,}'.format(round(np.average(df_insights['std']),2))
    badge_4 = '{:,}'.format(round(np.average(df_insights['avg_stud']),2))

    return fig2, fig3, fig4, fig5, fig1, badge_1, badge_2, badge_3, badge_4