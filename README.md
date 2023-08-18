
# Research Group Analitycs Dashboard

Herramienta para el análisis y visualización bibliométrica de la producción científica de los grupos de investigación en el departamento del Cauca.

Tiene las siguientes características principales:
- Extrae datos de investigadores y grupos de investigación de las plataformas CvLAC, GrupLAC y Scopus, de manera masiva o bajo demanda.
- Búsqueda y eliminación de documentos duplicados.
- Preprocesamiento de datos.
- Emparejamiento de datos entre GrupLAC y Scopus.
- Diferentes gráficos de visualización de datos.
- Redes de colaboración.
- Interfaces gráficas de usuario.



## Instalación

*Nota importante: para el funcionamiento de la herramienta, es obligatorio tener instalado [PostgreSQL.](https://www.postgresql.org/download/)*

Para clonar directamente la última versión del repositorio ejecute el siguiente comando git:
```bash
    git clone https://github.com/alexper11/General.git
```
Dentro de la carpeta generada, ejecute el siguiente comando para instalar las librerias necesarias:

```bash
    pip install -r requierements.txt
```
    
## Contenido
- Extractor de datos de GrupLAC y CvLAC.
- Extractor de datos de Scopus.
- Dashboard (Tablero de análisis).


## Extractor de datos de GrupLAC y CvLAC.

Esta herramienta extrae los datos del aplicativo CvLAC y GrupLAC pertenecientes al sistema Scienti en Colombia. Para utilizar esta herramienta, se requiere ingresar el enlace del CvLAC o GrupLAC de interés y la plataforma extraerá la información pública disponible en el sistema.
Se recomienda que cualquier persona que utilice esta herramienta lea detenidamente la [política de privacidad y los términos de uso](https://minciencias.gov.co/ciudadano/terminosycondiciones-datospersonales) definidos por MinCiencias, que establece las pautas y normas para el uso ético de los datos.

## Extractor de datos de Scopus.

Esta herramienta extrae datos de la plataforma Scopus. Para ello es necesario el registro de un Apikey suministrado por Scopus y un Token avalado por la institución.

## Dashboard

Se integra una sección llamada “Explorar datos” con el objetivo de inspeccionar los datos previamente obtenidos y preprocesados por medio los sistemas de extracción.
 
Se integran dos secciones para el análisis y visualización de los datos provenientes de GrupLAC y Scopus. El dashboard está desarrollado dentro del marco del trabajo de grado titulado “Dashboard para el análisis y visualización bibliométrica dentro del ámbito de los grupos de investigación en el departamento del Cauca” desarrollado en la Universidad del Cauca por los estudiantes Jarby Daniel Salazar Galindez y Edison Alexander Mosquera Perdomo. El dashboard busca ser un asistente para los actores del Sistema Regional de Ciencia, Tecnología e Innovación del Cauca.


## Instrucciones para ejecutar el proyecto

Para extraer los datos de CvLAC, Gruplac y Scopus de forma masiva (uso para administradores), ejecute el siguiente comado:

```bash
    python main.py    
```
Luego de la extracción, se ejecuta el preprocesamiento de los datos con el siguiente comando:

```bash
    python preprocessing.py
```
Para extraer los datos de CvLAC, Gruplac y Scopus bajo demanda (con interfaz de usuario), siga los siguientes pasos:

Para ejecutar la interfaz de usuario del extractor de CvLAC y Gruplac:
```bash
  python interfaz_extractor_scienti.py
```
Abra el siguiente link en el navegador: `127.0.0.1:5006`

Para ejecutar la interfaz de usuario del extractor de Scopus:
```bash
  python interfaz_extractor_scopus.py
```
Abra el siguiente link en el navegador: `127.0.0.1:5005`

Para ejecutar el dashboard ejecute el siguiente comando:
```bash
  python dashboard/index.py
```
Abra el siguiente link en el navegador: `localhost:8051`

## Autores

- [Jarby Daniel Salazar Galindez](https://www.github.com/jarbydaniel)
- [Edison Alexander Mosquera Perdomo](https://www.github.com/alexper11)

## License

[MIT](https://choosealicense.com/licenses/mit/)
