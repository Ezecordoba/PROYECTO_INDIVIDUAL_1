def cantidad_filmaciones_mes(mes):
    '''Devuelve la cantidad de películas que se estrenaron en el mes ingresado. 
    Si ya se importaton las librerías y se crearon los dataframe fuera de la función se pueden comentar esas lineas del código'''
    #Se impotan las linrerías necesarias
    import pandas as pd 
    import unicodedata as un
    def normalizacion(palabra):
        palabra=palabra.lower()  #saca las mayúsculas de la palabra
        palabra=''.join(i for i in un.normalize('NFD',palabra) if un.category(i)!='Mn')   #quita la tilde de la palabra
        return palabra
    movies = pd.read_csv('./Database/movies_normalizado.csv',delimiter = ',',encoding = "utf-8")  #se crea el dataframe 
    movies["release_date"] = pd.to_datetime(movies["release_date"],errors='coerce')  #convierte la columna release_date a tipo datetime 
    movies["meses"]=movies["release_date"].dt.month
    mes=normalizacion(mes)
    meses={"mes":["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"],
           "numero_mes":[1,2,3,4,5,6,7,8,9,10,11,12]}
    if mes in meses["mes"]:
        for i in range(12):
            if mes==meses["mes"][i]:
                movies_filtrado=movies[movies["meses"].apply(lambda x: meses["numero_mes"][i]==x)]
                nro_peliculas=movies_filtrado.shape[0]  
    else:
        print("No ha ingresado un mes del año en español")
        nro_peliculas=0
    return nro_peliculas
