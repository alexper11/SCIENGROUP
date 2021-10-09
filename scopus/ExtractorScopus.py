import time
import requests
import json
import pandas as pd


class ExtractorScopus:
    
    def __init__(self, api_key, inst_token):
        self.autores={"nombre":[],"autor_id":[],"eid":[],"orcid":[],"documentos":[],"fecha_creacion":[],"citado":[],
                     "citaciones":[],"h_index":[],"co_autores":[],"estado":[],"areas":[],"rango_publicacion":[],
                     "institucion":[],"departamento":[]}
        self.articulos={"scopus_id":[],"eid":[],"titulo":[],"creador":[],"nombre_publicacion":[],"issn":[],"eissn":[],
                        "volumen":[],"issue":[],"numero_articulo":[],"pag_inicio":[],"pag_fin":[],"pag_count":[],"fecha_publicacion":[],
                        "doi":[],"citado":[],"link":[],"afiliacion":[],"tipo_fuente":[],
                        "tipo_documento":[],"etapa_publicacion":[],"autores":[],"autores_id":[],"tipo_acceso":[],"palabras_clave":[],"agencia_fundadora":[]}
        self.API_KEY=api_key
        self.INST_TOKEN=inst_token
        
    def get_auid_list(self, affilid):
        result=''
        s=0
        url = f'https://api.elsevier.com/content/search/author?query=AF-ID({affilid})&start=0&count=200&field=dc:identifier'
        tries=3
        for i in range(tries):
            try:    
                response = requests.get(url,
                                            headers={'Accept':'application/json',
                                                    'X-ELS-APIKey': self.API_KEY,
                                                    'X-ELS-Insttoken': self.INST_TOKEN})
                
                result = response.json()    
                authorIdList=[''.join(filter(str.isdigit,str(r['dc:identifier']))) for r in result['search-results']["entry"]]
                TotalId= int(result['search-results']['opensearch:totalResults'])
                s=200
            except:
                print(result)
                if i < tries - 1:
                    continue
                else:
                    print('Error al extraer auid_list')
            break
        
        while s <= TotalId:
            time.sleep(0.5)
            url = f'https://api.elsevier.com/content/search/author?query=AF-ID({affilid})&start={s}&count=200&field=dc:identifier'
            tries=3
            for i in range(tries):
                try:    
                    response = requests.get(url,
                                                headers={'Accept':'application/json',
                                                        'X-ELS-APIKey': self.API_KEY,
                                                        'X-ELS-Insttoken': self.INST_TOKEN})
                    result = response.json()

                    
                    tempList=[''.join(filter(str.isdigit,str(r['dc:identifier']))) for r in result['search-results']["entry"]]
                    authorIdList.extend(tempList)
                    s=s+200
                except:
                    print(result) 
                    if i < tries - 1:
                        continue
                    else:
                        print('Error al extraer auid_list')
                break
                
        
        return authorIdList

    def get_field(self, field, r):
        if field=="subject-areas":
            try:
                c=0
                areas=''
                if isinstance(r[field], type(None)):
                    text=''
                elif isinstance(r[field]['subject-area'], list):
                    for rs in r[field]['subject-area']:
                        if c==0:
                            areas=str(rs['$'])
                        else:
                            areas=areas+', '+str(rs['$'])
                        c=1
                    text= areas
                else:
                    text=str(r[field]['subject-area']['$'])
            except KeyError:
                text=''
        elif field=="date-created":
            try:
                date= str(r[field]['@day'])+'/'+str(r[field]['@month'])+'/'+str(r['date-created']['@year'])
            except KeyError:
                date=''
            text=date
        elif field=="preferred-name":
            text=str(r[field]['given-name'])+' '+str(r[field]['surname'])
        
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
                            insts=insts+', '+str(i['ip-doc']['parent-preferred-name']['$'])
                        except KeyError:
                            try:
                                insts=insts+', '+str(i['ip-doc']['preferred-name']['$'])
                            except KeyError:
                                insts=insts+', '+' '
                text=insts
            else:
                try:
                    text=str(r['ip-doc']['parent-preferred-name']['$'])
                except KeyError:
                    try:
                        text=str(r['ip-doc']['preferred-name']['$'])
                    except KeyError:
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
                            departs=departs+', '+str(d['ip-doc']['preferred-name']['$'])
                        else:
                            departs=departs+', '+' '
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
        for author in authors:    
            time.sleep(0.3)
            url = f'https://api.elsevier.com/content/author/author_id/{author}?view=ENHANCED'
            tries=3
            for i in range(tries):
                try:
                    response = requests.get(url,
                                            headers={'Accept':'application/json',
                                                'X-ELS-APIKey': self.API_KEY,
                                                'X-ELS-Insttoken': self.INST_TOKEN})
                    
                    result = response.json()
                    r=result['author-retrieval-response'][0]['coredata']
                    r2=result['author-retrieval-response'][0]
                    r3=result['author-retrieval-response'][0]['author-profile']
                    r4=result['author-retrieval-response'][0]['author-profile']['affiliation-current']['affiliation']
                    flag=True
                except:
                    if i < tries - 1: # i is zero indexed
                        continue
                    else:
                        flag=False
                        print('Error al extraer el autor(authors_df): ',author)
                        
                break
            if flag==True:
                pass
            else:
                continue        
            
            self.autores['eid'].append(self.get_field('eid',r))
            self.autores['autor_id'].append(''.join(filter(str.isdigit,str(r['dc:identifier']))))
            self.autores['orcid'].append(self.get_field('orcid',r))
            self.autores['documentos'].append(self.get_field('document-count',r))
            self.autores['citado'].append(self.get_field('cited-by-count',r))
            self.autores['citaciones'].append(self.get_field('citation-count',r))
            self.autores['h_index'].append(self.get_field('h-index',r2))
            self.autores['co_autores'].append(self.get_field('coauthor-count',r2))
            self.autores['areas'].append(self.get_field('subject-areas',r2))
            self.autores['estado'].append(self.get_field('status',r3))
            self.autores['fecha_creacion'].append(self.get_field('date-created',r3))
            self.autores['nombre'].append(self.get_field('preferred-name',r3))
            self.autores['rango_publicacion'].append(self.get_field('publication-range',r3))
            self.autores['institucion'].append(self.get_field('inst',r4))
            self.autores['departamento'].append(self.get_field('depart',r4))
        
        df_autores = pd.DataFrame(self.autores) 
        df_autores.reset_index(drop=True)
        
        return df_autores
    
    def get_field_search(self, field,r,key=''):
        if key!='':
            if key == 'page_start':
                try:
                    if isinstance(r[field], type(None)):
                        text=''
                    else:
                        text = str(r[field].split('-')[0])
                except KeyError:
                    text =''
                    
            elif key == 'page_end':
                try:
                    if isinstance(r[field], type(None)):
                        text=''
                    else:
                        text = str(r[field].split('-')[1])
                except KeyError:
                    text =''
            else:
                try:
                    c=0
                    aff=''
                    if isinstance(r[field], type(None)):
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
                                    elif key=='authid':
                                        aff=aff+';'+str(rs[key])
                                    else:
                                        aff=aff+', '+str(rs[key])
                                    c=1
                        text= aff
                    else:
                        text=str(r[field][key])
                except KeyError:
                    text=''
        
        else:
            try:
                if isinstance(r[field], type(None)):
                    text=''
                elif field=="openaccess":
                    if r[field]=="1": 
                        text='Open Access'
                    else: 
                        text='' 
                else:
                    text = str(r[field])
            except KeyError:
                text =''
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
                                            'X-ELS-Insttoken': self.INST_TOKEN})
                        
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
                break
        return page_count
    
    def get_pub_stage(self,scopus_id):
        result=''
        url=f'https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}?view=FULL'
        tries=3
        for i in range(tries):
            try:
                response = requests.get(url,
                                        headers={'Accept':'application/json',
                                        'X-ELS-APIKey': self.API_KEY,
                                        'X-ELS-Insttoken': self.INST_TOKEN})
                        
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

    def get_articles_df(self, author_list):
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
                                            'X-ELS-Insttoken': self.INST_TOKEN})
                    
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
                self.articulos['eissn'].append(self.get_field_search('prism:eIssn',article))
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
                self.articulos['afiliacion'].append(self.get_field_search('affiliation',article,key='affilname'))
                self.articulos['tipo_fuente'].append(self.get_field_search('prism:aggregationType',article))
                self.articulos['tipo_documento'].append(self.get_field_search('subtypeDescription',article))
                self.articulos['autores'].append(self.get_field_search('author',article,key='authname'))
                self.articulos['autores_id'].append(self.get_field_search('author',article,key='authid'))
                self.articulos['tipo_acceso'].append(self.get_field_search('openaccess',article))
                self.articulos['palabras_clave'].append(self.get_field_search('authkeywords',article))
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
                                                'X-ELS-Insttoken': self.INST_TOKEN})
                        
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
                    self.articulos['eissn'].append(self.get_field_search('prism:eIssn',article))
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
                    self.articulos['afiliacion'].append(self.get_field_search('affiliation',article,key='affilname'))
                    self.articulos['tipo_fuente'].append(self.get_field_search('prism:aggregationType',article))
                    self.articulos['tipo_documento'].append(self.get_field_search('subtypeDescription',article))
                    self.articulos['etapa_publicacion'].append(self.get_pub_stage(self.articulos['scopus_id'][-1]))
                    self.articulos['autores'].append(self.get_field_search('author',article,key='authname'))
                    self.articulos['autores_id'].append(self.get_field_search('author',article,key='authid'))
                    self.articulos['tipo_acceso'].append(self.get_field_search('openaccess',article))
                    self.articulos['palabras_clave'].append(self.get_field_search('authkeywords',article))
                    self.articulos['agencia_fundadora'].append(self.get_field_search('fund-sponsor',article))
        
        df_articulos = pd.DataFrame(self.articulos) 
        df_articulos.reset_index(drop=True)
        return df_articulos