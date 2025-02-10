# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 14:18:50 2025

@author: tomas
"""
#%%

import pandas as pd

#with open('/home/Estudiante/Escritorio/cronograma_sugerido.csv', 'rt') as file:
    
file = '.git/labo2025/arbolado-en-espacios-verdes.csv'
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
                "altura_tot": fila['altura_tot'],
                "inclinacio": fila['inclinacio']
            }
            res.append(dic)  # Agregar el diccionario a la lista
    
    return res


# Llama a la función
resultado = leer_parque(df, 'GENERAL PAZ')
print(resultado)

#%%
"""

2. Escribir una función especies(lista_arboles) que tome una lista de árboles 
como la generada en el ejercicio anterior y devuelva el conjunto de especies (la 
columna 'nombre_com' del archivo) que figuran en la lista. 

"""

def especies(lista_arboles):
    lista = pd.DataFrame(lista_arboles)
    return lista['nombre_com'].value_counts()
    

arboles_gral_paz = leer_parque(df, 'GENERAL PAZ')

print(especies(arboles_gral_paz))


#print('Cantidad de especies', len(especies(arboles_gral_paz)))

#ejemplares = pd.DataFrame(especies(arboles_gral_paz))


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
    lista = pd.DataFrame(lista_arboles)
    
    res = {}
    
    for _,row in lista.iterrows():
        #SI EL ARBOL YA ESTÁ, SUMO UNO AL CONTADOR, ETC
        if not row['nombre_com'] in res:
            res[row['nombre_com']] = 1
        else:
            res[row['nombre_com']] += 1
        
    return res

contarej = contar_ejemplares(pd.DataFrame(leer_parque(df, 'GENERAL PAZ')))

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

def promedio(lista):
    return sum(lista) / len(lista)

print('El promedio de altura de los jacarandá del parque es', promedio(obtener_alturas(leer_parque(df, 'CENTENARIO'), 'Jacarandá')))
print('El ejemplar más alto del parque mide', max(obtener_alturas(leer_parque(df, 'CENTENARIO'), 'Jacarandá')))

#%%

"""

5. Escribir una función obtener_inclinaciones(lista_arboles, especie)
que, dada una lista como la generada con leer_parque(...) y una especie
de árbol, devuelva una lista con las inclinaciones (columna 'inclinacio') de
los ejemplares de esa especie.

"""

def obtener_inclinaciones(lista_arboles, especie):
    res = []
    
    for dic in lista_arboles:
        if especie in dic.values():
            res.append(float(dic['inclinacio']))
            
    return res  

print(obtener_inclinaciones(leer_parque(df, 'CENTENARIO'), 'Jacarandá'))


#%%

"""

6. Combinando la función especies() con obtener_inclinaciones() escribir
una función especimen_mas_inclinado(lista_arboles) que, dada una
lista de árboles devuelva la especie que tiene el ejemplar más inclinado y su
inclinación.
Correrlo para los tres parques mencionados anteriormente. Debería obtenerse,
por ejemplo, que en el Parque Centenario hay un Falso Guayabo inclinado 80
grados.

"""

def especimen_mas_inclinado(lista_arboles):
    res = ""
    count = 0
    
    for dic in lista_arboles:
        if dic['inclinacio'] >= count:
            res = dic['nombre_com']
            count = dic['inclinacio']
     
    return res, count
            
arboles_centenario = leer_parque(df, 'CENTENARIO')

especimen_mas_inclinado(arboles_centenario)


#%%

"""

7. Volver a combinar las funciones anteriores para escribir la función
especie_promedio_mas_inclinada(lista_arboles) que, dada una lista
de árboles devuelva la especie que en promedio tiene la mayor inclinación y el
promedio calculado.
Resultados. Debería obtenerse, por ejemplo, que los Álamos Plateados del
Parque Los Andes tiene un promedio de inclinación de 25 grados.

"""

def cant_especies(lista_arboles):
    res = 0 
    especies = []
    
    for dic in lista_arboles:
        if not dic['nombre_com'] in especies:
            especies.append(dic['nombre_com'])
            res += 1
    return (res, especies)


""" Chequeo que tiene que ser 70

dframe = pd.DataFrame(arboles_centenario)
print(len(dframe['nombre_com'].value_counts())) 

"""

#print(cant_especies(arboles_centenario))    
    

def especie_promedio_mas_inclinada(lista_arboles):
    especie = ''
    media = -1
    
    for esp in cant_especies(lista_arboles)[1]: #Usamos la lista de especies, no el nro
        if promedio(obtener_inclinaciones(lista_arboles, esp)) > media:
            especie = esp
            media = promedio(obtener_inclinaciones(lista_arboles, especie))
    
    return especie, media

print(especie_promedio_mas_inclinada(arboles_centenario))

print(especie_promedio_mas_inclinada(leer_parque(df, 'CHACABUCO')))

print(especie_promedio_mas_inclinada(arboles_gral_paz))

#%%

"""

