import base64
import io
import pandas as pd
from dash import dash_table, html
import requests
from dash import dcc
import json
import plotly.express as px

gruplac_articulos = pd.read_csv('./assets/data/gruplac_articulos.csv', dtype = str)
gruplac_basico = pd.read_csv('./assets/data/gruplac_basico.csv', dtype = str)
gruplac_caplibros = pd.read_csv('./assets/data/gruplac_caplibros.csv', dtype = str)
gruplac_integrantes = pd.read_csv('./assets/data/gruplac_integrantes.csv', dtype = str)
gruplac_libros = pd.read_csv('./assets/data/gruplac_libros.csv', dtype = str) 
gruplac_oarticulos = pd.read_csv('./assets/data/gruplac_oarticulos.csv', dtype = str)
gruplac_olibros = pd.read_csv('./assets/data/gruplac_olibros.csv', dtype = str)
gruplac_cdoctorado= pd.read_csv('./assets/data/gruplac_cdoctorado.csv', dtype = str)
gruplac_cmaestria= pd.read_csv('./assets/data/gruplac_cmaestria.csv', dtype = str)
gruplac_disenoind= pd.read_csv('./assets/data/gruplac_disenoind.csv', dtype = str)
gruplac_empresatec= pd.read_csv('./assets/data/gruplac_empresatec.csv', dtype = str)
gruplac_innovaempresa= pd.read_csv('./assets/data/gruplac_innovaempresa.csv', dtype = str)
gruplac_instituciones= pd.read_csv('./assets/data/gruplac_instituciones.csv', dtype = str)
gruplac_lineas= pd.read_csv('./assets/data/gruplac_lineas.csv', dtype = str)
gruplac_otecnologicos= pd.read_csv('./assets/data/gruplac_otecnologicos.csv', dtype = str)
gruplac_pdoctorado= pd.read_csv('./assets/data/gruplac_pdoctorado.csv', dtype = str)
gruplac_plantapiloto= pd.read_csv('./assets/data/gruplac_plantapiloto.csv', dtype = str)
gruplac_pmaestria= pd.read_csv('./assets/data/gruplac_pmaestria.csv', dtype = str)
gruplac_prototipos= pd.read_csv('./assets/data/gruplac_prototipos.csv', dtype = str)
gruplac_software= pd.read_csv('./assets/data/gruplac_software.csv', dtype = str)
scopus_autores= pd.read_csv('./assets/data/scopus_autores.csv', dtype = str)
scopus_productos=pd.read_csv('./assets/data/scopus_productos.csv', dtype = str)
cvlac_articulos = pd.read_csv('./assets/data/cvlac_articulos.csv', dtype = str)
cvlac_basico = pd.read_csv('./assets/data/cvlac_basico.csv', dtype = str)
cvlac_caplibros = pd.read_csv('./assets/data/cvlac_caplibros.csv', dtype = str)
cvlac_libros = pd.read_csv('./assets/data/cvlac_libros.csv', dtype = str) 
cvlac_empresatec= pd.read_csv('./assets/data/cvlac_empresatec.csv', dtype = str)
cvlac_innovaempresa= pd.read_csv('./assets/data/cvlac_innovaempresa.csv', dtype = str)
cvlac_lineas= pd.read_csv('./assets/data/cvlac_lineas.csv', dtype = str)
cvlac_tecnologicos= pd.read_csv('./assets/data/cvlac_otecnologicos.csv', dtype = str)
cvlac_prototipos= pd.read_csv('./assets/data/cvlac_prototipos.csv', dtype = str)
cvlac_software= pd.read_csv('./assets/data/cvlac_software.csv', dtype = str)
cvlac_areas= pd.read_csv('./assets/data/cvlac_areas.csv', dtype = str)
cvlac_reconocimiento= pd.read_csv('./assets/data/cvlac_reconocimiento.csv', dtype = str)
cvlac_identificadores=pd.read_csv('./assets/data/cvlac_identificadores.csv', dtype = str)

