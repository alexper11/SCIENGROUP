
# Research Group Analitycs Dashboard

Herramienta para el análisis y visualización bibliométrica de la producción científica de los grupos de investigación en el Departamento del Cauca.

Tiene las siguientes características principales:
- Extrae datos de investigadores y grupos de investigación de las plataformas CvLAC, GrupLAC y Scopus, de manera masiva o bajo demanda.
- Búsqueda y eliminación de documentos duplicados.
- Preprocesamiento de datos.
- Emparejamiento de datos entre GrupLAC y Scopus.
- Diferentes gráficos de visualización de datos.
- Redes de colaboración.
- Interfaces gráficas de usuario.

Video instructivo: https://youtu.be/tdp8FPcWMco

---

## Instalación
> [!IMPORTANT]
> ***Para el funcionamiento de la herramienta, es obligatorio tener instalado el gestor de base de datos [PostgreSQL.](https://www.postgresql.org/download/)*** *Si desea utilizar una herramienta gráfica para administrar PostgreSQL se recomienda instalar [PgAdmin 4.](https://www.pgadmin.org/download/)*

Para instalar el proyecto, realice una clonaciòn de la última versión del repositorio ejecutando el siguiente comando git:
```bash
    git clone https://github.com/alexper11/General.git
```
Dentro de la carpeta generada, ejecute el siguiente comando para instalar las librerias necesarias:

```bash
    pip install -r requierements.txt
```

---

## Contenido
- Base de datos para CvLAC, GrupLAC y Scopus.
- Extractor de datos de GrupLAC y CvLAC.
- Extractor de datos de Scopus.
- Dashboard (Tablero de análisis).

## Base de datos para CvLAC, GrupLAC y Scopus.

Los archivos generados en la extracción de datos usados en el dashboard se almacenan en el directorio `dashboard/assets/data/`.


Adicionalmente se brindan las bases de datos de la información extraída de manera masiva para el Departamento del Cauca en Cvlac, GrupLAC y Scopus, estos se encuentran en el directorio `BD/`.

## Extractor de datos de GrupLAC y CvLAC.

Esta herramienta extrae los datos del aplicativo CvLAC y GrupLAC pertenecientes al sistema Scienti en Colombia. Para utilizar esta herramienta, se requiere ingresar el enlace del CvLAC o GrupLAC de interés y la plataforma extraerá la información pública disponible en el sistema.
Se recomienda que cualquier persona que utilice esta herramienta lea detenidamente la [política de privacidad y los términos de uso](https://minciencias.gov.co/ciudadano/terminosycondiciones-datospersonales) definidos por MinCiencias, que establece las pautas y normas para el uso ético de los datos.

## Extractor de datos de Scopus.

Esta herramienta extrae datos de la plataforma Scopus. Para ello es necesario el registro de un Apikey suministrado por Scopus y un Token avalado por la institución.

## Dashboard

Se integra una sección llamada “Explorar datos” con el objetivo de inspeccionar los datos previamente obtenidos y preprocesados por medio de los sistemas de extracción, adicionalmente se integran dos secciones para el análisis y visualización de los datos provenientes de GrupLAC y Scopus. El dashboard está desarrollado dentro del marco del trabajo de grado titulado “Dashboard para el análisis y visualización bibliométrica dentro del ámbito de los grupos de investigación en el departamento del Cauca” desarrollado en la Universidad del Cauca por los estudiantes Jarby Daniel Salazar Galindez y Edison Alexander Mosquera Perdomo. El dashboard busca ser un asistente para los actores del Sistema Regional de Ciencia, Tecnología e Innovación del Cauca.

---

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

---

Para verificar la consistencia entre los datos extraídos y los registrados en las plataformas de CvLAC y GrupLAC, ejecute el siguiente comando :

```bash
  python testing_main.py
```
Tenga en cuenta que la verificación se hace con respecto a los archivos CSV que debe generar manualmente, para ello reemplace y siga la estructura de los archivos para [CvLAC](cvlac/testing/testing_cvlac)  y [GrupLAC.](cvlac/testing/testing_gruplac)

---

> [!NOTE]
> Para expandir el uso del proyecto a otros departamentos de Colombia, utilice el [buscador de grupos por departamento](https://scienti.minciencias.gov.co/ciencia-war/BusquedaGrupoXDepartamento.do) de Minciencias para elegir el departamento de interés y reemplace la url utilizada en la línea 83 del archivo main.py

Ejemplo utilizado para el Departamento del Cauca:
```python
[83] lista_gruplac=Extractor.get_gruplac_list('https://scienti.minciencias.gov.co/ciencia-war/busquedaGrupoXDepartamentoGrupo.do?codInst=&sglPais=COL&sgDepartamento=CA&maxRows=15&grupos_tr_=true&grupos_p_=1&grupos_mr_=130')    
```
---

> [!WARNING]
>*Debido al gran volúmen de datos utilizado, para evitar problemas de caché se recomienda desplegar el proyecto desde un navegador privado.*

---

## Autores

- [Jarby Daniel Salazar Galindez](https://www.github.com/jarbydaniel)
- [Edison Alexander Mosquera Perdomo](https://www.github.com/alexper11)

## License

[MIT](https://choosealicense.com/licenses/mit/)
