import pandas as pd
import requests
from bs4 import BeautifulSoup
from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.util import almacena, almacena_df
from cvlac.util import get_lxml, get_gruplacList
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class ExtractorGruplac(ExtractorCvlac):
    
    def __init__(self):
        super().__init__()
        #######
        #El prefijo 'grup' indica un atributo referente a una tabla de cvlac, dicho atributo almacena información
        #de un grupo de cvlacs pertenecientes a un solo gruplac.
        #######
        self.grup_academica=pd.DataFrame(columns=['idcvlac','tipo','institucion','titulo','fecha','proyecto'])
        self.grup_actuacion=pd.DataFrame(columns=['idcvlac','areas'])
        self.grup_articulos=pd.DataFrame(columns=['idcvlac','autores','nombre','tipo','verificado','lugar','revista','issn','editorial','volumen','fasciculo','doi','palabras','sectores'])
        self.grup_basico=pd.DataFrame(columns=['idcvlac','categoria','nombre','nombre_citaciones','nacionalidad','sexo'])
        self.grup_complementaria=pd.DataFrame(columns=['idcvlac','tipo','institucion','titulo','fecha'])
        self.grup_estancias=pd.DataFrame(columns=['idcvlac','nombre','entidad','area','fecha_inicio','fecha_fin'])
        self.grup_evaluador=pd.DataFrame(columns=['idcvlac','ambito','par_evaluador','editorial','revista','fecha','institucion'])
        self.grup_identificadores=pd.DataFrame(columns=['idcvlac','nombre','url'])
        self.grup_idioma=pd.DataFrame(columns=['idcvlac','idioma','habla','escribe','lee','entiende'])
        self.grup_investiga=pd.DataFrame(columns=['idcvlac','nombre','activa'])
        self.grup_jurado=pd.DataFrame(columns=['idcvlac','nombre','titulo','tipo','lugar','programa','orientado','palabras','areas','sectores'])
        self.grup_libros=pd.DataFrame(columns=['idcvlac','autores','nombre','tipo','verificado','lugar','fecha','editorial','isbn','volumen','paginas','palabras','areas','sectores'])
        self.grup_reconocimiento=pd.DataFrame(columns=['idcvlac','nombre','fecha'])
        self.grup_redes=pd.DataFrame(columns=['idcvlac','nombre','url'])
        self.grup_caplibros=pd.DataFrame(columns=['idcvlac','autores','nombre','lugar','verificado','fecha','editorial','isbn','volumen','paginas','palabras','areas','sectores'])
        self.grup_software=pd.DataFrame(columns=['idcvlac','autor','nombre','tipo','verificado','nombre_comercial','contrato_registro','lugar','fecha','plataforma','ambiente','palabras','areas','sectores'])
        self.grup_prototipo=pd.DataFrame(columns=['idcvlac','autor','nombre','tipo','verificado','nombre_comercial','contrato_registro','lugar','fecha','palabras','areas','sectores'])
        self.grup_tecnologicos=pd.DataFrame(columns=['idcvlac','autor','nombre','tipo','verificado','nombre_comercial','contrato_registro','lugar','fecha','palabras','areas','sectores'])
        self.grup_empresa_tecnologica=pd.DataFrame(columns=['idcvlac','autores','nombre','tipo','nit','registro_camara','verificado','palabras','areas','sectores'])
        self.grup_innovacion_empresarial=pd.DataFrame(columns=['idcvlac','autor','nombre','tipo','verificado','nombre_comercial','contrato_registro','lugar','fecha','palabras','areas','sectores'])
        #########
        #El prefijo 'perfil' indica un atributo refente a una tabla especifica del perfil de un gruplac
        #######
        #self.perfil_basico={'idgruplac':[],'nombre':[],'fecha_formacion':[],'lugar':[],'lider':[],'certificacion':[],'pagina_web':[],'email':[],'clasificacion':[],'areas':[],'programas':[],'programas_secundario':[]}
        self.perfil_instituciones={'idgruplac':[],'nombre':[],'aval':[]}
        self.perfil_lineas={'idgruplac':[],'lineas':[]}
        self.perfil_integrantes={'idgruplac':[],'url':[],'integrante':[],'vinculacion':[],'horas':[],'fecha_vinculacion':[]}
        self.perfil_programa_doctorado={'idgruplac':[],'programa':[],'fecha':[],'acto':[],'institucion':[]}
        self.perfil_programa_maestria={'idgruplac':[],'programa':[],'fecha':[],'acto':[],'institucion':[]}
        self.perfil_otro_programa={'idgruplac':[],'programa':[],'fecha':[],'acto':[],'institucion':[]}
        self.perfil_curso_doctorado={'idgruplac':[],'curso':[],'fecha':[],'acto':[],'programa':[]}
        self.perfil_curso_maestria={'idgruplac':[],'curso':[],'fecha':[],'acto':[],'programa':[]}
        self.perfil_articulos={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'lugar':[],'revista':[],'issn':[],'fecha':[],'volumen':[],'fasciculo':[],'paginas':[],'doi':[],'autores':[]}
        self.perfil_libros={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'lugar':[],'fecha':[],'isbn':[],'editorial':[],'autores':[]}
        self.perfil_caplibros={'idgruplac':[],'verificado':[],'tipo':[],'capitulo':[],'lugar':[],'fecha':[],'libro':[],'isbn':[],'volumen':[],'paginas':[],'editorial':[],'autores':[]}
        self.perfil_otros_articulos={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'lugar':[],'revista':[],'issn':[],'fecha':[],'volumen':[],'fasciculo':[],'paginas':[],'autores':[]}
        self.perfil_otros_libros={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'lugar':[],'fecha':[],'isbn':[],'volumen':[],'paginas':[],'editorial':[],'autores':[]}
        self.perfil_diseno_industrial={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'lugar':[],'fecha':[],'disponibilidad':[],'institucion':[],'autores':[]}
        self.perfil_otros_tecnologicos={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'lugar':[],'fecha':[],'disponibilidad':[],'nombre_comercial':[],'institucion':[],'autores':[]}
        self.perfil_prototipos={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'lugar':[],'fecha':[],'disponibilidad':[],'institucion':[],'autores':[]}
        self.perfil_software={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'lugar':[],'fecha':[],'disponibilidad':[],'url':[],'nombre_comercial':[],'nombre_proyecto':[],'institucion':[],'autores':[]}
        self.perfil_empresa_tecnologica={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'fecha':[],'nit':[],'fecha_registro':[],'mercado':[],'autores':[]}
        self.perfil_innovacion_empresarial={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'lugar':[],'fecha':[],'disponibilidad':[],'institucion':[],'autores':[]}
        self.perfil_planta_piloto={'idgruplac':[],'verificado':[],'tipo':[],'nombre':[],'lugar':[],'fecha':[],'disponibilidad':[],'nombre_comercial':[],'institucion':[],'autores':[]}

        ####
        self.perfil_basico=pd.DataFrame(columns=['idgruplac','nombre','fecha_formacion','lugar','lider','certificacion','pagina_web','email','clasificacion','areas','programas','programas_secundario'])
        

        
        
    def get_members_list(self,url):
        #recibe url de un gruplac y retorna la lista de cvlacs que contiene
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
            break
                    
        for a in url_inv:
            url_in = a['href']
            if(url_in.find('https://scienti.minciencias.gov.co/cvlac/visualizador')!=-1):
                dire.append(url_in) 
        return dire 
    
    def get_gruplac_list(self, url):
        #recibe url del buscador scienti que contiene la lista de gruplacs de un departamento
        gruplac_list=[]
        r=requests.get(url, verify=False) #Prescindir de Verify=False
        soup=BeautifulSoup(r.content,'lxml')
        links=soup.find_all('a', attrs={'target':'_blank'})
        for a in links:
            url_gruplac=a['href']
            if(url_gruplac.find('https://scienti.minciencias.gov.co/gruplac/jsp/visualiza')!=-1):
                gruplac_list.append(url_gruplac)
        print(len(gruplac_list))
        return gruplac_list
    
    def get_cvs(self, url_gruplac):
        #recibe url de un gruplac y extrae los cvlacs que contiene
        urls=self.get_members_list(url_gruplac)
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
            df_identifica = self.get_identificadores(lxml_url, url) #REVISAR
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
    
    
    def set_grup_attrs(self,gruplac_list):
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
                print('Error estableciendo atributos del objeto de prefijo grup')
       
    """
    def set_perfil_attrs(self, gruplac_list):
        #recibe una lista de urls de grupos de investigación y rellena los valores de los atributos de forma
        #acumulativa 
        for url in gruplac_list:
            lxml_url = get_lxml(url)
            self.get_perfil_articulos(lxml_url,url)
            self.get_perfil_basico(lxml_url,url)
            self.get_perfil_caplibros(lxml_url,url)
            self.get_perfil_curso_doctorado(lxml_url,url)
            self.get_perfil_curso_maestria(lxml_url,url)
            self.get_perfil_diseno_industrial(lxml_url,url)
            self.get_perfil_empresa_tecnologica(lxml_url,url)
            self.get_perfil_innovacion_empresarial(lxml_url,url)
            self.get_perfil_instituciones(lxml_url,url)
            self.get_perfil_integrantes(lxml_url,url)
            self.get_perfil_lineas(lxml_url,url)
            self.get_perfil_libros(lxml_url,url)
            self.get_perfil_otro_programa(lxml_url,url)
            self.get_perfil_planta_piloto(lxml_url,url)
            self.get_perfil_programa_maestria(lxml_url,url)
            self.get_perfil_programa_doctorado(lxml_url,url)
            self.get_perfil_otros_articulos(lxml_url,url)
            self.get_perfil_software(lxml_url,url)
            self.get_perfil_otros_libros(lxml_url,url)
            self.get_perfil_otros_tecnologicos(lxml_url,url)
            self.get_perfil_prototipos(lxml_url,url)
    """    
    
    def get_perfil_basico(self, soup, url):
        try:
            child=(soup.find('table')).findChildren("tr" , recursive=False) 
            for trs in child:
                td=(trs.find('td'))
                if td != None:               
                    if(str(td.contents[0])==("Datos básicos")):
                        dic2={'idgruplac':'','nombre':'','Año y mes de formación':'','Departamento - Ciudad':'','Líder':'','La información de este grupo se ha certificado':'','Página web':'','E-mail':'','Clasificación':'','Área de conocimiento':'','Programa nacional de ciencia y tecnología':'','Programa nacional de ciencia y tecnología (secundario)':''}           
                        rows=td.parent.parent.find_all('tr') 
                        fid = url.find('=')
                        dic2['idgruplac'] = url[fid+1:]
                        dic2['nombre'] = soup.find('span').text.strip()                     
                        for row in  rows:
                            if len(row.select('td')) == 2:
                                cells = row.findChildren('td')
                                try:
                                    cells[1]=" ".join(cells[1].text.split())
                                    dic2[re.sub('¿|\?','',cells[0].text.strip())]= cells[1]
                                except AttributeError:
                                    print('error gruplac basico url: : ', url)           
                        #dic2=dict(zip(self.perfil_basico.keys(),dic2.values()))  
                        dic2=pd.DataFrame([dict(zip(list(self.perfil_basico.columns),dic2.values()))])
                        self.perfil_basico = almacena_df(self.perfil_basico,dic2)
        except AttributeError:
            pass          
        df_perfil_basico = self.perfil_basico
        return df_perfil_basico

    def get_perfil_instituciones(self, soup, url):        
        try:            
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Instituciones').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')                
                for i in list_tr:
                    dic={'idgruplac':'','nombre':'','aval':''}
                    dic['idgruplac']=(url[fid+1:])                  
                    i_clear=i.text.strip()
                    index=i_clear.rfind('-  (')#posible futuro error: doble espacio
                    dic['nombre']=(i_clear[3:index].strip())
                    dic['aval']=(re.sub(r'[^A-Za-z0-9 ]+','',i_clear[index:]).strip())
                    dic=dict(zip(self.perfil_instituciones.keys(),dic.values()))  
                    self.perfil_instituciones = almacena(self.perfil_instituciones,dic)                                    
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass               
        df_grupintituciones = pd.DataFrame(self.perfil_instituciones)   
        df_grupintituciones = df_grupintituciones.reset_index(drop=True)   
        return df_grupintituciones  

    def get_perfil_lineas(self, soup, url):        
        try:            
            child=soup.find('td', attrs={'class':'celdaEncabezado'},string='Líneas de investigación declaradas por el grupo').find_parent('tr').find_next_siblings('tr')
            if(child!=None):
                dic={'idgruplac':'','lineas':''}
                fid = url.find('=')                
                dic['idgruplac']=(url[fid+1:])
                linea=""
                for i in child:                                       
                    linea=linea+i.text.strip()[3:]+";"
                dic['lineas']=(linea.strip())
                self.perfil_lineas = almacena(self.perfil_lineas,dic)               
        except AttributeError:
            pass          
        except:
            pass        
        df_gruplineas = pd.DataFrame(self.perfil_lineas)   
        df_gruplineas = df_gruplineas.reset_index(drop=True)   
        return df_gruplineas
    
    def get_perfil_integrantes(self, soup, url):
        dfs=pd.DataFrame(columns=self.perfil_integrantes.keys())               
        try:            
            child=soup.find('td', attrs={'class':'celdaEncabezado'},string='Integrantes del grupo').find_parent('table')
            if(child!=None):
                list_url=[]
                links=child.find_all('a', href=True)
                dfs = pd.read_html(str(child),header=1, keep_default_na=False)[0]
                for link in links:                    
                    list_url.append(link['href'])                
                dfs.insert(0, 'url', list_url)
                fid = url.find('=')
                dfs.insert(0, 'idgruplac', url[fid+1:])                              
                dfs.columns=self.perfil_integrantes.keys()
                dfs['integrante']=dfs['integrante'].str.replace(r'[^a-zA-Z\u00C0-\u017F\s]+','', regex=True).str.strip()           
                self.perfil_integrantes= almacena_df(self.perfil_integrantes,dfs)
            else:
                raise Exception
        except AttributeError:
            pass          
        except:
            pass
        print(type(self.perfil_integrantes))
        return self.perfil_integrantes

    def get_perfil_programa_doctorado(self, soup, url):        
        try:            
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Programa académico de doctorado').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')                
                for tr in list_tr:
                    dic={'idgruplac':'','Programa académico':'','Fecha acto administrativo programa':'','Número acto administrativo programa':'','Institución':''}
                    dic['idgruplac']=url[fid+1:]
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<br/>',tr)
                    for i,dato in enumerate(list_datos):
                        dato=re.sub('<[^<]+?>','',dato).strip()                     
                        if i==0:
                            dic[dato[dato.find('-')+2:dato.find(':')]]=dato[dato.find(':'):].lstrip(':').strip() 
                        else:
                            dic[dato[:dato.find(':')]]=dato[dato.find(':'):].lstrip(':').strip()                          
                        
                    dic=dict(zip(self.perfil_programa_doctorado.keys(),dic.values()))
                    self.perfil_programa_doctorado = almacena(self.perfil_programa_doctorado,dic)                                                        
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_programa_doctorado = pd.DataFrame(self.perfil_programa_doctorado)   
        df_programa_doctorado = df_programa_doctorado.reset_index(drop=True)   
        return df_programa_doctorado

    def get_perfil_programa_maestria(self, soup, url):        
        try:            
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Programa académico de maestría').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')                
                for tr in list_tr:
                    dic={'idgruplac':'','Programa académico':'','Fecha acto administrativo programa':'','Número acto administrativo programa':'','Institución':''}
                    dic['idgruplac']=url[fid+1:]
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<br/>',tr)
                    for i,dato in enumerate(list_datos):
                        dato=re.sub('<[^<]+?>','',dato).strip()                     
                        if i==0:                            
                            dic[dato[dato.find('-')+2:dato.find(':')]]=dato[dato.find(':'):].lstrip(':').strip() 
                        else:
                            dic[dato[:dato.find(':')]]=dato[dato.find(':'):].lstrip(':').strip()                          
                        
                    dic=dict(zip(self.perfil_programa_maestria.keys(),dic.values()))
                    self.perfil_programa_maestria = almacena(self.perfil_programa_maestria,dic)                                                        
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_programa_maestria = pd.DataFrame(self.perfil_programa_maestria)   
        df_programa_maestria = df_programa_maestria.reset_index(drop=True)   
        return df_programa_maestria

    def get_perfil_otro_programa(self, soup, url):        
        try:            
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Otro programa académico').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')                
                for tr in list_tr:
                    dic={'idgruplac':'','Programa académico':'','Fecha acto administrativo programa':'','Número acto administrativo programa':'','Institución':''}
                    dic['idgruplac']=url[fid+1:]
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<br/>',tr)
                    for i,dato in enumerate(list_datos):
                        dato=re.sub('<[^<]+?>','',dato).strip()                     
                        if i==0:
                            dic[dato[dato.find('-')+2:dato.find(':')]]=dato[dato.find(':'):].lstrip(':').strip() 
                        else:
                            dic[dato[:dato.find(':')]]=dato[dato.find(':'):].lstrip(':').strip()                          
                        
                    dic=dict(zip(self.perfil_otro_programa.keys(),dic.values()))
                    self.perfil_otro_programa = almacena(self.perfil_otro_programa,dic)                                                        
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_otro_programa = pd.DataFrame(self.perfil_otro_programa)   
        df_otro_programa = df_otro_programa.reset_index(drop=True)   
        return df_otro_programa

    def get_perfil_curso_doctorado(self, soup, url):        
        try:            
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Curso de doctorado').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')                
                for tr in list_tr:
                    dic={'idgruplac':'','Nombre del Curso':'','Fecha acto administrativo curso':'','Número acto administrativo curso':'','Programa académico':''}
                    dic['idgruplac']=url[fid+1:]
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<br/>',tr)
                    for i,dato in enumerate(list_datos):
                        dato=re.sub('<[^<]+?>','',dato).strip()                     
                        if i==0:
                            dic[dato[dato.find('-')+2:dato.find(':')]]=dato[dato.find(':'):].lstrip(':').strip() 
                        else:
                            dic[dato[:dato.find(':')]]=dato[dato.find(':'):].lstrip(':').strip()                          
                        
                    dic=dict(zip(self.perfil_curso_doctorado.keys(),dic.values()))
                    self.perfil_curso_doctorado = almacena(self.perfil_curso_doctorado,dic)                                                        
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_curso_doctorado = pd.DataFrame(self.perfil_curso_doctorado)   
        df_curso_doctorado = df_curso_doctorado.reset_index(drop=True)   
        return df_curso_doctorado

    def get_perfil_curso_maestria(self, soup, url):        
        try:            
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Curso de maestría').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')                
                for tr in list_tr:
                    dic={'idgruplac':'','Nombre del Curso':'','Fecha acto administrativo curso':'','Número acto administrativo curso':'','Programa académico':''}
                    dic['idgruplac']=url[fid+1:]
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<br/>',tr)
                    for i,dato in enumerate(list_datos):
                        dato=re.sub('<[^<]+?>','',dato).strip()                     
                        if i==0:
                            dic[dato[dato.find('-')+2:dato.find(':')]]=dato[dato.find(':'):].lstrip(':').strip() 
                        else:
                            dic[dato[:dato.find(':')]]=dato[dato.find(':'):].lstrip(':').strip()                          
                        
                    dic=dict(zip(self.perfil_curso_maestria.keys(),dic.values()))
                    self.perfil_curso_maestria = almacena(self.perfil_curso_maestria,dic)                                                        
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_curso_maestria = pd.DataFrame(self.perfil_curso_maestria)   
        df_curso_maestria = df_curso_maestria.reset_index(drop=True)   
        return df_curso_maestria

    def get_perfil_articulos(self, soup, url):        
        try:            
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Artículos publicados').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')                
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','lugar':'','revista':'','issn':'','fecha':'','volumen':'','fasciculo':'','paginas':'','doi':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):
                        dato=re.sub('<[^<]+?>','',dato).strip()                                                                    
                        if i==0:
                            dic['tipo']=dato.replace(":","")
                        elif i==1:
                            dic['nombre']=dato
                        elif i==2:
                            separador=re.split('ISSN:|vol:|fasc:|págs:',dato)                       
                            dic['lugar']=separador[0][:separador[0].find(',')]
                            dic['revista']=separador[0][separador[0].find(','):].lstrip(',').strip()
                            dic['issn']=separador[1][:separador[1].find(',')].strip()
                            dic['fecha']=separador[1][separador[1].find(','):].lstrip(',').strip()
                            dic['volumen']=separador[2]
                            dic['fasciculo']=separador[3]
                            dic['paginas']=separador[4].rstrip(',').strip()
                        elif dato=='DOI:':
                            dic['doi']=re.sub(r'http://dx.doi.org/|doi:|https://doi.org/|http://doi.org/','',list_datos[i+1]).strip()
                        else:
                            dic['autores']=dato[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_articulos = almacena(self.perfil_articulos,dic)                                                       
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_articulos = pd.DataFrame(self.perfil_articulos)   
        df_articulos = df_articulos.reset_index(drop=True)   
        return df_articulos

    def get_perfil_libros(self, soup, url):        
        try:                       
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string=' Libros publicados ').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')               
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','lugar':'','fecha':'','isbn':'','editorial':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):                                                                                            
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['nombre']=dato.lstrip(' : ')
                        elif i==2:
                            separador=re.split('ISBN:|Ed\.',dato)                       
                            dic['lugar']=separador[0][:separador[0].find(',')].strip()
                            dic['fecha']=separador[0][separador[0].find(','):].lstrip(',').strip()
                            dic['isbn']=separador[1].strip().rstrip(',')
                            dic['editorial']=separador[2].lstrip(',').strip()
                        else:                            
                            dic['autores']=re.sub('<[^<]+?>','',dato)[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_libros = almacena(self.perfil_libros,dic)                                                      
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_libros = pd.DataFrame(self.perfil_libros)   
        df_libros = df_libros.reset_index(drop=True)   
        return df_libros

    def get_perfil_caplibros(self, soup, url):        
        try:                       
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Capítulos de libro publicados ').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')             
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','capitulo':'','lugar':'','fecha':'','libro':'','isbn':'','volumen':'','paginas':'','editorial':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):                                                                                            
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['capitulo']=dato.lstrip(' : ')
                        elif i==2:
                            #revisar bd, calidad datos con esta separacion                            
                            index_lugar=dato.find(',')                                                                                    
                            dic['lugar']=dato[:index_lugar].strip()                            
                            dato=dato[index_lugar+1:]#dato no tiene lugar
                            index_fecha=dato.find(',')                                                        
                            dic['fecha']=dato[:index_fecha].strip()                                                       
                            dato=dato[index_fecha+1:]                                                      
                            index_isbn=dato.rfind('ISBN:')                            
                            dic['libro']=dato[:index_isbn].strip()
                            dato=dato[index_isbn:]
                            separador=re.split('Vol\.|págs:|Ed\.',dato)
                            dic['isbn']=separador[0][5:].rstrip(',').strip()
                            dic['volumen']=separador[1].rstrip(',').strip()
                            dic['paginas']=separador[2].rstrip(',').strip() 
                            dic['editorial']=separador[3].strip()  
                        else:
                            dic['autores']=re.sub('<[^<]+?>','',dato)[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_caplibros = almacena(self.perfil_caplibros,dic)                                                      
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_caplibros = pd.DataFrame(self.perfil_caplibros)   
        df_caplibros = df_caplibros.reset_index(drop=True).replace(to_replace ='^\W+$|,$', value = '', regex = True)   
        return df_caplibros

    def get_perfil_otros_articulos(self, soup, url):        
        try:            
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Otros artículos publicados').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')                
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','lugar':'','revista':'','issn':'','fecha':'','volumen':'','fasciculo':'','paginas':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):
                        dato=re.sub('<[^<]+?>','',dato).strip()                                                                    
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['nombre']=dato.replace(":","").strip()
                        elif i==2:
                            separador=re.split('ISSN:|vol:|fasc:|págs:',dato)                       
                            dic['lugar']=separador[0][:separador[0].find(',')]
                            dic['revista']=separador[0][separador[0].find(','):].lstrip(',').strip()
                            dic['issn']=separador[1][:separador[1].find(',')].strip()
                            dic['fecha']=separador[1][separador[1].find(','):].lstrip(',').strip()
                            dic['volumen']=separador[2]
                            dic['fasciculo']=separador[3]
                            dic['paginas']=separador[4].rstrip(',').strip()                       
                        else:
                            dic['autores']=dato[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_otros_articulos = almacena(self.perfil_otros_articulos,dic)                                                       
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_otros_articulos = pd.DataFrame(self.perfil_otros_articulos)   
        df_otros_articulos = df_otros_articulos.reset_index(drop=True)   
        return df_otros_articulos

    def get_perfil_otros_libros(self, soup, url):        
        try:                       
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string=' Otros Libros publicados ').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')               
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','lugar':'','fecha':'','isbn':'','volumen':'','paginas':'','editorial':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):                                                                                            
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['nombre']=dato.lstrip(' : ')
                        elif i==2:
                            separador=re.split('ISBN:|vol:|págs:|Ed\.',dato)                       
                            dic['lugar']=separador[0][:separador[0].find(',')].strip()
                            dic['fecha']=separador[0][separador[0].find(','):].lstrip(',').strip()
                            dic['isbn']=separador[1].strip().rstrip(',')
                            dic['volumen']=separador[2].strip()
                            dic['paginas']=separador[3].strip().rstrip(',')
                            dic['editorial']=separador[4].lstrip(',').strip()
                        else:                            
                            dic['autores']=re.sub('<[^<]+?>','',dato)[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_otros_libros = almacena(self.perfil_otros_libros,dic)                                                      
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_otros_libros = pd.DataFrame(self.perfil_otros_libros)   
        df_otros_libros = df_otros_libros.reset_index(drop=True)   
        return df_otros_libros

    def get_perfil_diseno_industrial(self, soup, url):        
        try:                       
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Diseños industriales').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')               
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','lugar':'','fecha':'','disponibilidad':'','institucion':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):                                                                                            
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['nombre']=dato.lstrip(' : ')
                        elif i==2:
                            #Pendiente: buscar y verificar separadores
                            separador=re.split('Disponibilidad:|Institución financiadora:',dato)                       
                            dic['lugar']=separador[0][:separador[0].find(',')].strip()
                            dic['fecha']=separador[0][separador[0].find(','):].lstrip(',').strip()
                            dic['disponibilidad']=separador[1].strip().rstrip(',')
                            dic['institucion']=separador[2].strip()
                        else:                            
                            dic['autores']=re.sub('<[^<]+?>','',dato)[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_diseno_industrial = almacena(self.perfil_diseno_industrial,dic)                                                      
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_diseno_industrial = pd.DataFrame(self.perfil_diseno_industrial)   
        df_diseno_industrial = df_diseno_industrial.reset_index(drop=True)   
        return df_diseno_industrial  

    def get_perfil_otros_tecnologicos(self, soup, url):        
        try:                       
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Otros productos tecnológicos').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')               
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','lugar':'','fecha':'','disponibilidad':'','nombre_comercial':'','institucion':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):                                                                                            
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['nombre']=dato.lstrip(' : ')
                        elif i==2:
                            #Pendiente: buscar y verificar separadores
                            separador=re.split('Disponibilidad:|Nombre comercial:',dato)                       
                            dic['lugar']=separador[0][:separador[0].find(',')].strip()
                            dic['fecha']=separador[0][separador[0].find(','):].lstrip(',').strip()
                            dic['disponibilidad']=separador[1].strip().rstrip(',')
                            dic['nombre_comercial']=separador[2].strip()
                        elif i==3:
                            dic['institucion']=dato[dato.find(':')+1:].strip()
                        else:                            
                            dic['autores']=re.sub('<[^<]+?>','',dato)[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_otros_tecnologicos = almacena(self.perfil_otros_tecnologicos,dic)                                                      
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_otros_tecnologicos = pd.DataFrame(self.perfil_otros_tecnologicos)   
        df_otros_tecnologicos = df_otros_tecnologicos.reset_index(drop=True)   
        return df_otros_tecnologicos

    def get_perfil_prototipos(self, soup, url):        
        try:                       
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Prototipos').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')               
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','lugar':'','fecha':'','disponibilidad':'','institucion':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):                                                                                            
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['nombre']=dato.lstrip(' : ')
                        elif i==2:
                            #Pendiente: buscar y verificar separadores
                            separador=re.split('Disponibilidad:|Institución financiadora:',dato)                       
                            dic['lugar']=separador[0][:separador[0].find(',')].strip()
                            dic['fecha']=separador[0][separador[0].find(','):].lstrip(',').strip()
                            dic['disponibilidad']=separador[1].strip().rstrip(',')
                            dic['institucion']=separador[2].strip()
                        else:                            
                            dic['autores']=re.sub('<[^<]+?>','',dato)[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_prototipos = almacena(self.perfil_prototipos,dic)                                                      
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_prototipos = pd.DataFrame(self.perfil_prototipos)   
        df_prototipos = df_prototipos.reset_index(drop=True)   
        return df_prototipos

    def get_perfil_software(self, soup, url):        
        try:                       
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Softwares ').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')               
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','lugar':'','fecha':'','disponibilidad':'','url':'','nombre_comercial':'','nombre_proyecto':'','institucion':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):                                                                                            
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['nombre']=dato.lstrip(' : ')
                        elif i==2:
                            #Pendiente: buscar y verificar separadores
                            separador=re.split('Disponibilidad:|, Sitio web:',dato)                       
                            dic['lugar']=separador[0][:separador[0].find(',')].strip()
                            dic['fecha']=separador[0][separador[0].find(','):].lstrip(',').strip()
                            dic['disponibilidad']=separador[1].strip()
                            dic['url']=separador[2].strip()
                        elif i==3:
                            index=dato.find(', Nombre del proyecto:')                                                                             
                            dic['nombre_comercial']=dato[dato.find(':')+1:index].lstrip(',').strip()
                            dato=dato[index:]
                            dic['nombre_proyecto']=dato[dato.find(':')+1:].strip()
                        elif i==4:
                            dic['institucion']=dato[dato.find(':')+1:].strip()                       
                        else:                            
                            dic['autores']=re.sub('<[^<]+?>','',dato)[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_software = almacena(self.perfil_software,dic)                                                                       
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_software = pd.DataFrame(self.perfil_software)   
        df_software = df_software.reset_index(drop=True)   
        return df_software

    def get_perfil_empresa_tecnologica(self, soup, url):        
        try:                       
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Empresas de base tecnológica ').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')               
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','fecha':'','nit':'','fecha_registro':'','mercado':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):                                                                                            
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['nombre']=dato.lstrip(' : ')
                        elif i==2:
                            #Pendiente: buscar y verificar separadores
                            separador=re.split('NIT:|Fecha de registro ante cámara:',dato)                       
                            dic['fecha']=separador[0].strip().rstrip(',')
                            dic['nit']=separador[1].strip().rstrip(',')
                            dic['fecha_registro']=separador[2].strip()
                        elif i==3:
                            dic['mercado']=dato.strip()
                        else:                            
                            dic['autores']=re.sub('<[^<]+?>','',dato)[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_empresa_tecnologica = almacena(self.perfil_empresa_tecnologica,dic)                                                                        
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_empresa_tecnologica = pd.DataFrame(self.perfil_empresa_tecnologica)   
        df_empresa_tecnologica = df_empresa_tecnologica.reset_index(drop=True)   
        return df_empresa_tecnologica

    def get_perfil_innovacion_empresarial(self, soup, url):        
        try:                       
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Innovaciones generadas en la Gestión Empresarial').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')               
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','lugar':'','fecha':'','disponibilidad':'','institucion':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):                                                                                            
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['nombre']=dato.lstrip(' : ')
                        elif i==2:
                            #Pendiente: buscar y verificar separadores
                            separador=re.split('Disponibilidad:|Institución financiadora:',dato)                       
                            dic['lugar']=separador[0][:separador[0].find(',')].strip()
                            dic['fecha']=separador[0][separador[0].find(','):].lstrip(',').strip()
                            dic['disponibilidad']=separador[1].strip().rstrip(',')
                            dic['institucion']=separador[2].strip()
                        else:                            
                            dic['autores']=re.sub('<[^<]+?>','',dato)[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_innovacion_empresarial = almacena(self.perfil_innovacion_empresarial,dic)                                                                         
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_innovacion_empresarial = pd.DataFrame(self.perfil_innovacion_empresarial)   
        df_innovacion_empresarial = df_innovacion_empresarial.reset_index(drop=True)   
        return df_innovacion_empresarial

    def get_perfil_planta_piloto(self, soup, url):        
        try:                       
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Plantas piloto').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')               
                for tr in list_tr:
                    dic={'idgruplac':'','verificado':'','tipo':'','nombre':'','lugar':'','fecha':'','disponibilidad':'','nombre_comercial':'','institucion':'','autores':''}
                    dic['idgruplac']=url[fid+1:] 
                    dic['verificado'] = False if tr.find('img')==None else True
                    tr=" ".join(str(tr).split())
                    list_datos=re.split('<strong>|</strong>|<br/>',tr)
                    list_datos.pop(0)
                    for i,dato in enumerate(list_datos):                                                                                            
                        if i==0:
                            dic['tipo']=dato
                        elif i==1:
                            dic['nombre']=dato.lstrip(' : ')
                        elif i==2:
                            #Pendiente: buscar y verificar separadores
                            separador=re.split('Disponibilidad:|Nombre comercial:',dato)                       
                            dic['lugar']=separador[0][:separador[0].find(',')].strip()
                            dic['fecha']=separador[0][separador[0].find(','):].lstrip(',').strip()
                            dic['disponibilidad']=separador[1].strip().rstrip(',')
                            dic['nombre_comercial']=separador[2].strip()
                        elif i==3:
                            dic['institucion']=dato[dato.find(':')+1:].strip()
                        else:                            
                            dic['autores']=re.sub('<[^<]+?>','',dato)[dato.find(':'):].lstrip(':').strip()  
                    self.perfil_planta_piloto = almacena(self.perfil_planta_piloto,dic)                                                      
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass        
        df_planta_piloto = pd.DataFrame(self.perfil_planta_piloto)   
        df_planta_piloto = df_planta_piloto.reset_index(drop=True)   
        return df_planta_piloto

##############
    def __del__(self):
        print('ExtractorGruplacList Object Destroyed')
