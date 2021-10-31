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
        
        self.preproccesed={"Authors":[],"Title":[],"Year":[],"Source title":[],"Volume":[],"Issue":[],
                           "Art. No.":[],"Page start":[],"Page end":[],"Page count":[],"Cited by":[],
                           "DOI":[],"Link":[],"Affiliations":[],"Authors with affiliations":[],"Abstract":[],
                           "Author Keywords":[],"Index Keywords":[],"bothKeywords":[],"Correspondence Address":[],
                           "Editors":[],"Publisher Address":[],"Conference name":[],"Conference location":[],
                           "Conference date":[],"Publisher":[],"ISSN":[],"ISBN":[],"CODEN":[],"PubMed ID":[],
                           "Language of Original Document":[],"Abbreviated Source Title":[],"Document Type":[],
                           "Source":[],"Subject":[],"EID":[],"duplicatedIn":[],"country":[],"emailHost":[],"institution":[],
                           "institutionWithCountry":[],"authorFull":[]}
    
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
    
    def scopus_preproccesed_papaer(self, topic):
        
        
        pass