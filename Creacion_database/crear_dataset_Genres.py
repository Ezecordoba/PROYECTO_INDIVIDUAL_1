import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import Funciones_normalizacion as fn

#creamos el dataframe
movies = pd.read_csv('./Database/movies_dataset.csv',delimiter = ',',encoding = "utf-8")

claves_de_interes=["name"]
generos=fn.csv_columna_desanidada(movies,"list","genres",claves_de_interes)

generos=generos.rename(columns={"Id_nuevo": "Id_genre"})
generos=generos.rename(columns={"name": "genre"})

#guardeo el dataframe en un csv 
generos.to_csv('./Database/genres.csv', index=False)