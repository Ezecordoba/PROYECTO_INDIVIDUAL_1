from babel.dates import format_date
from datetime import datetime
from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import unicodedata as un
import ast
import nltk
from rake_nltk import Rake
nltk.download('stopwords')
nltk.download('punkt_tab')

# Cargar los datasets como variables globales
movies = pd.read_csv('Database/movies_normalizado.csv', delimiter=',', encoding="utf-8")
titulos = pd.read_csv('Database/titles.csv', delimiter=',', encoding="utf-8")
credit = pd.read_csv('Database/credits_normalizado.csv', delimiter=',', encoding="utf-8")
franchises = pd.read_csv('Database/franchise.csv', delimiter=',', encoding="utf-8")
languages = pd.read_csv('Database/languages.csv', delimiter=',', encoding="utf-8")
texto = pd.read_csv('Sistema_de_recomendacion/texto_peliculas.csv', delimiter=',', encoding='utf-8')
matriz_primeros_vecinos=np.load("Sistema_de_recomendacion/matriz_k_vecinos.npy")

app = FastAPI()

app.title="Base de datos de películas"

# Normalización de palabras
def normalizacion(palabra):
    palabra = palabra.lower()
    palabra = ''.join(i for i in un.normalize('NFD', palabra) if un.category(i) != 'Mn')
    return palabra
def nombre_dia(fecha):
    '''Retorna el nombre del día en español (en minúsculas).'''
    if pd.isnull(fecha):
        return None
    # Con 'EEEE' Babel retorna el día completo (por ejemplo, 'lunes')
    return format_date(fecha, format='EEEE', locale='es').lower()

