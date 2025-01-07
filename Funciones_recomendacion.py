import ast
import nltk
from rake_nltk import Rake
#nltk.download('stopwords')
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import unicodedata as un

def matriz_k_vecinos_sim_cos(df):
    '''Arma la matriz con los primeros 100 vecinos mas parecidos (en terminos de la similitud del coseno). Paramtros:
    - df: Dataframe con la informacion a comparar entre película y película (deben ser textos o palabras). 
      Debe tener una colúmna con todos los tíulos de las películas llamada "titulos" y una con la descripcion de cda película. 
      Los valores Nan deben ser reemplazados previamente por " " (columnas con str) y "[]" (columnas con listas).'''
    
    for columna in df.columns:   #transformo str-->list en as columnas que tienen listas 
        if df.loc[0,columna].startswith("["):
            df[columna]=df[columna].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    #veo que columa str tiene mas caracteres para identifucarla como la que tiene las descripciones de las películas
    tamaño_columnas = {
        columna: df[columna].str.len().max()
        for columna in df.columns
        if not isinstance(df.loc[0, columna], list)}
    max_key = max(tamaño_columnas, key=tamaño_columnas.get) 

    #creo una columna con las palabras que mas se repiten de la columna con descropciones de las películas. La librería rake_nltk, luego de correr "nltk.download('stopwords')", contiene una lista de palabras que no cuentan como palabras reelevenates 
    df["palabras_clave_descripcion"] = ""
    r = Rake() #creo una instancia de la clase Rake. Me permite desatacar las palabras impotantes de una variable str
    for i, fila in df.iterrows():
        r.extract_keywords_from_text(fila[max_key]) #extrae las palanras clave de cada entrada de la columna "descripcion"
        palabras_puntuaciones = r.get_word_degrees()  #crea un diccionario donde las keys son las palabras reelevantes y los valores, sus puntuaciones de reelevancia
        df.at[i,"palabras_clave_descripcion"] = list(palabras_puntuaciones.keys()) #crea una lista con las keys (palabras impotantes) del diccionario "palabras_puntuaciones" 
    
    #Se quita los espacios en las variables str para que, luego al comparar, por ejemplo, "cris hemsworth" con "cris evans" tome la palabra "cris" como coincidencia
    lista_de_columnas=df.columns.drop(["titulo",max_key,"palabras_clave_descripcion"])
    for columna in lista_de_columnas:
        if type(df.loc[0,columna])==list:
            df[columna]=df[columna].map(lambda col: [x.lower().replace(' ', '') for x in col]) #quita las mayúsculas y los espacios dentro de una misma variable str
        else:
            df[columna]=df[columna].map(lambda x: x.split(',')) #convierte las palabras separadas por comas en una entrada en una lista de esas palabras
            df[columna]=df[columna].map(lambda col: [x.lower().replace(' ', '') for x in col])
    
    df["palabras"]=""  # Inicializa la columna "palabras"
    lista_de_columnas1=df.columns.drop(["titulo",max_key])
    #juntamos todas las palabras de las columnas de la lista "columnas" en una sola columna "palabras"
    for i, fila in df.iterrows():
        palabra=""
        for col in lista_de_columnas1:
            palabra+=" ".join(fila[col])+" " #junta todas las palabras de las columnas en una sola variable str separadas por espacios 
        df.loc[i,"palabras"]=palabra.strip()  #pone la variable palabra dentro de la columna "palabras"
    df_final=df[["titulo","palabras"]] #crea un dataframe solo con la columna "titulo" y  "palabras"

    #Una matriz de comparacion con la similitud del conseno de 45480x45480 ocupa demaciado memoria y no se puede cargar, por lo que la dividiremos en bloques y de allí de sdestacarán los primeros k vecinos mas cercanos "parecidos"
    count=CountVectorizer() #CountVectorizer() divide textos en palabras y cuneta la frecuencia de ocurrencia de cada una (no cuenta las stop words)
    matriz_count=count.fit_transform(df_final["palabras"])  #.fit_transform() convierte el texto en una matriz que representa la frecuencia de cada palabra
    # Definir parámetros
    tamanio_bloque=1000  # Tamaño del bloque para manejar la memoria
    k=5  # Número de vecinos más cercanos a guardar
    # Lista para almacenar los resultados
    resultados_vecinos=[]
    # Procesamiento de los bloques
    for i in range(0, df_final.shape[0], tamanio_bloque):
        bloque_inicio=i
        bloque_fin=min(i+tamanio_bloque, df_final.shape[0])
        print(f"Procesando bloque {bloque_inicio}-{bloque_fin}")
        # Calcula similitud coseno para el bloque actual
        bloque_actual=matriz_count[bloque_inicio:bloque_fin]
        similitudes=cosine_similarity(bloque_actual, matriz_count)
        # Guardar solo los k vecinos más cercanos para cada fila
        for fila_sim in similitudes:
            # Obtener índices de los k mayores valores (excepto la diagonal)
            k_vecinos=np.argsort(fila_sim)[-k-1:-1][::-1]
            resultados_vecinos.append(k_vecinos)
    # Convertimos los resultados a un arreglo numpy (matriz)
    resultados_vecinos=np.array(resultados_vecinos)
    #La fila i de la matriz resultados_vecinos tiene k vecinos que se acemejan mas (bajo el criterio de la similitud del conseno) a la i-ésima película del dataframe df
    return resultados_vecinos

def sist_recomendacion(titulo,df,matriz_primeros_vecinos,n=5):
    '''Recomienda n películas a parti de la ingresada. Parámetros:
    - titulos: película a partir de la cual se hacen las recomendaciones.
    - df: dataframe con los nombres de las películas. Tiene que ser a partir del cual se armó la matriz de primeros vecinos.
    - matriz_primeros_vecinos: matriz con los primeros vecinos mas parecidos a la pelícual ingresada.
    - n: numero de recomendaciones que se quieren (maximo 100). El valor por defecto es 5.'''

    def normalizacion(palabra):
        palabra=palabra.lower()
        palabra=''.join(i for i in un.normalize('NFD',palabra) if un.category(i)!='Mn')
        return palabra
    titulo_normalizado=normalizacion(titulo)
    df['titulo_normalizado']=df['titulo'].apply(normalizacion)
    
    # Buscar el índice del título en el DataFrame
    if titulo_normalizado not in df['titulo_normalizado'].values:
        return ["Título no encontrado en la base de datos."]
    
    indice=df[df['titulo_normalizado']==titulo_normalizado].index[0]
    
    # Obtener los índices de las películas recomendadas
    peliculas_indices = matriz_primeros_vecinos[indice,:n]
    
    # Retornar los títulos recomendados
    return df.loc[peliculas_indices, 'titulo'].tolist()