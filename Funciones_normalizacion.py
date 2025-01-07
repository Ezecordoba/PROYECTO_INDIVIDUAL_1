import pandas as pd
import ast

def columna_anidada(df,tipo,col,key):
    '''Esta funcion agarra un dataframe df con una columna 'col' anidada cuyos elementos son listas con diccionarios (tipo="list") o diccionarios (tipo="dicc"), en los cuales hay una clave key,
       y devuelve otro dataframe con una nueva columna con listas de los string que estabana asociados a la clave key. La columna vieja es eliminada.'''
    if tipo=="list":    
        col_vieja=col+"_viejo"   
        df=df.rename(columns={col:col_vieja})   #cambio el nombre de la columna
        columna_df=pd.DataFrame(df[col_vieja])  #creo un dataframe solo con la columna col_vieja
        df[col_vieja]=df[col_vieja].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)  #hago una transformacion str-->list para cada elemento
        columna_df=pd.concat([columna_df.drop(columns=col_vieja), pd.json_normalize(df[col_vieja])], axis=1) # desanida las listas y elimina la col_vieja
        columna_df.columns=[f"col{i}" for i in range(columna_df.shape[1])]  #cambia los nombres de las nuevas columnas
        columna_df=columna_df.map(lambda x: x if isinstance(x, dict) else {})  #convierte los elementos Nan en diccionarios vacíos
        lista_col=[]                                                                #
        for i in range(columna_df.shape[1]):                                        #
            columna_df_normalizado=pd.json_normalize(columna_df[f"col{i}"])         # desanida las columnas con diccionarios y se queda solo col los elementos 
            lista_col.append(columna_df_normalizado[key].rename(f"{col}_{i}"))      # relacionados con la clave 'name'
        columna_df1=pd.concat(lista_col, axis=1)                                    #

        columna_df[col]=columna_df1.apply(lambda row: row.tolist(), axis=1)         # crea una columna con listas de los elementos relacionados con la clave 'name'

        columna_df.drop(columns=[f"col{i}" for i in range(columna_df.shape[1]-1)], inplace=True)  # elimina las columnas viejas

        for i in columna_df.columns:                                                                                       # elimina los elementos Nan 
            columna_df[i] = columna_df[i].apply(lambda x: [j for j in x if not pd.isna(j)] if isinstance(x, list) else x)  # de las listas
        df_normalizado=pd.concat([df,columna_df],axis=1)    # crea un nuevo dataframe igual al inicial pero                                                                 
        df_normalizado.drop(columns=col_vieja,inplace=True) # con la nueva columna y elimina la columna col_vieja
        return df_normalizado
    
    elif tipo=="dicc":
        col_vieja=col+"_viejo"   
        df=df.rename(columns={col:col_vieja})   #cambio el nombre de la columna
        columna_df=pd.DataFrame(df[col_vieja])  #creo un dataframe solo con la columna col_vieja
        df[col_vieja]=df[col_vieja].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)  #hago una transformacion str-->dicc para cada elemento
        columna_df=columna_df.map(lambda x: x if isinstance(x, dict) else {})  #convierte los elementos Nan en diccionarios vacíos
        columna_df=pd.concat([columna_df.drop(columns=col_vieja), pd.json_normalize(df[col_vieja])], axis=1) # desanida las listas y elimina la col_vieja
        columna_df[key].fillna("Sin Dato",inplace=True)

        for i in columna_df.columns:                      #
            if i!=key:                                    # elimina las columnas que no estan relacionadas con la clave key
                columna_df.drop(columns=i, inplace=True)  # 

        columna_df=columna_df.rename(columns={key:col})
        df_normalizado=pd.concat([df,columna_df],axis=1)    # crea un nuevo dataframe igual al inicial pero                                                                 
        df_normalizado.drop(columns=col_vieja,inplace=True) # con la nueva columna y elimina la columna col_vieja
        return df_normalizado

    else:
        print("La variable tipo no tiene un valor correcto")  