#Duplicados gruplac
with open('./assets/data/gruplac_duplicados.json','r') as file:
    gruplac_duplicados=file.read()
gruplac_duplicados=json.loads(gruplac_duplicados)

#Re formateo de fechas y enteros
gruplac_basico['fecha_formacion']=pd.to_datetime(gruplac_basico['fecha_formacion']).dt.to_period('M')#DTYPE: period[M]
gruplac_articulos['fecha']=pd.to_datetime(gruplac_articulos['fecha']).dt.to_period('Y')
gruplac_caplibros['fecha']=pd.to_datetime(gruplac_caplibros['fecha']).dt.to_period('Y')
gruplac_pdoctorado['fecha']=pd.to_datetime(gruplac_pdoctorado['fecha'])#Tiene valores nulos!
gruplac_pmaestria['fecha']=pd.to_datetime(gruplac_pmaestria['fecha'])#Tiene valores nulos!
gruplac_cdoctorado['fecha']=pd.to_datetime(gruplac_cdoctorado['fecha'])#Tiene valores nulos![^a-zA-Z0-9]
gruplac_cmaestria['fecha']=pd.to_datetime(gruplac_cmaestria['fecha'])#Tiene valores nulos!
gruplac_oarticulos['fecha']=pd.to_datetime(gruplac_oarticulos['fecha']).dt.to_period('Y')
gruplac_olibros['fecha']=pd.to_datetime(gruplac_olibros['fecha']).dt.to_period('Y')
gruplac_disenoind['fecha']=pd.to_datetime(gruplac_disenoind['fecha']).dt.to_period('Y')
gruplac_innovaempresa['fecha']=pd.to_datetime(gruplac_innovaempresa['fecha']).dt.to_period('Y')
gruplac_plantapiloto['fecha']=pd.to_datetime(gruplac_plantapiloto['fecha']).dt.to_period('Y')
gruplac_otecnologicos['fecha']=pd.to_datetime(gruplac_otecnologicos['fecha']).dt.to_period('Y')
gruplac_prototipos['fecha']=pd.to_datetime(gruplac_prototipos['fecha']).dt.to_period('Y')
gruplac_software['fecha']=pd.to_datetime(gruplac_software['fecha']).dt.to_period('Y')
gruplac_empresatec['fecha_registro']=pd.to_datetime(gruplac_empresatec['fecha_registro'])
gruplac_libros['fecha']=pd.to_datetime(gruplac_libros['fecha']).dt.to_period('Y')
cvlac_empresatec=cvlac_empresatec.rename(columns={"registro_camara": "fecha"})
cvlac_articulos['fecha'] = pd.to_datetime(cvlac_articulos['fecha']).dt.to_period('Y')
cvlac_caplibros['fecha'] = pd.to_datetime(cvlac_caplibros['fecha']).dt.to_period('Y')
cvlac_libros['fecha'] = pd.to_datetime(cvlac_libros['fecha']).dt.to_period('Y')
cvlac_empresatec['fecha']= pd.to_datetime(cvlac_empresatec['fecha']).dt.to_period('Y')
cvlac_innovaempresa['fecha']= pd.to_datetime(cvlac_innovaempresa['fecha']).dt.to_period('Y')
cvlac_tecnologicos['fecha']= pd.to_datetime(cvlac_tecnologicos['fecha']).dt.to_period('Y')
cvlac_prototipos['fecha']= pd.to_datetime(cvlac_prototipos['fecha']).dt.to_period('Y')
cvlac_software['fecha']= pd.to_datetime(cvlac_software['fecha']).dt.to_period('Y')
scopus_productos['fecha_publicacion']= pd.to_datetime(scopus_productos['fecha_publicacion']).dt.to_period('M')


