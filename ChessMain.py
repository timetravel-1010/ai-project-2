""" 
Archivo encargado de manejar las entradas del usuario y mostrar
en pantalla el objeto de estado actual del juego (GameState).
"""
import pygame as pg
import ChessEngine 
from algoritmos.game import  start
from algoritmos.horse import Horse

ANCHO = 512  #400
ALTO = ANCHO 
DIMENSION = 8 #dimensiones de un tablero de ajedrez 8x8
TAM_CUADRADO = ALTO // DIMENSION
fps = 15 #para las animaciones
IMAGENES = {}

puntaje_ia = 0
puntaje_jugador = 0

""" 
Inicializar un diccionario global de imágenes. Se llamará solo una vez desde el main.
"""
def cargar_imagenes():
    piezas = ['bN', 'wN', "ce", "fl", "ma"]
    for pieza in piezas:
        IMAGENES[pieza] = pg.transform.scale(pg.image.load("resources/" + pieza + ".png"), (TAM_CUADRADO, TAM_CUADRADO))

""" 
Principal driver del código, Manejará la entrada del usuario y actualizará los gráficos.
"""
def main(profundidad):
    global movimiento_hecho, clock, fps
    #setup
    pg.init()
    pantalla = pg.display.set_mode((ANCHO, ALTO))
    pg.display.set_caption('Hungry Horses 1.0')
    pg.display.set_icon(pg.image.load("resources/images/wN.png"))
    clock = pg.time.Clock()
    pantalla.fill(pg.Color("white"))

    #variables para el juego.
    estado_juego = ChessEngine.EstadoJuego()
    movimientos_val = estado_juego.get_mov_validos()
    lista_movimientos = list(map(lambda mov: (mov.fila_final, mov.columna_final), movimientos_val))
    movimiento_hecho = False # variable bandera para cuando se realiza un movimiento
    horse1 = Horse(estado_juego.nuevo_tablero[0], estado_juego.nuevo_tablero[1], estado_juego.nuevo_tablero[2], 9, 0)
    nueva_coordenada_wN = ()

    cargar_imagenes()
    ejecutando = True
    cuadrado_seleccionado = () #no hay cuadrado seleccionado, guarda (fila, columna)
    clicks_jugador = [] #guarda los clicks del jugador -> (dos tuplas: [(fil1, col1), (fil2, col2)])
    
    #se muestra por primera vez la interfaz gráfica.
    dibujarEstadoJuego(pantalla, estado_juego)
    pg.display.flip()
    clock.tick(fps)
    fin = False

    while ejecutando:
    
        for e in pg.event.get():
            if e.type == pg.QUIT:
                ejecutando = False
            elif e.type == pg.MOUSEBUTTONDOWN and not fin:
                fps = 20
                localizacion = pg.mouse.get_pos() #pos x,y del ratón
                columna = localizacion[0] // TAM_CUADRADO
                fila = localizacion[1] // TAM_CUADRADO
                if cuadrado_seleccionado == (fila, columna): #el usuario seleccionó el mismo cuadrado
                    cuadrado_seleccionado = () #eliminar la selección anterior, "deseleccionar"
                    clicks_jugador = []
                else:
                    cuadrado_seleccionado = (fila, columna)
                    clicks_jugador.append(cuadrado_seleccionado)
                if len(clicks_jugador) == 2:
                    mover = ChessEngine.Mover(clicks_jugador[0], clicks_jugador[1], estado_juego.tablero)
                    print(mover.getNotacionAjedrez())
                    lista_movimientos = list(map(lambda mov: (mov.fila_final, mov.columna_final), movimientos_val))
                    if mover in movimientos_val:

                        estado_juego.realizar_movimiento(mover)
                        movimiento_hecho = True
                        cuadrado_seleccionado = () #restablecer los clicks del usuario
                        clicks_jugador = []
                        print("marcador: ", estado_juego.marcador)
                    else: 
                        print("¡movimiento inválido!")
                        clicks_jugador = [cuadrado_seleccionado]

                if not fin:
                    dibujarEstadoJuego(pantalla, estado_juego)
                    clock.tick(fps)
                    pg.display.flip()

        if movimiento_hecho and not fin:
            movimientos_val = estado_juego.get_mov_validos()
            movimiento_hecho = False
            fin = estado_juego.termina_juego()
            if fin:
                dibujarEstadoJuego(pantalla, estado_juego)
                clock.tick(1)
                pg.display.flip()
                game_over(pantalla, fin, estado_juego)

        if estado_juego.mueve_blanco and not fin:
            fps = 1
            nuevo_tablero = estado_juego.mapear_matriz()
            #horse1 = Horse(estado_juego.nuevo_tablero[0], estado_juego.nuevo_tablero[1], estado_juego.nuevo_tablero[2], 9, 0)
            nueva_coordenada_wN = start(Horse(nuevo_tablero[0], nuevo_tablero[1], nuevo_tablero[2], 9, 0), nuevo_tablero[3], profundidad)  

            mover = ChessEngine.Mover(nuevo_tablero[1], nueva_coordenada_wN, estado_juego.tablero)
            if mover in movimientos_val:
                estado_juego.realizar_movimiento(mover)
                movimiento_hecho = True
                print("marcador: ", estado_juego.marcador)
                cuadrado_seleccionado = () #restablecer los clicks del usuario
                clicks_jugador = []
            else:
                print("¡inválido!")

            if not fin:
                dibujarEstadoJuego(pantalla, estado_juego)
                clock.tick(fps)
                pg.display.flip()


def dibujarEstadoJuego(pantalla, estado_juego):
    dibujarTablero(pantalla)
    dibujarPiezas(pantalla, estado_juego.tablero)

def dibujarTablero(pantalla):
    colores = [pg.Color(232,188,144), pg.Color(202,137,61)]
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            color = colores[((fila+columna) % 2)]
            pg.draw.rect(pantalla, color, pg.Rect(columna*TAM_CUADRADO, fila*TAM_CUADRADO, TAM_CUADRADO, TAM_CUADRADO))

def dibujarPiezas(pantalla, tablero):
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            pieza = tablero[fila][columna]
            if pieza != "--": #una pieza no vacía
                pantalla.blit(IMAGENES[pieza], pg.Rect(columna*TAM_CUADRADO, fila*TAM_CUADRADO, TAM_CUADRADO, TAM_CUADRADO))

def game_over(pantalla, fin, estado_juego):
    pantalla.fill("black")
    ganador = "¡Ha ganado la Máquina!" if fin == "P1" else "¡Has ganado!"
    mensaje = get_font(21).render(ganador, True, "White")
    mensaje_marcador = get_font(21).render(str(estado_juego.marcador[0])+" - "+str(estado_juego.marcador[1]), True, "White")
    print(ganador+"\n"+str(estado_juego.marcador[0])+" - "+str(estado_juego.marcador[1]))
    cuadro_mensaje = mensaje.get_rect(center=(ANCHO//2, 250))
    cuadro_mensaje_marcador = mensaje_marcador.get_rect(center=(ANCHO//2, 300))
    pantalla.blit(mensaje, cuadro_mensaje)
    pantalla.blit(mensaje_marcador, cuadro_mensaje_marcador)
    pg.display.update()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pg.font.Font("resources/assets/font.ttf", size)

if __name__ == "__main__":
    profundidad = 2
    main(profundidad)