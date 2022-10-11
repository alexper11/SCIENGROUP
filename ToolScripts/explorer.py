import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import os

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


dire=[]
url_general="https://scienti.minciencias.gov.co/ciencia-war/busquedaGrupoXDepartamentoGrupo.do?codInst=&sglPais=COL&sgDepartamento=CA&maxRows=15&grupos_tr_=true&grupos_p_=1&grupos_mr_=117"
#url='https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000013056'
r_general=requests.get(url_general, verify=False)
soup_general=BeautifulSoup(r_general.content,'lxml')
links_total=soup_general.find_all('a', attrs={'target':'_blank'})
lista_gruplacs=[]
lista_cvlacs=[]
for a in links_total:
    url_gruplac=a['href']
    if(url_gruplac.find('https://scienti.minciencias.gov.co/gruplac/jsp/visualiza')!=-1):
        tries=3
        for i in range(tries):
            try: 
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                r = requests.get(url_gruplac, headers=headers, verify=False)
            except:
                print("Error con :",url_gruplac)
                continue
            break
        
        #for generar lista cvlacs
        soup_cvlac=BeautifulSoup(r.content,'lxml')
        links_cvlacs_all=soup_cvlac.find_all('a',attrs={'target':'_blank'})
        
        for a_c in links_cvlacs_all:
            url_cvlac=a_c['href']
            if (url_cvlac.find('https://scienti.minciencias.gov.co/cvlac/visualizador')!=-1):
                triesc=3
                for i in range(triesc):
                    try: 
                        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                        r_cvlac = requests.get(url_cvlac, headers=headers, verify=False)
                    except:
                        print("Error con :",url_cvlac)
                        continue
                    break
                #for para iterar esa lista         
                soup = BeautifulSoup(r_cvlac.content,'lxml')
                dic2={}        
                child=(soup.find('table'))   
                child=(child.find_all('tr')) 
                flag=0
                for trs in child:
                    h3s=(trs.find('td'))
                    try:
                        h3s=(h3s.find('h3'))
                    except:
                        pass
                    if h3s!=None:                
                        titulo_c=str(h3s.contents[0]).strip()
                        if titulo_c == "Productos tecnológicos":
                            print(url_cvlac)    
                            if titulo_c in lista_cvlacs:
                                pass
                            else:
                                lista_cvlacs.append(titulo_c)
                            
#print(lista_cvlacs)
#print(len(lista_cvlacs)) 