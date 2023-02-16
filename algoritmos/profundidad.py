class Profundidad:

    def __init__(self, padres_hijos) -> None:
        self.padres_hijos = padres_hijos

    def total_nodos(self):
        count = 0
        for nodo in self.padres_hijos:
            for _ in nodo.hijos:
                count += 1
        return count