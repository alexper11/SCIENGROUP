import pandas as pd
from cvlac.util import almacena
import re

class ExtractorCvlac():
    
    def __init__(self):
        self.academica={'idcvlac':[],'tipo':[],'institucion':[],'titulo':[],'fecha':[],'proyecto':[]}
        self.actuacion={'idcvlac':[],'areas':[]}
        self.articulos={'idcvlac':['IDCVLAC'],'autores':['Autores'],'nombre':['Nombre'],'lugar':['En'],'revista':['Revista'],'issn':['ISSN:'],'editorial':['ed:'],'volumen':['v.'],'fasciculo':['fasc.'], 'paginas':['p.'],'fecha':['fecha.'],'doi':[' DOI: '], 'palabras':['Palabras: '], 'sectores':['Sectores: ']}
        self.basico={'idcvlac':['IDCVLAC'],'Categoría':[],'Nombre':[],'Nombre en citaciones':[],'Nacionalidad':[],'Sexo':[]}
        self.complementaria={'idcvlac':[],'tipo':[],'institucion':[],'titulo':[],'fecha':[]}
        self.estancias={'idcvlac':[],'nombre':[],'entidad':[],'area':[],'fecha_inicio':[],'fecha_fin':[],'descripcion':[]}
        self.evaluador={'IDCVLAC':[],'Ámbito: ':[],'Par evaluador de: ':[],'Editorial: ':[],'Revista: ':[],'Institución: ':[],'fecha':[]}
        self.idioma={'IDCVLAC':[],'Idioma':[],'Habla':[],'Escribe':[],'Lee':[],'Entiende':[]}
        self.investigacion={'IDCVLAC':[],'Nombre':[],'Activa':[]}
        self.jurados={'IDCVLAC':[],'Nombre':[],'Titulo: ':[],'Tipo de trabajo presentado: ':[],'en: ':[],'programa académico':[],'Nombre del orientado: ':[],'Palabras: ':[],'Areas: ':[],'Sectores: ':[]}
        self.libros={'IDCVLAC':[],'Autores':[],'Nombre':[],'En':[],'fecha':[],'Editorial':[],'ISBN:':[],'v. ':[],'pags.':[], 'Palabras: ':[], 'Areas: ':[], 'Sectores: ':[]}
        self.reconocimiento={'idcvlac':[],'nombre':[],'fecha':[]}
        self.redes={'IDCVLAC':[],'Nombre':[],'Url':[]}
        self.identificadores={'IDCVLAC':[],'Nombre':[],'Url':[]}
        #nuevas tablas 2git 2 no sape
        self.caplibros={'IDCVLAC':[],'Autores':[],'Capitulo':[],'Libro':[],'En':[],'ISBN:':[],'ed:':[],', v.':[],'paginas':[],'fecha':[], 'Palabras: ':[], 'Areas: ':[], 'Sectores: ':[]}
        self.software={'IDCVLAC':[],'Autor':[],'Nombre':[],'Nombre comercial:':[],'contrato/registro:':[],'lugar':[],'fecha':[],'plataforma:':[], 'ambiente:':[], 'Palabras: ':[],'Areas: ':[], 'Sectores: ':[]}
        self.prototipo={'IDCVLAC':[],'Autores':[],'Nombre':[],'En':[],'Editorial':[],'ISBN:':[],'v. ':[],'pags.':[], 'Palabras: ':[], 'Areas: ':[], 'Sectores: ':[]}
        
    def get_academica(self, soup, url):
        dic_aux={}   
        try:    
            tableacad=(soup.find('a', attrs={'name':'formacion_acad'}).parent)
            b_academicas=tableacad.find_all('b')
            if(str((tableacad).find('h3').contents[0])==('Formación Académica')):
                list=['tipo', 'institucion', 'titulo', 'fecha', 'proyecto']
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
                    self.academica = almacena(self.academica,dic_aux)
                    dic_aux={}
        except AttributeError:
            pass
        df_academica= pd.DataFrame(self.academica)
        df_academica = df_academica.reset_index(drop=True)  
        return df_academica
    
    def get_actuacion(self, soup, url):
        actuacion_individual={} 
        try:    
            tableactua=(soup.find('a', attrs={'name':'otra_info_personal'}).parent)
            if(str((tableactua).find('h3').contents[0])==('Áreas de actuación')):
                li_actuacion = tableactua.find_all('li')
                for li_actuacion in li_actuacion:
                    li_act_text = " ".join((li_actuacion.text).split())            
                    actuacion_individual['idcvlac'] = url[(url.find('=') )+1:]
                    actuacion_individual['areas'] = li_act_text            
                    self.actuacion = almacena(self.actuacion,actuacion_individual) 
                    actuacion_individual={}     
        except AttributeError:
            pass   
        df_actuacion = pd.DataFrame(self.actuacion)
        df_actuacion = df_actuacion.reset_index(drop=True)  
        return df_actuacion
    
    def get_articulo(self, soup, url):
        art_individual={}
        try:
            tableart=(soup.find('a', attrs={'name':'articulos'}).parent)
            blocks_arts = tableart.find_all('blockquote')
            if(str((tableart).find('h3').contents[0])==('Artículos')):
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
                    art_individual['IDCVLAC'] = url[(url.find('='))+1:]  
                    try:           
                        for dato in list_string: 
                            art_individual[str(informacion[x])]=("".join(dato)).strip()                                      
                            x=x+1
                    except IndexError:
                        x=0
                        print('Articulos > 4: ',url)
                        informacion=['Autores','Nombre','En']
                        list_string2=(re.split('<br/>',bloque_string[:fblock]))
                        """
                        Pendiente:manejo de excepcion, separador (, ")
                        Poner un contador
                        """
                        list_string=(re.split(', "|" . En:',list_string2[0]))
                        art_individual['Revista']=("".join(list_string2[1])).strip()
                        try:
                            for dato in list_string:
                                art_individual[str(informacion[x])]=("".join(dato)).strip()                                      
                                x=x+1
                        except IndexError:
                            art_individual['En']=("".join(list_string[-1])).strip()
                            list_string.pop(-1)
                            art_individual['Nombre']=("".join(list_string[-1])).strip()
                            list_string.pop(-1)
                            art_individual['Autores']=";".join(list_string).strip()
                    for dato in list_datos:                            
                        for key in self.articulos:                                                              
                            if(key == dato):
                                if(dato=="fasc."):
                                    list_fasc=(re.split('p\.| ,',list_datos[list_datos.index(dato)+1]))  
                                    art_individual['fasc.']=list_fasc[0]                        
                                    art_individual['p.']=list_fasc[1]
                                    art_individual['fecha.']=list_fasc[2].replace(',','')
                                else:
                                    art_individual[dato]=(list_datos[list_datos.index(dato)+1]).strip()                                            
                    self.articulos= almacena(self.articulos,art_individual)        
                    art_individual={} 
        except AttributeError:
            pass       
        df_articulos = pd.DataFrame(self.articulos)    
        df_articulos.columns = ['idcvlac','autores','nombre','lugar','revista','issn','editorial','volumen','fasciculo', 'paginas', 'fecha', 'doi', 'palabras', 'sectores']
        df_articulos = df_articulos.reset_index(drop=True)  
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
                try:
                    cells[1]=" ".join(cells[1].text.split())
                    dic2[cells[0].string]= cells[1]
                except AttributeError:
                    print('BASICO ? : ', url)             
        self.basico = almacena(self.basico,dic2) 
        dic2={}
        df = pd.DataFrame(self.basico)
        df.columns = ['idcvlac','categoria','nombre','citaciones','nacionalidad','sexo']
        df = df.reset_index(drop=True)
        return df
    
    def get_complementaria(self, soup, url):
        dic_aux={}  
        try:
            tablecomp=(soup.find('a', attrs={'name':'formacion_comp'}).parent)   
            b_compl=tablecomp.find_all('b')
            if(str((tablecomp).find('h3').contents[0])==('Formación Complementaria')):
                list=['tipo', 'institucion', 'titulo', 'fecha']
                for td_compl in b_compl:
                    info=td_compl.parent
                    td_text_clear=re.sub('<b>|<td>|</td>','',(" ".join((str(info)).split())))
                    td_text_clear=td_text_clear.replace('&amp;','&')                      
                    list_datos=(re.split('<br/>|</b>',td_text_clear))
                    list_datos.pop(-1)
                    if len(list_datos)>4:
                        print('Formacion complementaria > 3: ',url)
                    
                    x=0               
                    for datos in list_datos:
                        dic_aux['idcvlac'] = url[(url.find('='))+1:]
                        dic_aux[str(list[x])]=("".join(datos)).strip()                            
                        x=x+1
                    self.complementaria = almacena(self.complementaria,dic_aux)
                    dic_aux={}
        except AttributeError:
            pass
        df_complementaria= pd.DataFrame(self.complementaria)
        df_complementaria = df_complementaria.reset_index(drop=True)    
        return df_complementaria
    
    def get_estancias(self, soup, url):
        dic_aux={}    
        try:
            tablestan=(soup.find('a', attrs={'name':'estancias_posdoctorales'}).parent) 
            b_estancias=tablestan.find_all('b')
            if(str((tablestan).find('h3').contents[0])==('Estancias posdoctorales')):
                list=['nombre', 'entidad', 'area', 'fecha_inicio', 'fecha_fin', 'descripcion']
                for td_estancia in b_estancias:
                    info=td_estancia.parent
                    td_text_clear=re.sub('<b>|<td>|</td>','',(" ".join((str(info)).split())))
                    td_text_clear=td_text_clear.replace('&amp;','&')                      
                    list_datos=(re.split('<br/>|</b>',td_text_clear))                    
                    #list_datos.pop(-1) lo deje por algo, no recuerdo. daba error en descripcion (eliminar)
                                        
                    x=0
                    dic_aux['idcvlac'] = url[(url.find('='))+1:]              
                    for datos in list_datos:                        
                        dic_aux[str(list[x])]=("".join(datos)).strip().replace('Desde: ','').replace('Hasta: ','')                       
                        x=x+1
                    self.estancias = almacena(self.estancias,dic_aux)
                    dic_aux={}
        except AttributeError:
            pass
        df_estancias= pd.DataFrame(self.estancias)    
        df_estancias = df_estancias.reset_index(drop=True)
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
                            for key in self.evaluador:  
                                #dic2[key][0]                                                            
                                if(key == dato):
                                    if(dato=='Editorial: 'or dato=='Revista: ' or dato =='Institución: '):
                                        dato2=((list_datos[list_datos.index(dato)+1]))
                                        var=re.findall(r"(?s:.*), (\d{4}, \D+)",dato2)
                                        if isinstance(var,list) and len(var)!=0:
                                            index=dato2.rfind((var[0]))
                                            dic2[dato]=dato2[:index]
                                            dic2['fecha']=dato2[index:]
                                        else:                                           
                                            dic2[dato]=dato2
                                            dic2['fecha']=""
                                    else:
                                        dic2[dato]=(list_datos[list_datos.index(dato)+1]).strip()                          
                        self.evaluador = almacena(self.evaluador,dic2)
                        dic2={}
                    #Encuentra tabla, retorna dataframe por lo que deja de buscar
                    df_evaluador= pd.DataFrame(self.evaluador)
                    #eliminar 
                    df_evaluador.columns = ['idcvlac','ambito','par_evaluador','editorial','revista','institucion','fecha']
                    df_evaluador = df_evaluador.reset_index(drop=True)
                    return df_evaluador
        #No encuentra tabla, retorna dataframe vacío (vale la pena retornar mejor un null y condicionar en el llamado?)
        df_evaluador= pd.DataFrame(self.evaluador)
        df_evaluador.columns = ['idcvlac','ambito','par_evaluador','editorial','revista','institucion']
        df_evaluador = df_evaluador.reset_index(drop=True)
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
                        self.idioma = almacena(self.idioma,dic2)
                    dic2={}
                    #Encuentra tabla, retorna dataframe por lo que deja de buscar
                    df_idioma = pd.DataFrame(self.idioma)  
                    df_idioma.columns = ['idcvlac','idioma','habla','escribe','lee','entiende']
                    df_idioma = df_idioma.reset_index(drop=True)      
                    return df_idioma
        #No encuentra tabla, retorna dataframe vacío (vale la pena retornar mejor un null y condicionar en el llamado?)
        df_idioma = pd.DataFrame(self.idioma)  
        df_idioma.columns = ['idcvlac','idioma','habla','escribe','lee','entiende']
        df_idioma = df_idioma.reset_index(drop=True)      
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
                            for i in j[0:2]:
                                dic2['IDCVLAC'] = url[(url.find('='))+1:]
                                dic2[str(list[x])]=("".join(i)).strip()                            
                                x=x+1                                          
                            self.investigacion = almacena(self.investigacion,dic2)
                        dic2={}
                    df_investiga= pd.DataFrame(self.investigacion) 
                    df_investiga.columns = ['idcvlac','nombre','activa']
                    df_investiga = df_investiga.reset_index(drop=True)             
                    return df_investiga
        df_investiga= pd.DataFrame(self.investigacion) 
        df_investiga.columns = ['idcvlac','nombre','activa']
        df_investiga = df_investiga.reset_index(drop=True)             
        return df_investiga
    
    def get_jurado(self, soup, url):
        dic_aux={}   
        try:
            tablejur=(soup.find('a', attrs={'name':'jurado'}).parent)     
            blocks_jurados = tablejur.find_all('blockquote')
            if(str((tablejur).find('h3').contents[0])==('Jurado en comités de evaluación')):
                for block_jur in blocks_jurados:
                    quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_jur)).split())))
                    quote_text_clear=quote_text_clear.replace('&amp;','&')               
                    list_datos=(re.split('<i>|</i>|<b>|</b>',quote_text_clear))
                    dic_aux['IDCVLAC'] = url[(url.find('='))+1:]
                    dic_aux['Nombre'] = (list_datos[0]).strip()                   
                    for dato in list_datos:                            
                        for key in self.jurados:                                                              
                            if(key == dato):
                                dic_aux[dato]=(list_datos[list_datos.index(dato)+1]).strip()                          
                    self.jurados = almacena(self.jurados,dic_aux)
                    dic_aux={}
        except AttributeError:
            pass
        df_jurado= pd.DataFrame(self.jurados)
        df_jurado.columns = ['idcvlac','nombre','titulo','tipo','lugar','programa','orientado','palabras','areas','sectores']
        df_jurado = df_jurado.reset_index(drop=True)    
        return df_jurado
    
    def get_libro(self, soup, url):
        libros_aux={}
        try:
            tablelib=(soup.find('a', attrs={'name':'libros'}).parent)
            blocks_arts = tablelib.find_all('blockquote')
            if(str((tablelib).find('h3').contents[0])==('Libros')):
                for block_art in blocks_arts:
                    quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_art)).split())))
                    quote_text_clear=quote_text_clear.replace('&amp;','&')               
                    list_datos=(re.split('<i>|</i>|<b>|</b>',quote_text_clear))
                    list_datos.pop(0)
                    bloque_string = " ".join((block_art.text).split())
                    bloque_string=bloque_string.replace('&amp;','&')   
                    fblock=bloque_string.rfind("ISBN:")
                    list_string=(re.split('ed:|, "|" En:',bloque_string[:fblock]))        
                    x=0
                    informacion=['Autores','Nombre','En','Editorial']               
                    for dato in list_string:            
                        libros_aux['IDCVLAC'] = url[(url.find('='))+1:]
                        if(str(informacion[x])=='En'):
                            var=re.split('',dato)
                            libros_aux['En']=var[0]
                            libros_aux['fecha']=var[1]
                        else:
                            libros_aux[str(informacion[x])]=("".join(dato)).strip()                                       
                        x=x+1
                    for dato in list_datos:                            
                        for key in self.libros:                                                              
                            if(key == dato):
                                libros_aux[dato]=(list_datos[list_datos.index(dato)+1]).strip()                            
                    self.libros= almacena(self.libros,libros_aux)   
                    libros_aux={}   
        except AttributeError:
            pass     
        df_libros = pd.DataFrame(self.libros)   
        df_libros.columns = ['idcvlac','autores','nombre','lugar','editorial','isbn','volumen','paginas', 'palabras', 'areas', 'sectores']
        df_libros = df_libros.reset_index(drop=True)   
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
                        self.reconocimiento = almacena(self.reconocimiento,dic2)
                    dic2={}
                    df_reconocimiento= pd.DataFrame(self.reconocimiento)
                    df_reconocimiento = df_reconocimiento.reset_index(drop=True)       
                    return df_reconocimiento
        df_reconocimiento= pd.DataFrame(self.reconocimiento)
        df_reconocimiento = df_reconocimiento.reset_index(drop=True)       
        return df_reconocimiento
    
    def get_redes(self, soup, url):        
        redes_individual={}
        #td_redes= soup.find('a', attrs={'name':'{}'.format(filtro)})
        try:         
            tdredes=(soup.find('a', attrs={'name':'redes_identificadoes'}).parent)
            if(str((tdredes).find('h3').contents[0])==('Redes sociales académicas')):
                child=((tdredes).find('table')).find_all("a")
                for trs in child:
                    redes_individual['IDCVLAC'] = url[(url.find('='))+1:]
                    redes_individual['Nombre']=trs.text 
                    redes_individual['Url']=trs['href']                   
                    self.redes= almacena(self.redes,redes_individual) 
                    redes_individual={}                      
        except AttributeError:
            pass
        df_redes = pd.DataFrame(self.redes)      
        df_redes.columns = ['idcvlac','nombre','url']
        df_redes = df_redes.reset_index(drop=True)    
        return df_redes   
        
    def get_identificadores(self, soup, url):        
        identificadores_individual={}
        try:             
            td_identificadores= (soup.find('a', attrs={'name':'red_identificadores'}).parent)
            if(str((td_identificadores.parent).find('h3').contents[0])=="Identificadores de autor"):
                child=((td_identificadores.parent).find('table')).find_all("a")
                for trs in child:
                    identificadores_individual['IDCVLAC'] = url[(url.find('='))+1:]
                    identificadores_individual['Nombre']=trs.text 
                    identificadores_individual['Url']=trs['href']                   
                    self.identificadores= almacena(self.identificadores,identificadores_individual) 
                    identificadores_individual={}                      
        except AttributeError:
            pass
        df_identificadores = pd.DataFrame(self.identificadores)      
        df_identificadores.columns = ['idcvlac','nombre','url']
        df_identificadores = df_identificadores.reset_index(drop=True)    
        return df_identificadores
    
    #########################################################
                #Nuevas tablas
    #########################################################
    def get_caplibro(self, soup, url):
        cap_libros_aux={}
        try:
            table_cap_libros=(soup.find('a', attrs={'name':'capitulos'}).parent)            
            if(str((table_cap_libros).find('h3').contents[0])==('Capitulos de libro')):
                blocks_cap = table_cap_libros.find_all('blockquote')
                for block_cap in blocks_cap:
                    block_cap=re.sub('<blockquote>|</blockquote>','',(" ".join((str(block_cap)).split()))).replace('&amp;','&')
                    print(block_cap)
                    var=(re.findall(r', "',dato))
                    index=dato.rfind((var[0]))
                    quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_cap)).split())))
                    quote_text_clear=quote_text_clear.replace('&amp;','&')
                    #print((quote_text_clear))             
                    list_datos=(re.split('<i>|</i>|<b>|</b>',quote_text_clear))
                    list_datos.pop(0)
                    bloque_string = " ".join((block_cap.text).split())
                    bloque_string=bloque_string.replace('&amp;','&').replace('Tipo: Capítulo de libro ','')  
                    fblock=bloque_string.rfind("ISBN:")
                    list_string=(re.split(', "|. En:|" ',bloque_string[:fblock])) 
                    #print(list_datos)       
                    x=0
                    informacion=['Autores','Capitulo','Libro','En']               
                    for dato in list_string:            
                        cap_libros_aux['IDCVLAC'] = url[(url.find('='))+1:]                                                                                        
                        cap_libros_aux[str(informacion[x])]=("".join(dato)).strip()
                        x=x+1
                    for dato in list_datos:                            
                        for key in self.caplibros:                                                              
                            if(key == dato):
                                if(dato==", v."):
                                    list_fasc=(re.split(',',list_datos[list_datos.index(dato)+1]))  
                                    cap_libros_aux[', v.']=list_fasc[0]                        
                                    cap_libros_aux['paginas']=list_fasc[1].replace("p.","")
                                    cap_libros_aux['fecha']=list_fasc[2]
                                    #.replace(',','')
                                else:
                                    cap_libros_aux[dato]=(list_datos[list_datos.index(dato)+1]).strip()                            
                    self.libros= almacena(self.caplibros,cap_libros_aux)   
                    cap_libros_aux={}   
        except AttributeError:
            pass     
        df_libros = pd.DataFrame(self.caplibros)   
        df_libros.columns = ['idcvlac','autores','capitulo','libro','lugar','isbn','editorial','volumen','paginas','fecha','palabras', 'areas', 'sectores']
        df_libros = df_libros.reset_index(drop=True)   
        return df_libros
    
    def get_software(self, soup, url):
        soft_aux={}
        try:
            tablelib=(soup.find('a', attrs={'name':'software'}).parent)
            blocks_arts = tablelib.find_all('blockquote')
            if(str((tablelib).find('h3').contents[0])==('Softwares')):
                for block_art in blocks_arts:
                    quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_art)).split())))
                    quote_text_clear=quote_text_clear.replace('&amp;','&') 
                    bloque_string = " ".join((block_art.text).split())
                    bloque_string=bloque_string.replace('&amp;','&')   
                    fblock=bloque_string.find(",")
                    list_string=(re.split('Nombre comercial:|contrato/registro:|. En:|plataforma:|ambiente:',bloque_string[fblock:]))
                    soft_aux['IDCVLAC'] = url[(url.find('='))+1:]
                    soft_aux['Autor'] = bloque_string[:fblock]  
                    soft_aux['Nombre'] = list_string[0]
                    list_string.pop(0)
                    print(list_string)                    
                    x=0
                    informacion=['Nombre comercial:','contrato/registro:','lugar','plataforma:','ambiente:']                    
                    for dato in list_string:
                        if(dato=='. En:'):                                            
                            dato=(re.split(',\d*\D+',list_datos[list_datos.index(dato)+1]))  
                            soft_aux['lugar']=list_datos[0]
                            soft_aux['fecha']=list_datos[1]
                        else:
                            soft_aux[str(informacion[x])]=("".join(dato)).strip()
                        x=x+1
                    list_datos=(re.split('<i>|</i>|<b>|</b>',quote_text_clear))
                    list_datos.pop(0)
                    for dato in list_datos:                            
                        for key in self.software:                                                              
                            if(key == dato):
                                soft_aux[dato]=(list_datos[list_datos.index(dato)+1]).strip()                            
                    self.software= almacena(self.software,soft_aux)   
                    soft_aux={}   
        except AttributeError:
            pass     
        df_libros = pd.DataFrame(self.software)   
        df_libros.columns = ['idcvlac','autor','nombre_software','nombre_comercial','contrato','lugar','fecha','plataforma','ambiente', 'palabras', 'areas', 'sectores']
        df_libros = df_libros.reset_index(drop=True)   
        return df_libros
    
    def get_prototipo(self, soup, url):
        proto_aux={}
        try:
            tablelib=(soup.find('a', attrs={'name':'libros'}).parent)
            blocks_arts = tablelib.find_all('blockquote')
            if(str((tablelib).find('h3').contents[0])==('Libros')):
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
                        proto_aux['IDCVLAC'] = url[(url.find('='))+1:]
                        proto_aux[str(informacion[x])]=("".join(dato)).strip()                                       
                        x=x+1
                    for dato in list_datos:                            
                        for key in self.prototipo:                                                              
                            if(key == dato):
                                proto_aux[dato]=(list_datos[list_datos.index(dato)+1]).strip()                            
                    self.prototipo= almacena(self.prototipo,proto_aux)   
                    proto_aux={}   
        except AttributeError:
            pass     
        df_libros = pd.DataFrame(self.prototipo)   
        df_libros.columns = ['idcvlac','autores','nombre','lugar','editorial','isbn','volumen','paginas', 'palabras', 'areas', 'sectores']
        df_libros = df_libros.reset_index(drop=True)   
        return df_libros