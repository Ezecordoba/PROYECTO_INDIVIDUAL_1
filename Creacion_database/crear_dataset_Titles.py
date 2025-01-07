import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast

#creamos el dataframe
movies=pd.read_csv('./Database/movies_dataset.csv',delimiter = ',',encoding = "utf-8")

df=pd.DataFrame({"Id_movie_viejo":movies["id"],"title":movies["title"]})
df.drop_duplicates(subset="Id_movie_viejo", keep='first',inplace=True)
df.reset_index(drop=True,inplace=True)
df["Id_movie"] = range(1,df.shape[0]+1)
index=[]
for i in range(df.shape[0]):
    if "-" in df.loc[i,"Id_movie_viejo"]:
        index.append(i)
lista=[]
for i in range(1,8):
    if str(i) in df["Id_movie_viejo"].values:
        pass
    else:
        lista.append(str(i))
df.loc[index[0],"Id_movie_viejo"]=lista[0]
df.loc[index[1],"Id_movie_viejo"]=lista[1]
df.loc[index[2],"Id_movie_viejo"]=lista[2]
df["Id_movie"]=df["Id_movie"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
df["Id_movie_viejo"]=df["Id_movie_viejo"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

df.to_csv('./Database/titles.csv', index=False)