Explorar el dataset nuevo de árboles en veredas.

Armar un DataFrame data_arboles_veredas que tenga solamente las siguiente

columnas: 'nombre_cientifico', 'ancho_acera', 'diametro_altura_pecho', 'altura_arbol'

Sugerimos trabajar al menos con las siguientes especies seleccionadas:
    
especies_seleccionadas = ['Tilia x moltkei', 'Jacaranda mimosifolia', 'Tipuana tipu']

"""

archivo = '.git/labo2025/arbolado-publico-lineal-2017-2018.csv'
        
#No entiendo que está pasando con esto que dá error

df2 = pd.read_csv(archivo)
      
#%%
"""
Advertencia: El GCBA usa distintos nombres para especie, altura y diámetro según el
dataset, por ejemplo 'altura_tot' en uno y 'altura_arbol' en otro. Los nombres cientícos
varían de un dataset al otro. Por ejemplo 'Tipuana Tipu' se transforma en 'Tipuana tipu'.
Proponemos los siguientes pasos para comparar los diámetros a la altura del pecho de
las tipas en ambos tipos de entornos.

    8. Para cada dataset, armar otro seleccionando solamente las filas correspondientes
    a las tipas (llamalos df_tipas_parques y df_tipas_veredas, respectivamente) y las
    columnas correspondientes al diámetro a la altura del pecho y alturas. Usar como
    copias (usando .copy()) para poder trabajar en estos nuevos dataframes sin
    modicar los dataframes grandes originales. Renombrar las columnas necesarias
    para que se llamen igual en ambos dataframes.

    9. Agregar a cada dataframe (df_tipas_parques y df_tipas_veredas) una columna
    llamada 'ambiente' que en un caso valga siempre 'parque' y en el otro caso
    'vereda'.
    
    10. Concatenar los dataframes.
    
    11. Explorar y analizar sobre la cuestión planteada:
        ¿Hay diferencias entre los ejemplares de una misma especie según si crecen en
        un un parque o en la vereda?
"""

""" Nos quedamos con las columnas que nos pide el ejercicio """
data_arboles_veredas = df2[['nombre_cientifico', 'ancho_acera', 'diametro_altura_pecho', 'altura_arbol']].copy()

data_arboles_parques = df[['nombre_cie', 'diametro', 'altura_tot']].copy()

"8)"

""" Usemos un filtro que solo se quede con las filas de las 'Tipuana tipu' !! """
df_tipas_veredas = data_arboles_veredas.loc[data_arboles_veredas['nombre_cientifico'] == 'Tipuana tipu'].copy()

df_tipas_parques = data_arboles_parques.loc[data_arboles_parques['nombre_cie'] == 'Tipuana Tipu'].copy()

df_tipas_parques = df_tipas_parques.rename(columns = {'nombre_cie': 'nombre_cientifico', 'altura_tot': 'altura_arbol'})
df_tipas_veredas = df_tipas_veredas.rename(columns = {'diametro_altura_pecho': 'diametro'})

"9)"

#df_tipas_parques['ambiente'] = 'parque'
#df_tipas_veredas['ambiente'] = 'vereda'

"10)"

#df_concatenado = pd.concat([df_tipas_parques, df_tipas_veredas], ignore_index=True)

"veamos que relación hay entre el ambiente y el alto/diametro de los arboles"

def diametro_promedio(dataframe):
    lista = []
    for _, row in dataframe.iterrows():
        if not pd.isna(row['diametro']):
            lista.append(row['diametro'])
    return promedio(lista)

print('diametro promedio en parques', diametro_promedio(df_tipas_parques),
      'diametro promedio en veredas', diametro_promedio(df_tipas_veredas))

def altura_promedio(dataframe):
    lista = []
    for _, row in dataframe.iterrows():
        if not pd.isna(row['altura_arbol']):
            lista.append(row['altura_arbol'])
    return promedio(lista)

print('altura promedio en parques', altura_promedio(df_tipas_parques),
      'altura promedio en veredas', altura_promedio(df_tipas_veredas))

""" Conclusiónes:
  
    Con los datos que tenemos podemos ver que, en promedio, en nuestro conjunto de estudio
    las tipas crecidas en parques son más altas y tienen mayor diámetro que las tipas crecidas
    en vereda.
  
"""
