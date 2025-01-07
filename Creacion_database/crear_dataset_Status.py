import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast

#creamos el dataframe
movies=pd.read_csv('./Database/movies_dataset.csv',delimiter = ',',encoding = "utf-8")

df=pd.DataFrame({"status":movies["status"]})
df["status"]=df["status"].fillna("Sin Dato")
df.drop_duplicates(subset="status", keep='first',inplace=True)
df["Id_status"] = range(1,df.shape[0]+1)


df.to_csv('./Database/status.csv', index=False)