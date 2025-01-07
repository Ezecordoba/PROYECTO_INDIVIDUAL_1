A continuación, se explica el contenido de cada archivo, notebook y directorio presente en este repositorio:

- **`Funciones.py`**  
  Contiene las funciones que debían desarrollarse como parte del ejercicio.

- **`Funciones_normalizacion.py`**  
  Este archivo contiene las funciones utilizadas en las notebooks 
  [`Procesamiento_credits.ipynb`](Procesamiento_credits.ipynb) y 
  [`Procesamiento_movies.ipynb`](Procesamiento_movies.ipynb), facilitando el 
  proceso de desanidado de los datos en los datasets originales.

- **`Funciones_recomendacion.py`**  
  Contiene las funciones empleadas en la notebook 
  [`sistema_de_recomendacion.ipynb`](sistema_de_recomendacion.ipynb). Estas 
  funciones crean la matriz de similitud (basada en la similitud del coseno) y 
  generan la lista de películas recomendadas.

- **`Funciones_FastApi.py`**  
  Aquí se desarrolla la aplicación de **FastAPI**, donde se definen los distintos 
  endpoints que reprecentan las funciones a desarrollar para este proyecto.

- **`Procesamiento_movies.ipynb`**  
  En esta notebook se detalla el proceso de normalización para generar el dataset 
  `movies_normalizado.csv` a partir del archivo original `movies_dataset.csv`.

- **`Procesamiento_credits.ipynb`**  
  Explica el proceso de normalización para crear el dataset `credits_normalizado.csv`
  a partir del archivo `credits.csv`.

- **`sistema_de_recomendacion.ipynb`**  
  Muestra cómo funcionan las funciones de 
  [`Funciones_recomendacion.py`](Funciones_recomendacion.py) mediante un 
  ejemplo práctico para la generación de recomendaciones de películas.

- **`EDA.ipynb`**  
  Presenta el Análisis Exploratorio de Datos (EDA) realizado sobre el dataset 
  `movies_normalizado.csv`.
  
- **`Creacion_database`**
  Aquí se presentan los archivos .py que crean las tablas de dimensión

- **`Database`**
  Aquí se encuentran las tablas de hecho y las de dimensión de la base de datos

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
**`Resumen del procesamiento realizado sobre el dataset movies_dataset.csv`**

Se eliminó la columna anidada `spoken_languages` ya que no es util para el análisis. A las columnas anidadas `genres`, `production_companies`, `production_countries` fueron convertidas a   columnas con una lista de los géneros, companias productoras y parises productores respectivamente. De la columna `belongs_to_collection` la única información util era la del nombre de     la franquicia a la que pertenece la película, ya que es un buen parámetro para agruparlas. Tambien se cambió el id original de la tabla para cambiarlo por un nuevo Id_movies que arranca    desde 1. A partir de este dataset tambien se crearon las tablas de dimension que nos permitieron eliminar las columnas `franchise`, `status`, `language` y `title` para solo dejar los     
id's   correspondientes a cada una.

**`Resumen del procesamiento realizado sobre el dataset credits.csv`**

**`Funcionamiento de la funcion de recomendacion`** 

Para el funcionamiento lo que se utilizan son las columnas `overview`, `language`, `franchise`, `"genres"`, `production_companies`, `actors` y `directors`. El calculo de la matriz de similitud se realizó aparte de la funcion `recomendacion`. El objetivo de esto es no tener que calcular esta matriz cada vez que se busca correr la funcion de recomendacion, ya que este proceso puede tardar al rededor de 5 minutos. Lo que se hace primero es sacar las palabras reelevantes de la columna `overview`, de las otras columnas se usa todo el texto. Luego se junta todo el texto de las columnas en una sola llamada `palabras`. Esta es con la cual se genera la matriz de similitud con la `similitud del coseno`. El problema es que, como el dataset tiene mas de 40000 de filas, no se puede hacer todo el proceso se calculo de similitud en una sola matriz ya que ocupa mucho espacio. Para resolver esto se dividió el dataset en bloques de mil filas. Una vez terminado el cálculo se juntó todo en una sola matriz y se creó otra matriz donde figuran los índices de las 5 palículas mas similares a la película de la fila correspondiente. A esta matriz se la guardó en un archivo de numpy y luego se utilizará dentro de la funcion `recomendacion`. 
El paso a paso de como se hace este cálculo se explica en el notebook `sistema_de_recomendacion.ipynb`.
