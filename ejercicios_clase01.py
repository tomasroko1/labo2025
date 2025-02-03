# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 14:18:50 2025

@author: tomas
"""
#%%

import pandas as pd

#with open('/home/Estudiante/Escritorio/cronograma_sugerido.csv', 'rt') as file:
    
file = 'arbolado-en-espacios-verdes.csv'
df = pd.read_csv(file)

#%%    Guía de ejercicios de la Primera clase.

"""

1. Definir una función leer_parque(nombre_archivo, parque) que abra el
archivo indicado y devuelva una lista de diccionarios con la información del
parque especificado. La lista debe tener un diccionario por cada árbol del parque
elegido. Dicho diccionario debe tener los datos correspondientes a un árbol
(recordar que cada fila del csv corresponde a un árbol).

Probar la función en el parque ‘GENERAL PAZ’ y debería dar una lista con 690
árboles.

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
                "origen": fila['origen'],
                "altura_tot": fila['altura_tot']
            }
            res.append(dic)  # Agregar el diccionario a la lista
    
    print('En', parque, 'hay', len(res), 'árboles')
    return res


# Llama a la función
resultado = leer_parque(df, 'GENERAL PAZ')


# Convertir a DataFrame para ver los resultados
arboles_gral_paz = pd.DataFrame(resultado)

#%%
"""

2. Escribir una función especies(lista_arboles) que tome una lista de árboles 
como la generada en el ejercicio anterior y devuelva el conjunto de especies (la 
columna 'nombre_com' del archivo) que figuran en la lista. 

"""

def especies(lista_arboles):
    return lista_arboles['nombre_com'].value_counts()
    
print(especies(arboles_gral_paz))

print('Cantidad de especies', len(especies(arboles_gral_paz)))

ejemplares = pd.DataFrame(especies(arboles_gral_paz))

#%%

"""
3. Escribir una función contar_ejemplares(lista_arboles) que, dada una 
lista como la generada con leer_parque(...), devuelva un diccionario en el 
que las especies sean las claves y tengan como valores asociados la cantidad de 
ejemplares en esa especie en la lista dada. 
Debería verse que en el parque General Paz hay 20 Jacarandás, en el Parque Los 
Andes hay 3 Tilos y en Parque Centenario hay 1 Laurel. 

"""

def contar_ejemplares(lista_arboles):
    res = {}
    
    for _, row in lista_arboles.iterrows():
        #SI EL ARBOL YA ESTÁ, SUMO UNO AL CONTADOR, ETC
        if not row['nombre_com'] in res:
            res[row['nombre_com']] = 1
        else:
            res[row['nombre_com']] += 1
        
    return res

contarej = contar_ejemplares(pd.DataFrame(leer_parque(df, 'GENERAL PAZ')))


Parques = df['espacio_ve'].value_counts()

#%%

"""

4. Escribir una función obtener_alturas(lista_arboles, especie) que, 
dada una lista como la generada con leer_parque(...) y una especie de 
árbol (un valor de la columna 'nombre_com' del archivo), devuelva una lista con 
las alturas (columna 'altura_tot') de los ejemplares de esa especie en la lista. 
Observación: Conviene devolver las alturas como números (de punto flotante) y 
no como cadenas de caracteres. Sugerimos hacer esto modificando 
leer_parque(...) o modificando el tipo del valor antes de utilizarlo. 

Usar la función para calcular la altura promedio y altura máxima de los 
'Jacarandá' en los tres parques mencionados. Debería obtenerse esto: 

"""

def obtener_alturas(lista_arboles, especie):
    res = []
    
    for dic in lista_arboles:
        if especie in dic.values():
            res.append(float(dic['altura_tot']))
            
    return res


print(obtener_alturas(leer_parque(df, 'GENERAL PAZ'), 'Jacarandá'))

print('El promedio de altura de los jacarandá del parque General Paz es', (sum(obtener_alturas(leer_parque(df, 'GENERAL PAZ'), 'Jacarandá')) / len(obtener_alturas(leer_parque(df, 'GENERAL PAZ'), 'Jacarandá'))))






