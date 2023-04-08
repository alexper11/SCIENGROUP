import re

import pandas as pd

from cvlac.util import almacena, almacena_df, get_lxml


class ExtractorCvlac():
    
    def __init__(self):
        self.academica=pd.DataFrame(columns=['idcvlac','tipo','institucion','titulo','fecha','proyecto'])
        self.actuacion=pd.DataFrame(columns=['idcvlac','areas'])
        self.articulos=pd.DataFrame(columns=['idcvlac','autores','nombre','tipo','verificado','lugar','revista','issn','editorial','volumen','fasciculo', 'paginas','fecha','doi', 'palabras', 'sectores'])
        self.basico=pd.DataFrame(columns=['idcvlac','categoria','nombre','nombre_citaciones','nacionalidad','sexo'])
        self.complementaria=pd.DataFrame(columns=['idcvlac','tipo','institucion','titulo','fecha'])
        self.estancias=pd.DataFrame(columns=['idcvlac','nombre','entidad','area','fecha_inicio','fecha_fin','descripcion'])
        self.evaluador=pd.DataFrame(columns=['idcvlac','ambito','par_evaluador','editorial','revista','institucion','fecha'])
        self.idioma=pd.DataFrame(columns=['idcvlac','idioma','habla','escribe','lee','entiende'])
        self.investigacion=pd.DataFrame(columns=['idcvlac','nombre','activa'])
        self.jurados=pd.DataFrame(columns=['idcvlac','nombre','titulo','tipo','lugar','programa','orientado','palabras','areas','sectores'])
        self.libros=pd.DataFrame(columns=['idcvlac','autores','nombre','tipo','verificado','lugar','fecha','editorial','isbn','volumen','paginas', 'palabras', 'areas', 'sectores'])
        self.reconocimiento=pd.DataFrame(columns=['idcvlac','nombre','fecha'])
        self.redes=pd.DataFrame(columns=['idcvlac','nombre','url'])
        self.identificadores=pd.DataFrame(columns=['idcvlac','nombre','url'])        
        self.caplibros=pd.DataFrame(columns=['idcvlac','autores','capitulo','libro','lugar','verificado','isbn','editorial','volumen','paginas','fecha', 'palabras', 'areas', 'sectores'])
        self.software=pd.DataFrame(columns=['idcvlac','autor','nombre','tipo','verificado','nombre_comercial','contrato_registro','lugar','fecha','plataforma', 'ambiente', 'palabras','areas', 'sectores'])
        self.prototipo=pd.DataFrame(columns=['idcvlac','autor','nombre','tipo','verificado','nombre_comercial','contrato_registro','lugar','fecha', 'palabras','areas', 'sectores'])
        self.tecnologicos=pd.DataFrame(columns=['idcvlac','autor','nombre','tipo','verificado','nombre_comercial','contrato_registro','lugar','fecha', 'palabras','areas', 'sectores'])
        self.empresa_tecnologica=pd.DataFrame(columns=['idcvlac','autores','nombre','tipo','verificado','nit','registro_camara','palabras','areas','sectores'])
        self.innovacion_empresarial=pd.DataFrame(columns=['idcvlac','autor','nombre','tipo','verificado','nombre_comercial','contrato_registro','lugar','fecha', 'palabras','areas', 'sectores'])

    def get_academica(self, soup, url):
        dic_aux={}   
        try:    
            tableacad=soup.find('a', attrs={'name':'formacion_acad'}).parent           
            if(str((tableacad).find('h3').contents[0])==('Formación Académica')):
                list1=['tipo', 'institucion', 'titulo', 'fecha', 'proyecto']
                b_academicas=tableacad.find_all('b')
                for td_academi in b_academicas:
                    info=td_academi.parent
                    td_text_clear=re.sub('<b>|<td>|</td>','',(" ".join((str(info)).split())))
                    td_text_clear=td_text_clear.replace('&amp;','&')                      
                    list_datos=(re.split('<br/>|</b>',td_text_clear))        
                    x=0               
                    for datos in list_datos:
                        dic_aux['idcvlac'] = url[(url.find('='))+1:]
                        dic_aux[str(list1[x])]=("".join(datos)).rstrip(', .').strip()                         
                        x=x+1
                    dic_aux=pd.DataFrame([dic_aux])
                    self.academica = almacena_df(self.academica,dic_aux)
                    dic_aux={}
        except AttributeError:
            pass
        df_academica= self.academica
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
                    actuacion_individual=pd.DataFrame([actuacion_individual])          
                    self.actuacion = almacena_df(self.actuacion,actuacion_individual)                    
                    actuacion_individual={}     
        except AttributeError:
            pass  
        return self.actuacion
    
    """def get_articulo(self, soup, url):
        try:
            tableart=(soup.find('a', attrs={'name':'articulos'}).parent)            
            if(str((tableart).find('h3').contents[0])==('Artículos')):                                
                blocks_arts = tableart.find_all('blockquote')
                for block_art in blocks_arts:
                    art_individual={'IDCVLAC':'','Autores':'','Nombre':'','tipo':'','verificado':'','En':'','Revista':'','ISSN:':'','ed:':'','v.':'','fasc.':'', 'p.':'','fecha.':'',' DOI: ':'', 'Palabras: ':'', 'Sectores: ':''}
                    tipo=block_art.find_parent('tr').find_previous_sibling('tr')                    
                    if tipo.find('img') == None:
                        art_individual['verificado']=False
                    else:
                        art_individual['verificado']=True
                    art_individual['tipo']=tipo.find('b').text
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
                        
                        #Pendiente:manejo de excepcion, separador (, ")
                        #Poner un contador
                        
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
                        for key in art_individual:                                                              
                            if(key == dato):
                                if(dato=="fasc."):
                                    #list_fasc=re.split('p.| ,',list_datos[list_datos.index(dato)+1]) #escape despues de p type: ignore
                                    art_individual['fasc.']=list_fasc[0].strip()                 
                                    art_individual['p.']=list_fasc[1].strip()
                                    art_individual['fecha.']=list_fasc[2].replace(',','').strip()
                                else:
                                    art_individual[dato]=(list_datos[list_datos.index(dato)+1]).strip()
                    
                    art_individual=pd.DataFrame([dict(zip(list(self.articulos.columns),art_individual.values()))])
                    #self.articulos = almacena_df(self.articulos,art_individual).reset_index(drop=True).replace(to_replace ='^W+$|,$', value = '', regex = True) #escape antes de W type: ignore
        except AttributeError:
            pass       
        
        df_articulos = self.articulos
        return df_articulos
    """
    def get_articulo(self, soup, url):
        try:                       
            list_blockquote=soup.find('h3',string='Artículos').find_parent('table').find_all('blockquote')
            if(list_blockquote!=None):
                fid = url.find('=')               
                for blockquote in list_blockquote:
                    dic={'idcvlac':'','autores':'','nombre':'','tipo':'','verificado':'','lugar':'','revista':'','ISSN:':'','ed:':'','v.':'','fasc.':'', 'p.':'','fecha.':'',' DOI: ':'', 'Palabras: ':'', 'Sectores: ':''}
                    dic['idcvlac']=url[fid+1:]                    
                    tipo=blockquote.find_parent('tr').find_previous_sibling('tr')                    
                    if tipo.find('img') == None:
                        dic['verificado']=False #type: ignore
                    else:
                        dic['verificado']=True  #type: ignore
                    dic['tipo']=tipo.find('b').text
                    blockquote=re.sub('</blockquote>|<blockquote>',''," ".join(str(blockquote).split())).replace('&amp;','&')
                    index_i=blockquote.find('<br/>')
                    dato=blockquote[:index_i]
                    
                    if len(re.findall(', "', dato)) > 1:
                        print('Revisar separación:',url)
                        
                    dic['autores']=dato[:dato.find(', "')].strip()
                    dic['nombre']=dato[dato.find(', "')+3:dato.rfind('. En:')].strip().rstrip('"')
                    dic['lugar']=dato[dato.rfind('. En:')+5:].strip()
                    list_datos=re.split('<i>|</i>|<b>|</b>',blockquote[index_i:].replace('<br/>',''))                    
                    dic['revista']=list_datos[0].strip()
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):
                        dato=dato.replace('<br/>','')
                        if dato in dic:                                                        
                            if dato != 'fasc.':
                                dato=re.sub('http://dx.doi.org/|https://doi.org/|https://doi.org/','',dato)            
                                if dato == 'v.':
                                    dic[dato]=(list_datos[i+1]).rstrip(' ,.No').strip()
                                else:
                                    dic[dato]=(list_datos[i+1]).rstrip(' ,.-').strip()
                            else:                                
                                index_pg=list_datos[i+1].rfind('p.')
                                dic['fasc.']=list_datos[i+1][:index_pg].strip()
                                dato2=list_datos[i+1][index_pg+2:].strip().rstrip(', ')
                                index_fe=dato2.rfind(',')
                                dic['p.']=dato2[:index_fe].rstrip(', -').strip()
                                dic['fecha.']=dato2[index_fe+1:]
                                #list_fasc=re.split('p\.| ,',list_datos[list_datos.index(dato)+1])                                                         
                                #dic['fasc.']=dato[:index_pg].strip()                 
                                #dic['p.']=list_fasc[1].strip()
                                #dic['fecha.']=list_fasc[2].replace(',','').strip()
                    
                    dic=pd.DataFrame([dict(zip(list(self.articulos.columns),dic.values()))])                                
                    self.articulos = almacena_df( self.articulos,dic).replace(to_replace ='^\W+$|,$', value = '', regex = True)# type: ignore                                   
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass   
        return self.articulos

    def get_basico(self, soup, url):
        dic2={'IDCVLAC':'','Categoría':'','Nombre':'','Nombre en citaciones':'','Nacionalidad':'','Sexo':''}         
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
        
        dic2=pd.DataFrame([dict(zip(list(self.basico.columns),dic2.values()))])
        self.basico = almacena_df(self.basico,dic2)
        df = self.basico
        return df
    
    def get_complementaria(self, soup, url):
        dic_aux={}  
        try:
            tablecomp=(soup.find('a', attrs={'name':'formacion_comp'}).parent)
            if(str((tablecomp).find('h3').contents[0])==('Formación Complementaria')):
                list1=['tipo', 'institucion', 'titulo', 'fecha']
                b_compl=tablecomp.find_all('b')
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
                        dic_aux[str(list1[x])]=("".join(datos)).strip()                            
                        x=x+1    
                    dic_aux=pd.DataFrame([dict(zip(list(self.complementaria.columns),dic_aux.values()))])
                    self.complementaria = almacena_df(self.complementaria,dic_aux)
                    dic_aux={}
        except AttributeError:
            pass
        df_complementaria= self.complementaria  
        return df_complementaria
    
    def get_estancias(self, soup, url):
        dic_aux={}    
        try:
            tablestan=(soup.find('a', attrs={'name':'estancias_posdoctorales'}).parent) 
            if(str((tablestan).find('h3').contents[0])==('Estancias posdoctorales')):
                list1=['nombre', 'entidad', 'area', 'fecha_inicio', 'fecha_fin', 'descripcion']
                b_estancias=tablestan.find_all('b')
                for td_estancia in b_estancias:
                    info=td_estancia.parent
                    td_text_clear=re.sub('<b>|<td>|</td>','',(" ".join((str(info)).split())))
                    td_text_clear=td_text_clear.replace('&amp;','&')                      
                    list_datos=(re.split('<br/>|</b>',td_text_clear))                    
                    #list_datos.pop(-1) lo deje por algo, no recuerdo. daba error en descripcion (eliminar)
                    x=0
                    dic_aux['idcvlac'] = url[(url.find('='))+1:]              
                    for datos in list_datos:                        
                        dic_aux[str(list1[x])]=("".join(datos)).strip().replace('Desde: ','').replace('Hasta: ','').rstrip(', .')                       
                        x=x+1
                    dic_aux=pd.DataFrame([dic_aux])   
                    self.estancias = almacena_df(self.estancias,dic_aux)
                    dic_aux={}
        except AttributeError:
            pass
        df_estancias= self.estancias 
        return df_estancias 
    
    def get_evaluador(self, soup, url):
        child=(soup.find('table')).findChildren("tr" , recursive=False)        
        for trs in child:
            h3s=(trs.find('h3'))
            if h3s!=None:                
                if(str(h3s.contents[0])==("Par evaluador")):
                    for div_i in ((h3s.parent.parent.parent).find_all('blockquote')):
                        dic2={'IDCVLAC':'','Ámbito: ':'','Par evaluador de: ':'','Editorial: ':'','Revista: ':'','Institución: ':'','fecha':''}       
                        quote_text_clear=re.sub('<blockquote>|</blockquote>','',(" ".join((str(div_i)).split())))                 
                        list_datos=(re.split('<i>|</i>',quote_text_clear))
                        dic2['IDCVLAC'] = url[(url.find('='))+1:]                    
                        for dato in list_datos:                            
                            for key in dic2:  
                                #dic2[key][0]                                                            
                                if(key == dato):
                                    if(dato=='Editorial: 'or dato=='Revista: ' or dato =='Institución: '):
                                        dato2=((list_datos[list_datos.index(dato)+1]))
                                        var=re.findall(r"(?s:.*), (\d{4}, \D+)",dato2)
                                        if isinstance(var,list) and len(var)!=0:
                                            index=dato2.rfind((var[0]))
                                            dic2[dato]=dato2[:index].rstrip(', .').strip()
                                            dic2['fecha']=dato2[index:].strip()
                                        else:                                           
                                            dic2[dato]=dato2.rstrip(', .').strip()
                                            dic2['fecha']=""
                                    else:
                                        dic2[dato]=(list_datos[list_datos.index(dato)+1]).rstrip(', .').strip()   
                                        
                        dic2=pd.DataFrame([dict(zip(list(self.evaluador.columns),dic2.values()))])
                        self.evaluador = almacena_df(self.evaluador,dic2)                 
                        dic2={}
                    #Encuentra tabla, retorna dataframe por lo que deja de buscar
                    df_evaluador= self.evaluador
                    return df_evaluador
        #No encuentra tabla, retorna dataframe vacío (vale la pena retornar mejor un null y condicionar en el llamado?)
        df_evaluador= self.evaluador
        return df_evaluador 
    
    def get_idioma(self, soup, url): ############################## PROBARLO CON UNA LISTA DE CVLACS
        
        child=(soup.find('table') ).findChildren("tr" , recursive=False)        
        for trs in child:            
            h3s=(trs.find('h3'))
            if h3s != None:                
                if(str(h3s.contents[0])==("Idiomas")):                    
                    list1=['idioma','habla','escribe','lee','entiende']
                    li_idioma=(h3s.parent.parent.parent).find_all('li')
                    for div_i in li_idioma:  
                        dic2={'idcvlac':'','idioma':'','habla':'','escribe':'','lee':'','entiende':''}                     
                        div_info=(div_i.parent.parent).find_all('td')                        
                        x=0
                        for inf in div_info:                        
                            dic2['idcvlac'] = url[(url.find('='))+1:]
                            dic2[str(list1[x])]=("".join(inf.text)).strip()                          
                            x=x+1 
                        dic2=pd.DataFrame([dic2])                                    
                        self.idioma = almacena_df(self.idioma,dic2)
                        dic2={}
                    #Encuentra tabla, retorna dataframe por lo que deja de buscar
                    df_idioma = self.idioma    
                    return df_idioma
        #No encuentra tabla, retorna dataframe vacío (vale la pena retornar mejor un null y condicionar en el llamado?)
        df_idioma = self.idioma   
        return df_idioma
    
    def get_investiga(self, soup, url): ############################## PROBARLO CON UNA LISTA DE CVLACS
        dic2={}        
        child=(soup.find('table')).findChildren("tr" , recursive=False)        
        for trs in child:
            h3s=(trs.find('h3'))
            if h3s != None:                
                if(str(h3s.contents[0])==("Líneas de investigación")):
                    list1=['nombre','activa']
                    li_idioma=(h3s.parent.parent.parent).find_all('li')
                    for div_i in li_idioma:                                         
                        for titulo in div_i.find_all('i'):                           
                            j=((div_i.text ).split(titulo.text))                            
                            x=0 
                            for i in j[0:2]:
                                dic2['idcvlac'] = url[(url.find('='))+1:]
                                dic2[str(list1[x])]=("".join(i)).rstrip(', .').strip()                            
                                x=x+1     
                            dic2=pd.DataFrame([dic2]) 
                            self.investigacion = almacena_df(self.investigacion,dic2)
                            dic2={}                            
                                            
        df_investiga= self.investigacion            
        return df_investiga
    
    def get_jurado(self, soup, url):
        try:
            tablejur=(soup.find('a', attrs={'name':'jurado'}).parent)
            if(str((tablejur).find('h3').contents[0])==('Jurado en comités de evaluación')):
                blocks_jurados = tablejur.find_all('blockquote')
                for block_jur in blocks_jurados:
                    dic_aux={'IDCVLAC':'','Nombre':'','Titulo: ':'','Tipo de trabajo presentado: ':'','en: ':'','programa académico':'','Nombre del orientado: ':'','Palabras: ':'','Areas: ':'','Sectores: ':''}   
                    quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_jur)).split())))
                    quote_text_clear=quote_text_clear.replace('&amp;','&')               
                    list_datos=(re.split('<i>|</i>|<b>|</b>',quote_text_clear))
                    dic_aux['IDCVLAC'] = url[(url.find('='))+1:]
                    dic_aux['Nombre'] = list_datos[0].rstrip(', ').strip()                   
                    for dato in list_datos:                            
                        for key in dic_aux:                                                              
                            if(key == dato):
                                dic_aux[dato]=(list_datos[list_datos.index(dato)+1]).rstrip(', .').strip() 
                    
                    dic_aux=pd.DataFrame([dict(zip(list(self.jurados.columns),dic_aux.values()))])
                    self.jurados = almacena_df(self.jurados,dic_aux)

        except AttributeError:
            pass
        df_jurado= self.jurados
        return df_jurado
    
    def get_libro(self, soup, url):
        try:
            tablelib=(soup.find('a', attrs={'name':'libros'}).parent)            
            if(str((tablelib).find('h3').contents[0])==('Libros')):
                blocks_arts = tablelib.find_all('blockquote')
                for block_art in blocks_arts:
                    libros_aux={'IDCVLAC':'','Autores':'','Nombre':'','tipo':'','verificado':'','En':'','fecha':'','Editorial':'','ISBN:':'','v. ':'','pags.':'', 'Palabras: ':'', 'Areas: ':'', 'Sectores: ':''}
                    
                    tipo=block_art.find_parent('tr').find_previous_sibling('tr')                    
                    if tipo.find('img') == None:
                        libros_aux['verificado']=False  #type: ignore
                    else:
                        libros_aux['verificado']=True   #type: ignore
                    libros_aux['tipo']=tipo.find('b').text
                    
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
                            var=(re.findall(r"(?s:.*)(\d{4})",dato))
                            if isinstance(var,list) and len(var)!=0:
                                index=dato.rfind((var[0]))
                                libros_aux['En']=dato[:index].strip()
                                libros_aux['fecha']=dato[index:].strip().rstrip(".")
                            else:
                                libros_aux['En']=dato.strip()
                                libros_aux['fecha']=""
                        else:
                            libros_aux[str(informacion[x])]=("".join(dato)).strip()                                       
                        x=x+1
                    for dato in list_datos:                            
                        for key in libros_aux:                                                              
                            if(key == dato):
                                libros_aux[dato]=(list_datos[list_datos.index(dato)+1]).strip()  
                    libros_aux=pd.DataFrame([dict(zip(list(self.libros.columns),libros_aux.values()))])
                    self.libros = almacena_df(self.libros,libros_aux).replace(to_replace ='^\W+$|,$', value = '', regex = True)# type: ignore   
        except AttributeError:
            pass     
        df_libros = self.libros 
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
                        dic2['nombre'] = ((div_i.text)[:fecha]).rstrip(', .').strip() 
                        dic2['fecha'] = ((div_i.text)[fecha+1:]).strip() 
                        dic2=pd.DataFrame([dic2])                      
                        self.reconocimiento = almacena_df(self.reconocimiento,dic2)
                        dic2={}
        df_reconocimiento= self.reconocimiento      
        return df_reconocimiento
    
    def get_redes(self, soup, url):        
        redes_individual={}
        #td_redes= soup.find('a', attrs={'name':'{}'.format(filtro)})
        try:         
            tdredes=(soup.find('a', attrs={'name':'redes_identificadoes'}).parent)
            if(str((tdredes).find('h3').contents[0])==('Redes sociales académicas')):
                child=((tdredes).find('table')).find_all("a")
                for trs in child:
                    redes_individual['idcvlac'] = url[(url.find('='))+1:]
                    redes_individual['nombre']=trs.text 
                    redes_individual['url']=trs['href']
                    redes_individual=pd.DataFrame([redes_individual])               
                    self.redes = almacena_df( self.redes,redes_individual)
                    redes_individual={}                      
        except AttributeError:
            pass
        df_redes = self.redes    
        return df_redes   
        
    def get_identificadores(self, soup, url):        
        identificadores_individual={}
        try:             
            td_identificadores= (soup.find('a', attrs={'name':'red_identificadores'}).parent)
            if(str((td_identificadores.parent).find('h3').contents[0])=="Identificadores de autor"):
                child=((td_identificadores.parent).find('table')).find_all("a")
                for trs in child:
                    identificadores_individual['idcvlac'] = url[(url.find('='))+1:]
                    identificadores_individual['nombre']=trs.text 
                    identificadores_individual['url']=trs['href']  
                    identificadores_individual=pd.DataFrame([identificadores_individual])                 
                    self.identificadores = almacena_df(self.identificadores,identificadores_individual) 
                    identificadores_individual={}                      
        except AttributeError:
            pass
        df_identificadores = self.identificadores         
        return df_identificadores
    
    def get_caplibro(self, soup, url):
        try:
            table_cap_libros=(soup.find('a', attrs={'name':'capitulos'}).parent)            
            if(str((table_cap_libros).find('h3').contents[0])==('Capitulos de libro')):
                blocks_cap = table_cap_libros.find_all('blockquote')
                for block_cap in blocks_cap:
                    cap_libros_aux={'idcvlac':'','autores':'','capitulo':'','libro':'','lugar':'','verificado':'','ISBN:':'','ed:':'',', v.':'','paginas':'','fecha':'', 'Palabras: ':'', 'Areas: ':'', 'Sectores: ':''}
                    if block_cap.find('img') == None:
                        cap_libros_aux['verificado']=False  #type: ignore
                    else:
                        cap_libros_aux['verificado']=True   #type: ignore
                    block_cap=re.sub('<blockquote>|</blockquote>','',(" ".join((str(block_cap)).split()))).replace('&amp;','&')
                    index_name=block_cap.find(', "')
                    list_autores=block_cap[:index_name].replace('Tipo: Capítulo de libro','').split('<br/>')
                    list_autores.pop(0)
                    autores=""
                    for autor in list_autores:
                        var2=autor.split(',')[0].rstrip()
                        autores=autores+var2+","
                    cap_libros_aux['idcvlac'] = url[(url.find('='))+1:]
                    cap_libros_aux['autores'] = autores.strip()
                    block_name_out=block_cap[index_name+3:].replace("<br/>","")
                    index_lugar=block_name_out.rfind(". En:")
                    index_cap=block_name_out[:index_lugar].rfind('"')                    
                    cap_libros_aux['capitulo'] = block_name_out[:index_cap]
                    cap_libros_aux['libro'] = block_name_out[index_cap+1:index_lugar].strip()
                    index_en=block_name_out.find("<i>ISBN:")
                    cap_libros_aux['lugar'] = block_name_out[index_lugar+5:index_en].strip()                             
                    list_datos=re.split('<i>|</i>|<b>|</b>',block_name_out[index_en:])                 
                    for dato in list_datos:                            
                        for key in cap_libros_aux:                                                                                          
                            if(key == dato):
                                if(dato==", v."):
                                    list_fasc=(re.split(',',list_datos[list_datos.index(dato)+1]))  
                                    cap_libros_aux[', v.']=list_fasc[0].strip()                   
                                    cap_libros_aux['paginas']=list_fasc[1].replace("p.","").strip()
                                    cap_libros_aux['fecha']=list_fasc[2].strip()                                    
                                else:
                                    cap_libros_aux[dato]=(list_datos[list_datos.index(dato)+1]).strip()
                    cap_libros_aux=pd.DataFrame([dict(zip(list(self.caplibros.columns),cap_libros_aux.values()))])
                    self.caplibros = almacena_df(self.caplibros,cap_libros_aux).replace(to_replace ='^\W+$|,$', value = '', regex = True) #type: ignore
                    cap_libros_aux={}   
        except AttributeError:
            pass     
        df_libros = self.caplibros    
        return df_libros
    
    def get_software(self, soup, url):
        try:
            tablelib=(soup.find('a', attrs={'name':'software'}).parent)            
            if(str((tablelib).find('h3').contents[0])==('Softwares')):
                blocks_arts = tablelib.find_all('blockquote')
                for block_art in blocks_arts:
                    quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_art)).split())))
                    quote_text_clear=quote_text_clear.replace('&amp;','&')                                              
                    #################################
                    # Pendiente: manejo de excepcion nombre software con mayuscula
                    list_datos=re.split('<i>|<b>',quote_text_clear)
                    dic={'idcvlac':'','autor':'','nombre':'','tipo':'','verificado':'','Nombre comercial':'','contrato/registro':'','lugar':'','fecha':'','plataforma':'', 'ambiente':'', 'Palabras':'','Areas':'', 'Sectores':''}
                    tipo=block_art.find_parent('tr').find_previous_sibling('tr')                    
                    if tipo.find('img') == None:
                        dic['verificado']=False #type: ignore
                    else:
                        dic['verificado']=True  #type: ignore
                    dic['tipo']=tipo.find('b').text
                    dic['idcvlac'] = url[(url.find('='))+1:]
                    for i,item in enumerate(list_datos):
                        if i == 0:
                            try:
                                index1=re.search('(?s:.*)-,|(?s:.*)[A-Z\u00C0-\u00DC],',item.strip().rstrip(',')).end() #type: ignore #re.sub('(?s:.*)![A-Z],','',cadena)).end()
                            except:
                                index1=0
                            dic['autor'] = item[:index1].strip()
                            dic['nombre'] = item[index1+1:].strip()
                        else :
                            dic[item[:item.find(':')]]=re.sub('<[^<]+?>', '',item[item.find(':'):]).lstrip(':').rstrip('. ,').strip()
                    cont_aux=dic['contrato/registro'].split('. En:') 
                    dic['contrato/registro']=cont_aux[0].strip() if len(dic['contrato/registro']) != 0 else ''
                    lugg=cont_aux[1] if len(dic['contrato/registro']) >= 1 else ''
                    try:     
                            #lugg=cont_aux[1] if len(dic['contrato/registro']) >= 1 else ''
                            index_datos=re.search(',(\d{4})',lugg).start()  #type: ignore       
                    except :
                        index_datos= -1
                    dic['lugar']=lugg[:index_datos].strip()
                    dic['fecha']=lugg[index_datos+1:].rstrip('. ,').strip()
                    
                    dic=pd.DataFrame([dict(zip(list(self.software.columns),dic.values()))])
                    self.software = almacena_df(self.software,dic).replace(to_replace ='^\W+$|,$', value = '', regex = True)# type: ignore
                    
        except AttributeError:
            pass
        df_software = self.software  
        return df_software
    
    def get_prototipo(self, soup, url):
        try:
            child=(soup.find('table')).findChildren("tr" , recursive=False)            
            for trs in child:
                h3s=(trs.find('h3'))
                if h3s != None:                
                    if(str(h3s.contents[0])==("Prototipos")):
                        for blockquote in ((h3s.parent.parent.parent).find_all('blockquote')):
                            quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(blockquote)).split())))
                            quote_text_clear=quote_text_clear.replace('&amp;','&')                                                      
                            #################################
                            # Pendiente: manejo de excepcion nombre software con mayuscula
                            list_datos=re.split('<i>|<b>',quote_text_clear)
                            dic={'idcvlac':'','autor':'','nombre':'','tipo':'','verificado':'','Nombre comercial':'','contrato/registro':'','lugar':'','fecha':'', 'Palabras':'','Areas':'', 'Sectores':''}
                            
                            tipo=blockquote.find_parent('tr').find_previous_sibling('tr')                    
                            if tipo.find('img') == None:
                                dic['verificado']=False #type: ignore
                            else:
                                dic['verificado']=True  #type: ignore
                            dic['tipo']=tipo.find('b').text
                            
                            dic['idcvlac'] = url[(url.find('='))+1:]
                            
                            for i,item in enumerate(list_datos):
                                if i == 0:
                                    try:
                                        index1=re.search('(?s:.*)-,|(?s:.*)[A-Z\u00C0-\u00DC],',item.strip().rstrip(',')).end()#type: ignore #re.sub('(?s:.*)![A-Z],','',cadena)).end()
                                    except:
                                        index1=0
                                    dic['autor'] = item[:index1].strip()
                                    dic['nombre'] = item[index1+1:].rstrip(', .').strip()
                                else :
                                    dic[item[:item.find(':')]]=re.sub('<[^<]+?>', '',item[item.find(':'):]).lstrip(':').strip()
                            cont_aux=dic['contrato/registro'].split('. En:') 
                            dic['contrato/registro']=cont_aux[0].strip() if len(dic['contrato/registro']) != 0 else ''
                            lugg=cont_aux[1] if len(dic['contrato/registro']) >= 1 else ''
                            try:     
                                    #lugg=cont_aux[1] if len(dic['contrato/registro']) >= 1 else ''
                                    index_datos=re.search(',(\d{4})',lugg).start() #type: ignore               
                            except :
                                index_datos= -1
                            dic['lugar']=lugg[:index_datos].strip()
                            dic['fecha']=lugg[index_datos+1:].strip()

                            dic=pd.DataFrame([dict(zip(list(self.prototipo.columns),dic.values()))])
                            self.prototipo = almacena_df(self.prototipo,dic).replace(to_replace ='^\W+$|,$', value = '', regex = True)# type: ignore
                            
        except AttributeError:
            pass           
        df_prototipo = self.prototipo    
        return df_prototipo

    def get_tecnologicos(self, soup, url):
        try:
            tablelib=(soup.find('a', attrs={'name':'tecnologicos'}).parent)
            if(str((tablelib).find('h3').contents[0])==('Productos tecnológicos')):
                blocks_arts = tablelib.find_all('blockquote')
                for block_art in blocks_arts:
                    quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_art)).split())))
                    quote_text_clear=quote_text_clear.replace('&amp;','&')                                              
                    #################################
                    # Pendiente: manejo de excepcion nombre software con mayuscula
                    list_datos=re.split('<i>|<b>',quote_text_clear)
                    dic={'idcvlac':'','autor':'','nombre':'','tipo':'','verificado':'','Nombre comercial':'','contrato/registro':'','lugar':'','fecha':'', 'Palabras':'','Areas':'', 'Sectores':''}
                    tipo=block_art.find_parent('tr').find_previous_sibling('tr')                    
                    if tipo.find('img') == None:
                        dic['verificado']=False #type: ignore
                    else:
                        dic['verificado']=True  #type: ignore
                    dic['tipo']=tipo.find('b').text.strip()
                    
                    dic['idcvlac'] = url[(url.find('='))+1:]
                    for i,item in enumerate(list_datos):
                        if i == 0:
                            try:
                                index1=re.search('(?s:.*)-,|(?s:.*)[A-Z\u00C0-\u00DC],',item.strip().rstrip(',')).end() #type: ignore #re.sub('(?s:.*)![A-Z],','',cadena)).end()
                            except:
                                index1=0
                            dic['autor'] = item[:index1].strip()
                            dic['nombre'] = item[index1+1:].strip()
                        else :
                            dic[item[:item.find(':')]]=re.sub('<[^<]+?>', '',item[item.find(':'):]).lstrip(':').strip()
                    cont_aux=dic['contrato/registro'].split('. En:') 
                    dic['contrato/registro']=cont_aux[0].strip() if len(dic['contrato/registro']) != 0 else ''
                    lugg=cont_aux[1] if len(dic['contrato/registro']) >= 1 else ''
                    try:     
                            #lugg=cont_aux[1] if len(dic['contrato/registro']) >= 1 else ''
                            index_datos=re.search(',(\d{4})',lugg).start()  #type: ignore
                    except :
                        index_datos= -1
                    dic['lugar']=lugg[:index_datos].strip()
                    dic['fecha']=lugg[index_datos+1:].strip()
          
                    dic=pd.DataFrame([dict(zip(list(self.tecnologicos.columns),dic.values()))])
                    self.tecnologicos = almacena_df(self.tecnologicos,dic).replace(to_replace ='^\W+$|,$', value = '', regex = True)# type: ignore 
                     
        except AttributeError:
            pass
        df_tecnologicos = self.tecnologicos   
        return df_tecnologicos
        

    def get_empresa_tecnologica(self, soup, url):
        try:
            tablelib=(soup.find('h3', attrs={'id':'base_tecnologica'}).parent.parent.parent)
            if(str((tablelib).find('h3').contents[0])==('Empresas de base tecnológica')):
                blocks_arts = tablelib.find_all('blockquote')
                for block_art in blocks_arts:
                    quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(block_art)).split())))
                    quote_text_clear=quote_text_clear.replace('&amp;','&')                                              
                    #################################
                    # Pendiente: manejo de excepcion nombre software con mayuscula
                    list_datos=re.split('<i>|<b>',quote_text_clear)
                    dic={'idcvlac':'','autores':'','nombre':'','tipo':'','verificado':'','nit':'','Registrado ante la c´mara el':'','verificado':'','Palabras':'','Areas':'', 'Sectores':''}
                    tipo=block_art.find_parent('tr').find_previous_sibling('tr')                    
                    if tipo.find('img') == None:
                        dic['verificado']=False #type: ignore
                    else:
                        dic['verificado']=True  #type: ignore
                    dic['tipo']=tipo.find('b').text
                    
                    dic['idcvlac'] = url[(url.find('='))+1:]
                    for i,item in enumerate(list_datos):
                        if i == 0:
                            try:
                                index1=re.search('(?s:.*)-,|(?s:.*)[A-Z\u00C0-\u00DC],',item.strip().rstrip(',')).end() #type: ignore #re.sub('(?s:.*)![A-Z],','',cadena)).end()
                            except:
                                index1=0
                            dic['autores'] = item[:index1].strip()
                            dic['nombre'] = item[index1+1:].strip()
                        else:
                            separador=item.find(':')
                            if(separador!=-1):
                                dic[item[:separador]]=re.sub('<[^<]+?>', '',item[separador:]).lstrip(':').strip()
                            elif(item.find('Nit')!=-1):
                                dic['nit']=re.sub('<[^<]+?>', '',item[item.rfind('Nit')+3:]).rstrip(', .').strip()         
                            else: pass

                    dic=pd.DataFrame([dict(zip(list(self.empresa_tecnologica.columns),dic.values()))])
                    self.empresa_tecnologica = almacena_df(self.empresa_tecnologica,dic).replace(to_replace ='^\W+$|,$', value = '', regex = True)# type: ignore
                      
        except AttributeError:
            pass            
        df_empresa_tecnologica = self.empresa_tecnologica     
        return df_empresa_tecnologica

    def get_innovacion(self, soup, url):
        try:
            child=(soup.find('table')).findChildren("tr" , recursive=False)            
            for trs in child:
                h3s=(trs.find('h3'))
                if h3s != None:                
                    if(str(h3s.contents[0])==("Innovación generada en la gestión empresarial")):
                        for blockquote in ((h3s.parent.parent.parent).find_all('blockquote')):
                            quote_text_clear=re.sub('<blockquote>|</blockquote>|<br>|<br/>','',(" ".join((str(blockquote)).split())))
                            quote_text_clear=quote_text_clear.replace('&amp;','&')                                                      
                            #################################
                            # Pendiente: manejo de excepcion nombre software con mayuscula
                            list_datos=re.split('<i>|<b>',quote_text_clear)
                            dic={'idcvlac':'','autor':'','nombre':'','tipo':'','verificado':'','Nombre comercial':'','contrato/registro':'','lugar':'','fecha':'', 'Palabras':'','Areas':'', 'Sectores':''}
                            tipo=blockquote.find_parent('tr').find_previous_sibling('tr')                    
                            if tipo.find('img') == None:
                                dic['verificado']=False  # type: ignore
                            else:
                                dic['verificado']=True  # type: ignore
                            dic['tipo']=tipo.find('b').text
                            dic['idcvlac'] = url[(url.find('='))+1:]
                            
                            for i,item in enumerate(list_datos):
                                if i == 0:
                                    try:
                                        index1=re.search('(?s:.*)-,|(?s:.*)[A-Z\u00C0-\u00DC],',item.strip().rstrip(',')).end() #type: ignore #re.sub('(?s:.*)![A-Z],','',cadena)).end()
                                    except:
                                        index1=0
                                    dic['autor'] = item[:index1].strip()
                                    dic['nombre'] = item[index1+1:].strip()
                                else :
                                    dic[item[:item.find(':')]]=re.sub('<[^<]+?>', '',item[item.find(':'):]).lstrip(':').strip()
                            cont_aux=dic['contrato/registro'].split('. En:') 
                            dic['contrato/registro']=cont_aux[0] if len(dic['contrato/registro']) != 0 else ''
                            lugg=cont_aux[1] if len(dic['contrato/registro']) >= 1 else ''
                            try:     
                                    #lugg=cont_aux[1] if len(dic['contrato/registro']) >= 1 else ''
                                    index_datos=re.search(',(\d{4})',lugg).start()  #type: ignore      
                            except :
                                index_datos= -1
                            dic['lugar']=lugg[:index_datos].strip()
                            dic['fecha']=lugg[index_datos+1:].strip()

                            dic=pd.DataFrame([dict(zip(list(self.innovacion_empresarial.columns),dic.values()))])
                            self.innovacion_empresarial = almacena_df(self.innovacion_empresarial,dic).replace(to_replace ='^\W+$|,$', value = '', regex = True)# type: ignore   
                            
        except AttributeError:
            pass           
        df_innovacion = self.innovacion_empresarial  
        return df_innovacion

    def get_cv(self, url):
        #recibe url de un cvlac y lo extrae
        lxml_url = get_lxml(url)            
        df_basico = self.get_basico(lxml_url, url)
        df_articulos = self.get_articulo(lxml_url, url)
        df_actuacion = self.get_actuacion(lxml_url, url)
        df_idioma = self.get_idioma(lxml_url, url)
        df_investiga = self.get_investiga(lxml_url, url)
        df_reconocimiento = self.get_reconocimiento(lxml_url, url)
        df_evaluador = self.get_evaluador(lxml_url, url) 
        df_redes = self.get_redes(lxml_url, url)
        df_identifica = self.get_identificadores(lxml_url, url)
        df_libros = self.get_libro(lxml_url, url)
        df_jurado = self.get_jurado(lxml_url, url)
        df_complementaria = self.get_complementaria(lxml_url, url)
        df_estancias = self.get_estancias(lxml_url, url)
        df_academica = self.get_academica(lxml_url, url)
        df_caplibros = self.get_caplibro(lxml_url, url)
        df_software = self.get_software(lxml_url, url)
        df_prototipo = self.get_prototipo(lxml_url, url)
        df_tecnologicos = self.get_tecnologicos(lxml_url, url)
        df_empresa = self.get_empresa_tecnologica(lxml_url, url)
        df_innovacion = self.get_innovacion(lxml_url, url)
        #limpiar atributos si se desea
        super().__init__()
        return {"basico":df_basico,"articulos":df_articulos,"actuacion":df_actuacion,"idioma":df_idioma,                                #type: ignore    
                "investigacion":df_investiga,"reconocimiento":df_reconocimiento,"evaluador":df_evaluador,                               #type: ignore
                "redes":df_redes,"identificadores":df_identifica,"libros":df_libros,"jurado":df_jurado,                                 #type: ignore
                "complementaria":df_complementaria,"estancias":df_estancias,"academica":df_academica,                                   #type: ignore
                "caplibros":df_caplibros,"software":df_software,"prototipo":df_prototipo,"tecnologicos":df_tecnologicos,                #type: ignore
                "empresa_tecnologica":df_empresa,"innovacion_empresarial":df_innovacion}  
