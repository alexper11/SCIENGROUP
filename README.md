# General


El proyecto en su versión actual extrae información relevante de perfiles de investigadores en Colombia a través de métodos de scraping usados sobre la pagina web de CVLAC y GRUPLAC, esto con ayuda de las librerías 'requests' y 'BeautifulSoup' de Python. Además extrae información de investigadores cuyos perfiles están presentes en la base de datos de Scopus así cómo sus publicaciones
y afiliaciones haciendo uso de una 'API KEY'  y un 'INSTITUTIONAL TOKEN' solicitados previamente a la firma. Los datos se persisten de forma estructurada en bases de datos construidas en PostgreSQL a través de un ORM (SqlAlchemy) en Python que permite realizar operaciones CRUD sobre las tablas.

Los modulos 'cvlac' y 'scopus' contienen las clases, metodos, modelos y controladores con los cuales se realizan todas las funciones mencionadas previamente.