#----------------------------------------------------------------------------------------------
def csv_columna_desanidada(df,tipo,columna_anidada,claves_que_se_quedan):
    '''Esta funcion agarra la columna anidada cuyos elementos son listas de diccioanrios de un dataframe y crea, 
    a partir de ella, otro dataframe cuyas columnas con las claves de los diccionarios con los que me quiero quedar mas una columna "Id_nuevo". Las variables son:
    - df: dataframe con la columna a desanidar
    - tipo: marca si los datos de la columna anidada son listas de diccionarios ("lis") o diccionarios ("dicc")
    - columna_anidada: columna a desanidar
    - claves_que_se_quedan: lista con los nombres de las claves de los diccionarios con los que me voy a quedar para el nuevo dataframe. Deben estar en el orden original de las claves del diccionario'''
    if tipo=="list":
        df[columna_anidada] = df[columna_anidada].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x) #transformacion str-->list
        df_anidado=pd.DataFrame(df[columna_anidada])  #creo un dataframe solo con la columna anidada
        df_anidado.dropna(inplace=True)  #elimino valores Nan
        df_anidado.reset_index(drop=True,inplace=True)
        df_desanidado=pd.concat([df_anidado.drop(columns=columna_anidada), pd.json_normalize(df_anidado[columna_anidada])], axis=1) # desanida las listas y elimina la columna anidada
        df_desanidado.columns=[f"col{i}" for i in range(df_desanidado.shape[1])]  #cambia los nombres de las nuevas columnas
        df_desanidado=df_desanidado.map(lambda x: x if isinstance(x, dict) else {})  #convierte los elementos Nan en diccionarios vacíos
        indice=0                                               #
        for i in range(df_desanidado.shape[0]):                #
            if df_desanidado.loc[i,"col0"]!={}:                # creo una lista con las claves del diccionario 
                indice+=i                                      #
                break                                          #
        claves=list(df_desanidado.loc[indice,"col0"].keys())   #
        for i in range(df_desanidado.shape[1]):
            df_desanidado=pd.concat([df_desanidado.drop(columns=[f"col{i}"]), pd.json_normalize(df_desanidado[f"col{i}"])], axis=1) #desanidamos las columnas con diccionarios 
            for j in range(len(claves)):
                df_desanidado=df_desanidado.rename(columns={claves[j]: f"{claves[j]}_{i}"}) #pongo a las columnas los nombres de las claves del diccionario 
        lista=[]                                                                              #
        for i in range(len(claves)):                                                          # Creo una lisa de listas. En las listas secundarias estan 
            calve_lista=[j for j in df_desanidado.columns if j.startswith(f"{claves[i]}")]    # los nombres de las columnas asocioadas a cada clave del diccionario
            lista.append(calve_lista)                                                         #
        dicc={}                                                                                     # creo un diccionario en el que cada clave tendrá como
        for i in range(len(claves)):                                                                # valor una concatenacion de cada columna asociada a la 
            dicc[f"{claves[i]}"]=pd.concat([df_desanidado[j] for j in lista[i]], ignore_index=True) # clave correespondiente del diccionario original 
        df_final=pd.DataFrame(dicc)  #tranformo el diccionario dicc en un dataframe 
        for i in df_final.columns:                    #
            if i not in claves_que_se_quedan:         # elimino las columnas relacionadas a las claves del diccionario original que no me interesan 
                df_final.drop(columns=i,inplace=True) #
        df_final.drop_duplicates(inplace=True,ignore_index=True)  #elimino los duplicados 
        df_final.fillna("Sin Dato",inplace=True)
        df_final.dropna(inplace=True)
        df_final["Id_nuevo"]=range(1,df_final.shape[0]+1)  #creo la columna "Id_nuevo"
        return df_final
    elif tipo=="dicc":
        df[columna_anidada] = df[columna_anidada].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x) #transformacion str-->dicc
        df_desanidado=pd.DataFrame(df[columna_anidada])  #creo un dataframe solo con la columna anidada
        df_desanidado=df_desanidado.map(lambda x: x if isinstance(x, dict) else {})  #convierte los elementos Nan en diccionarios vacíos
        indice=0                                               #
        for i in range(df_desanidado.shape[0]):                #
            if df_desanidado.loc[i,columna_anidada]!={}:                # creo una lista con las claves del diccionario 
                indice+=i                                      #
                break                                          #
        claves=list(df_desanidado.loc[indice,columna_anidada].keys())     #
        df_final=pd.concat([df_desanidado.drop(columns=columna_anidada), pd.json_normalize(df_desanidado[columna_anidada])], axis=1) #desanidamos la columna con diccionarios
        for i in df_final.columns:                    #
            if i not in claves_que_se_quedan:         # elimino las columnas relacionadas a las claves del diccionario original que no me interesan 
                df_final.drop(columns=i,inplace=True) #
        df_final.drop_duplicates(inplace=True,ignore_index=True)  #elimino los duplicados 
        df_final.fillna("Sin Dato",inplace=True)
        df_final["Id_nuevo"]=range(1,df_final.shape[0]+1)  #creo la columna "Id_nuevo"
        return df_final
    else:
        print("La variable tipo no tiene un valor correcto") 