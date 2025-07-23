"""ESTE ARCHIVO MANEJARA LA CARGA DE INFORMACION Y HARA FUNCIONES BASICAS
   DE Procesado 
"""
import pandas as pd
from inline_sql import sql, sql_val
def leer_csv(nombre):
    data=pd.read_csv(nombre+".csv")
    atributos=data.columns
    columnas=[]
    for atributo in atributos:
        columnas.append(atributo.lower())
    data.columns=columnas
    return data

