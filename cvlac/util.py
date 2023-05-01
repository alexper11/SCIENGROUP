from wsgiref import validate
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from selenium import webdriver
import pathlib
import platform
import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
############# Quitar msj alertas certificado en consola
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
###########
    
#Recibe cualquier url y retorna su DOM
def get_lxml(url):        
    tries=3
    r=''
    for i in range(tries):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get(url, headers=headers)#, verify=False)
            #r.encoding = "UTF-8"
            soup = BeautifulSoup(r.content,'lxml')
        except:
            print('request...',r)
            if i < tries - 1:
                continue
            else:
                print('Error al extraer url_lxml:',url)
                raise
        break
    return soup

def almacena(diccionario1, diccionario2):
    if list(diccionario1.keys()) not in list(diccionario2.keys()):
        temp = [item for item in diccionario1 if item not in diccionario2]
        for x in temp:
            diccionario2[x]=''
    for data in diccionario2.keys():
        diccionario1[data].append(diccionario2[data])   
    return diccionario1    

def almacena_df(df1, df2):
    df= pd.concat([df1,df2]).reset_index(drop=True) 
    return df