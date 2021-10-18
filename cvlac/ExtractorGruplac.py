#from re import A
from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.util import get_lxml, get_urls, get_gruplacList
import pandas as pd

class ExtractorGruplac(ExtractorCvlac):
    
    def __init__(self):
        super().__init__()
        self.basico={}        
        
    #recibe url de un gruplac
    """
    def get_cvs(self, url_gruplac):
        filtro= "https://scienti.minciencias.gov.co/cvlac/visualizador/"
        urls=get_urls(url_gruplac, filtro)
        print(urls)
        for url in urls:
            lxml_url = get_lxml(url)            
            '''       
            df_basico = self.get_basico(lxml_url, url)
            df_articulos = self.get_articulo(lxml_url, url)
            df_actuacion = self.get_actuacion(lxml_url, url)
            df_idioma = self.get_idioma(lxml_url, url)
            df_investiga = self.get_investiga(lxml_url, url)
            df_reconocimiento = self.get_reconocimiento(lxml_url, url)
            df_evaluador = self.get_evaluador(lxml_url, url) 
            df_redes = self.get_redes(lxml_url, url,'redes_identificadoes')    #Corregir metodo
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
        """  
    def get_cvs(self, url_uni,universidad):
        url_grup_uni=get_gruplacList(url_uni,universidad)#  lista de todos los gruplac de la institucion (links externos)
        #print(url_grup_uni)
        import pandas as pd
        df33 = pd.DataFrame(url_grup_uni, columns=["colummn"])
        df33.to_csv('list.csv', index=False)
        
        for url_prueba in url_grup_uni:
            filtro_gruplac= "https://scienti.minciencias.gov.co/gruplac/jsp/visualiza"
            url_gruplac=get_urls(url_prueba, filtro_gruplac)
            url_gruplac= "".join(url_gruplac)
            print(url_gruplac)
            #----extra investigadores de un gruplac
            filtro_investiga= "https://scienti.minciencias.gov.co/cvlac/visualizador/"
            urls=get_urls(url_gruplac, filtro_investiga)
            for url in urls:
                lxml_url = get_lxml(url)
                df_prueba = self.get_redes(lxml_url, url,'redes_identificadoes')
                """
                df_basico = self.get_basico(lxml_url, url)
                df_articulos = self.get_articulo(lxml_url, url)
                df_actuacion = self.get_actuacion(lxml_url, url)
                df_idioma = self.get_idioma(lxml_url, url)
                df_investiga = self.get_investiga(lxml_url, url)
                df_reconocimiento = self.get_reconocimiento(lxml_url, url)
                df_evaluador = self.get_evaluador(lxml_url, url) 
                df_redes = self.get_redes(lxml_url, url,'redes_identificadoes') 
                df_identifica = self.get_redes(lxml_url, url,'red_identificadores')
                df_libros = self.get_libro(lxml_url, url)
                df_jurado = self.get_jurado(lxml_url, url)
                df_complementaria = self.get_complementaria(lxml_url, url)
                df_estancias = self.get_estancias(lxml_url, url)
                df_academica = self.get_academica(lxml_url, url)
                """
        return df_prueba
