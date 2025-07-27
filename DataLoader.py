"""ESTE ARCHIVO MANEJARA LA CARGA DE INFORMACION Y HARA FUNCIONES BASICAS
   DE Procesado 
"""
import pandas as pd
from inline_sql import sql, sql_val

#normaliza los nombres de las columnas a minuscula por comodidad
def leer_csv(nombre):
    
    if nombre[-4:]!=".csv":
        nombre=nombre+".csv"
    atributos=data.columns
    columnas=[]
    for atributo in atributos:
        columnas.append(atributo.lower())
    data.columns=columnas
    return data


    
    
    