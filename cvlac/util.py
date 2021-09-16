import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
  
def get_urls(url,filtro):
    dire=[]
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'lxml')
    
    url_inv = soup.find_all('a', attrs={'target':'_blank'})             
    for a in url_inv:
        url_in = a['href']
        if(url_in.find(filtro)!=-1):
            dire.append(url_in) 
    return dire

def get_gruplacList(url,filtro):
    dire=[]
    r = requests.get(url)        
    soup = BeautifulSoup(r.content,'lxml')
    div_uni = soup.find_all('div', attrs={'class':'nonblock nontext clearfix colelem'})             
    for a_uni in div_uni:                            
        if((str(a_uni.contents[0])).find(filtro.upper())!=-1):                
            div_grup=a_uni.parent.parent     
            page = pq(str(div_grup))                
            page.make_links_absolute(url)
            for a in page.find('a'):
                if 'href' in a.attrib and 'sba.minciencias.gov.co/Buscador_Grupos' in a.attrib['href']:
                    a=("".join(a.attrib['href']).replace(" ","%20"))
                    dire.append(a)
    return dire

#Es llamada desde investigador, recibe url y retorna xml
def get_lxml(url):        
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'lxml')
    return soup

def almacena(diccionario1, diccionario2):
    if list(diccionario1.keys()) not in list(diccionario2.keys()):
        temp = [item for item in diccionario1 if item not in diccionario2]
        for x in temp:
            diccionario2[x]=''
    for data in diccionario2.keys():
        diccionario1[data].append(diccionario2[data])   
    return diccionario1    