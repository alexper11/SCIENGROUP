from wsgiref import validate
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from selenium import webdriver
import pathlib
import platform
import time
import pandas as pd
############# Quitar msj alertas certificado en consola
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
###########

#Recibe nombre de una institución y retorna lista de urls de cada perfil de los gruplacs
#obsoleta
def get_gruplacList(institucion):
    dire=[]
    linkinsti=str(institucion).replace(' ','+')
    url='https://sba.minciencias.gov.co/Buscador_Instituciones/BuscadorIFindIt/busqueda?q='+linkinsti+'&pagenum=1&start=0&type=load&lang=es&idss=KybEn3DTvayjMVm'
    tries=3
    
    if platform.system()=='Windows': 
        current_path=str(pathlib.Path().resolve())+"\cvlac\WebDriver\chromedriver.exe" 
    elif platform.system()=='Linux': 
        current_path=str(pathlib.Path().resolve())+"/cvlac/WebDriver/chromedriver"   
    print(current_path) 
    
    for i in range(tries):
        try:
            #CORREGIR PATH
            
            driver = webdriver.Chrome(executable_path=current_path)
            driver.get(url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            a_unis = soup.find_all('a', attrs={'class':'link_res fontColor titlesSized'})            
        except:
            if i < tries - 1:
                continue
            else:
                print('Error al extraer perfiles gruplac')
                raise
        break    
    for a_uni in a_unis:                           
        if((str(a_uni.contents[0])).find(institucion.upper())!=-1):                
            div_grup=a_uni.findParents('table')[0]    
            page = pq(str(div_grup))                
            page.make_links_absolute(url)
            for a in page.find('a'):
                if 'href' in a.attrib and 'sba.minciencias.gov.co/Buscador_Grupos' in a.attrib['href']:
                    aj=a.attrib['href']
                    resp=''
                    for j in range(tries):
                        try:                            
                            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                            resp = requests.get(aj, headers=headers)               
                            soup2 = BeautifulSoup(resp.content,'lxml')  
                            link_clear = soup2.find_all('a', attrs={'class':'link_res fontColor titlesSized'}) 
                        except:
                            if j < tries - 1:
                                continue
                            else:
                                print('Error al extraer perfiles gruplac')
                                raise
                        break
                    
                    for link in link_clear:                        
                        url_in = link['href'].replace(" ","%20").replace("-"," ")
                        print(url_in)
                        dire.append(url_in)
                        #if(url_in.find('https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/')!=-1):
                            #dire.append(url_in)
    return dire
    
#Recibe cualquier url y retorna su DOM
def get_lxml(url):        
    tries=3
    r=''
    for i in range(tries):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get(url, headers=headers, verify=False)
            #r.encoding = "UTF-8"
            soup = BeautifulSoup(r.content,'lxml')
        except:
            print(r)
            if i < tries - 1:
                continue
            else:
                print('Error al extraer url_lxml')
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