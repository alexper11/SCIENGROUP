import pandas as pd
import requests
from bs4 import BeautifulSoup
from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.util import almacena
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
        self.perfil_basico={'idgruplac':[],'nombre':[],'fecha_formacion':[],'lugar':[],'lider':[],'certificacion':[],'pagina_web':[],'email':[],'clasificacion':[],'areas':[],'programas':[],'programas_secundario':[]}
        self.perfil_intituciones={'idgruplac':[],'nombre':[],'aval':[]}
        self.perfil_lineas={'idgruplac':[],'lineas':[]}
        self.perfil_integrantes={'idgruplac':[],'url':[],'integrante':[],'vinculacion':[],'horas':[],'fecha_vinculacion':[]}

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
                
    #procesamiento de datos

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
                        dic2=dict(zip(self.perfil_basico.keys(),dic2.values()))  
                        self.perfil_basico = almacena(self.perfil_basico,dic2)
        except AttributeError:
            pass          
        df_perfil_basico = pd.DataFrame(self.perfil_basico)   
        df_perfil_basico = df_perfil_basico.reset_index(drop=True)   
        return df_perfil_basico

    def get_perfil_intituciones(self, soup, url):
        dic={'idgruplac':[],'nombre':[],'aval':[]}
        try:            
            list_tr=soup.find('td', attrs={'class':'celdaEncabezado'},string='Instituciones').find_parent('tr').find_next_siblings('tr')
            if(list_tr!=None):
                fid = url.find('=')
                for i in list_tr:
                    dic['idgruplac'].append(url[fid+1:])
                    i_clear=i.text.strip()
                    index=i_clear.rfind('-  (')#posible futuro error: doble espacio
                    dic['nombre'].append(i_clear[3:index].strip())
                    dic['aval'].append(re.sub(r'[^A-Za-z0-9 ]+','',i_clear[index:]).strip())                                     
            else:
                raise Exception  
        except AttributeError:
            pass          
        except:
            pass
        self.perfil_intituciones = dic
        df_grupintituciones = pd.DataFrame(self.perfil_intituciones)   
        df_grupintituciones = df_grupintituciones.reset_index(drop=True)   
        return df_grupintituciones  

    def get_perfil_lineas(self, soup, url):
        dic={'idgruplac':[],'linea':[]}
        try:            
            child=soup.find('td', attrs={'class':'celdaEncabezado'},string='Líneas de investigación declaradas por el grupo').find_parent('tr').find_next_siblings('tr')
            if(child!=None):
                fid = url.find('=')                
                dic['idgruplac'].append(url[fid+1:])
                linea=""
                for i in child:                                       
                    linea=linea+i.text.strip()[3:]+";"
                dic['linea'].append(linea.strip())
                
        except AttributeError:
            pass          
        except:
            pass
        self.perfil_lineas = dic
        print(dic)
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
            else:
                raise Exception
        except AttributeError:
            pass          
        except:
            pass      
        return dfs
##############
    def __del__(self):
        print('ExtractorGruplacList Object Destroyed')
