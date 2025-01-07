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