@app.get("/cantidad_filmaciones_mes/",tags=["Cantidad de estrenos"])
def cantidad_filmaciones_mes(mes: str):
    '''Devuelve la cantidad de películas que se estrenaron en el mes ingresado.'''
    try:
        movies2=movies.copy()
        movies2["release_date"] = pd.to_datetime(movies2["release_date"], errors='coerce')
        movies2["meses"] = movies2["release_date"].dt.month
        meses = {"mes": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
                "numero_mes": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
        mes = normalizacion(mes)
        if mes in meses["mes"]:
            index = meses["mes"].index(mes)
            movies_filtrado = movies2[movies2["meses"] == meses["numero_mes"][index]]
            return len(movies_filtrado)
        else:
            raise HTTPException(status_code=400, detail="El mes ingresado no es válido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cantidad_filmaciones_dia/",tags=["Cantidad de estrenos"])
def cantidad_filmaciones_dia(dia: str):
    '''Devuelve el número de películas estrenadas en el día ingresado.'''
    try:
        movies3 = movies.copy()
        dia = normalizacion(dia)
        dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        if dia not in dias:
            raise HTTPException(status_code=400, detail="El día ingresado no es válido")
        movies3["release_date"] = pd.to_datetime(movies3["release_date"], errors='coerce')
        movies3["dias"] = movies3["release_date"].apply(nombre_dia)
        movies3["dias"] = movies3["dias"].apply(normalizacion)
        movies_filtrado = movies3[movies3["dias"] == dia]
        return len(movies_filtrado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/score_titulo/",tags=["Películas"])
def score_titulo(titulo: str):
    '''Devuelve una lista con el título de la película ingresado, el año de estreno y el score de popularidad.'''
    try:
        movies_merged = movies.merge(titulos[["Id_movie", "title"]], on="Id_movie", how="left")
        movies_merged["release_date"] = pd.to_datetime(movies_merged["release_date"], errors='coerce')
        titulo_normalizado = normalizacion(titulo)
        movies_merged["titulos_normalizados"] = movies_merged["title"].apply(normalizacion)
        movies_filtrado = movies_merged[movies_merged["titulos_normalizados"] == titulo_normalizado]
        
        if not movies_filtrado.empty:
            pelicula = movies_filtrado.iloc[0]
            return {"titulo": pelicula["title"], "año": pelicula["release_date"].year, "popularidad": pelicula["popularity"]}
        else:
            raise HTTPException(status_code=404, detail="Película no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/votos_titulo/",tags=["Películas"])
def votos_titulo(titulo: str):
    '''Devuelve un diccionario con el título de la película ingresado, el número de votaciones y la valoración promedio.'''
    try:
        movies_merged = movies.merge(titulos[["Id_movie", "title"]], on="Id_movie", how="left")
        titulo_normalizado = normalizacion(titulo)
        movies_merged["titulos_normalizados"] = movies_merged["title"].apply(normalizacion)
        movies_filtrado = movies_merged[movies_merged["titulos_normalizados"] == titulo_normalizado]
        
        if not movies_filtrado.empty:
            pelicula = movies_filtrado.iloc[0]
            if pelicula["vote_count"] >= 2000:
                return {"titulo": pelicula["title"], "votos": pelicula["vote_count"], "valoracion_promedio": pelicula["vote_average"]}
            else:
                return {"titulo": pelicula["title"], "votos": pelicula["vote_count"], "valoracion_promedio": None}
        else:
            raise HTTPException(status_code=404, detail="Película no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_actor/",tags=["Actores y Directores"])
def get_actor(actor: str):
    '''Esta función retorna un diccionario con el nombre del actor ingresado, el número de películas en el que actúa,
       el retorno total que tiene y el retorno promedio por pelicula.'''
    try:
        credit1=credit.copy()
        actor = normalizacion(actor)
        credit1["actors_normalizado"] = credit1["actors"].apply(normalizacion)
        credit_merged = credit1.merge(movies[["Id_movie", "return"]], on="Id_movie", how="left")
        credit_filtrado=credit_merged[credit_merged["actors_normalizado"].apply(lambda x: actor in x)]
        
        if not credit_filtrado.empty:
            nro_peliculas = len(credit_filtrado)
            retorno_total = credit_filtrado["return"].sum()
            retorno_promedio = retorno_total / nro_peliculas
            return {"actor": actor, "numero_peliculas": nro_peliculas, "retorno_total": round(retorno_total,2), "retorno_promedio": round(retorno_promedio,2)}
        else:
            raise HTTPException(status_code=404, detail="Actor no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_director/",tags=["Actores y Directores"])
def get_director(director: str):
    '''Esta función retorna una lista con el nombre del director ingresado, el número de películas que dirigió,
       el retorno total que tiene y el retorno promedio por pelicula.'''
    try:
        credit2=credit.copy()
        director = normalizacion(director)
        credit2["director_normalizado"] = credit2["directors"].apply(normalizacion)
        credit_merged = credit2.merge(movies[["Id_movie", "return", "budget", "revenue", "release_date"]], on="Id_movie", how="left")
        credit_merged = credit_merged.merge(titulos[["Id_movie","title"]], on="Id_movie", how="left")
        credit_filtrado=credit_merged[credit_merged["director_normalizado"].apply(lambda x: director in x)]
        credit_filtrado.drop(columns=["Id_movie","actors","directors","director_normalizado"],inplace=True)
        
        if not credit_filtrado.empty:
            retorno_total = credit_filtrado["return"].sum()
            return {"director": director, "retorno_total": round(retorno_total,2), "info_peliculas": credit_filtrado.to_dict(orient='records')}
        else:
            raise HTTPException(status_code=404, detail="Director no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sist_recomendacion_con_matriz/",tags=["Recomendación de Películas"])
def recomendacion(titulo: str) -> List[str]:
    '''Devuelve una lista de películas recomendadas basadas en el título ingresado.'''
    try:
        texto1=texto.copy()
        titulo_normalizado = normalizacion(titulo)
        texto1['titulo_normalizado'] = texto1['titulo'].apply(normalizacion)

        if titulo_normalizado not in texto1['titulo_normalizado'].values:
            raise HTTPException(status_code=404, detail="Título no encontrado en la base de datos.")

        indice = texto1[texto1['titulo_normalizado'] == titulo_normalizado].index[0]
        peliculas_indices = matriz_primeros_vecinos[indice, :5]

        return texto1.loc[peliculas_indices, 'titulo'].tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   
