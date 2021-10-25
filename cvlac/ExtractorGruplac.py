import pandas as pd
import requests
from bs4 import BeautifulSoup
from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.util import get_lxml, get_gruplacList

class ExtractorGruplac(ExtractorCvlac):
    
    def __init__(self):
        super().__init__()
        self.grup_academica=pd.DataFrame(columns=['idcvlac','tipo','institucion','area','fecha','nombre'])
        self.grup_actuacion=pd.DataFrame(columns=['idcvlac','nombre'])
        self.grup_articulos=pd.DataFrame(columns=['idcvlac','autores','nombre','lugar','revista','issn','editorial','volumen','fasciculo','doi','palabras','sectores'])
        self.grup_basico=pd.DataFrame(columns=['idcvlac','categoria','nombre','nombre_citaciones','nacionalidad','sexo'])
        self.grup_complementaria=pd.DataFrame(columns=['idcvlac','tipo','institucion','area','fecha'])
        self.grup_estancias=pd.DataFrame(columns=['idcvlac','nombre','entidad','area','fecha_inicio','fecha_fin'])
        self.grup_evaluador=pd.DataFrame(columns=['idcvlac','ambito','par_evaluador','editorial','revista','institucion'])
        self.grup_identificadores=pd.DataFrame(columns=['idcvlac','nombre','url'])
        self.grup_idioma=pd.DataFrame(columns=['idcvlac','idioma','habla','escribe','lee','entiende'])
        self.grup_investiga=pd.DataFrame(columns=['idcvlac','nombre','activa'])
        self.grup_jurado=pd.DataFrame(columns=['idcvlac','nombre','titulo','tipo','lugar','programa','orientado','palabras','areas','sectores'])
        self.grup_libros=pd.DataFrame(columns=['idcvlac','autores','nombre','lugar','editorial','isbn','volumen','paginas','palabras','areas','sectores'])
        self.grup_reconocimiento=pd.DataFrame(columns=['idcvlac','nombre','fecha'])
        self.grup_redes=pd.DataFrame(columns=['idcvlac','nombre','url'])

    def get_investigadoresList(self,url):
        dire=[]
        r=''
        tries=3
        for i in range(tries):
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.content,'lxml') 
                url_inv = soup.find_all('a', attrs={'target':'_blank'})
            except:
                print(r)
                if i < tries - 1:
                    continue
                else:
                    print('Error al extraer urls')
                    raise
            break
                    
        for a in url_inv:
            url_in = a['href']
            if(url_in.find('https://scienti.minciencias.gov.co/cvlac/visualizador')!=-1):
                dire.append(url_in) 
        return dire 
    #recibe url de un gruplac
    def get_cvs(self, url_gruplac):
        
        urls=self.get_investigadoresList(url_gruplac)
        print('Extrayendo...')
        for url in urls:
            lxml_url = get_lxml(url)            
            df_basico = self.get_basico(lxml_url, url)
            df_articulos = self.get_articulo(lxml_url, url)
            df_actuacion = self.get_actuacion(lxml_url, url)
            df_idioma = self.get_idioma(lxml_url, url)
            df_investiga = self.get_investiga(lxml_url, url)
            df_reconocimiento = self.get_reconocimiento(lxml_url, url)
            df_evaluador = self.get_evaluador(lxml_url, url) 
            df_redes = self.get_redes(lxml_url, url)    
            df_identifica = self.get_redes(lxml_url, url) 
            df_libros = self.get_libro(lxml_url, url)
            df_jurado = self.get_jurado(lxml_url, url)
            df_complementaria = self.get_complementaria(lxml_url, url)
            df_estancias = self.get_estancias(lxml_url, url)
            df_academica = self.get_academica(lxml_url, url)
        #limpiar atributos
        super().__init__()
            
        return {"basico":df_basico,"articulos":df_articulos,"actuacion":df_actuacion,"idioma":df_idioma,
                "investigacion":df_investiga,"reconocimiento":df_reconocimiento,"evaluador":df_evaluador,
                "redes":df_redes,"identificadores":df_identifica,"libros":df_libros,"jurado":df_jurado,
                "complementaria":df_complementaria,"estancias":df_estancias,"academica":df_academica}
    
    def set_gruplac_attrs(self,gruplac_list):
        for gruplac in gruplac_list:
            try:
                dataframes=self.get_cvs(gruplac)
                self.grup_academica=self.grup_academica.append(dataframes['academica'])
                self.grup_actuacion=self.grup_actuacion.append(dataframes['actuacion'])
                self.grup_articulos=self.grup_articulos.append(dataframes['articulos'])
                self.grup_basico=self.grup_basico.append(dataframes['basico'])
                self.grup_complementaria=self.grup_complementaria.append(dataframes["complementaria"])
                self.grup_estancias=self.grup_estancias.append(dataframes["estancias"])
                self.grup_evaluador=self.grup_evaluador.append(dataframes["evaluador"])
                self.grup_identificadores=self.grup_identificadores.append(dataframes["identificadores"])
                self.grup_idioma=self.grup_idioma.append(dataframes["idioma"])
                self.grup_investiga=self.grup_investiga.append(dataframes["investigacion"])
                self.grup_jurado=self.grup_jurado.append(dataframes["jurado"])
                self.grup_libros=self.grup_libros.append(dataframes["libros"])
                self.grup_reconocimiento=self.grup_reconocimiento.append(dataframes["reconocimiento"])
                self.grup_redes=self.grup_redes.append(dataframes["redes"])
            except:
                print('Error estableciendo atributos del objeto')
                raise
        
        #PREPROCESAMIENTO
        #Limpiar duplicados por el titulos del producto

            
    def __del__(self):
        print('ExtractorGruplac Object Destroyed')