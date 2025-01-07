import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import Funciones_normalizacion as fn

#creamos el dataframe
movies = pd.read_csv('./Database/movies_dataset.csv',delimiter = ',',encoding = "utf-8")

claves_de_interes=["name"]
franchise=fn.csv_columna_desanidada(movies,"dicc","belongs_to_collection",claves_de_interes)

franchise=franchise.rename(columns={"Id_nuevo": "Id_franchise"})
franchise=franchise.rename(columns={"name": "franchise"})

franchise.to_csv('./Database/franchise.csv', index=False)