#----------------------------------------------------------------------------------------------
def cantidad_filmaciones_dia(dia):
    '''Devuelve el numero de películas estrenadas en el dia ingresado.
    Si ya se importaton las librerías y se crearon los dataframe fuera de la función se pueden comentar esas lineas del código'''
    import pandas as pd
    import locale
    import unicodedata as un
    from datetime import datetime
    def normalizacion(palabra):
        palabra=palabra.lower()  #saca las mayúsculas de la palabra
        palabra=''.join(i for i in un.normalize('NFD',palabra) if un.category(i)!='Mn')   #quita la tilde de la palabra
        return palabra
    def nombre_dia(fecha):
        locale.setlocale(locale.LC_TIME, 'spanish')  #Esto sirve para que los nombres de los dias estén es español
        dia=fecha.strftime('%A')
        return dia
    movies = pd.read_csv('./Database/movies_normalizado.csv',delimiter = ',',encoding = "utf-8")  #se crea el dataframe 
    movies["release_date"] = pd.to_datetime(movies["release_date"],errors='coerce')  #convierte la columna release_date a tipo datetime
    movies["dias"]=movies["release_date"].apply(nombre_dia)
    movies["dias"]=movies["dias"].apply(normalizacion)
    dias=["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]
    dia=normalizacion(dia)
    if dia in dias:
        movies_filtrado=movies[movies["dias"].apply(lambda x: dia in x)]
        nro_peliculas=movies_filtrado.shape[0]
    else:
        print("No estcribió un dia en español")
        nro_peliculas=0
    return nro_peliculas 
#----------------------------------------------------------------------------------------------
def score_titulo(titulo):
    '''Devuelve una lista con el título de la película ingresado, el año de estreno y el score de popularidad.
    Si ya se importaton las librerías y se crearon los dataframe fuera de la función se pueden comentar esas lineas del código'''    
    import pandas as pd
    import unicodedata as un
    def normalizacion(palabra):
        palabra=palabra.lower()
        palabra=''.join(i for i in un.normalize('NFD',palabra) if un.category(i)!='Mn')
        return palabra
    movies = pd.read_csv('./Database/movies_normalizado.csv',delimiter = ',',encoding = "utf-8")  #se crea el dataframe 
    titulos= pd.read_csv('./Database/titles.csv',delimiter = ',',encoding = "utf-8")
    movies=movies.merge(titulos[["Id_movie", "title"]], left_on="Id_movie", right_on="Id_movie", how="left")
    movies["release_date"] = pd.to_datetime(movies["release_date"],errors='coerce')
    titulo_normalizado=normalizacion(titulo)
    movies["titulos_normalizados"]=movies["title"].apply(normalizacion)
    movies_filtrado=movies[movies["titulos_normalizados"].apply(lambda x: titulo==x)]
    movies_filtrado.reset_index(inplace=True)
    if movies_filtrado.shape[0]>0:
        info={"Pelicula":movies_filtrado.loc[0,"title"],"Fecha de estreno":movies_filtrado.loc[0,"release_date"].year,"Popularidad":float(movies_filtrado.loc[0,"popularity"])}
    else:
        info={"Pelicula":titulo,"Fecha de estreno":None,"Popularidad":None}
    return info
#----------------------------------------------------------------------------------------------
def votos_titulo(titulo):
    '''Devuelve un diccionario con el título de la película ingresado, el número de votaciones y la valoración promedio.
    Si ya se importaton las librerías y se crearon los dataframe fuera de la función se pueden comentar esas lineas del código'''    
    import pandas as pd
    import unicodedata as un
    def normalizacion(palabra):
        palabra=palabra.lower()
        palabra=''.join(i for i in un.normalize('NFD',palabra) if un.category(i)!='Mn')
        return palabra
    movies = pd.read_csv('./Database/movies_normalizado.csv',delimiter = ',',encoding = "utf-8") 
    titulos= pd.read_csv('./Database/titles.csv',delimiter = ',',encoding = "utf-8")
    movies=movies.merge(titulos[["Id_movie", "title"]], left_on="Id_movie", right_on="Id_movie", how="left")
    titulo=normalizacion(titulo)
    movies["titulos_normalizados"]=movies["title"].apply(normalizacion)
    movies_filtrado=movies[movies["titulos_normalizados"].apply(lambda x: titulo==x)]
    movies_filtrado.reset_index(inplace=True)
    if movies_filtrado.shape[0]>0 and float(movies_filtrado.loc[0,"vote_count"])>=2000:
        info={"Pelicula":movies_filtrado.loc[0,"title"],"Numero de votos":float(movies_filtrado.loc[0,"vote_count"]),"Votacion promedio":float(movies_filtrado.loc[0,"vote_average"])}
    else:
        info={"Pelicula":titulo,"Numero de votos":None,"Votacion promedio":None}
    return info
#----------------------------------------------------------------------------------------------
def get_actor(actor):
    '''Esta función retorna un diccionario con el nombre del actor ingresado, el número de películas en el que actúa,
       el retorno total que tiene y el retorno promedio por pelicula. 
       Si ya se importaton las librerías y se crearon los dataframe fuera de la función se pueden comentar esas lineas del código'''
    import pandas as pd
    import unicodedata as un
    def normalizacion(palabra):
        palabra=palabra.lower()
        palabra=''.join(i for i in un.normalize('NFD',palabra) if un.category(i)!='Mn')
        return palabra
    movies = pd.read_csv('./Database/movies_normalizado.csv',delimiter = ',',encoding = "utf-8") 
    credit=pd.read_csv('./Database/credits_normalizado.csv',delimiter=',',encoding="utf-8")
    actor=normalizacion(actor)
    credit["actors_normalizado"]=credit["actors"].apply(normalizacion)
    credit=credit.merge(movies[["Id_movie", "return"]], left_on="Id_movie", right_on="Id_movie", how="left")
    credit_filtrado=credit[credit["actors_normalizado"].apply(lambda x: actor in x)]
    nro_peliculas=len(credit_filtrado)
    retorno=credit_filtrado["return"].sum()
    if nro_peliculas>0:
        prom_retorno=retorno/nro_peliculas
        return {"Actor":actor,"Numero de peliculas":nro_peliculas,"Retorno":retorno,"Retorno promedio por película":retorno/nro_peliculas}
    else:
        print("El actor ingresado no está en ninguna película dentro de la base de datos")
        return {"Actor":actor,"Numero de peliculas":0,"Retorno":0,"Retorno promedio por película":0}
#----------------------------------------------------------------------------------------------
def get_director(director):
    '''Esta función retorna una lista con el nombre del director ingresado, el número de películas que dirigió,
       el retorno total que tiene y el retorno promedio por pelicula. 
       Si ya se importaton las librerías y se crearon los dataframe fuera de la función se pueden comentar esas lineas del código'''
    import pandas as pd
    import unicodedata as un
    def normalizacion(palabra):
        palabra=palabra.lower()
        palabra=''.join(i for i in un.normalize('NFD',palabra) if un.category(i)!='Mn')
        return palabra
    movies = pd.read_csv('./Database/movies_normalizado.csv',delimiter = ',',encoding = "utf-8")
    titulos= pd.read_csv('./Database/titles.csv',delimiter = ',',encoding = "utf-8")
    credit=pd.read_csv('./Database/credits_normalizado.csv',delimiter=',',encoding="utf-8")
    director=normalizacion(director)
    credit["director_normalizado"]=credit["directors"].apply(normalizacion)
    credit=credit.merge(movies[["Id_movie", "return"]], left_on="Id_movie", right_on="Id_movie", how="left")
    credit=credit.merge(titulos[["Id_movie", "title"]], left_on="Id_movie", right_on="Id_movie", how="left")
    credit=credit.merge(movies[["Id_movie", "budget"]], left_on="Id_movie", right_on="Id_movie", how="left")
    credit=credit.merge(movies[["Id_movie", "revenue"]], left_on="Id_movie", right_on="Id_movie", how="left")
    credit=credit.merge(movies[["Id_movie", "release_date"]], left_on="Id_movie", right_on="Id_movie", how="left")
    credit_filtrado=credit[credit["director_normalizado"].apply(lambda x: director in x)]
    credit_filtrado.drop(columns=["Id_movie","actors","directors","director_normalizado"],inplace=True)
    retorno=credit_filtrado["return"].sum()
    if credit_filtrado.shape[0]>0:
        return {"Director":director,"Retorno":retorno,"Info_peliculas":credit_filtrado}
    else:
        df=pd.DataFrame({"return":[],"title":[],"budget":[],"revenue":[],"release_date":[]})
        print("El actor ingresado no está en ninguna película dentro de la base de datos")
        return {"Director":director,"Retorno":retorno,"Info_peliculas":df}