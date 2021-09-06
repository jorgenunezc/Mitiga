
import os
import numpy as np
import pickle
import pandas as pd
from netCDF4 import Dataset

#Función que prepara input del modelo.
# Resample según serie que presente la altura maxima "mismo T".
def input_model_alerta(file_L0):
    f_L0=Dataset(file_L0,'r')
    n_boyas=6
    dataX = {}
    for i in range(n_boyas):
        etaL0 = f_L0.variables['eta'][:,i] -f_L0.variables['eta'][:,i][0]# eta corregido
        etaL0 = etaL0.data.tolist()
        dataX['boya'+str(i) ]= etaL0
        
    df_x = pd.DataFrame(dataX)
    index = pd.date_range('25/8/2020', periods=len(df_x), freq='10S')
    Datetime = pd.DataFrame({'Datetime':index})
    df_x = pd.concat([Datetime, df_x], axis=1,)
    df_x = df_x.loc[0:180*2]# solo la primera hora de registro
    df_x0 = df_x.resample('10S', on='Datetime').mean()
    #print(df_x0.columns)
    
    #grouper = df_x0['boya0'].groupby(pd.Grouper(freq='1min')) # genera groups intervalos de 1 minuto
    #max_index=grouper.idxmax() # conserva el index del maximo del intervalo


    #escenarios = df_x0.columns
    #cont=0
    #for i in escenarios:
     #   boyas_esc = df_x0.columns[cont:cont+6]
      #  df_x_i = df_x0[boyas_esc].loc[max_index[i]]# extrae el valor en el tiempo Y
       # df_x_i = df_x_i.resample('T').max()# reindex
        #if cont ==0:
         #   dfx = df_x_i
        #else:
         #   dfx = pd.concat([dfx, df_x_i], axis=1)

        #cont+=6
    dfx = df_x0.resample('T').max()
    df_x = dfx.values.astype('float32')
    
    boyasX = split_sequence_X(df_x,n_boyas)
    return boyasX



# genera secuencias de entrada
#n_boyas = 6
def split_sequence_X(df_x,n_boyas):
    X = list()
    for n in range(0,df_x.shape[1],n_boyas):
        x = list()
        for i in range(n,n+n_boyas):

        # se suma uno porque no considera el ultimo
            seq_x = df_x[:,i]
            x.append(seq_x)
        x = np.array(x).T
        X.append(np.array(x))
        
    return np.array(X)

