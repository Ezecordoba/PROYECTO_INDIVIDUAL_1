import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import Funciones_normalizacion as fn

#creamos el dataframe
movies = pd.read_csv('./Database/movies_dataset.csv',delimiter = ',',encoding = "utf-8")

claves_de_interes=["iso_3166_1","name"]
paises=fn.csv_columna_desanidada(movies,"list","production_countries",claves_de_interes)

paises=paises.rename(columns={"Id_nuevo": "Id_production_countri"})
paises=paises.rename(columns={"name": "production_countri"})
paises=paises.rename(columns={"iso_3166_1": "cod_production_countri"})

#guardeo el dataframe en un csv 
paises.to_csv('./Database/production_countries.csv', index=False)