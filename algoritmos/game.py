from algoritmos.horse import Horse
from algoritmos.padre_hijo import PadreHijo
from algoritmos.profundidad import Profundidad
import numpy as np
import random


all_profundidad = []
lista_movimientos_aux = []
profundidad = 0


# función que calcula la distancia de manhattan de un nodo con respecto a un ítem.
def manhattan(x1, y1, x2, y2): # nodo, pos_item
    # resultado = abs(nodo.x - pos_item['posx']) + abs(nodo.y - pos_item['posy'])
    resultado = abs(x2 - x1) + abs(y2 - y1)
    return resultado

def start(horse1, lista_movimientos, profundidad_aux): 
    global all_profundidad, lista_movimientos_aux, profundidad
    lista_movimientos_aux = lista_movimientos
    profundidad = profundidad_aux

    all_profundidad = []
    for i in range(profundidad): # itera la cantidad de profundidades que hay
        count = 0
        aux_profundidad = np.array([])
        if i: # se verifica quien viene con el turno para pasarselo al otro participante
            if horse1.tipo_jugador == 9:
                horse1.tipo_jugador = 8
                horse1.coordenadas = horse1.coordenadas_humano
            else:
                horse1.tipo_jugador = 9
                horse1.coordenadas = horse1.coordenadas_maquina

            j = 0
            for _ in range(all_profundidad[i-1].total_nodos()): # itera la cantidadad de nodos que se generaron en la anterior profundidad, 
                                                                # ya que esos hijos se convierte en los padres de la profundidad siguiente
                try:
                    horse1.padre = all_profundidad[i-1].padres_hijos[count].hijos[j] #horse1.nuevos_movimientos[j]
                except IndexError:
                    j = 0
                    count += 1
                    horse1.padre = all_profundidad[i-1].padres_hijos[count].hijos[j] #horse1.nuevos_movimientos[j]

                j += 1
                hijos = horse1.movimientos(profundidad-i)

                aux_profundidad = np.append(aux_profundidad, PadreHijo(horse1.padre, hijos))        
        else: 
            hijos = horse1.movimientos(profundidad-i)
            horse1.nuevos_movimientos = hijos
            aux_profundidad = np.append(aux_profundidad, PadreHijo(hijos=hijos))
        all_profundidad.append(Profundidad(aux_profundidad))

    return obtener_movimiento()


def _max(lista) -> bool:
    """recorre una lista de padre-hijos, determinando 
    cual es el hijo max de cada conjunto de padre-hijos
    guarda la decisión en el atributo nodo_elegido del padre correspondiente"""
    for padre_hijos in lista:
        sub_hijos = padre_hijos.hijos
        o_max = (sub_hijos[0].nodo_elegido, abs(sub_hijos[0].nodo_elegido.utilidad))
        for i in range(1, len(sub_hijos)):
            utilidad = abs(sub_hijos[i].nodo_elegido.utilidad) 
            if utilidad > o_max[1]:
                o_max = (sub_hijos[i].nodo_elegido, utilidad)        
        try: # En la profundidad 1, los nodos no tienen padres, por consecuencia no tienen nodos elegidos, 
             # por lo anterior se captura la excepción de tipo AttributeError y se crea un nuevo padre para el nodo en consecuencia
            padre_hijos.padre.nodo_elegido = o_max[0]  
        except AttributeError:
            if o_max[1] == 0:                                                        
                padre_hijos.padre = random.choice(sub_hijos).nodo_elegido
            else:
                padre_hijos.padre = o_max[0]   
    return True
        

def _min(lista) -> bool:
    """recorre una lista de padre-hijos, determinando 
        cual es el hijo menor de cada conjunto de padre-hijos
        guarda la decisión en el atributo nodo_elegido del padre correspondiente"""
    for padre_hijos in lista:
        sub_hijos = padre_hijos.hijos
        o_min = (sub_hijos[0].nodo_elegido, sub_hijos[0].nodo_elegido.utilidad)
        for i in range(1, len(padre_hijos.hijos)):
            if sub_hijos[i].nodo_elegido.utilidad < o_min[1]:
                o_min = (sub_hijos[i].nodo_elegido, sub_hijos[i].nodo_elegido.utilidad)
        padre_hijos.padre.nodo_elegido = o_min[0]        
    return True


def _min_aux(lista) -> bool:
    """Es una extensión de _min(), en esta función no se
        tiene en cuenta el atributo nodo_elegido"""
    for padre_hijos in lista:
        sub_hijos = padre_hijos.hijos
        o_min = (sub_hijos[0], sub_hijos[0].utilidad)
        for i in range(1, len(sub_hijos)):
            if sub_hijos[i].utilidad < o_min[1]:
                o_min = (sub_hijos[i], sub_hijos[i].utilidad)
        padre_hijos.padre.nodo_elegido = o_min[0]
    return True


def obtener_movimiento() -> tuple:
    """Está función se encarga de hacer el recorrido por el arbol,
        aplicando el algoritmo minimax, finalmente retorna la coordenada
        hacia donde debe moverse la maquina"""

    answer = ()
    _min_aux(all_profundidad[profundidad-1].padres_hijos)
    for i in range(profundidad-2, -1, -1):
        if i%2==0:
            _max(all_profundidad[i].padres_hijos)
        else:
            _min(all_profundidad[i].padres_hijos)
        #lista_aux = []
    answer = all_profundidad[0].padres_hijos[0].padre
    for _ in range(profundidad-1): # hace un recorrido hasta el ultimo padre, ya que es el que guarda la coordenada hacia donde debe moverse
        answer = answer.padre
    return answer.coordenadas


def all_zeros(lista):
    for x in lista:
        if x.nodo_elegido.utilidad != 0:
            return False
    return True    