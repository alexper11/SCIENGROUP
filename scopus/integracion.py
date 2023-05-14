import pandas as pd
import numpy as np
#from scopus.controllers.ProductosController import ProductosController  

###############################
#INTEGRACIÓN DE MODULOS PARA DATOS DE GRUPOS DE INVESTIGACIÓN
#################################
def integrar(aux_articulosg,aux_basicog,aux_caplibrosg,aux_identificadores,aux_integrantes,aux_librosg,aux_oarticulos,aux_olibros,df_autores,df_productos):
    #INTEGRACIÓN DE DATOS DE AUTORES
    ident=aux_identificadores[(aux_identificadores['nombre']=='Autor ID (Scopus)') & (aux_identificadores['url'].str.contains(pat='https://www.scopus.com/authid'))]
    ident['author_id']=ident['url'].str.extract(r'([^=]*$)')
    ident=ident.drop_duplicates(subset=['url'])[['idcvlac','author_id']]
    ident1=aux_identificadores[(aux_identificadores['nombre']=='Open Researcher and Contributor ID (ORCID)') & (aux_identificadores['url'].str.contains(pat='https://orcid.org/'))]
    ident1['orcid']=ident1['url'].str.extract(r'([^/]*$)')
    ident1=ident1.drop_duplicates(subset=['url'])[['idcvlac','orcid']]
    integ=aux_integrantes[['idgruplac','url']]
    integ['idcvlac']=integ['url'].str.extract(r'([^=]*$)')
    integ=integ[['idgruplac','idcvlac']]

    basic = aux_basicog[['idgruplac','nombre']]

    ident_integ=ident.merge(integ,how = 'left', left_on='idcvlac', right_on='idcvlac')
    ident_integ_basic=ident_integ.merge(basic,how = 'left', left_on='idgruplac', right_on='idgruplac')
    ident_integ1=ident1.merge(integ,how = 'left', left_on='idcvlac', right_on='idcvlac')
    ident_integ_basic1=ident_integ1.merge(basic,how = 'left', left_on='idgruplac', right_on='idgruplac')

    def f(x):
        d={}
        d['idgruplac']=';'.join(x['idgruplac'])
        d['nombre']=';'.join(x['nombre'])
        d['idcvlac']=x['idcvlac'].values[0]
        return pd.Series(d, index=['idgruplac','nombre','idcvlac'])
    
    auth_gruplac=ident_integ_basic.groupby(['author_id']).apply(f).reset_index()
    df_autores_sco=df_autores[['nombre','autor_id']]
    df_autores_match=auth_gruplac.merge(df_autores_sco,how = 'inner', left_on='author_id', right_on='autor_id')
    df_autores_match.rename(columns = {'nombre_x':'nombre_grupo','nombre_y':'nombre_cvlac'}, inplace = True)
    df_autores_match.drop('autor_id', inplace=True, axis=1)

    auth_gruplac1=ident_integ_basic1.groupby(['orcid']).apply(f).reset_index()
    df_autores_sco1=df_autores[['nombre','orcid']]
    df_autores_match1=auth_gruplac1.merge(df_autores_sco1,how = 'inner', left_on='orcid', right_on='orcid')
    df_autores_match1.rename(columns = {'nombre_x':'nombre_grupo','nombre_y':'nombre_cvlac'}, inplace = True)
    df_autores_match1=df_autores_match1.merge(df_autores_match,how = 'left', on='idcvlac', indicator='ind').query('ind == "left_only"')
    df_autores_match1=df_autores_match1[['orcid','idgruplac_x','nombre_grupo_x','idcvlac']]
    df_autores_match1.rename(columns={'idgruplac_x':'idgruplac','nombre_grupo_x':'nombre_grupo'},inplace=True)

    df_autores_merged1=df_autores.merge(df_autores_match,how = 'left', left_on='autor_id', right_on='author_id')
    df_autores_merged1.drop(['author_id','nombre_cvlac'], inplace=True, axis=1)
    df_autores_merged2=df_autores.merge(df_autores_match1,how = 'left', left_on='orcid', right_on='orcid')
    df_autores_merged=pd.concat([df_autores_merged1,df_autores_merged2])
    df_autores_merged=df_autores_merged[~df_autores_merged['idgruplac'].isna()].drop_duplicates(subset=['eid'])
    df_autores_final=df_autores.merge(df_autores_merged[['eid','idgruplac','nombre_grupo','idcvlac']],how='left',on='eid')
    
    #INTEGRACIÓN DE DATOS DE PRODUCTOS
    #df_productos_sco=df_productos[['scopus_id','titulo','isbn','doi']]
    df_productos_articulos=df_productos[(df_productos['tipo_documento']=='Article') | 
                                (df_productos['tipo_documento']=='Review') | 
                                (df_productos['tipo_documento']=='Letter') |
                                (df_productos['tipo_documento']=='Note') |
                                (df_productos['tipo_documento']=='Erratum') |
                                (df_productos['tipo_documento']=='Data Paper') |
                                (df_productos['tipo_documento']=='Short Survey')]
    def g(x):
        d={}
        d['idgruplac']=';'.join(set(x['idgruplac']))
        d['nombre_grupo']=';'.join(set(x['nombre_grupo']))
        return pd.Series(d, index=['idgruplac','nombre_grupo'])
    #df basic es el df con idgruplac vs nombre_grupo

    def match_articulos_doi(art_scopus,art_gruplac):
        art_gruplac1=art_gruplac[['idgruplac','doi']].replace({r'^NaN':''}).fillna('')
        art_scopus_1=art_scopus[['doi']].fillna('').replace({r'NaN':''}).fillna('')
        art_scopus_1=art_scopus_1[~(art_scopus_1['doi']=='')]
        art_gruplac1=art_gruplac1[~(art_gruplac1['doi']=='')]
        matched=art_scopus_1.merge(art_gruplac1,how ='inner', on='doi')
        matched=matched.merge(basic[['idgruplac','nombre']].rename(columns={'nombre':'nombre_grupo'}),how ='left', on='idgruplac')
        matched=matched.groupby(['doi']).apply(g).reset_index()
        return art_scopus.merge(matched,how='left', on='doi')

    result=match_articulos_doi(df_productos_articulos,aux_articulosg)

    def match_articulos_nombre(art_scopus,art_gruplac):
        art_gruplac1=art_gruplac.copy().replace({r'NaN':''})
        art_scopus1=art_scopus[art_scopus['idgruplac'].isna()].replace({r'^NaN':''})
        art_scopus1['titulo']=art_scopus1['titulo'].str.replace(r'[^\w\d\s:]', '', regex=True).str.replace(r'/\s+/g',' ',regex=True).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip()
        art_gruplac1['nombre']=art_gruplac1['nombre'].str.replace(r'[^\w\d\s:]', '', regex=True).str.replace(r'/\s+/g',' ',regex=True).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip()
        art_scopus1['titulo']=art_scopus1['titulo'].str.lower().fillna('')
        art_gruplac1['nombre']=art_gruplac1['nombre'].str.lower().fillna('')
        art_gruplac1=art_gruplac1[art_gruplac1['nombre'].str.len()>10]
        
        prod_index_match=art_gruplac1.apply(lambda x: art_scopus1['titulo'][art_scopus1['titulo'].str.contains(str(x['nombre']).lower())].index.values, axis=1)
        prod_index_match=prod_index_match.apply(lambda x: x if len(x)>0 else np.nan)
        prod_index_match=prod_index_match[~prod_index_match.isna()]
        
        list_prod_title_gruplac=prod_index_match.index.values.tolist()
        list_prod_title_scopus=prod_index_match.tolist()
        
        #print('procesando...')
        aux_articulosg_indexed=art_gruplac.iloc[list_prod_title_gruplac]
        for idxg,idxs1 in zip(list_prod_title_gruplac,list_prod_title_scopus):
            for idxs in idxs1:
                if art_scopus.loc[art_scopus.index==idxs, 'idgruplac'].isna().values[0]:
                    nombre_grupo=basic[basic['idgruplac']==aux_articulosg_indexed.loc[aux_articulosg_indexed.index==idxg]['idgruplac'].values[0]]['nombre'].values[0]
                    idgruplac=aux_articulosg_indexed.loc[aux_articulosg_indexed.index==idxg]['idgruplac'].values[0]
                    art_scopus.loc[art_scopus.index==idxs, 'nombre_grupo']=nombre_grupo
                    art_scopus.loc[art_scopus.index==idxs, 'idgruplac']=idgruplac
                else:
                    nombre_grupo=basic[basic['idgruplac']==aux_articulosg_indexed.loc[aux_articulosg_indexed.index==idxg]['idgruplac'].values[0]]['nombre'].values[0]
                    idgruplac=aux_articulosg_indexed.loc[aux_articulosg_indexed.index==idxg]['idgruplac'].values[0]
                    if idgruplac in art_scopus.loc[art_scopus.index==idxs, 'idgruplac'].values[0]:
                        pass
                    else:
                        art_scopus.loc[art_scopus.index==idxs, 'nombre_grupo']=art_scopus.loc[art_scopus.index==idxs, 'nombre_grupo'].values[0]+';'+nombre_grupo
                        art_scopus.loc[art_scopus.index==idxs, 'idgruplac']=art_scopus.loc[art_scopus.index==idxs, 'idgruplac'].values[0]+';'+idgruplac

        return art_scopus

    result=match_articulos_nombre(result,aux_articulosg)
    result=match_articulos_nombre(result,aux_oarticulos)
    df_productos_articulos=result
    result=''

    df_productos_libros=df_productos[(df_productos['tipo_documento']=='Book') | 
                                (df_productos['tipo_documento']=='Book Chapter')]
    df_productos_libros['idgruplac']=np.nan
    df_productos_libros['nombre_grupo']=np.nan
    aux_librosg['isbn']= aux_librosg['isbn'].str.upper().str.replace(r'^X{2,}$|[^0-9|X]+', '',regex=True).fillna('')
    aux_olibros['isbn']= aux_olibros['isbn'].str.upper().str.replace(r'^X{2,}$|[^0-9|X]+', '',regex=True).fillna('')
    #aux_caplibrosg['isbn'] = aux_caplibrosg['isbn'].str.replace(r'-', '', regex=True)

    def match_libros_isbn(lib_scopus,lib_gruplac):
        lib_scopus1=lib_scopus[lib_scopus['idgruplac'].isna()].replace({r'^NaN':''}).fillna('')
        lib_gruplac1=lib_gruplac[['idgruplac','isbn']].dropna(subset=['isbn']).replace({r'^NaN':''}).fillna('')
        index_aux = lib_gruplac1[(lib_gruplac1['isbn'] == '0') | (lib_gruplac1['isbn'] == '')].index
        lib_gruplac1.drop(index_aux , inplace=True)
        lib_scopus1=lib_scopus[['titulo','isbn']].dropna(subset=['isbn'])
        
        prod_index_match=lib_gruplac1.apply(lambda x: lib_scopus1[lib_scopus1['isbn'].str.contains(str(x['isbn']))].index.values, axis=1)
        prod_index_match=prod_index_match.apply(lambda x: x if len(x)>0 else np.nan)
        prod_index_match=prod_index_match[~prod_index_match.isna()]
        
        #print(prod_index_match)
        
        list_prod_isbn_gruplac=prod_index_match.index.values.tolist()
        list_prod_isbn_scopus=prod_index_match.tolist()
        
        #print('procesando...')
        try:
            librosg_indexed=lib_gruplac.iloc[list_prod_isbn_gruplac]
            for idxg,idxs1 in zip(list_prod_isbn_gruplac,list_prod_isbn_scopus):
                for idxs in idxs1:
                    if lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac'].isna().values[0]:
                        nombre_grupo=basic[basic['idgruplac']==librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]]['nombre'].values[0]
                        idgruplac=librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]
                        lib_scopus.loc[lib_scopus.index==idxs, 'nombre_grupo']=nombre_grupo
                        lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac']=idgruplac
                    else:
                        nombre_grupo=basic[basic['idgruplac']==librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]]['nombre'].values[0]
                        idgruplac=librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]
                        if idgruplac in lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac'].values[0]:
                            pass
                        else:
                            lib_scopus.loc[lib_scopus.index==idxs, 'nombre_grupo']=lib_scopus.loc[lib_scopus.index==idxs, 'nombre_grupo'].values[0]+';'+nombre_grupo
                            lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac']=lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac'].values[0]+';'+idgruplac
        except:
            #raise
            pass
        
        return lib_scopus

    def match_libros_nombre(lib_scopus,lib_gruplac):
            if 'capitulo' in lib_gruplac:
                lib_scopus1=lib_scopus[lib_scopus['idgruplac'].isna()].replace({r'^NaN':''})
                lib_gruplac1=lib_gruplac[['idgruplac','capitulo']].replace({r'^NaN':''})
                lib_scopus1['titulo']=lib_scopus1['titulo'].str.replace(r'[^\w\d\s:]', '', regex=True).str.strip().str.replace(r'/\s+/g',' ',regex=True).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip()
                lib_gruplac1['capitulo']=lib_gruplac1['capitulo'].str.replace(r'[^\w\d\s:]', '', regex=True).str.strip().str.replace(r'/\s+/g',' ',regex=True).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip()
                lib_scopus1['titulo']=lib_scopus1['titulo'].str.lower().fillna('')
                lib_gruplac1['capitulo']=lib_gruplac1['capitulo'].str.lower().fillna('')
                lib_gruplac1=lib_gruplac1[lib_gruplac1['capitulo'].str.len()>10]

                prod_index_match=lib_gruplac1.apply(lambda x: lib_scopus1[lib_scopus1['titulo'].str.contains(str(x['capitulo']))].index.values, axis=1)
                prod_index_match=prod_index_match.apply(lambda x: x if len(x)>0 else np.nan)
                prod_index_match=prod_index_match[~prod_index_match.isna()]

                list_prod_nombre_gruplac=prod_index_match.index.values.tolist()
                list_prod_nombre_scopus=prod_index_match.tolist()

                #print('procesando...')
                try:
                    librosg_indexed=lib_gruplac.iloc[list_prod_nombre_gruplac]
                    for idxg,idxs1 in zip(list_prod_nombre_gruplac,list_prod_nombre_scopus):
                        for idxs in idxs1:
                            if lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac'].isna().values[0]:
                                nombre_grupo=basic[basic['idgruplac']==librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]]['nombre'].values[0]
                                idgruplac=librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]
                                lib_scopus.loc[lib_scopus.index==idxs, 'nombre_grupo']=nombre_grupo
                                lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac']=idgruplac
                            else:
                                nombre_grupo=basic[basic['idgruplac']==librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]]['nombre'].values[0]
                                idgruplac=librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]
                                if idgruplac in lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac'].values[0]:
                                    pass
                                else:
                                    lib_scopus.loc[lib_scopus.index==idxs, 'nombre_grupo']=lib_scopus.loc[lib_scopus.index==idxs, 'nombre_grupo'].values[0]+';'+nombre_grupo
                                    lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac']=lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac'].values[0]+';'+idgruplac
                except:
                    #raise
                    pass

                return lib_scopus
            
            else:
                lib_scopus1=lib_scopus[lib_scopus['idgruplac'].isna()].replace({r'NaN':''})
                lib_gruplac1=lib_gruplac[['idgruplac','nombre']].replace({r'NaN':''})
                lib_scopus1['titulo']=lib_scopus1['titulo'].str.replace(r'[^\w\d\s:]', '', regex=True).str.strip().str.replace(r'/\s+/g',' ',regex=True).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip()
                lib_gruplac1['nombre']=lib_gruplac1['nombre'].str.replace(r'[^\w\d\s:]', '', regex=True).str.strip().str.replace(r'/\s+/g',' ',regex=True).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip()
                lib_scopus1['titulo']=lib_scopus1['titulo'].str.lower().fillna('')
                lib_gruplac1['nombre']=lib_gruplac1['nombre'].str.lower().fillna('')
                lib_gruplac1=lib_gruplac1[lib_gruplac1['nombre'].str.len()>10]

                prod_index_match=lib_gruplac1.apply(lambda x: lib_scopus1[lib_scopus1['titulo'].str.contains(str(x['nombre']))].index.values, axis=1)
                prod_index_match=prod_index_match.apply(lambda x: x if len(x)>0 else np.nan)
                prod_index_match=prod_index_match[~prod_index_match.isna()]

                list_prod_nombre_gruplac=prod_index_match.index.values.tolist()
                list_prod_nombre_scopus=prod_index_match.tolist()

                #print('procesando...')
                try:
                    librosg_indexed=lib_gruplac.iloc[list_prod_nombre_gruplac]
                    for idxg,idxs1 in zip(list_prod_nombre_gruplac,list_prod_nombre_scopus):
                        for idxs in idxs1:
                            if lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac'].isna().values[0]:
                                nombre_grupo=basic[basic['idgruplac']==librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]]['nombre'].values[0]
                                idgruplac=librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]
                                lib_scopus.loc[lib_scopus.index==idxs, 'nombre_grupo']=nombre_grupo
                                lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac']=idgruplac
                            else:
                                nombre_grupo=basic[basic['idgruplac']==librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]]['nombre'].values[0]
                                idgruplac=librosg_indexed.loc[librosg_indexed.index==idxg]['idgruplac'].values[0]
                                if idgruplac in lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac'].values[0]:
                                    pass
                                else:
                                    lib_scopus.loc[lib_scopus.index==idxs, 'nombre_grupo']=lib_scopus.loc[lib_scopus.index==idxs, 'nombre_grupo'].values[0]+';'+nombre_grupo
                                    lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac']=lib_scopus.loc[lib_scopus.index==idxs, 'idgruplac'].values[0]+';'+idgruplac
                except:
                    #raise
                    pass

                return lib_scopus

    result2=match_libros_isbn(df_productos_libros,aux_librosg)
    result2=match_libros_isbn(result2,aux_olibros)
    #result2=match_libros_isbn(result2,aux_caplibrosg)

    result3=match_libros_nombre(result2,aux_caplibrosg)
    result3=match_libros_nombre(result3,aux_librosg)
    result3=match_libros_nombre(result3,aux_olibros)

    df_productos_libros=result3
    result2=''
    result3=''

    df_productos_otros=df_productos[(df_productos['tipo_documento']=='Conference Paper') | 
                                (df_productos['tipo_documento']=='Editorial')]

    result4 = match_articulos_doi(df_productos_otros,aux_articulosg)
    result4 = match_articulos_nombre(result4,aux_articulosg)
    result4 = match_articulos_nombre(result4,aux_oarticulos)
    result4 = match_libros_isbn(result4,aux_librosg)
    result4 = match_libros_isbn(result4,aux_olibros)
    #result4 = match_libros_isbn(result4,aux_caplibrosg)
    result4 = match_libros_nombre(result4,aux_librosg)
    result4 = match_libros_nombre(result4,aux_olibros)
    result4 = match_libros_nombre(result4,aux_caplibrosg)
    df_productos_otros=result4

    result4=''
    aux_articulosg=''
    aux_basicog=''
    aux_caplibrosg=''
    aux_librosg=''
    aux_oarticulos=''
    aux_olibros=''
    aux_identificadores=''
    aux_integrantes=''

    df_productos_concat=pd.concat([df_productos_articulos,df_productos_libros,df_productos_otros])
    df_productos=df_productos.merge(df_productos_concat[['scopus_id','idgruplac','nombre_grupo']], how='inner', on='scopus_id')
    print('Productos: Emparejados '+str(df_productos[~df_productos['idgruplac'].isna()].shape[0])+' de '+str(df_productos.shape[0]))
    df_autores=df_autores_final
    print('Autores: Emparejados '+str(df_autores[~df_autores['idgruplac'].isna()].shape[0])+' de '+str(df_autores.shape[0]))

    #Inserción a base de datos de SCOPUS

    print('integracion return')
    
    return df_productos, df_autores
