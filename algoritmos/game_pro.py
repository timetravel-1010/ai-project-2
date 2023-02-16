from horse import Horse
import numpy as np
import queue


test_list = [ # maquina -> 9, humano -> 8
    [9, 0, 0, 3, 0],
    [1, 0, 3, 0, 1],
    [0, 1, 0, 0, 0],
    [0, 5, 0, 8, 0],
    [1, 0, 0, 0, 0],
]
profundidad = 2

horse1 = Horse(test_list, (0, 0), (3, 3), 9, 0)
horse1.nuevos_movimientos
for i in range(profundidad):
    if i:
        if horse1.tipo_jugador == 9:
            horse1.tipo_jugador = 8
            horse1.coordenadas = horse1.coordenadas_humano
        else:
            horse1.tipo_jugador = 9
            horse1.coordenadas = horse1.coordenadas_maquina

        for j in range(len(horse1.nuevos_movimientos)):
            #print(horse1.nuevos_movimientos)
            #print(j)
            #horse1.coordenadas = horse1.nuevos_movimientos[j].coordenadas
            horse1.padre = horse1.nuevos_movimientos[j]
            horse1.nuevos_movimientos[j] = horse1.movimientos()
    else: 
        #horse1.posibles_movimientos = horse1.movimientos()
        horse1.nuevos_movimientos = horse1.movimientos()
        print(f"Primero: {horse1.nuevos_movimientos[1]}")



'''for a in horse1.nuevos_movimientos:
    print(len(a))
    print(a[0].mundo)
    #print(a[1].coordenadas)

print(a[0].padre.mundo, a[0].padre.coordenadas)'''


def _max(lista):
    o_max = (lista[0], lista[0].utilidad)
    for i in range(1, len(lista)):
        if lista[i].utilidad >= o_max[1]:
            o_max = (lista[i], lista[i].utilidad)
    return o_max[0]
        

def _min(lista):
    o_min = (lista[0], lista[0].utilidad)
    for i in range(1, len(lista)):
        if lista[i].utilidad <= o_min[1]:
            o_min = (lista[i], lista[i].utilidad)
    return o_min[0]


def obtener_movimiento():
    lista_movimientos = horse1.nuevos_movimientos.copy()
    lista_aux = []
    for i in range(profundidad):
        if i%2==0:
            for obj in lista_movimientos:
                lista_aux.append(_min(obj))
        else:
            for obj in lista_movimientos:
                lista_aux.append(_max(obj))
        lista_movimientos = [lista_aux.copy()]
        lista_aux = []
    return lista_movimientos[0]

x = obtener_movimiento()
print(x[0].padre.coordenadas)
#print(horse1.nuevos_movimientos)