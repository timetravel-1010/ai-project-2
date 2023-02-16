import pygame, sys
from button import Button

from ChessMain import main

pygame.init()

ANCHO = 512
ALTO = ANCHO
SCREEN = pygame.display.set_mode((ANCHO, ANCHO))
pygame.display.set_caption("Menu")

BG = pygame.image.load("resources/assets/Background-2.png")
BG = pygame.transform.scale(BG, (ANCHO, ALTO))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("resources/assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(25).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(ANCHO//2, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(ANCHO//2, 360), 
                            text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(21).render("Seleccione la dificultad", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(ANCHO//2, 80))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        PRINCIPIANTE = Button(image=None, pos=(ANCHO//2, 180), 
                            text_input="PRINCIPIANTE", font=get_font(30), base_color="Black", hovering_color="Green")
        PRINCIPIANTE.changeColor(OPTIONS_MOUSE_POS)
        PRINCIPIANTE.update(SCREEN)

        AMATEUR = Button(image=None, pos=(ANCHO//2, 260), 
                            text_input="AMATEUR", font=get_font(30), base_color="Black", hovering_color="Green")
        AMATEUR.changeColor(OPTIONS_MOUSE_POS)
        AMATEUR.update(SCREEN)

        EXPERTO = Button(image=None, pos=(ANCHO//2, 340), 
                            text_input="EXPERTO", font=get_font(30), base_color="Black", hovering_color="Green")
        EXPERTO.changeColor(OPTIONS_MOUSE_POS)
        EXPERTO.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=(ANCHO//2, 480), 
                            text_input="REGRESAR", font=get_font(25), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                elif PRINCIPIANTE.checkForInput(OPTIONS_MOUSE_POS):
                    main(2)
                elif AMATEUR.checkForInput(OPTIONS_MOUSE_POS):
                    main(4)
                elif EXPERTO.checkForInput(OPTIONS_MOUSE_POS):
                    main(6)
                    
                
        pygame.display.update()    

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(28).render("Hungry Horses 1.0", True, (232,188,144))
        MENU_RECT = MENU_TEXT.get_rect(center=(ANCHO//2, 100))

        """ PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("resources/assets/Play Rect.png"), (300, 60)), pos=(ANCHO//2, 220), 
                            text_input="PLAY", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
         """
        OPTIONS_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("resources/assets/Options Rect.png"), (300,60)), pos=(ANCHO//2, 300), 
                            text_input="JUGAR", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("resources/assets/Quit Rect.png"), (300,60)), pos=(ANCHO//2, 420), 
                            text_input="SALIR", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [OPTIONS_BUTTON, QUIT_BUTTON]:#[PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                """ if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play() """
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == '__main__':
    main_menu()