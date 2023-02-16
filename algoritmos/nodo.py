class Nodo:

    def __init__(self, mundo, coordenadas, utilidad, padre, nodo_elegido=None) -> None:
        self.mundo = mundo
        self.coordenadas = coordenadas
        self.utilidad = utilidad
        self.padre = padre
        self.nodo_elegido = nodo_elegido