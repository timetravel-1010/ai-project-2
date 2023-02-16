import numpy as np
from algoritmos.nodo import Nodo

# caballo1 -> 1 -> machine
# caballo2 -> 2 -> humanoide
DIRECCIONES = ["A", "B", "C", "D", "E", "F", "G", "H"]

class Horse:

    def __init__(self, mundo, coordenadas_maquina, coordenadas_humano, tipo_jugador, total_puntos) -> None:
        self.mundo = np.array(mundo)
        self.mundo_aux = self.mundo.copy()
        self.tipo_jugador = tipo_jugador
        self.total_puntos = total_puntos
        self.coordenadas_maquina = coordenadas_maquina
        self.coordenadas_humano = coordenadas_humano
        self.coordenadas = coordenadas_maquina # coordenadas del caballo en turno
        self.nuevos_movimientos = [] # esta lista cambia en el tiempo
        self.direcciones = {}
        self.padre = None
        self.start = False
        self.x = 0
        self.y = 0



    def movimientos(self, profundidad) -> list:
        if self.start:
            
            self.mundo_aux = self.padre.mundo.copy()
            if not self.padre.padre is None:
                self.coordenadas = (self.padre.padre.coordenadas[0], self.padre.padre.coordenadas[1])
        else: self.start = True

        self.nuevas_direcciones()
        lista_movimientos = []

        for i in range(8):
            if self.verifica_movimiento(self.direcciones[DIRECCIONES[i]] ):
                self.x = self.direcciones[DIRECCIONES[i]][0]
                self.y = self.direcciones[DIRECCIONES[i]][1]
                try: # Excepción para capturar el error en el nodo 1, debido a que en ese momento no tiene definido padre
                    utilidad = (self.mundo_aux[self.x][self.y] - self.padre.utilidad)*profundidad # si es Max(maquina) -> item - puntos acumulados
                except AttributeError:
                    utilidad = self.mundo_aux[self.x][self.y]

                nuevo_mundo_aux = self.mundo_aux.copy() 
                nuevo_mundo_aux[self.coordenadas[0]][self.coordenadas[1]] = 0
                nuevo_mundo_aux[self.x][self.y] = self.tipo_jugador

                new_nodo = Nodo(nuevo_mundo_aux, self.direcciones[DIRECCIONES[i]], utilidad, self.padre)
                
                lista_movimientos.append(new_nodo)
        return np.array(lista_movimientos)
        

    def verifica_movimiento(self, nueva_coordenada) -> bool:
        if (nueva_coordenada[0] >= 0 and nueva_coordenada[0] < len(self.mundo[0])
            and nueva_coordenada[1] >= 0 and nueva_coordenada[1] < len(self.mundo) 
            and (self.mundo_aux[nueva_coordenada[0]][nueva_coordenada[1]] != 8 and self.mundo_aux[nueva_coordenada[0]][nueva_coordenada[1]] != 9)):
            return True
        else: return False


    def nuevas_direcciones(self) -> None:
        self.direcciones = {
            "A": (self.coordenadas[0]-1, self.coordenadas[1]+2),
            "B": (self.coordenadas[0]-2, self.coordenadas[1]+1),
            "C": (self.coordenadas[0]-2, self.coordenadas[1]-1),
            "D": (self.coordenadas[0]-1, self.coordenadas[1]-2),
            "E": (self.coordenadas[0]+1, self.coordenadas[1]-2),
            "F": (self.coordenadas[0]+2, self.coordenadas[1]-1),
            "G": (self.coordenadas[0]+2, self.coordenadas[1]+1),
            "H": (self.coordenadas[0]+1, self.coordenadas[1]+2),
        }