import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url_general="https://scienti.minciencias.gov.co/ciencia-war/busquedaGrupoXDepartamentoGrupo.do?codInst=&sglPais=COL&sgDepartamento=CA&maxRows=15&grupos_tr_=true&grupos_p_=1&grupos_mr_=118"

dire=[]
r_general=requests.get(url_general, verify=False)
soup_general=BeautifulSoup(r_general.content,'lxml')
links_total=soup_general.find_all('a', attrs={'target':'_blank'})
count=0
for a in links_total:
    url_gruplac=a['href']
    if(url_gruplac.find('https://scienti.minciencias.gov.co/gruplac/jsp/visualiza')!=-1):
        tries=3
        for i in range(tries):
            try: 
                headers = {'ruplac, headUser-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                r = requests.get(url_gruplac, headers=headers, verify=False)
            except:
                print("Error con :",url_gruplac)
                continue
            break        
        soup=BeautifulSoup(r.content,'lxml')
       
        child=(soup.find_all('table'))
        for table in child:
            trs=table.find_all('tr')
            titulo=trs[0].find('td').text.strip()
            if (len(trs) > 1) and (titulo=='Poblaciones mejoradas de razas pecuarias'):
                print(url_gruplac)
                count=count+1
print('count : ',count)