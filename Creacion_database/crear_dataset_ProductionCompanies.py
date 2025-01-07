import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import Funciones_normalizacion as fn

#creamos el dataframe
movies = pd.read_csv('./Database/movies_dataset.csv',delimiter = ',',encoding = "utf-8")

claves_de_interes=["name"]
companies=fn.csv_columna_desanidada(movies,"list","production_companies",claves_de_interes)

companies=companies.rename(columns={"Id_nuevo": "Id_production_compani"})
companies=companies.rename(columns={"name": "production_compani"})

#guardeo el dataframe en un csv 
companies.to_csv('./Database/production_companies.csv', index=False)