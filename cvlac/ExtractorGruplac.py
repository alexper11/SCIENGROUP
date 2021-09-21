from re import A
from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.util import get_lxml, get_urls, get_gruplacList
import pandas as pd

class ExtractorGruplac(ExtractorCvlac):
    
    def __init__(self):
        super().__init__()
        self.basico={}
        
    #recibe url de un gruplac
    def get_cvs(self,url_gruplac): 
        filtro= "https://scienti.minciencias.gov.co/cvlac/visualizador/"
        urls=get_urls(url_gruplac, filtro)
        for url in urls:
            lxml_url = get_lxml(url)
            
            df_basico = self.get_basico(lxml_url, url)
            df_articulos = self.get_articulo(lxml_url, url)
            df_actuacion = self.get_actuacion(lxml_url, url)
            df_idioma = self.get_idioma(lxml_url, url)
            df_investiga = self.get_investiga(lxml_url, url)
            df_reconocimiento = self.get_reconocimiento(lxml_url, url)
            df_evaluador = self.get_evaluador(lxml_url, url) 
            df_redes = self.get_redes(lxml_url, url,'redes_identificadores')    #Corregir metodo
            df_identifica = self.get_redes(lxml_url, url,'red_identificadores') #Corregir metodo
            df_libros = self.get_libro(lxml_url, url)
            df_jurado = self.get_jurado(lxml_url, url)
            df_complementaria = self.get_complementaria(lxml_url, url)
            df_estancias = self.get_estancias(lxml_url, url)
            df_academica = self.get_academica(lxml_url, url)
        
        return {"basico":df_basico,"articulos":df_articulos,"actuacion":df_actuacion,"idioma":df_idioma,
                "investigacion":df_investiga,"reconocimiento":df_reconocimiento,"evaluador":df_evaluador,
                "redes":df_redes,"identificadores":df_identifica,"libros":df_libros,"jurado":df_jurado,
                "complementaria":df_complementaria,"estancias":df_estancias,"academica":df_academica}
        


#-- Extrae los grupalc de una universidad
"""
universidad=(input("Digite nombre de la Institución:"))
url_uni="https://sba.minciencias.gov.co/Buscador_Instituciones/busqueda?q="+(universidad.replace(" ","+"))
url_grup_uni=get_gruplacList(url_uni,universidad)#  lista de todos los gruplac de la institucion (links externos)
print(url_grup_uni)
"""


#para pruebas se usa el gruplac de telematica (unicauca)
"""
url_prueba="https://sba.minciencias.gov.co/tomcat/Buscador_Grupos/busqueda?q=GRUPO%20DE%20INGENIERIA%20TELEMATICA&pagenum=1&start=0&type=load&inmeta=COD_ID_GRUPO_s!COL0008586&lang=es"
filtro_gruplac= "https://scienti.minciencias.gov.co/gruplac/jsp/visualiza"
url_gruplac=get_urls(url_prueba, filtro_gruplac)
url_gruplac= "".join(url_gruplac)
#---- extrae investigadores
filtro_investiga= "https://scienti.minciencias.gov.co/cvlac/visualizador/"
urls=get_urls(url_gruplac, filtro_investiga)

"""

'''
df_basico.to_csv('cvlac/Docs_extraidos/basico.csv',index=False)
df_articulos.to_csv('cvlac/Docs_extraidos/articulos.csv',index=False)
df_actuacion.to_csv('cvlac/Docs_extraidos/actuacion.csv',index=False)
df_investiga.to_csv('cvlac/Docs_extraidos/investigacion.csv',index=False)
df_reconocimiento.to_csv('cvlac/Docs_extraidos/reconocimiento.csv',index=False)
df_evaluador.to_csv('cvlac/Docs_extraidos/evaluador.csv',index=False)
df_redes.to_csv('cvlac/Docs_extraidos/redes.csv',index=False)
df_identifica.to_csv('cvlac/Docs_extraidos/identificadores.csv',index=False)
df_idioma.to_csv('cvlac/Docs_extraidos/idioma.csv',index=False)
df_libros.to_csv('cvlac/Docs_extraidos/libros.csv',index=False)
df_jurado.to_csv('cvlac/Docs_extraidos/jurados.csv',index=False)
df_complementaria.to_csv('cvlac/Docs_extraidos/complementaria.csv',index=False)
df_estancias.to_csv('cvlac/Docs_extraidos/estancias.csv',index=False)
df_academica.to_csv('cvlac/Docs_extraidos/academica.csv',index=False)
'''
        
        
        
        