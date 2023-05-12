import time
import requests
import json
import pandas as pd


class ExtractorScopus:
    
    def __init__(self, api_key, inst_token):
        self.autores={"nombre":[],"nombre_index":[],"autor_id":[],"eid":[],"orcid":[],"documentos":[],"fecha_creacion":[],"documentos_citados":[],
                     "citaciones":[],"h_index":[],"co_autores":[],"estado":[],"areas":[],"rango_publicacion":[],
                     "institucion":[],"affil_id":[],"departamento":[], "idgruplac":[], "nombre_grupo":[], "idcvlac":[]}
            #Agregar indexed name
        self.articulos={"scopus_id":[],"eid":[],"titulo":[],"creador":[],"nombre_publicacion":[],"editorial":[],"issn":[],"isbn":[],
                        "volumen":[],"issue":[],"numero_articulo":[],"pag_inicio":[],"pag_fin":[],"pag_count":[],"fecha_publicacion":[],"idioma":[],
                        "doi":[],"citado":[],"link":[],"institucion":[],"abstract":[],"affil_id":[],"tema":[],"tipo_fuente":[], "tipo_documento":[],
                        "etapa_publicacion":[], "autores":[],"autores_id":[],"tipo_acceso":[],"palabras_clave_autor":[],"palabras_clave_index":[],
                        "agencia_fundadora":[],"pais":[], "idgruplac":[], "nombre_grupo":[]}
            #Agregar indexed name
        
        self.API_KEY=api_key
        self.INST_TOKEN=inst_token
        
    def get_auid_list(self, affilid):
        result=''
        s=0
        url = f'https://api.elsevier.com/content/search/author?query=AF-ID({affilid})&start=0&count=200&field=dc:identifier'
        tries=3
        TotalId=0
        for i in range(tries):
            try:    
                response = requests.get(url,
                                            headers={'Accept':'application/json',
                                                    'X-ELS-APIKey': self.API_KEY,
                                                    'X-ELS-Insttoken': self.INST_TOKEN})#, verify=False)#eliminar verify=False
                
                result = response.json()    
                authorIdList=[''.join(filter(str.isdigit,str(r['dc:identifier']))) for r in result['search-results']["entry"]]
                TotalId= int(result['search-results']['opensearch:totalResults'])
                s=200
            except:
                #print(result)
                if result['search-results']['opensearch:totalResults']==0 or result['search-results']['opensearch:totalResults']=='0':
                        authorIdList=[]
                        #print('ok')
                        break
                if i < tries - 1:
                    continue
                else:
                    print('Error al extraer auid_list')
                    print(response.headers)
            break
        
        while s <= TotalId:
            time.sleep(0.45)
            url = f'https://api.elsevier.com/content/search/author?query=AF-ID({affilid})&start={s}&count=200&field=dc:identifier'
            tries=3
            for i in range(tries):
                try:    
                    response = requests.get(url,
                                                headers={'Accept':'application/json',
                                                        'X-ELS-APIKey': self.API_KEY,
                                                        'X-ELS-Insttoken': self.INST_TOKEN})#, verify=False)#eliminar verify=False
                    
                    result = response.json()
                    
                    tempList=[''.join(filter(str.isdigit,str(r['dc:identifier']))) for r in result['search-results']["entry"]]
                    authorIdList.extend(tempList)
                    
                except KeyError:
                    #print('KeyError al extraer auid_list')
                    #print(result)
                    if result['search-results']['opensearch:totalResults']==0 or result['search-results']['opensearch:totalResults']=='0':
                        authorIdList=[]
                        break
                    #raise
                    
                except:
                    print(result)    
                    if i < tries - 1:
                        continue
                    else:
                        print('Error al extraer auid_list')
                        print(response.headers)
                        print(result) 
                break
            s=s+200
                
        return authorIdList

    def get_field(self, field, r):
        if field=="subject-areas":
            try:
                c=0
                areas=''
                if isinstance(r, type(None)):
                        text=''
                elif isinstance(r[field], type(None)):
                    text=''
                elif isinstance(r[field]['subject-area'], list):
                    for rs in r[field]['subject-area']:
                        if c==0:
                            areas=str(rs['$'])
                        else:
                            areas=areas+';'+str(rs['$'])
                        c=1
                    text= areas
                else:
                    text=str(r[field]['subject-area']['$'])
            except KeyError:
                text=''
            except TypeError:
                text=''
        elif field=="date-created":
            try:
                date= str(r[field]['@day'])+'/'+str(r[field]['@month'])+'/'+str(r['date-created']['@year'])
            except KeyError:
                date=''
            text=date
        elif field=="preferred-name":
            text=str(r[field]['given-name'])+' '+str(r[field]['surname'])
        elif field=="indexed-name":
            try:
                text=str(r["preferred-name"][field])
            except:
                text=''
        
        elif field=="publication-range":
            try:
                text=str(r[field]['@start'])+'-'+str(r[field]['@end'])
            except KeyError:
                text=''
        elif field=="inst":
            if isinstance(r, list):
                c=0
                insts=''
                for i in r:
                    if c==0:
                        try:
                            insts=str(i['ip-doc']['parent-preferred-name']['$'])
                        except KeyError:
                            try:
                                insts=str(i['ip-doc']['preferred-name']['$'])
                            except KeyError:
                                insts=' '
                        c=1
                    else:
                        try:
                            insts=insts+';'+str(i['ip-doc']['parent-preferred-name']['$'])
                        except KeyError:
                            try:
                                insts=insts+';'+str(i['ip-doc']['preferred-name']['$'])
                            except KeyError:
                                insts=insts+';'+' '
                text=insts
            else:
                try:
                    text=str(r['ip-doc']['parent-preferred-name']['$'])
                except KeyError:
                    try:
                        text=str(r['ip-doc']['preferred-name']['$'])
                    except KeyError:
                        text=''     
        elif field=="inst_id":
            if isinstance(r, list):
                c=0
                insts=''
                for i in r:
                    if c==0:
                        try:
                            insts=str(i['@affiliation-id'])
                        except:
                            insts=' '
                        c=1
                    else:
                        try:
                            insts=insts+';'+str(i['@affiliation-id'])
                        except: 
                            insts=insts+';'+' '
                text=insts
            else:
                try:
                    text=str(r['@affiliation-id'])
                except:
                    text=''
        elif field=="depart":
            if isinstance(r, list):
                c=0
                departs=''
                for d in r:
                    if c==0:
                        if 'parent-preferred-name' in d['ip-doc'].keys():
                            departs=str(d['ip-doc']['preferred-name']['$'])
                        else:
                            departs=' '
                        c=1
                    else:
                        if 'parent-preferred-name' in d['ip-doc'].keys(): 
                            departs=departs+';'+str(d['ip-doc']['preferred-name']['$'])
                        else:
                            departs=departs+';'+' '
                text=departs
            else:
                if 'parent-preferred-name' in r['ip-doc'].keys():
                    text=str(r['ip-doc']['preferred-name']['$'])
                else:
                    text=''
        else:    
            try:
                text = str(r[field])
            except KeyError:
                text =''
        
        return text
    
    def get_authors_df(self, authors):    
        
        print('Extrayendo autores...')
        count=0
        for author in authors:   
            print('Extrayendo author id: ',author,'...',count+1,' de ',len(authors))
            time.sleep(0.3)
            url = f'https://api.elsevier.com/content/author/author_id/{author}?view=ENHANCED'
            tries=3
            for i in range(tries):
                try:
                    response = requests.get(url,
                                            headers={'Accept':'application/json',
                                                'X-ELS-APIKey': self.API_KEY,
                                                'X-ELS-Insttoken': self.INST_TOKEN})#, verify=False)#eliminar verify=False
                    
                    result = response.json()
                    r=result['author-retrieval-response'][0]['coredata']
                    r2=result['author-retrieval-response'][0]
                    r3=result['author-retrieval-response'][0]['author-profile']
                    r4=result['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation']
                    flag=True
                except:
                    if i < tries - 1: 
                        continue
                    else:
                        flag=False
                        print('Error al extraer el autor(authors_df): ',author)
                        #Poner excepción para agotamiento de request del servicio api scopus
                        #RESPONSE
                        try:
                            if (response.headers['X-RateLimit-Remaining']=='0') or (response.headers['X-RateLimit-Remaining']==0):
                                return 'API Error: Limite de solicitudes de la API alcanzado' 
                            elif result['service-error']['status']:
                                return 'API Error: '+result['service-error']['status']['statusText']
                            else:
                                pass
                        except KeyError:
                            print('KeyError: X-RateLimit-Remaining')
                            print(response.headers)
                        except:
                            print('Unknown error:')
                            print(response.headers)    
                break
            
            if flag==True:
                pass
            else:
                continue        
            
            self.autores['eid'].append(self.get_field('eid',r))
            self.autores['autor_id'].append(''.join(filter(str.isdigit,str(r['dc:identifier']))))
            self.autores['orcid'].append(self.get_field('orcid',r))
            self.autores['documentos'].append(self.get_field('document-count',r))
            self.autores['documentos_citados'].append(self.get_field('cited-by-count',r))
            self.autores['citaciones'].append(self.get_field('citation-count',r))
            self.autores['h_index'].append(self.get_field('h-index',r2))
            self.autores['co_autores'].append(self.get_field('coauthor-count',r2))
            self.autores['areas'].append(self.get_field('subject-areas',r2))
            self.autores['estado'].append(self.get_field('status',r3))
            self.autores['fecha_creacion'].append(self.get_field('date-created',r3))
            self.autores['nombre'].append(self.get_field('preferred-name',r3))
            self.autores['nombre_index'].append(self.get_field("indexed-name",r3))
            self.autores['rango_publicacion'].append(self.get_field('publication-range',r3))
            self.autores['institucion'].append(self.get_field('inst',r4))
            self.autores['affil_id'].append(self.get_field('inst_id',r4))
            self.autores['departamento'].append(self.get_field('depart',r4))
            self.autores['idgruplac'].append('')
            self.autores['nombre_grupo'].append('')
            self.autores['idcvlac'].append('')
            count=count+1
            
        
        df_autores = pd.DataFrame(self.autores) 
        df_autores.drop_duplicates(subset ="autor_id", inplace = True)
        df_autores= df_autores.reset_index(drop=True).reset_index(drop=True).replace(to_replace ='&amp;', value = '&', regex=True)
        self.__init__(self.API_KEY, self.INST_TOKEN)
        return df_autores
    
    def get_field_search(self, field, r, key=''):
        if key!='':
            if key == 'page_start':
                try:
                    if isinstance(r[field], type(None)):
                        text=''
                    else:
                        text = str(r[field].split('-')[0])
                except:
                    text =''
                    
            elif key == 'page_end':
                try:
                    if isinstance(r[field], type(None)):
                        text=''
                    else:
                        text = str(r[field].split('-')[1])
                except:
                    text =''
            else:
                try:
                    c=0
                    aff=''
                    if isinstance(r, type(None)):
                        text=''
                    elif isinstance(r[field], list):
                        if field=='link':
                            for rs in r[field]:
                                if rs[key] == 'scopus':
                                    aff=str(rs['@href'])
                        else:
                            for rs in r[field]:
                                    if c==0:
                                        aff=str(rs[key])
                                    elif key=='authid' or key=='$':
                                        aff=aff+';'+str(rs[key])
                                    else:
                                        aff=aff+';'+str(rs[key])
                                    c=1
                        text= aff
                    else:
                        if isinstance(r[field][key], type(None)):
                            text=''
                        else:
                            text=str(r[field][key])
                except KeyError:
                    text=''
                except TypeError:
                    text=''
        
        else:
            try:
                if isinstance(r, type(None)):
                        text=''
                elif field=="openaccess":
                    if r[field]=="1": 
                        text='Open Access'
                    else: 
                        text='' 
                else:
                    if isinstance(r[field], type(None)):
                        text=''
                    else:
                        text = str(r[field])
            except KeyError:
                text =''
            except TypeError:
                text=''
        return text
    
    def get_page_count(self,scopus_id,condition):
        if condition=='':
            page_count = ''
        else:
            result=''
            url=f'https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}?view=FULL'
            tries=3
            for i in range(tries):
                try:
                    response = requests.get(url,
                                            headers={'Accept':'application/json',
                                            'X-ELS-APIKey': self.API_KEY,
                                            'X-ELS-Insttoken': self.INST_TOKEN})#, verify=False)#eliminar verify=False
                        
                    result = response.json()
                    try:
                        page_count=str(result["abstracts-retrieval-response"]["item"]["bibrecord"]["head"]["source"]["volisspag"]["pagecount"]["$"])
                    except KeyError:
                        page_count=''
                except:
                    print(result)
                    if i < tries - 1:
                        continue
                    else:
                        print('Error al extraer page_count de scopus id:',scopus_id)
                        page_count=''
                break
        return page_count
    """
    def get_pub_stage(self,scopus_id):
        result=''
        url=f'https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}?view=FULL'
        tries=3
        for i in range(tries):
            try:
                response = requests.get(url,
                                        headers={'Accept':'application/json',
                                        'X-ELS-APIKey': self.API_KEY,
                                        'X-ELS-Insttoken': self.INST_TOKEN}, verify=False) #eliminar verify=False
                        
                result = response.json()
                try:
                    stage=str(result["abstracts-retrieval-response"]["item"]["ait:process-info"]["ait:status"]["@stage"])
                except:
                    stage=''
            except:
                print(result)
                if i < tries - 1:
                    continue
                else:
                    print('Error al extraer page_count de scopus id:',scopus_id)
            break
        return stage
    """
    def get_eid_list(self,affil):
        result=''
        scopusid_list=[]
        eid_list=[]
        cursor=0
        tries=3
        url = f'https://api.elsevier.com/content/search/scopus?query=af-id({affil})&start=0&count=1&field=dc:identifier&view=STANDARD'
        for i in range(tries):
            try:
                response = requests.get(url,
                                        headers={'Accept':'application/json',
                                        'X-ELS-APIKey': self.API_KEY,
                                        'X-ELS-Insttoken': self.INST_TOKEN})#, verify=False) #eliminar verify=False
                
                result = response.json()
                TotalArt = int(result['search-results']['opensearch:totalResults'])
            except:
                print(result)
                if i < tries - 1:
                    continue
                else:
                    print('Error al extraer scopus_id list:',affil)
                    TotalArt=0
            break      
        while cursor <= TotalArt:
            url = f'https://api.elsevier.com/content/search/scopus?query=af-id({affil})&start={cursor}&count=200&field=dc:identifier,eid&view=STANDARD'
            tries=3
            for i in range(tries):
                try:
                    response = requests.get(url,
                                            headers={'Accept':'application/json',
                                            'X-ELS-APIKey': self.API_KEY,
                                            'X-ELS-Insttoken': self.INST_TOKEN})#, verify=False) #eliminar verify=False
                    
                    result = response.json()        
                    flag=True
                except:
                    print(result)
                    if i < tries - 1:
                        continue
                    else:
                        print('Error al extraer el scopusid list de autor: ',affil)
                        flag=False
                break
            cursor = cursor + 200
            if flag==True:
                pass
            else:
                continue
            
            try:
                articles=result['search-results']['entry']
            except KeyError:
                print(result)
                print('KEY ERROR EN get_eid_list')
                continue
            
            for article in articles:
                #scopusid_list.append(''.join(filter(str.isdigit,str(article['dc:identifier']))))
                try:
                    eid_list.append(str(article['eid']))  #USAR EID
                except:
                    print('eid Key error')
                    print(article)
                    print('affilition:', affil)
                    
        #return scopusid_list   
        return eid_list
    """    
    def get_articles_lite(self, author_list):
        result=''
        for author in author_list:
            cursor=0
            tries=3
            #url = f'https://api.elsevier.com/content/search/scopus?query=au-id({author})&cursor=*&count=25&view=COMPLETE'
            url = f'https://api.elsevier.com/content/search/scopus?query=au-id({author})&start={cursor}&count=25&view=COMPLETE'
            
            for i in range(tries):
                try:
                    response = requests.get(url,
                                            headers={'Accept':'application/json',
                                            'X-ELS-APIKey': self.API_KEY,
                                            'X-ELS-Insttoken': self.INST_TOKEN}, verify=False) #eliminar verify=False
                    
                    result = response.json()
                    TotalArt = int(result['search-results']['opensearch:totalResults'])
                    flag=True
                except:
                    print(result)
                    if i < tries - 1:
                        continue
                    else:
                        print('Error al extraer autor(articles_df):',author)
                        flag=False
                break
            if flag==True:
                pass
            else:
                continue          
            #cursor_next=result['search-results']['cursor']['@next']
            cursor=25
            try:
                articles=result['search-results']['entry']
            except KeyError:
                print(result)
                continue
            
            for article in articles:
                
                self.articulos['scopus_id'].append(''.join(filter(str.isdigit,str(article['dc:identifier']))))
                self.articulos['eid'].append(self.get_field_search('eid',article))
                self.articulos['titulo'].append(self.get_field_search('dc:title',article))
                self.articulos['creador'].append(self.get_field_search('dc:creator',article))
                self.articulos['nombre_publicacion'].append(self.get_field_search('prism:publicationName',article))
                self.articulos['issn'].append(self.get_field_search('prism:issn',article))
                self.articulos['volumen'].append(self.get_field_search('prism:volume',article))
                self.articulos['issue'].append(self.get_field_search('prism:issueIdentifier',article))
                self.articulos['numero_articulo'].append(self.get_field_search('article-number',article))
                self.articulos['pag_inicio'].append(self.get_field_search('prism:pageRange',article,key='page_start'))
                self.articulos['pag_fin'].append(self.get_field_search('prism:pageRange',article,key='page_end'))
                self.articulos['pag_count'].append(self.get_page_count(self.articulos['scopus_id'][-1],self.articulos['pag_inicio'][-1]))
                self.articulos['fecha_publicacion'].append(self.get_field_search('prism:coverDate',article))
                self.articulos['doi'].append(self.get_field_search('prism:doi',article))
                self.articulos['citado'].append(self.get_field_search('citedby-count',article))
                self.articulos['link'].append(self.get_field_search('link',article,key='@ref'))
                self.articulos['etapa_publicacion'].append(self.get_pub_stage(self.articulos['scopus_id'][-1]))
                self.articulos['institucion'].append(self.get_field_search('affiliation',article,key='affilname'))
                self.articulos['tipo_fuente'].append(self.get_field_search('prism:aggregationType',article))
                self.articulos['tipo_documento'].append(self.get_field_search('subtypeDescription',article))
                self.articulos['autores'].append(self.get_field_search('author',article,key='authname'))
                self.articulos['autores_id'].append(self.get_field_search('author',article,key='authid'))
                self.articulos['tipo_acceso'].append(self.get_field_search('openaccess',article))
                #self.articulos['palabras_clave'].append(self.get_field_search('authkeywords',article))
                self.articulos['agencia_fundadora'].append(self.get_field_search('fund-sponsor',article))
                
            while cursor <= TotalArt:
                #url = f'https://api.elsevier.com/content/search/scopus?query=au-id({author})&cursor={cursor_next}&count=25&view=COMPLETE'
                url = f'https://api.elsevier.com/content/search/scopus?query=au-id({author})&start={cursor}&count=25&view=COMPLETE'
                tries=3
                for i in range(tries):
                    try:
                        response = requests.get(url,
                                                headers={'Accept':'application/json',
                                                'X-ELS-APIKey': self.API_KEY,
                                                'X-ELS-Insttoken': self.INST_TOKEN}, verify=False) #eliminar verify=False
                        
                        result = response.json()
                        #cursor_next=str(result['search-results']['cursor']['@next'])
                        cursor = cursor + 25        
                        flag=True
                    except:
                        print(result)
                        if i < tries - 1:
                            continue
                        else:
                            print('Error al extraer el autor(articles_df): ',author)
                            flag=False
                    break
                if flag==True:
                    pass
                else:
                    continue
                
                try:
                    articles=result['search-results']['entry']
                except KeyError:
                    print(result)
                    continue
                
                for article in articles:
                        
                    self.articulos['scopus_id'].append(''.join(filter(str.isdigit,str(article['dc:identifier']))))
                    self.articulos['eid'].append(self.get_field_search('eid',article))
                    self.articulos['titulo'].append(self.get_field_search('dc:title',article))
                    self.articulos['creador'].append(self.get_field_search('dc:creator',article))
                    self.articulos['nombre_publicacion'].append(self.get_field_search('prism:publicationName',article))
                    self.articulos['issn'].append(self.get_field_search('prism:issn',article))
                    self.articulos['volumen'].append(self.get_field_search('prism:volume',article))
                    self.articulos['issue'].append(self.get_field_search('prism:issueIdentifier',article))
                    self.articulos['numero_articulo'].append(self.get_field_search('article-number',article))
                    self.articulos['pag_inicio'].append(self.get_field_search('prism:pageRange',article,key='page_start'))
                    self.articulos['pag_fin'].append(self.get_field_search('prism:pageRange',article,key='page_end'))
                    self.articulos['pag_count'].append(self.get_page_count(self.articulos['scopus_id'][-1],self.articulos['pag_inicio'][-1]))
                    self.articulos['fecha_publicacion'].append(self.get_field_search('prism:coverDate',article))
                    self.articulos['doi'].append(self.get_field_search('prism:doi',article))
                    self.articulos['citado'].append(self.get_field_search('citedby-count',article))
                    self.articulos['link'].append(self.get_field_search('link',article,key='@ref'))
                    self.articulos['institucion'].append(self.get_field_search('affiliation',article,key='affilname'))
                    self.articulos['tipo_fuente'].append(self.get_field_search('prism:aggregationType',article))
                    self.articulos['tipo_documento'].append(self.get_field_search('subtypeDescription',article))
                    self.articulos['etapa_publicacion'].append(self.get_pub_stage(self.articulos['scopus_id'][-1]))
                    self.articulos['autores'].append(self.get_field_search('author',article,key='authname'))
                    self.articulos['autores_id'].append(self.get_field_search('author',article,key='authid'))
                    self.articulos['tipo_acceso'].append(self.get_field_search('openaccess',article))
                    self.articulos['palabras_clave'].append(self.get_field_search('authkeywords',article))
                    self.articulos['agencia_fundadora'].append(self.get_field_search('fund-sponsor',article))
        
        df_articulos = pd.DataFrame(self.articulos) 
        #PRUEBA ID:
        df_articulos.to_csv('articulosSco.csv') #########
        df_articulos.reset_index(drop=True)
        self.__init__(self.API_KEY, self.INST_TOKEN)
        return df_articulos
    """
    def get_field_abstract(self, field, r, key=''):
        if key!='':
            if key=='stage': ##################
                try:
                    text=str(r[field]["ait:status"]["@stage"])
                except:
                    text=''
            else:
                try:
                    c=0
                    aff=''
                    if isinstance(r, type(None)):
                        text=''
                    elif isinstance(r[field], list):
                        if field=='author' and key=='preferred-name': ####################
                            for author in r[field]:
                                #Mostrar posible excepción
                                if c==0:
                                    try:
                                        aff=str(author[key]["ce:indexed-name"])#str(author[key]["ce:given-name"])+' '+str(author['preferred-name']["ce:surname"])
                                    except:
                                        aff=''
                                        print('excepcion en texto autores con el articulo: ', self.articulos['eid'][-1])
                                else:
                                    try:
                                        aff=aff+';'+str(author[key]["ce:indexed-name"])#+str(author[key]["ce:given-name"])+' '+str(author['preferred-name']["ce:surname"])
                                    except:
                                        print('excepcion en texto autores con el articulo: ', self.articulos['eid'][-1])
                                c=1
                        
                        elif field=='affiliation' and key=="affiliation-country":
                            for affil in r[field]:
                                if c==0:
                                    try:
                                        aff=str(affil[key])
                                    except KeyError:
                                        aff=''
                                        print('excepcion en texto pais con el articulo: ', self.articulos['scopus_id'][-1])
                                elif str(affil[key]) in aff:
                                    continue
                                else:
                                    aff=aff+';'+str(affil[key])
                                c=1
                        text= aff
                    else:
                        if isinstance(r[field][key], type(None)):
                            text=''
                        else:
                            text=str(r[field][key])
                except KeyError:
                    text=''
                except TypeError:
                    text=''
        else:
            try:
                if isinstance(r, type(None)):
                        text=''
                elif field=="dc:creator": #################
                    if isinstance(r[field]['author'], list):
                        #Mostrar posible excepción
                        if len(r[field].keys()) > 1: print('dc:creator con mas de un autor en el articulo: ', self.articulos['scopus_id'][-1])
                        for element in r[field]['author']:
                            #Mostrar posible excepción
                            try:
                                text=str(element['preferred-name']["ce:given-name"])+' '+str(element['preferred-name']["ce:surname"])
                            except KeyError:
                                text=''
                                print('excepcion en texto dc:creator con el articulo: ', self.articulos['scopus_id'][-1])
                elif field=="page_count": ################
                    text=str(r["bibrecord"]["head"]["source"]["volisspag"]["pagecount"]["$"])
                elif field=="abstracts": #####################
                    if isinstance(r["bibrecord"]["head"]["abstracts"], type(None)):
                        text=''
                    else:
                        text=str(r["bibrecord"]["head"]["abstracts"])
                elif field=="xocs:meta": ##################
                    text=str(r[field]["xocs:funding-list"]["xocs:funding"]["xocs:funding-agency"])
                elif field=="prism:isbn":
                    if isinstance(r[field], list):
                        c=0
                        for isbn in r[field]:
                            if c==0:
                                text=str(isbn['$'])
                            else:
                                text=text+';'+str(isbn['$'])
                            c=1
                    else:
                        try:
                            text=str(r[field]['$'])
                        except:
                            text=str(r[field])
                else:
                    if isinstance(r[field], type(None)):
                        text=''
                    else:
                        text = str(r[field])
            except KeyError:
                text =''
            except TypeError:
                text =''
        return text
        
    def get_articles_full(self, affil_list):
        result=''
        count=0
        for affil in affil_list:
            print('Extrayendo productos de afiliación...',count+1,' de ', len(affil_list))
            tries=3
            articles=self.get_eid_list(affil)
            if len(articles)==0:
                count=count+1
                continue
            for article in articles:
                ##################
                #HACER UNA FUNCIÓN PARA ESTE UNICO PROCESO
                ##################
                url=f'https://api.elsevier.com/content/abstract/eid/{article}?view=FULL'  #USAR EID
                #url=f'https://api.elsevier.com/content/abstract/scopus_id/{article}?view=FULL'   #USAR SCOPUS ID
                for i in range(tries):
                    try:
                        response = requests.get(url,
                                                headers={'Accept':'application/json',
                                                'X-ELS-APIKey': self.API_KEY,
                                                'X-ELS-Insttoken': self.INST_TOKEN})#, verify=False) #eliminar verify=False
                        
                        result = response.json()
                        flag=True
                    except:
                        print('retrying request...')
                        #print(result)
                        if i < tries - 1:
                            continue
                        else:
                            print('Error al extraer el articulo: ',article)
                            flag=False
                    break
                if flag==True:
                    pass
                else:
                    continue
                try:
                    coredata=result['abstracts-retrieval-response']['coredata']
                    item=result["abstracts-retrieval-response"]["item"]
                    language=result["abstracts-retrieval-response"]["language"]
                    complete=result["abstracts-retrieval-response"]
                    subject=result["abstracts-retrieval-response"]["subject-areas"]
                    authors=result["abstracts-retrieval-response"]["authors"]
                    keywords=result["abstracts-retrieval-response"]["authkeywords"]
                    idxterms=result["abstracts-retrieval-response"]["idxterms"]
                except:
                    try:
                        msg=result['service-error']['status']['statusCode']
                        print('ERROR DEL SERVICIO: ', msg)
                        print('PRODUCTO SCOPUS_ID: ', article)
                        continue
                    except:
                        print('Falla del servicio API: ')
                        print(result)
                #####################METODOS PARA EXTRACCION DE CAMPOS
                
                self.articulos['scopus_id'].append(article[article.rfind('-')+1:-1]) #revisar
                self.articulos['eid'].append(self.get_field_search('eid',coredata))
                self.articulos['titulo'].append(self.get_field_search('dc:title',coredata))
                self.articulos['creador'].append(self.get_field_abstract('dc:creator',coredata))
                self.articulos['nombre_publicacion'].append(self.get_field_search('prism:publicationName',coredata))
                self.articulos['editorial'].append(self.get_field_abstract('dc:publisher',coredata))
                self.articulos['issn'].append(self.get_field_abstract('prism:issn',coredata))
                self.articulos['isbn'].append(self.get_field_abstract('prism:isbn',coredata))
                self.articulos['volumen'].append(self.get_field_abstract('prism:volume',coredata))
                self.articulos['issue'].append(self.get_field_abstract('prism:issueIdentifier',coredata))
                self.articulos['numero_articulo'].append(self.get_field_abstract('article-number',coredata))
                self.articulos['pag_inicio'].append(self.get_field_search('prism:pageRange',coredata,key='page_start'))
                self.articulos['pag_fin'].append(self.get_field_search('prism:pageRange',coredata,key='page_end'))
                self.articulos['pag_count'].append(self.get_field_abstract('page_count',item))
                self.articulos['fecha_publicacion'].append(self.get_field_search('prism:coverDate',coredata))
                self.articulos['idioma'].append(self.get_field_abstract('@xml:lang',language))
                self.articulos['doi'].append(self.get_field_abstract('prism:doi',coredata))
                self.articulos['citado'].append(self.get_field_abstract('citedby-count',coredata))
                self.articulos['link'].append(self.get_field_search('link',coredata,key='@rel'))
                self.articulos['institucion'].append(self.get_field_search('affiliation',complete,key='affilname'))
                self.articulos['affil_id'].append(self.get_field_search('affiliation',complete,key='@id'))#####revisar
                self.articulos['abstract'].append(self.get_field_abstract('abstracts',item))
                self.articulos['tema'].append(self.get_field_search('subject-area',subject,key='$'))
                self.articulos['tipo_fuente'].append(self.get_field_abstract('prism:aggregationType',coredata))
                self.articulos['tipo_documento'].append(self.get_field_abstract('subtypeDescription',coredata))
                self.articulos['etapa_publicacion'].append(self.get_field_abstract('ait:process-info',item,key='stage'))
                self.articulos['autores'].append(self.get_field_abstract('author',authors,key='preferred-name'))
                self.articulos['autores_id'].append(self.get_field_search('author',authors,key='@auid'))
                self.articulos['tipo_acceso'].append(self.get_field_search('openaccess',coredata))
                self.articulos['palabras_clave_autor'].append(self.get_field_search('author-keyword',keywords,key='$'))
                self.articulos['palabras_clave_index'].append(self.get_field_search('mainterm',idxterms,key='$'))
                self.articulos['agencia_fundadora'].append(self.get_field_abstract('xocs:meta',item))
                self.articulos['pais'].append(self.get_field_abstract('affiliation',complete,key='affiliation-country'))
                self.articulos['idgruplac'].append('')
                self.articulos['nombre_grupo'].append('')
                
            count=count+1
            #############################
        df_articulos = pd.DataFrame(self.articulos) 
        df_articulos.drop_duplicates(subset ="scopus_id", inplace = True)
        df_articulos=df_articulos.reset_index(drop=True).replace(to_replace ='&amp;', value = '&', regex=True) 
        self.__init__(self.API_KEY, self.INST_TOKEN)    #limpia atributos
        return df_articulos
    
    def get_article(self, article):
        #parameter 'article' is eid of the article
        tries=3
        url=f'https://api.elsevier.com/content/abstract/eid/{article}?view=FULL'  #USAR EID
        #url=f'https://api.elsevier.com/content/abstract/scopus_id/{article}?view=FULL'   #USAR SCOPUS ID
        for i in range(tries):
            try:
                response = requests.get(url,
                                        headers={'Accept':'application/json',
                                        'X-ELS-APIKey': self.API_KEY,
                                        'X-ELS-Insttoken': self.INST_TOKEN})#, verify=False) #eliminar verify=False
                result = response.json()
                coredata=result['abstracts-retrieval-response']['coredata']
                item=result["abstracts-retrieval-response"]["item"]
                language=result["abstracts-retrieval-response"]["language"]
                complete=result["abstracts-retrieval-response"]
                subject=result["abstracts-retrieval-response"]["subject-areas"]
                authors=result["abstracts-retrieval-response"]["authors"]
                keywords=result["abstracts-retrieval-response"]["authkeywords"]
                idxterms=result["abstracts-retrieval-response"]["idxterms"]
        
            except:
                print('retrying request...')
                #print(result)
                if i < tries - 1:
                    continue
                else:
                    print('Error al extraer el articulo: ',article)
                    try:
                        if (response.headers['X-RateLimit-Remaining']=='0') or (response.headers['X-RateLimit-Remaining']==0):
                            return 'API Error: Limite de solicitudes de la API alcanzado' 
                        elif result['service-error']['status']:
                            return 'API Error: '+result['service-error']['status']['statusText']
                        else:
                            pass
                    except KeyError:
                        print('KeyError: X-RateLimit-Remaining')
                        print(response.headers)
                    except:
                        print('Unknown error')
                        print(response.headers)
            break
                
        dic_article={"scopus_id":[],"eid":[],"titulo":[],"creador":[],"nombre_publicacion":[],"editorial":[],"issn":[],"isbn":[],
                        "volumen":[],"issue":[],"numero_articulo":[],"pag_inicio":[],"pag_fin":[],"pag_count":[],"fecha_publicacion":[],"idioma":[],
                        "doi":[],"citado":[],"link":[],"institucion":[],"abstract":[],"affil_id":[],"tema":[],"tipo_fuente":[], "tipo_documento":[],"etapa_publicacion":[],
                        "autores":[],"autores_id":[],"tipo_acceso":[],"palabras_clave_autor":[],"palabras_clave_index":[],"agencia_fundadora":[],"pais":[]}
        
        dic_article['scopus_id'].append(article[article.rfind('-')+1:-1]) #revisar
        dic_article['eid'].append(self.get_field_search('eid',coredata))
        dic_article['titulo'].append(self.get_field_search('dc:title',coredata))
        dic_article['creador'].append(self.get_field_abstract('dc:creator',coredata))
        dic_article['nombre_publicacion'].append(self.get_field_search('prism:publicationName',coredata))
        dic_article['editorial'].append(self.get_field_abstract('dc:publisher',coredata))
        dic_article['issn'].append(self.get_field_abstract('prism:issn',coredata))
        dic_article['isbn'].append(self.get_field_abstract('prism:isbn',coredata))
        dic_article['volumen'].append(self.get_field_abstract('prism:volume',coredata))
        dic_article['issue'].append(self.get_field_abstract('prism:issueIdentifier',coredata))
        dic_article['numero_articulo'].append(self.get_field_abstract('article-number',coredata))
        dic_article['pag_inicio'].append(self.get_field_search('prism:pageRange',coredata,key='page_start'))
        dic_article['pag_fin'].append(self.get_field_search('prism:pageRange',coredata,key='page_end'))
        dic_article['pag_count'].append(self.get_field_abstract('page_count',item))
        dic_article['fecha_publicacion'].append(self.get_field_search('prism:coverDate',coredata))
        dic_article['idioma'].append(self.get_field_abstract('@xml:lang',language))
        dic_article['doi'].append(self.get_field_abstract('prism:doi',coredata))
        dic_article['citado'].append(self.get_field_abstract('citedby-count',coredata))
        dic_article['link'].append(self.get_field_search('link',coredata,key='@rel'))
        dic_article['institucion'].append(self.get_field_search('affiliation',complete,key='affilname'))
        dic_article['affil_id'].append(self.get_field_search('affiliation',complete,key='@id'))#####revisar
        dic_article['abstract'].append(self.get_field_abstract('abstracts',item))
        dic_article['tema'].append(self.get_field_search('subject-area',subject,key='$'))
        dic_article['tipo_fuente'].append(self.get_field_abstract('prism:aggregationType',coredata))
        dic_article['tipo_documento'].append(self.get_field_abstract('subtypeDescription',coredata))
        dic_article['etapa_publicacion'].append(self.get_field_abstract('ait:process-info',item,key='stage'))
        dic_article['autores'].append(self.get_field_abstract('author',authors,key='preferred-name'))
        dic_article['autores_id'].append(self.get_field_search('author',authors,key='@auid'))
        dic_article['tipo_acceso'].append(self.get_field_search('openaccess',coredata))
        dic_article['palabras_clave_autor'].append(self.get_field_search('author-keyword',keywords,key='$'))
        dic_article['palabras_clave_index'].append(self.get_field_search('mainterm',idxterms,key='$'))
        dic_article['agencia_fundadora'].append(self.get_field_abstract('xocs:meta',item))
        dic_article['pais'].append(self.get_field_abstract('affiliation',complete,key='affiliation-country'))
        #############################
        df_articulo = pd.DataFrame(dic_article)
        df_articulo=df_articulo.reset_index(drop=True).replace(to_replace ='&amp;', value = '&', regex=True) 
        return df_articulo
    
    def get_credential_validator(self,affil):
        result=''        
        url = f'https://api.elsevier.com/content/search/scopus?query=af-id({affil})&start=0&count=1&field=dc:identifier&view=STANDARD'
        
        try:
            response = requests.get(url,
                                    headers={'Accept':'application/json',
                                    'X-ELS-APIKey': self.API_KEY,
                                    'X-ELS-Insttoken': self.INST_TOKEN})#, verify=False) #eliminar verify=False
                    
            result = response.json()
            #print(type(result))                 
            if result['error-response']['error-code'] == 'APIKEY_INVALID':
                self.STATE_API=result['error-response']['error-code']                            
                return self.STATE_API
            else:
                self.STATE_API='APIKEY_VALID'
        except:
            self.STATE_API='APIKEY_VALID'
            #print('Credencial valida, request: ', result)         
        return self.STATE_API
    
    def __del__(self):
        print('ExtractorScopus Object Destroyed')