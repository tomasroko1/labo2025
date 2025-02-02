# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 18:18:25 2025

@author: tomas
"""

#%%

"""      1)

         Una mañana ponés un billete en la vereda al lado del obelisco porteño. A partir
         de ahí, cada día vas y duplicás la cantidad de billetes, apilándolos prolijamente.
         ¿Cuánto tiempo pasa antes de que la pila de billetes sea más alta que el
         obelisco?
         
         Datos: espesor del billete: 0.11 mm, altura obelisco: 67.5 m
"""

billete_alto = 0.11
obelisco_alto = 67500

suma = 0.11
dias = 1
while suma <= obelisco_alto:
    dias += 1
    suma += suma
    
print(dias) # Tardás 21 días 

#%%

"""         2) 

            Usá una iteración sobre el string cadena para agregar la sílaba 'pa', 'pe',
            'pi', 'po', o 'pu' según corresponda luego de cada vocal.
            
            Ejemplo:
            cadena = 'Casa'
            cadena_geringosa = ''
            for c in cadena:
                COMPLETAR
                
            print(cadena_geringosa)
            # Geperipingoposopo
            Luego hacelo con un while en vez del for.

"""

def aux(vocal):
    return vocal + "p" + vocal

def geringoso(palabra):
    res = " "
    
    for letra in palabra:
        if letra in 'aeiou':
            res = res + aux(letra)
        else:
            res = res + letra
            
    return res

def geringoso_while(palabra):
    res = " "
    i = 0
    while i < len(palabra):
        if palabra[i] in 'aeiou':
            res = res + aux(palabra[i])
        else:
            res = res + palabra[i] 
            
        i += 1
            
    return res

#%%

"""     3)

        Definir una función pertenece(lista, elem) que tome una lista y un
        elemento, y devuelva True si la lista tiene al elemento dado y False en caso
        contrario

"""

def pertenece(lista, elem):
    return (elem in lista)

#%%

"""     4)

        Definir una función mas_larga(lista1, lista2) que tome dos listas y
        devuelva la más larga.
        
"""

def mas_larga(lista1, lista2):
    if len(lista1) > len(lista2):
        return lista1
    else:
        return lista2

#%%

"""     5)

        Una pelota de goma es arrojada desde una altura de 100 metros y cada vez que
        toca el piso salta 3/5 de la altura desde la que cayó. Escribí un programa
        rebotes.py que imprima una tabla mostrando las alturas que alcanza en cada uno
        de sus primeros diez rebotes.

"""

def tabla_alturas():
    count = 100
    res = []
    for i in range(0,10):
        res.append( count *  (3/5) )
        count = count * (3/5)
    return res

print(tabla_alturas())

import pandas as pd

df = pd.DataFrame(tabla_alturas())

#%%
    
"""     6)

        Denir la función mezclar(cadena1, cadena2) que tome dos strings y
        devuelva el resultado de intercalar elemento a elemento. Por ejemplo: si
        intercalamos Pepe con Jose daría PJeopsee. En el caso de Pepe con Josefa daría
        PJeopseefa.

""" 

def mezclar(cadena1, cadena2):
    res = ""
    
    if len(cadena1) > len(cadena2):
        maslarge = cadena1
        corto = cadena2
    else:
        maslarge = cadena2
        corto = cadena1
    
    for i in range(len(maslarge)):
            
        res += maslarge[i]
        res += corto[i]
        
        if len(res) > len(maslarge):
            res += maslarge[i+1]
            break

    return res

print(mezclar('Pepe', 'Jose'))

print(mezclar('Pepe', 'Josefa'))

#%%

"""     7)

    David solicitó un crédito a 30 años para comprar una vivienda, con una tasa fija
    nominal anual del 5%. Pidió $500000 al banco y acordó un pago mensual fijo de
    $2684,11
    
        a)
        Escribir un programa que calcula el monto total que pagará David a lo
        largo de los años. Deberías obtener que en total paga $966279.6.
        
        b)
        Supongamos que David adelanta pagos extra de $1000/mes durante los
        primeros 12 meses de la hipoteca. Modicá el programa para incorporar
        estos pagos extra y que imprima el monto total pagado junto con la
        cantidad de meses requeridos. Deberías obtener que el pago total es de
        $929965.62 en 342 meses.
        
        c) ¿Cuánto pagaría David si agrega $1000 por mes durante cuatro años,
        comenzando en el sexto año de la hipoteca (es decir, luego de 5 años)?
        Modicá tu programa de forma que la información sobre pagos extras sea
        incorporada de manera versátil. Sugerimos utilizar los parámetros:
        pago_extra_monto, pago_extra_mes_comienzo, pago_extra_mes_fin.    
        
"""

"a)"

res = 0
for n in range(0,30*12):
    res += 2684.11

print(res)

        
"b)"

res = 0
for n in range(0,342):
    res += 2684.11
    if n < 12:
        res += 1000

print(res)

"c)"

res = 0
pago_extra_monto = 0
for n in range(0,30*12):
    res += 2684.11

    if n >= 6*12 and n < 10*12:
        pago_extra_monto += 1000

print(res + pago_extra_monto)

#%%
"""     8)
        
        Construí una función traductor_geringoso(lista) que, a partir de una lista de
        palabras, devuelva un diccionario geringoso. Las claves del diccionario deben ser
        las palabras de la lista y los valores deben ser sus traducciones al geringoso.
        Por ejemplo, al tomar la lista ['banana', 'manzana', 'mandarina'] debe
        devolver {
                  'banana': 'bapanapanapa',
                  'manzana': 'mapanzapanapa',
                  'mandarina': 'mapandaparipinapa'
                  }
        
"""

def traductor_geringoso(lista):
    res = {}
    
    for palabra in lista:
        if palabra not in res.keys():
            res[palabra] = geringoso(palabra)
    
    return res

print(traductor_geringoso(['banana', 'manzana', 'mandarina']))

#%%
    
        
    
        
        
    
    




