import pandas as pd
from cvlac.util import almacena
import re

class ExtractorCvlac():
    
    def __init__(self):
        self.dic_academica={'idcvlac':[],'tipo':[],'institucion':[],'area':[],'fecha':[],'nombre':[]}
        self.actuacion={'idcvlac':[],'nombre':[]}
        self.articulos={'IDCVLAC':[],'Autores':[],'Nombre':[],'En':[],'Revista':[],'ISSN:':[],'ed:':[],'v.':[],'fasc.':[], 'p.':[],'fecha.':[],' DOI: ':[], 'Palabras: ':[], 'Sectores: ':[]}
        self.dic={'IDCVLAC':[],'Categoría':[],'Nombre':[],'Nombre en citaciones':[],'Nacionalidad':[],'Sexo':[]}
        self.dic_complementaria={'idcvlac':[],'tipo':[],'institucion':[],'area':[],'fecha':[]}
        self.dic_estancias={'idcvlac':[],'nombre':[],'entidad':[],'area':[],'fecha_inicio':[],'fecha_fin':[]}
        self.dic_evaluador={'IDCVLAC':[],'Ámbito: ':[],'Par evaluador de: ':[],'Editorial: ':[],'Revista: ':[],'Institución: ':[]}
        self.dic_idioma={'IDCVLAC':[],'Idioma':[],'Habla':[],'Escribe':[],'Lee':[],'Entiende':[]}
        self.dic_investiga={'IDCVLAC':[],'Nombre':[],'Activa':[]}
        self.dic_jurado={'IDCVLAC':[],'Nombre':[],'Titulo: ':[],'Tipo de trabajo presentado: ':[],'en: ':[],'programa académico':[],'Nombre del orientado: ':[],'Palabras: ':[],'Areas: ':[],'Sectores: ':[]}
        self.libros={'IDCVLAC':[],'Autores':[],'Nombre':[],'En':[],'Editorial':[],'ISBN:':[],'v. ':[],'pags.':[], 'Palabras: ':[], 'Areas: ':[], 'Sectores: ':[]}
        self.dic_reconocimiento={'idcvlac':[],'nombre':[],'fecha':[]}
        self.redes={'IDCVLAC':[],'Nombre':[],'Url':[]}
    
    def get_academica(self, soup, url):
        dic_aux={}        
        b_academicas=(soup.find('a', attrs={'name':'formacion_acad'}).parent).find_all('b')
        list=['tipo', 'institucion', 'area', 'fecha', 'nombre']
        for td_academi in b_academicas:
            info=td_academi.parent
            td_text_clear=re.sub('<b>|<td>|</td>','',(" ".join((str(info)).split())))
            td_text_clear=td_text_clear.replace('&amp;','&')                      
            list_datos=(re.split('<br/>|</b>',td_text_clear))        
            x=0               
            for datos in list_datos:
                dic_aux['idcvlac'] = url[(url.find('='))+1:]
                dic_aux[str(list[x])]=("".join(datos)).strip()                         
                x=x+1
            self.dic_academica = almacena(self.dic_academica,dic_aux)
            dic_aux={}
        df_academica= pd.DataFrame(self.dic_academica)
        df_academica = df_academica.rename_axis('id').reset_index()  
        return df_academica 
    
    def get_actuacion(self, soup, url):
        actuacion_individual={} 
        li_actuacion = (soup.find('a', attrs={'name':'otra_info_personal'}).parent).find_all('li')
        for li_actuacion in li_actuacion:
            li_act_text = " ".join((li_actuacion.text).split())            
            actuacion_individual['idcvlac'] = url[(url.find('=') )+1:]
            actuacion_individual['nombre'] = li_act_text            
            self.actuacion = almacena(self.actuacion,actuacion_individual) 
            actuacion_individual={}        
        df_actuacion = pd.DataFrame(self.actuacion)
        df_actuacion = df_actuacion.reset_index(drop=True)  
        return df_actuacion
    
    def get_articulo(self, soup, url):
        art_individual={}
        blocks_arts = (soup.find('a', attrs={'name':'articulos'}).parent).find_all('blockquote')
        for block_art in blocks_arts:
            quote_text_clear=re.sub('http://dx.doi.org/|http://doi.org/|https://doi.org/|<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_art)).split())))
            quote_text_clear=quote_text_clear.replace('&amp;','&')            
            list_datos=(re.split('<i>|</i>|</b>|<b>',quote_text_clear))
            list_datos.pop(0)
            bloque_string=re.sub('http://dx.doi.org/|https://doi.org/|https://doi.org/|<blockquote>|</blockquote>','',(" ".join((str(block_art)).split()))) 
            bloque_string=bloque_string.replace('&amp;','&')   
            fblock=bloque_string.find("<i>")
            list_string=(re.split('<br/>|, "|" . En:',bloque_string[:fblock]))        
            x=0
            informacion=['Autores','Nombre','En','Revista']               
            for dato in list_string:            
                art_individual['IDCVLAC'] = url[(url.find('='))+1:]
                art_individual[str(informacion[x])]=("".join(dato)).strip()                                      
                x=x+1
            for dato in list_datos:                            
                for key in self.articulos:                                                              
                    if(key == dato):
                        if(dato=="fasc."):
                            list_fasc=(re.split('p.| ,',list_datos[list_datos.index(dato)+1]))  
                            art_individual['fasc.']=list_fasc[0]                        
                            art_individual['p.']=list_fasc[1]
                            art_individual['fecha.']=list_fasc[2].replace(',','')
                        else:
                            art_individual[dato]=(list_datos[list_datos.index(dato)+1]).strip()                                            
            self.articulos= almacena(self.articulos,art_individual)        
            art_individual={}        
        df_articulos = pd.DataFrame(self.articulos)    
        df_articulos.columns = ['idcvlac','autores','nombre','lugar','revista','issn','editorial','volumen','fasciculo', 'paginas', 'fecha', 'doi', 'palabras', 'sectores']
        df_articulos = df_articulos.rename_axis('id').reset_index()  
        return df_articulos
    
    def get_basico(self, soup, url):
        dic2={}         
        table = soup.find('a', attrs={'name':'datos_generales'}).parent
        rows = table.find_all('tr')

        for row in  rows:            
            fid = url.find('=')
            dic2['IDCVLAC'] = url[fid+1:]
            if len(row.select('td')) == 2:
                cells = row.findChildren('td')
                dic2[cells[0].string]= " ".join(cells[1].string.split())              
        self.dic = almacena(self.dic,dic2) 
        dic2={}
        df = pd.DataFrame(self.dic)
        df.columns = ['idcvlac','categoria','nombre','citaciones','nacionalidad','sexo']
        df = df.rename_axis('id').reset_index()
        return df
    
    def get_complementaria(self, soup, url):
        dic_aux={}        
        b_compl=(soup.find('a', attrs={'name':'formacion_comp'}).parent).find_all('b')
        list=['tipo', 'institucion', 'area', 'fecha']
        for td_compl in b_compl:
            info=td_compl.parent
            td_text_clear=re.sub('<b>|<td>|</td>','',(" ".join((str(info)).split())))
            td_text_clear=td_text_clear.replace('&amp;','&')                      
            list_datos=(re.split('<br/>|</b>',td_text_clear))
            list_datos.pop(4)
            x=0               
            for datos in list_datos:
                dic_aux['idcvlac'] = url[(url.find('='))+1:]
                dic_aux[str(list[x])]=("".join(datos)).strip()                            
                x=x+1
            self.dic_complementaria = almacena(self.dic_complementaria,dic_aux)
            dic_aux={}
        df_complementaria= pd.DataFrame(self.dic_complementaria)
        df_complementaria = df_complementaria.rename_axis('id').reset_index()    
        return df_complementaria
    
    def get_estancias(self, soup, url):
        dic_aux={}        
        b_estancias=(soup.find('a', attrs={'name':'estancias_posdoctorales'}).parent).find_all('b')
        list=['nombre', 'entidad', 'area', 'fecha_inicio', 'fecha_fin']
        for td_estancia in b_estancias:
            info=td_estancia.parent
            td_text_clear=re.sub('<b>|<td>|</td>','',(" ".join((str(info)).split())))
            td_text_clear=td_text_clear.replace('&amp;','&')                      
            list_datos=(re.split('<br/>|</b>',td_text_clear))
            list_datos.pop(5)
            x=0               
            for datos in list_datos:
                dic_aux['idcvlac'] = url[(url.find('='))+1:]
                dic_aux[str(list[x])]=("".join(datos)).strip()                        
                x=x+1
            self.dic_estancias = almacena(self.dic_estancias,dic_aux)
            dic_aux={}
        df_estancias= pd.DataFrame(self.dic_estancias)    
        df_estancias = df_estancias.rename_axis('id').reset_index()
        return df_estancias 
    
    def get_evaluador(self, soup, url):
        dic2={}        
        child=(soup.find('table')).findChildren("tr" , recursive=False)        
        for trs in child:
            h3s=(trs.find('h3'))
            if h3s!=None:                
                if(str(h3s.contents[0])==("Par evaluador")):
                    for div_i in ((h3s.parent.parent.parent).find_all('blockquote')):
                        quote_text_clear=re.sub('<blockquote>|</blockquote>','',(" ".join((str(div_i)).split())))                 
                        list_datos=(re.split('<i>|</i>',quote_text_clear))
                        dic2['IDCVLAC'] = url[(url.find('='))+1:]                    
                        for dato in list_datos:                            
                            for key in self.dic_evaluador:                                                              
                                if(key == dato):
                                    dic2[dato]=(list_datos[list_datos.index(dato)+1]).strip()                          
                        self.dic_evaluador = almacena(self.dic_evaluador,dic2)
                        dic2={}
        df_evaluador= pd.DataFrame(self.dic_evaluador)
        df_evaluador.columns = ['idcvlac','ambito','par_evaluador','editorial','revista','institucion']
        df_evaluador = df_evaluador.rename_axis('id').reset_index()
        return df_evaluador 
    
    def get_idioma(self, soup, url):
        dic2={}       
        child=(soup.find('table') ).findChildren("tr" , recursive=False)
        list=['Idioma','Habla','Escribe','Lee','Entiende']
        for trs in child:
            h3s=(trs.find('h3'))
            if h3s != None:                
                if(str(h3s.contents[0])==("Idiomas")):
                    li_idioma=(h3s.parent.parent.parent).find_all('li')
                    for div_i in li_idioma:                        
                        div_info=(div_i.parent.parent).find_all('td')                        
                        x=0
                        for inf in div_info:                        
                            dic2['IDCVLAC'] = url[(url.find('='))+1:]
                            dic2[str(list[x])]=("".join(inf.text)).strip()                          
                            x=x+1                                          
                        self.dic_idioma = almacena(self.dic_idioma,dic2)
                    dic2={}
        df_idioma = pd.DataFrame(self.dic_idioma)  
        df_idioma.columns = ['idcvlac','idioma','habla','escribe','lee','entiende']
        df_idioma = df_idioma.rename_axis('id').reset_index()      
        return df_idioma
    
    def get_investiga(self, soup, url):
        dic2={}        
        child=(soup.find('table')).findChildren("tr" , recursive=False)
        list=['Nombre','Activa']
        for trs in child:
            h3s=(trs.find('h3'))
            if h3s != None:                
                if(str(h3s.contents[0])==("Líneas de investigación")):
                    li_idioma=(h3s.parent.parent.parent).find_all('li')
                    for div_i in li_idioma:                                         
                        for titulo in div_i.find_all('i'):                           
                            j=((div_i.text ).split(titulo.text))                            
                            x=0 
                            for i in j:
                                dic2['IDCVLAC'] = url[(url.find('='))+1:]
                                dic2[str(list[x])]=("".join(i)).strip()                            
                                x=x+1                                          
                            self.dic_investiga = almacena(self.dic_investiga,dic2)
                        dic2={}
        df_investiga= pd.DataFrame(self.dic_investiga) 
        df_investiga.columns = ['idcvlac','nombre','activa']
        df_investiga = df_investiga.rename_axis('id').reset_index()             
        return df_investiga
    
    def get_jurado(self, soup, url):
        dic_aux={}        
        blocks_jurados = (soup.find('a', attrs={'name':'jurado'}).parent).find_all('blockquote')
        for block_jur in blocks_jurados:
            quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_jur)).split())))
            quote_text_clear=quote_text_clear.replace('&amp;','&')               
            list_datos=(re.split('<i>|</i>|<b>|</b>',quote_text_clear))
            dic_aux['IDCVLAC'] = url[(url.find('='))+1:]
            dic_aux['Nombre'] = (list_datos[0]).strip()                   
            for dato in list_datos:                            
                for key in self.dic_jurado:                                                              
                    if(key == dato):
                        dic_aux[dato]=(list_datos[list_datos.index(dato)+1]).strip()                          
            self.dic_jurado = almacena(self.dic_jurado,dic_aux)
            dic_aux={}
        df_jurado= pd.DataFrame(self.dic_jurado)
        df_jurado.columns = ['idcvlac','nombre','titulo','tipo','lugar','programa','orientado','palabras','areas','sectores']
        df_jurado = df_jurado.rename_axis('id').reset_index()    
        return df_jurado
    
    def get_libro(self, soup, url):
        libros_aux={}
        blocks_arts = (soup.find('a', attrs={'name':'libros'}).parent).find_all('blockquote')
        for block_art in blocks_arts:
            quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_art)).split())))
            quote_text_clear=quote_text_clear.replace('&amp;','&')               
            list_datos=(re.split('<i>|</i>|<b>|</b>',quote_text_clear))
            list_datos.pop(0)
            bloque_string = " ".join((block_art.text).split())
            bloque_string=bloque_string.replace('&amp;','&')   
            fblock=bloque_string.find("ISBN:")
            list_string=(re.split('ed:|, "|" En:',bloque_string[:fblock]))        
            x=0
            informacion=['Autores','Nombre','En','Editorial']               
            for dato in list_string:            
                libros_aux['IDCVLAC'] = url[(url.find('='))+1:]
                libros_aux[str(informacion[x])]=("".join(dato)).strip()                                       
                x=x+1
            for dato in list_datos:                            
                for key in self.libros:                                                              
                    if(key == dato):
                        libros_aux[dato]=(list_datos[list_datos.index(dato)+1]).strip()                            
            self.libros= almacena(self.libros,libros_aux)   
            libros_aux={}        
        df_libros = pd.DataFrame(self.libros)   
        df_libros.columns = ['idcvlac','autores','nombre','lugar','editorial','isbn','volumen','paginas', 'palabras', 'areas', 'sectores']
        df_libros = df_libros.rename_axis('id').reset_index()   
        return df_libros
    
    def get_reconocimiento(self, soup, url):
        dic2={}       
        child=(soup.find('table') ).findChildren("tr" , recursive=False)        
        for trs in child:
            h3s=(trs.find('h3'))
            if h3s != None:                
                if(str(h3s.contents[0])==("Reconocimientos")):
                    li_idioma=(h3s.parent.parent.parent).find_all('li')
                    for div_i in li_idioma:
                        fecha=(div_i.text).rfind("-")
                        dic2['idcvlac'] = url[(url.find('='))+1:]
                        dic2['nombre'] = ((div_i.text)[:fecha]).strip() 
                        dic2['fecha'] = ((div_i.text)[fecha+1:]).strip()                                
                        self.dic_reconocimiento = almacena(self.dic_reconocimiento,dic2)
                    dic2={}
        df_reconocimiento= pd.DataFrame(self.dic_reconocimiento)
        df_reconocimiento = df_reconocimiento.rename_axis('id').reset_index()       
        return df_reconocimiento
    
    def get_redes(self, soup, url,filtro):        
        redes_individual={}
        try:    
            td_redes= soup.find('a', attrs={'name':'{}'.format(filtro)})            
            child=((td_redes.parent).find('table')).find_all("a")
            for trs in child:
                redes_individual['IDCVLAC'] = url[(url.find('='))+1:]
                redes_individual['Nombre']=trs.text 
                redes_individual['Url']=trs['href']                   
                self.redes= almacena(self.redes,redes_individual) 
                redes_individual={}                      
            df_redes = pd.DataFrame(self.redes)
            df_redes.columns = ['idcvlac','nombre','url']
            df_redes = df_redes.rename_axis('id').reset_index()        
            return df_redes
        except:
            df_redes = pd.DataFrame(self.redes)      
            df_redes.columns = ['idcvlac','nombre','url']
            df_redes = df_redes.rename_axis('id').reset_index()    
            return df_redes   
        
        
        