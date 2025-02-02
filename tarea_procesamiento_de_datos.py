#%  Actividad 01

empleado_01 = [[20222333, 45, 2, 20000],[33456234,40,0,25000],[45432345,41,1,10000]]

def superanSalarioAcividad01(M, umbral):
    res = []
    
    for i in range(len(M)):
        
        if M[i][3] > umbral:
            res.append(M[i])

    return res
  
print(superanSalarioAcividad01(empleado_01, 15000))
    
    
# Costó bastante arrancar

#%%  Actividad 02

empleado_02 = [
    [20222333, 45, 2, 20000],
    [33456234, 40, 0, 25000],
    [45432345, 41, 1, 10000],
    [43967304, 37, 0, 12000],
    [42236276, 36, 0, 18000]
]


print(superanSalarioAcividad01(empleado_02, 15000))

#%%  Actividad 03

empleado_03 = [
    [20222333, 20000, 45, 2],
    [33456234, 25000, 40, 0],
    [45432345, 10000, 41, 1],
    [43967304, 12000, 37, 0],
    [42236276, 18000, 36, 0]
]


print(superanSalarioAcividad01(empleado_03, 15000)) # La función superanSalarioActividad01 funciona mal
print("Funciona mal, hay que cambiar la implementación")


# Tengo que hacer algo que vea, ahora el elemento 1 de las filas, pero además las ordene según el criterio anterior

def superanSalarioAcividad03(M, umbral):
    res = []

    for i in range(len(M)):
        if M[i][1] > umbral:
            res.append([M[i][0],M[i][2],M[i][3],M[i][1]])
    return res


print(superanSalarioAcividad03(empleado_03, 15000))    # Listo

#%%   Actividad 04

empleado_04 = [                                          # Lista de columnas
    [20222333, 33456234, 45432345, 43967304, 42236276],     # Primera columna
    [20000, 25000, 10000, 12000, 18000],                    # Segunda columna
    [45, 40, 41, 37, 36],                                   # Tercera columna
    [2, 0, 1, 0, 0]                                         # Cuarta columna
]


def superanSalarioAcividad04(M, umbral):
    res = []
    for i in range(len(M[0])):
        if M[1][i] > umbral:
            res.append([M[0][i],M[2][i],M[3][i],M[1][i]])
    return res
        

print(superanSalarioAcividad04(empleado_04, 15000))  # Listo

#%%   Actividad 05

# 1A | Al agregar más filas, la función original no tuvo problemas
# 1B | Al alterar el orden de columnas, debí cambiar la implementación

# 2 | Nuevamente tuve que cambiar la implementación de la función

# 3 | Entiendo que la ventaja es poder manipular las funciones para adecuarlas a nuestro objetivo

#%%
