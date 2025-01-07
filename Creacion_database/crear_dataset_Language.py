import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import Funciones_normalizacion as fn

movies = pd.read_csv('./Database/movies_dataset.csv',delimiter = ',',encoding = "utf-8")

claves_de_interes=["iso_639_1","name"]
language=fn.csv_columna_desanidada(movies,"list","spoken_languages",claves_de_interes)

language=language.rename(columns={"Id_nuevo": "Id_language"})
language=language.rename(columns={"iso_639_1": "language"})
language.drop(columns="name",inplace=True)
#guardeo el dataframe en un csv 
language.to_csv('./Database/languages.csv', index=False)