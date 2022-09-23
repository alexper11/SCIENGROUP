
"""
import re
h3s="¿patente? ".strip()
k=re.sub('¿|\?','',h3s)
print(k+'d')

libros_aux={}
dato='fdkkj 2012.'.replace(".","")
var=(re.findall(r"(?s:.*)(\d{4})",dato))
if isinstance(var,list) and len(var)!=0:
    print('es lista') 
    index=dato.rfind((var[0]))
    libros_aux['En']=dato[:index]
    libros_aux['fecha']=dato[index:]
    print(index)
else:
    print("no es lista")
    libros_aux['En']=dato
    libros_aux['fecha']=""


#index=dato.rfind(var[0])
#str(re.findall(r"(?s:.*), (\d{4}, \D+)",datos))
#var=re.split(' (\d+)',dato)
print(libros_aux)




#tbody es la lista de todos los trs de la tabla en cuestion
tbody=h3s.parent.parent.parent.find_all('tr')
for i,t in enumerate(tbody):
    if not (i % 2) == 0:
        print(t.find('b'))
"""













"""datos='International journal, a2017, on Semantic Web and Information Systems, a2017, Agosto'
dato=(re.split('(?s:.*), (\d{4}, \D+)',datos))
var=str(re.findall(r"(?s:.*), (\d{4}, \D+)",datos))
index=datos.rfind(var)
c="hola"
index=4
nombre=c[:index]
fecha=datos[index:]
print(nombre)
print(fecha)
"""
"""if isinstance(var,list) and len(var)!=0:
    print('es lista') 
    index=datos.rfind((var[0]))
else:
    print("no es lista")
"""
#nombre=datos
"""

import pandas as pd
url='https://scienti.minciencias.gov.co/gruplac/jsp/visualiza/visualizagr.jsp?nro=00000000003625'

dfs = pd.read_html(url, header=1, match=r'^Integrantes del grupo$')

#dfs=dfs[0].set_index("Datos básicos").T.reset_index(drop=True)
#dfs.columns.name=None
print(dfs[0])#.rename(columns=dfs[0].iloc[0]))#.rename(columns=dfs[4].iloc[1]).drop(labels=[0,1],axis=0))
"""
import re
dato='"NOE ALBAN LOPEZ, ""EVALUACIÓN DE DIFERENTES, "FORMULACIONES DE COMPOSTAJE A PARTIR DE RESIDUOS DE COSECHA DE TOMATE (Solanum lycopersicum)" . En: Colombia" '
if len(re.findall(', "', dato)) > 1:
    print('ok')

c='asdasd....,,,,   '
print(c.rstrip('. ,'))