elementos={'Artículos':gruplac_articulos.drop(columns=['volumen','fasciculo','paginas','doi','autores']),
           'Capítulos':gruplac_caplibros.drop(columns=['isbn','volumen','paginas','autores']),
           'Libros':gruplac_libros.drop(columns=['isbn','autores']),
           'Cursos de Doctorado':gruplac_cdoctorado.drop(columns=['acto']),
           'Cursos de Maestría':gruplac_cmaestria.drop(columns=['acto']),
           'Otros Artículos':gruplac_oarticulos.drop(columns=['volumen','fasciculo','paginas','autores']),
           'Otros Libros':gruplac_olibros.drop(columns=['isbn','volumen','paginas','autores']),
           'Diseño industrial':gruplac_disenoind.drop(columns=['autores']),
           'Empresa Tecnológica':gruplac_empresatec.drop(columns=['nit','fecha','autores']),
           'Innovación Empresarial':gruplac_innovaempresa.drop(columns=['autores']),
           'Otros Productos Tecnológicos':gruplac_otecnologicos.drop(columns=['autores']),
           'Programa de Doctorado':gruplac_pdoctorado.drop(columns=['acto']), 
           'Programa de Maestría':gruplac_pmaestria.drop(columns=['acto']),
           'Planta Piloto':gruplac_plantapiloto.drop(columns=['autores']),
           'Prototipos':gruplac_prototipos.drop(columns=['autores']),
           'Software':gruplac_software.drop(columns=['url','nombre_proyecto','autores']),
           'Institución':gruplac_instituciones,
           'Líneas de Investigación':gruplac_lineas,
           'Datos Básicos':gruplac_basico.drop(columns=['nombre','lider','pagina_web','email','programas_secundario'])}

elementos_cvlac={'Áreas de Actuación':cvlac_areas,
                 'Artículos':cvlac_articulos.drop(columns=['autores','volumen','fasciculo','paginas','doi']),
                 'Datos Básicos':cvlac_basico.drop(columns=['nombre_citaciones']),
                 'Capítulos':cvlac_caplibros.drop(columns=['autores','isbn','volumen','paginas']),
                 'Empresa Tecnológica':cvlac_empresatec.drop(columns=['autores','nit']),
                 'Identificadores':cvlac_identificadores.drop(columns=['url']),
                 'Innovación Empresarial':cvlac_innovaempresa.drop(columns=['autor','contrato_registro']),
                 'Líneas de Investigación':cvlac_lineas,
                 'Libros':cvlac_libros.drop(columns=['autores','isbn','volumen','paginas']),
                 'Prototipos':cvlac_prototipos.drop(columns=['autor','contrato_registro']),
                 'Reconocimientos':cvlac_reconocimiento,
                 'Software':cvlac_software.drop(columns=['autor','contrato_registro']),
                 'Productos Tecnológicos':cvlac_tecnologicos.drop(columns=['autor','contrato_registro'])}