"""
aux_articulosg = pd.read_csv('aux_articulosg.csv', dtype = str)
aux_basicog = pd.read_csv('aux_basicog.csv', dtype = str)
aux_caplibrosg = pd.read_csv('aux_caplibrosg.csv', dtype = str)
aux_identificadores = pd.read_csv('aux_identificadores.csv', dtype = str)
aux_integrantes = pd.read_csv('aux_integrantes.csv', dtype = str)
aux_librosg = pd.read_csv('aux_librosg.csv', dtype = str) #pendiente de remplazo
aux_oarticulos = pd.read_csv('aux_oarticulos.csv', dtype = str)
aux_olibros = pd.read_csv('aux_olibros.csv', dtype = str)
df_autores = pd.read_csv('aux_autores.csv', dtype = str)
df_productos = pd.read_csv('aux_productos.csv', dtype = str)

df_productos=integracion(aux_articulosg,aux_basicog,aux_caplibrosg,aux_identificadores,aux_integrantes,
                      aux_librosg,aux_oarticulos,aux_olibros,df_autores,df_productos)

productos = ProductosController()
try:
    productos.insert_df(df_productos)
    #df_productos.to_csv('df_productos_scopus.csv',index=False)
except:
    raise
    df_productos.to_csv('df_productos_scopus.csv',index=False)
    print('error en inserción de datos para productos de scopus')
del productos
"""