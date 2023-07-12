import requests
import pandas as pd
import json
#This module make all the queries to the backend server
#be careful, the backend server ONLY recieve petitions from 
#frontend server, if you tray to scarp data, the server didn't respond

ip='http://3.90.183.244'

def get_subject_options(sch,prog,peri,subj):
    """
    Input:
        (1) Schedule selected - String
        (2) Program Selected - String
        (3) Period Selected - String
        (4) Subject Selected - String
    Output:
        (1) Dataframe with the response from server
    Description:
    Gets a list of subjects based on options
    
    """

    raw_response =requests.get(ip+'/subjects?sch={}&prog={}&peri={}&subj={}'.format(sch,prog,peri,subj))
    response= pd.DataFrame(json.loads(raw_response.text))
    return response

def run_arima(subject, sch):
    """
    Input:
        (1) Schedule selected - String
        (2) Program Selected - String
        (3) Period Selected - String
        (4) Subject Selected - String
    Output:
        (1) Dataframe with the response from server
    Description:
    Executes the arima model in the backend server
    
    """

    if(subject):
        timeline = requests.get(ip+'/timeline_model?subject='+subject+'&sch='+sch)
    else:
        timeline= requests.get(ip+'/timeline_model?sch='+sch)

    timeline = pd.DataFrame(json.loads( timeline.text))
    
    return timeline

def get_schedules(sch,prog,peri,subj):
    """
    Input:
        (1) Schedule selected - String
        (2) Program Selected - String
        (3) Period Selected - String
        (4) Subject Selected - String
    Output:
        (1) Dataframe with the response from server
    Description:
    Gets a list of schedules based on options
    
    """

    schedule= requests.get(ip+'/jorn?sch={}&prog={}&peri={}&subj={}'.format(sch,prog,peri,subj))
    df_schedule = pd.DataFrame(json.loads( schedule.text))
    return df_schedule
 
def get_periods(sch,prog,peri,subj):
    """
    Input:
        (1) Schedule selected - String
        (2) Program Selected - String
        (3) Period Selected - String
        (4) Subject Selected - String
    Output:
        (1) Dataframe with the response from server
    Description:
    Gets a list of periods based on options
    
    """

    period= requests.get(ip+'/period?sch={}&prog={}&peri={}&subj={}'.format(sch,prog,peri,subj))
    df_period = pd.DataFrame(json.loads( period.text))
    return df_period

def get_programs(sch,prog,peri,subj):
    """
    Input:
        (1) Schedule selected - String
        (2) Program Selected - String
        (3) Period Selected - String
        (4) Subject Selected - String
    Output:
        (1) Dataframe with the response from server
    Description:
    Gets a list of programs based on options
    
    """

    program= requests.get(ip+'/program?sch={}&prog={}&peri={}&subj={}'.format(sch,prog,peri,subj))
    df_program = pd.DataFrame(json.loads( program.text))
    return df_program

def get_grades(sch,prog,peri,subj):
    """
    Input:
        (1) Schedule selected - String
        (2) Program Selected - String
        (3) Period Selected - String
        (4) Subject Selected - String
    Output:
        (1) Dataframe with the response from server
    Description:
    Gets a all the grades based on options
    
    """

    x= requests.get(ip+'/filtered?sch={}&prog={}&peri={}&subj={}'.format(sch,prog,peri,subj))
    df = pd.DataFrame(json.loads( x.text))
    df.rename(columns={"0":"Grade","1":"State","2":"Cantidad"}, inplace=True)
    return df

def get_quotas(sch,prog,peri,subj):
    """
    Input:
        (1) Schedule selected - String
        (2) Program Selected - String
        (3) Period Selected - String
        (4) Subject Selected - String
    Output:
        (1) Dataframe with the response from server
    Descriotion
    Gets a table with periods and number of quotas based on options
    
    """
    timeline= requests.get(ip+'/timeline?sch={}&prog={}&peri={}&subj={}'.format(sch,prog,peri,subj))
    df_timeline = pd.DataFrame(json.loads( timeline.text))
    return df_timeline

def get_st_path(sch,prog,peri,subj):
    """
    Input:
        (1) Schedule selected - String
        (2) Program Selected - String
        (3) Period Selected - String
        (4) Subject Selected - String
    Output:
        (1) Dataframe with the response from server

    Description
    Gets a table with grades classified  and number of quotas based on options
    
    """
    parallel= requests.get(ip+'/groups?sch={}&prog={}&peri={}&subj={}'.format(sch,prog,peri,subj))
    df_parallel = pd.DataFrame(json.loads( parallel.text))
    return df_parallel

def get_resume(sch,prog,peri,subj):
    """
    Input:
        (1) Schedule selected - String
        (2) Program Selected - String
        (3) Period Selected - String
        (4) Subject Selected - String
    Output:
        (1) Dataframe with the response from server

    Description
    Gets a some data like average, std and count per subject for the desired filters.
    """
    insights= requests.get(ip+'/insights?sch={}&prog={}&peri={}&subj={}'.format(sch,prog,peri,subj))
    df_insights = pd.DataFrame(json.loads( insights.text))
    return df_insights