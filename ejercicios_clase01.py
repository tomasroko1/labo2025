# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 14:18:50 2025

@author: tomas
"""
#%%

import pandas as pd

#with open('/home/Estudiante/Escritorio/cronograma_sugerido.csv', 'rt') as file:
    
file = 'C:/Users/tomas/.git/labo2025/arbolado-en-espacios-verdes.csv'
df = pd.read_csv(file)

#%%    Guía de ejercicios de la Primera clase.

"""

1. Definir una función leer_parque(nombre_archivo, parque) que abra el
archivo indicado y devuelva una lista de diccionarios con la información del
parque especicado. La lista debe tener un diccionario por cada árbol del parque
elegido. Dicho diccionario debe tener los datos correspondientes a un árbol
(recordar que cada la del csv corresponde a un árbol).

Probar la función en el parque ‘GENERAL PAZ’ y debería dar una lista con 690
árboles.

"""

"""

def leer_parque(nombre_archivo, parque):

    res = []

    # Iterar sobre las filas usando itertuples
    for _, fila in df.iterrows():
        dic = {}
        
        if fila['espacio_ve'] == parque:  # Filtrar por parque
        
            dic['nombre_com'] = [df['nombre_cie'], df['nombre_fam'], df['origen']]
            
            res.append(dic)  # Agregar el diccionario a la lista

    return res

# Probar la función
resultado = leer_parque(df, 'GENERAL PAZ')

# Veamoslo como dataframe

arboles_gralpaz = pd.DataFrame(leer_parque(df, 'GENERAL PAZ'))

# Verificar el número de árboles encontrados
#print(f"Número de árboles encontrados en 'GENERAL PAZ': {len(resultado)}")
"""


#%%
def leer_parque(nombre_archivo, parque):
    """
    Lee un archivo CSV y devuelve una lista de diccionarios con información
    de los árboles en el parque especificado.
    """
    res = []

    # Iterar sobre las filas usando iterrows
    for _, fila in df.iterrows():
        if fila['espacio_ve'] == parque:  # Filtrar por parque
            # Crear un diccionario con los datos del árbol
            dic = {
                "nombre_com": fila['nombre_com'],
                "nombre_ce": fila['nombre_cie'],
                "nombre_fam": fila['nombre_fam'],
                "origen": fila['origen']
            }
            res.append(dic)  # Agregar el diccionario a la lista

    return res


# Llama a la función
resultado = leer_parque(df, 'GENERAL PAZ')

# Convertir a DataFrame para inspeccionar los resultados
arboles_gral_paz = pd.DataFrame(resultado)
print(arboles_gral_paz.head())

