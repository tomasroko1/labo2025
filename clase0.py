# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 14:24:19 2025

@author: tomas
"""

# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

with open('Escritorio/datame.txt','rt') as file:
    data = file.read()

data_nuevo = "Este 2025 \n \n" + data + "\nChau"

print(data_nuevo)

with open('/home/Estudiante/Escritorio/cronograma_sugerido.csv', 'rt') as file:
    lista = []
   
    encabezado = next(file)
    for line in file:
       
        datos_linea = line.split(',')
       
        lista.append(datos_linea[1])
   
print(lista)


#{Escribir una función generala_tirar() que simule una tirada de dados para el juego de la
#generala. Es decir, debe
#devolver una lista aleatoria de 5 valores de dados. Por ejemplo [2,3,2,1,6].

import random

def generala_tirar():
    res = []
    for i in range(0,5):
        nro = random.randint(1,6)
        res.append(nro)
    return res

generala_tirar()

#Escribir un programa que recorra las líneas del archivo ‘datame.txt’ e imprima solamente
#las líneas que contienen la
#palabra ‘estudiante’ .


with open('Escritorio/datame.txt','rt') as file:
    res = []
    for fila in file:
        if 'estudiante' in fila:
            res.append(fila)
    print(res)
           
           
#Utilizando el archivo cronograma_sugerido , armar una lista de las materias del cronograma,
# llamada “lista_materias ”.

with open('/home/Estudiante/Escritorio/cronograma_sugerido.csv', 'rt') as file:
    lista = []
   
    encabezado = next(file)
    for line in file:
       
        datos_linea = line.split(',')
       
        lista.append(datos_linea[1])
   
print(lista)

#Luego, definir una función “cuantas_materias (n)” que, dado un número de cuatrimestre
#(n entre 3 y 8), devuelva la cantidad de materias a cursar en ese cuatrimestre.
# Por ejemplo: cuantas_materias(5) debe devolver 3.

#def cuantas_materias(n):
 
    ###### COMPLETAR
 
import numpy as np

a = np.array([1,2,3,4,5])
b= np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
print(a[0])
print(b[0])
print(b[2][3])
print(b[2,3])
np.zeros(2)
np.zeros((2,3))

np.arange(4)

arreglo = np.linspace(1, 10 , num=5)

arreglo.ndim
arreglo.shape
print(arreglo)

np.ones(2)

b[0,0:1]

b.sum()

#Definir una función pisar_elemento(M,e) que tome una matriz de enteros M y un entero e y
#devuelva
#una matriz similar a M donde las entradas coincidentes con e fueron cambiadas por -1.
#Por ejemplo si M = np.array([[0, 1, 2, 3], [4, 5, 6, 7]]) y e = 2, entonces la función
#debe devolver la matriz np.array([[0, 1, -1, 3], [4, 5, 6, 7]])

def pisar_elemento(M,e):
    for i in range(len(M)):
        for j in range(len(M[i])):
            if M[i,j] == e:
                M[i,j] = -1
    return M

print(pisar_elemento(np.array([[0, 1, 2, 3], [4, 5, 6, 7]]), 6))

####

import pandas as pd

d = {'nombre':['Antonio', 'Brenda', 'Camilo', 'David'], 'apellido': ['Restrepo', 'Saenz','Torres', 'Urondo'], 'lu': ['78/23', '449/22', '111/24', '1/21']}

df = pd.DataFrame(data = d) # creamos un df a partir de un diccionario
df.set_index('lu', inplace = True) # seteamos una columna como index


fname = '/home/Estudiante/Descargas/pandas_script1.py'
df = pd.read_csv(fname)

df[['Cuatrimestre', 'Asignatura']]


df.iloc[2:6]
