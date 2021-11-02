import requests
import json
import pandas as pd

from scopus.ExtractorScopus import ExtractorScopus

class Scientopy(ExtractorScopus):
    def __init__(self, api_key, inst_token):
        super().__init__(api_key, inst_token)
        self.input={"Authors":[],"Author(s) ID":[],"Title":[],"Year":[],"Source title":[],"Volume":[],
                    "Issue":[],"Art. No.":[],"Page start":[],"Page end":[],"Cited by":[],
                    "DOI":[],"Link":[],"Document Type":[],"Access Type":[],"Source":[],"EID":[]}
        
        self.preprocessed={"Authors":[],"Title":[],"Year":[],"Source title":[],"Volume":[],"Issue":[],
                           "Art. No.":[],"Page start":[],"Page end":[],"Page count":[],"Cited by":[],
                           "DOI":[],"Link":[],"Affiliations":[],"Authors with affiliations":[],"Abstract":[],
                           "Author Keywords":[],"Index Keywords":[],"bothKeywords":[],"Correspondence Address":[],
                           "Editors":[],"Publisher Address":[],"Conference name":[],"Conference location":[],
                           "Conference date":[],"Publisher":[],"ISSN":[],"ISBN":[],"CODEN":[],"PubMed ID":[],
                           "Language of Original Document":[],"Abbreviated Source Title":[],"Document Type":[],
                           "Source":[],"Subject":[],"EID":[],"duplicatedIn":[],"country":[],"emailHost":[],"institution":[],
                           "institutionWithCountry":[],"authorFull":[]}
        ##AGRGAR INST + COUNTRY
    
    def year(self,date):
        if date=='':
            year=''
        else:
            year=date[0:4]
        return year
    
    def scopus_input_df(self,topic):
        result=''
        cursor=0
        tries=3
        url=f'http://api.elsevier.com/content/search/scopus?query=TITLE-ABS-KEY({topic})&start={cursor}&count=25&view=COMPLETE'
        for i in range(tries):
            try:
                response = requests.get(url,
                                        headers={'Accept':'application/json',
                                        'X-ELS-APIKey': self.API_KEY,
                                        'X-ELS-Insttoken': self.INST_TOKEN})
                        
                result = response.json()
                TotalArt = int(result['search-results']['opensearch:totalResults'])
                print('Total articulos: ',TotalArt)
            except:
                print(result)
                if i < tries - 1:
                    continue
                else:
                    print('Error al extraer articulos del topic:',topic)
            break         
        #cursor_next=result['search-results']['cursor']['@next']
        cursor=25
        try:
            articles=result['search-results']['entry']
        except KeyError:
            print(result)
            
        for article in articles:
            scopus_id=''.join(filter(str.isdigit,str(article['dc:identifier'])))
            self.input['Authors'].append(self.get_field_search('author',article,key='authname'))
            self.input['Author(s) ID'].append(self.get_field_search('author',article,key='authid'))
            self.input['Title'].append(self.get_field_search('dc:title',article))
            self.input['Year'].append(self.year(self.get_field_search('prism:coverDate',article)))
            self.input['Source title'].append(self.get_field_search('prism:publicationName',article))
            self.input['Volume'].append(self.get_field_search('prism:volume',article))
            self.input['Issue'].append(self.get_field_search('prism:issueIdentifier',article))
            self.input['Art. No.'].append(self.get_field_search('article-number',article))
            self.input['Page start'].append(self.get_field_search('prism:pageRange',article,key='page_start'))
            self.input['Page end'].append(self.get_field_search('prism:pageRange',article,key='page_end'))
            self.input['Cited by'].append(self.get_field_search('citedby-count',article))
            self.input['DOI'].append(self.get_field_search('prism:doi',article))
            self.input['Link'].append(self.get_field_search('link',article,key='@ref'))
            self.input['Document Type'].append(self.get_field_search('subtypeDescription',article))
            self.input['Access Type'].append(self.get_field_search('openaccess',article))
            self.input['Source'].append('Scopus')        
            self.input['EID'].append(self.get_field_search('eid',article))
                
        while cursor <= TotalArt:
            url=f'http://api.elsevier.com/content/search/scopus?query=TITLE-ABS-KEY({topic})&start={cursor}&count=25&view=COMPLETE'
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
                            print('Error al extraer el topic: ',topic)
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
                scopus_id=''.join(filter(str.isdigit,str(article['dc:identifier'])))
                self.input['Authors'].append(self.get_field_search('author',article,key='authname'))
                self.input['Author(s) ID'].append(self.get_field_search('author',article,key='authid'))
                self.input['Title'].append(self.get_field_search('dc:title',article))
                self.input['Year'].append(self.year(self.get_field_search('prism:coverDate',article)))
                self.input['Source title'].append(self.get_field_search('prism:publicationName',article))
                self.input['Volume'].append(self.get_field_search('prism:volume',article))
                self.input['Issue'].append(self.get_field_search('prism:issueIdentifier',article))
                self.input['Art. No.'].append(self.get_field_search('article-number',article))
                self.input['Page start'].append(self.get_field_search('prism:pageRange',article,key='page_start'))
                self.input['Page end'].append(self.get_field_search('prism:pageRange',article,key='page_end'))
                self.input['Cited by'].append(self.get_field_search('citedby-count',article))
                self.input['DOI'].append(self.get_field_search('prism:doi',article))
                self.input['Link'].append(self.get_field_search('link',article,key='@ref'))
                self.input['Document Type'].append(self.get_field_search('subtypeDescription',article))
                self.input['Access Type'].append(self.get_field_search('openaccess',article))
                self.input['Source'].append('Scopus')        
                self.input['EID'].append(self.get_field_search('eid',article))
                        
        df_input = pd.DataFrame(self.input) 
        df_input.reset_index(drop=True)
        return df_input
    
    def authors_scientopy(self,r):
        text=''
        c=0
        try:
            authors=r['author']
            for author in authors:
                if c==0:
                    try:
                        text=str(author["ce:surname"])+', '+str(author["ce:initials"])
                    except KeyError:
                        print('excepcion en texto autores scientopy, eid: ', self.preprocessed['EID'][-1])
                        text=str(author["ce:surname"])
                        continue
                else:
                    try:
                        text=text+'; '+str(author["ce:surname"])+', '+str(author["ce:initials"])
                    except:
                        text=text+'; '+str(author["ce:surname"])
                c=1
        except:
            text=''
            print('Excepción en authors_scientopy con documento: ',self.preprocessed['EID'][-1])  
        return text
    
    def get_institutionWithCountry(self,r):
        text=''
        c=0
        try:
            affiliations=r['affiliation']
            if isinstance(affiliations, list):
                for affiliation in affiliations:
                    try:
                        institution=str(affiliation['affilname'])
                    except:
                        institution=' '
                    try:
                        country=str(affiliation['affiliation-country'])
                    except:
                        country=' '
                    if c==0:
                        text=institution+', '+country
                    else:
                        text=text+';'+institution+', '+country
                    c=1
            else:
                try:
                    institution=str(affiliations['affilname'])
                except:
                    institution=' '
                try:
                    country=str(affiliations['affiliation-country'])
                except:
                    country=' '
                text=text=institution+', '+country
        except:
            text=''
            #print('Excepción en get_institutionWithCountry con documento: ',self.preprocessed['EID'][-1])  
        clean=False
        for char in text:
            if (char==' ' or char==',' or char==';'):
                clean=True
            else:
                clean=False
                break
        if clean==True:
            text=''
        return text
            
    def scopus_preprocessed_df(self, topic):
        result=''
        cursor=0
        tries=3
        scopus_id_list=[]
        eid_list=[]
        url=f'http://api.elsevier.com/content/search/scopus?query=TITLE-ABS-KEY({topic})&start={cursor}&count=1&view=COMPLETE'
        for i in range(tries):
            try:
                response = requests.get(url,
                                        headers={'Accept':'application/json',
                                        'X-ELS-APIKey': self.API_KEY,
                                        'X-ELS-Insttoken': self.INST_TOKEN})
                        
                result = response.json()
                TotalArt = int(result['search-results']['opensearch:totalResults'])
                print('Total articulos: ',TotalArt)
            except:
                print(result)
                if i < tries - 1:
                    continue
                else:
                    print('Error al extraer articulos del topic:',topic)
            break  
               
        while cursor <= TotalArt:
            tries=3
            url=f'http://api.elsevier.com/content/search/scopus?query=TITLE-ABS-KEY({topic})&start={cursor}&count=200&field=dc:identifier,eid&view=STANDARD'
            for i in range(tries):
                try:
                    response = requests.get(url,
                                            headers={'Accept':'application/json',
                                            'X-ELS-APIKey': self.API_KEY,
                                            'X-ELS-Insttoken': self.INST_TOKEN})
                    
                    result = response.json()        
                    flag=True
                except:
                    print(result)
                    if i < tries - 1:
                        continue
                    else:
                        print('Error al extraer el scopusid list para el topic: ',topic)
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
                continue
            
            for article in articles:
                #scopus_id_list.append(''.join(filter(str.isdigit,str(article['dc:identifier']))))
                eid_list.append(str(article["eid"]))
                
        for article in eid_list:     #USAR LISTA DE REFERENCIAS EID
        #for article in scopus_id_list:
            url=f'https://api.elsevier.com/content/abstract/eid/{article}?view=FULL'  #REQUEST EID
            #url=f'https://api.elsevier.com/content/abstract/scopus_id/{article}?view=FULL'
            for i in range(tries):
                try:
                    response = requests.get(url,
                                            headers={'Accept':'application/json',
                                            'X-ELS-APIKey': self.API_KEY,
                                            'X-ELS-Insttoken': self.INST_TOKEN})
                    
                    result = response.json()
                    flag=True
                except:
                    print(result)
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
            
            self.preprocessed['Title'].append(self.get_field_search('dc:title',coredata))
            self.preprocessed['Year'].append(self.year(self.get_field_search('prism:coverDate',coredata)))
            self.preprocessed['Source title'].append(self.get_field_search('prism:publicationName',coredata))
            self.preprocessed['Volume'].append(self.get_field_abstract('prism:volume',coredata))
            self.preprocessed['Issue'].append(self.get_field_abstract('prism:issueIdentifier',coredata))
            self.preprocessed['Art. No.'].append(self.get_field_abstract('article-number',coredata))
            self.preprocessed['Page start'].append(self.get_field_search('prism:pageRange',coredata,key='page_start'))
            self.preprocessed['Page end'].append(self.get_field_search('prism:pageRange',coredata,key='page_end'))
            self.preprocessed['Page count'].append(self.get_field_abstract('page_count',item))
            self.preprocessed['Cited by'].append(self.get_field_abstract('citedby-count',coredata))
            self.preprocessed['DOI'].append(self.get_field_abstract('prism:doi',coredata))
            self.preprocessed['Link'].append(self.get_field_search('link',coredata,key='@rel'))
            self.preprocessed['Affiliations'].append('') ######
            self.preprocessed['Authors with affiliations'].append('') ######
            self.preprocessed['Abstract'].append(self.get_field_abstract('abstracts',item))
            self.preprocessed['Author Keywords'].append(self.get_field_search('author-keyword',keywords,key='$'))
            self.preprocessed['Index Keywords'].append(self.get_field_search('mainterm',idxterms,key='$'))
            self.preprocessed['bothKeywords'].append(self.get_field_search('mainterm',idxterms,key='$')+self.get_field_search('author-keyword',keywords,key='$'))
            self.preprocessed['Correspondence Address'].append('')
            self.preprocessed['Editors'].append('')
            self.preprocessed["Publisher Address"].append('')
            self.preprocessed['Conference name'].append('')
            self.preprocessed['Conference location'].append('')
            self.preprocessed['Conference date'].append('')
            self.preprocessed['Publisher'].append(self.get_field_abstract('dc:publisher',coredata))
            self.preprocessed['ISSN'].append(self.get_field_abstract('prism:issn',coredata))
            self.preprocessed['ISBN'].append(self.get_field_abstract('prism:isbn',coredata))
            self.preprocessed['CODEN'].append('')
            self.preprocessed['PubMed ID'].append('')
            self.preprocessed['Language of Original Document'].append(self.get_field_abstract('@xml:lang',language))
            self.preprocessed['Abbreviated Source Title'].append('')
            self.preprocessed['Document Type'].append(self.get_field_abstract('subtypeDescription',coredata))
            self.preprocessed['Source'].append('Scopus')
            self.preprocessed['Subject'].append(self.get_field_search('subject-area',subject,key='$'))
            self.preprocessed['EID'].append(self.get_field_search('eid',coredata))
            self.preprocessed['duplicatedIn'].append('')
            self.preprocessed['Authors'].append(self.get_field_abstract('author',authors,key='preferred-name'))
            #self.preprocessed['Authors'].append(self.authors_scientopy(authors))
            self.preprocessed['country'].append(self.get_field_abstract('affiliation',complete,key='affiliation-country'))
            self.preprocessed['emailHost'].append('')
            self.preprocessed['institution'].append(self.get_field_search('affiliation',complete,key='affilname'))
            self.preprocessed['institutionWithCountry'].append(self.get_institutionWithCountry(complete))
            self.preprocessed['authorFull'].append('')
            
            #############################
        df_preprocessed = pd.DataFrame(self.preprocessed) 
        df_preprocessed.reset_index(drop=True)
        self.__init__(self.API_KEY, self.INST_TOKEN)
        return df_preprocessed
        
        