import random

""" 
Esta clase es responsable de restaurar toda de la información del
estado actual del juego. También será responsable de determinar los
movimientos válidos en el estado actual. También guardará un registro
de movimientos.
"""
class EstadoJuego():
    def __init__(self):
        self.total_items = 21
        # el tablero es una lista 8x8 donde cada elemento tiene 2 caracteres
        # -- -> espacio en blanco, wN -> caballo blanco, bN -> caballo negro
        # ce -> césped, fl -> flor, ma -> manzana.
        self.tablero = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
        ]
        self.funciones_desplazamiento = {"N": self.get_movimientos_caballo}
        self.mueve_blanco = True
        self.registro_movimientos = []
        self.marcador = [0, 0]
        self.puntajes = { "ce":1, "fl":3, "ma":5, "--":0 }
        self.generar_random()
        self.nuevo_tablero = self.mapear_matriz()

    
    def generar_random(self):
        posibilidades = [ "wN", "bN",
                          "ce", "ce", "ce", "ce",  "ce", "ce", "ce", "ce", "ce", "ce", "ce", "ce", "ce", "ce",
                          "fl", "fl", "fl", "fl", "fl",
                          "ma", "ma" ]

        while posibilidades:
            fila = random.randint(0, 7)
            columna = random.randint(0,7)
            anterior = self.tablero[fila][columna]
            if anterior == "--":
                random.shuffle(posibilidades)
                self.tablero[fila][columna] = posibilidades.pop()
        
    
    def mapear_matriz(self):
        valores = self.puntajes 
        valores["wN"] = 9 
        valores["bN"] = 8
        valores["--"] = 0
        nuevo_tablero = []
        pos_wN = ()
        pos_bN = ()
        lista_movimientos = []
        
        for fila in range(len(self.tablero)):
            nuevo_tablero.append([])
            for col in range(len(self.tablero[fila])):
                valor = self.tablero[fila][col]
                nuevo_tablero[fila].append(valores[valor])  
                if valor == "wN":
                    pos_wN = (fila, col)
                elif valor == "bN":
                    pos_bN = (fila, col)
                elif valor != "--":
                    lista_movimientos.append((fila, col))
                    
        return [nuevo_tablero, pos_wN, pos_bN, lista_movimientos]



    def realizar_movimiento(self, mover):
        actual = self.tablero[mover.fila_inicial][mover.columna_inicial]
        if (actual == "wN" or actual == "bN"):
            self.tablero[mover.fila_inicial][mover.columna_inicial] = "--"
            self.tablero[mover.fila_final][mover.columna_final] = mover.pieza_movida
            self.registro_movimientos.append(mover)
            i = 0 if self.mueve_blanco else 1 #0 -> juega el blanco, 1 juega el negro
            self.marcador[i] += self.puntajes[mover.pieza_capturada]
            if mover.pieza_capturada != "--":
                self.total_items -= 1
            self.mueve_blanco = not self.mueve_blanco #intercambiar jugadores
            return True
        else:
            return False

    def validar_movimiento(self, actual):
        return None
    
    def get_mov_validos(self):
        return self.get_mov_posibles() #no se ha implementado el jaque mate.

    def get_mov_posibles(self):
        movimientos = []
        for fila in range(len(self.tablero)):
            for columna in range(len(self.tablero[fila])):
                turno = self.tablero[fila][columna][0]
                if (turno == "w" and self.mueve_blanco) or (turno == "b" and not self.mueve_blanco):
                    pieza = self.tablero[fila][columna][1]
                    self.funciones_desplazamiento[pieza](fila, columna, movimientos)
                    """ if pieza == 'N': #un caballo
                        self.get_movimientos_caballo() """
        return movimientos

    def get_movimientos_caballo(self, fila, columna, movimientos):
        movimientos_caballo =  ( (-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1) )
        color_aliado = "w" if self.mueve_blanco else "b"
        
        for mov in movimientos_caballo:
            fila_f = fila + mov[0]
            col_f = columna + mov[1]
            if (0 <= fila_f < 8 and 0 <= col_f < 8):
                pieza_f = self.tablero[fila_f][col_f]
                if (pieza_f[0] != color_aliado) and (pieza_f[1] != "N"): #no hay una pieza aliada -> vacío o enemigo.
                    movimientos.append(Mover((fila, columna), (fila_f, col_f), self.tablero))

    def termina_juego(self):
        if self.total_items == 0: #se termina el juego
            if self.marcador[0] > self.marcador[1]: #gana la máquina
                return "P1"
            else:
                return "P2"
        else:
            return False

class Mover():
    # mapear claves a valores
    rango_a_fila =  { "1":7, "2":6, "3":5, "4":4,
                      "5":3, "6":2, "7":1, "8":0 }
        
    fila_a_rango = {val: key for key, val in rango_a_fila.items()}
    file_a_columna = { "a":0, "b":1, "c":2, "d":3,
                       "e":4, "f":5, "g":6, "h":7 }
    columna_a_file = {val: key for key, val in file_a_columna.items()}

    def __init__(self, cuadrado_i, cuadrado_f, tablero):
        self.fila_inicial = cuadrado_i[0]
        self.columna_inicial = cuadrado_i[1]
        self.fila_final = cuadrado_f[0]
        self.columna_final = cuadrado_f[1]
        self.pieza_movida = tablero[self.fila_inicial][self.columna_inicial]
        self.pieza_capturada = tablero[self.fila_final][self.columna_final]
        self.ID_movimiento = (self.fila_inicial * 1000) + (self.columna_inicial * 100) + (self.fila_final * 10) + self.columna_final

    """ 
    Se sobreescribe el metodo para comparar
    """
    def __eq__(self, other):
        if isinstance(other, Mover):
            return self.ID_movimiento == other.ID_movimiento
        return False

    def getNotacionAjedrez(self):
        return self.getRangoFile(self.fila_inicial, self.columna_inicial) + self.getRangoFile(self.fila_final, self.columna_final)

    def getRangoFile(self, fila, col):
        return self.columna_a_file[col] + self.fila_a_rango[fila]