elementos_scopus={'Artículos':scopus_productos[scopus_productos['tipo_documento']=='Article'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso']),
                  'Documentos de Conferencia':scopus_productos[scopus_productos['tipo_documento']=='Conference Paper'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso']),
                  'Revisiónes':scopus_productos[scopus_productos['tipo_documento']=='Review'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso']),
                  'Capítulos':scopus_productos[scopus_productos['tipo_documento']=='Book Chapter'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso']),
                  'Editoriales':scopus_productos[scopus_productos['tipo_documento']=='Editorial'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso']),
                  'Cartas':scopus_productos[scopus_productos['tipo_documento']=='Letter'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso']),
                  'Notas':scopus_productos[scopus_productos['tipo_documento']=='Note'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso']),
                  'Erratum':scopus_productos[scopus_productos['tipo_documento']=='Erratum'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso']),
                  'Documento de Datos':scopus_productos[scopus_productos['tipo_documento']=='Data Paper'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso']),
                  'Encuesta Corta':scopus_productos[scopus_productos['tipo_documento']=='Short Survey'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso']),
                  'Libros':scopus_productos[scopus_productos['tipo_documento']=='Book'].drop(columns=['scopus_id','eid','creador','nombre_publicacion','isbn','volumen','issue','numero_articulo','pag_inicio','pag_fin','pag_count','doi','link','affil_id','abstract','tipo_fuente','tipo_documento','etapa_publicacion','autores','autores_id','tipo_acceso'])}


caracteristicas={'idgruplac':'Código de GrupLAC','verificado':'Verificado','tipo':'Tipo','nombre':'Nombre',
                 'lugar':'Lugar','revista':'Revista','issn':'ISSN','fecha':'Fecha','capitulo':'Nombre del Capítulo','libro':'Libro',
                 'editorial':'Editorial','curso':'Nombre del Curso','programa':'Nombre del Programa','disponibilidad':'Disponibilidad',
                 'institucion':'Institución','fecha_registro':'Fecha de Registro','mercado':'Mercado','aval':'Aval',
                 'lineas':'Líneas de Investigación','fecha_formacion':'Fecha de Formación','certificacion':'Certificación',
                 'clasificacion':'Clasificación','areas':'Áreas','programas':'Programas','nombre_comercial':'Nombre Comercial',
                 'titulo':'Título','fecha_publicacion':'Fecha de Publicación','idioma':'Idioma','citado':'Citaciones',
                 'tema':'Temáticas','palabras_clave_autor':'Palabras Clave de Autor','palabras_clave_index':'Palabras Clave Indizadas',
                 'institucion':'Institución','agencia_fundadora':'Agencia Fundadora','pais':'País',
                 'categoria':'Categoría','idcvlac':'Código de CVLAC','sexo':'Sexo','sectores':'Sectores','palabras':'Palabras Clave',
                 'area':'Área','plataforma':'Plataforma','ambiente':'Ambiente'}

referencias={'SCOPUS':
                 {
                    'Artículos':'scopus_productos',
                    'Documentos de Conferencia':'scopus_productos',
                    'Revisiónes':'scopus_productos',
                    'Capítulos':'scopus_productos',
                    'Editoriales':'scopus_productos',
                    'Cartas':'scopus_productos',
                    'Notas':'scopus_productos',
                    'Erratum':'scopus_productos',
                    'Documento de Datos':'scopus_productos',
                    'Encuesta Corta':'scopus_productos',
                    'Libros':'scopus_productos'
                 },
             'GRUPLAC':
                 {
                    'Artículos':'gruplac_articulos','Capítulos':'gruplac_caplibros','Libros':'gruplac_libros',
                    'Cursos de Doctorado':'gruplac_cdoctorado','Cursos de Maestría':'gruplac_cmaestria',
                    'Otros Artículos':'gruplac_oarticulos','Otros Libros':'gruplac_olibros',
                    'Diseño industrial':'gruplac_disenoind','Empresa Tecnológica':'gruplac_empresatec',
                    'Innovación Empresarial':'gruplac_innovaempresa','Otros Productos Tecnológicos':'gruplac_otecnologicos',
                    'Programa de Doctorado':'gruplac_pdoctorado','Programa de Maestría':'gruplac_pmaestria',
                    'Planta Piloto':'gruplac_plantapiloto','Prototipos':'gruplac_prototipos',
                    'Software':'gruplac_software','Institución':'gruplac_instituciones',
                    'Líneas de Investigación':'gruplac_lineas','Datos Básicos':'gruplac_basico'
                 },
             'CVLAC':
                 {
                    'Artículos':'cvlac_articulos','Áreas de Actuación':'cvlac_areas','Datos Básicos':'cvlac_basico',
                    'Datos Básicos':'cvlac_basico','Capítulos':'cvlac_caplibros','Empresa Tecnológica':'cvlac_empresatec',
                    'Identificadores':'cvlac_identificadores','Innovación Empresarial':'cvlac_innovaempresa',
                    'Líneas de Investigación':'cvlac_lineas','Libros':'cvlac_libros','Prototipos':'cvlac_prototipos',
                    'Reconocimientos':'cvlac_reconocimiento','Software':'cvlac_software','Productos Tecnológicos':'cvlac_tecnologicos'
                 }
            }

caracteristicas_invertido= {v: k for k, v in caracteristicas.items()}

fuente_dic={'CVLAC':elementos_cvlac,'GRUPLAC':elementos,'SCOPUS':elementos_scopus}
