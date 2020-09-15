import pygame, time, random, sys, settings
from button_class import *
import numpy as np

class Game:

    def __init__(self, width, text_width, height, nxC, nyC, language):
        pygame.init()
        # Estado de las celdas:
        #   - 1: celula viva
        #   - 0: celula muerta
        self.width = width
        self.text_width = text_width
        self.height = height
        self.nxC = nxC
        self.nyC = nyC
        self.dimCW = width / nxC
        self.dimCH = height / nyC
        self.gameState = np.zeros((nxC, nyC))
        self.newGameState = np.zeros((nxC, nyC))
        self.pause = True
        self.cell_color = [[128, 128, 128], [255, 255, 255]]
        self.font = pygame.font.Font('KidGames.ttf',64)
        self.language = language
        self.playing_buttons = []
        self.load_buttons()

    def event_handler(self):
        for event in pygame.event.get():
            # Detectamos si se presiona una tecla
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit('user quit')
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                
                # PATRONES
                if event.key == pygame.K_a:
                    # patron acorn
                    self.draw_acorn()
                if event.key == pygame.K_o:
                    # oscilador 9x9
                    self.draw_oscilator9x9()
                if event.key == pygame.K_u:
                    # oscilador 13x13
                    self.draw_oscilator13x13()
                if event.key == pygame.K_k:
                    # oscilador 12x12
                    self.draw_oscilator12x12()
                if event.key == pygame.K_q:
                    # oscilador 10x3
                    self.draw_oscilator10x3()
                if event.key == pygame.K_s:
                    # oscilador 6x6
                    self.draw_oscilator6x6()
                if event.key == pygame.K_w:
                    # oscilador 4x4
                    self.draw_oscilator4x4()
                if event.key == pygame.K_x:
                    # automata movil 3x3
                    self.draw_movil3x3()
                if event.key == pygame.K_n:
                    # automata movil 7x4
                    self.draw_movil7x4()
                if event.key == pygame.K_p:
                    # automata palo 1x3
                    self.draw_stick()
                if event.key == pygame.K_v:
                    # pistola vertical 36x9
                    self.draw_gun36x9()
                if event.key == pygame.K_h:
                    # pistola horizontal 9x36
                    self.draw_gun9x36()
                    
                # BORRAR
                if event.key == pygame.K_d:
                    self.gameState = np.zeros((self.nxC, self.nyC))
                    time.sleep(0.01)
                
                # COLOR DE CELDA
                if event.key == pygame.K_r:
                    # Rojo
                    self.cell_color[1] = [255,0,0]
                if event.key == pygame.K_g:
                    # Verde
                    self.cell_color[1] = [0,255,0]
                if event.key == pygame.K_b:
                    # Azul
                    self.cell_color[1] = [0,0,255]
                if event.key == pygame.K_c:
                    # Cyan
                    self.cell_color[1] = [0,255,255]
                if event.key == pygame.K_m:
                    # Magenta
                    self.cell_color[1] = [255,0,255]
                if event.key == pygame.K_y:
                    # Amarillo
                    self.cell_color[1] = [255,255,0]
                if event.key == pygame.K_z:
                    # Random color
                    self.cell_color[1] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
                
                # SALIR
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit('user quit')

            #Detectamos si se presiona el raton
            if sum(pygame.mouse.get_pressed()) > 0:
                posX, posY = pygame.mouse.get_pos()
                celX, celY = int(np.floor(posX / self.dimCW)), int(np.floor(posY / self.dimCH))
                if celX < self.nxC and celY < self.nyC:
                    self.gameState[celX, celY] = not pygame.mouse.get_pressed()[2]
                else:
                    for button in self.playing_buttons:
                        button.update(pygame.mouse.get_pos())
                        if button.highLighted:
                            button.click()

    def update(self, x, y):
        # Calculamos los vecinos cercanos
        n_neigh = self.gameState[(x - 1) % self.nxC, (y - 1) % self.nyC] + \
                  self.gameState[(x)     % self.nxC, (y - 1) % self.nyC] + \
                  self.gameState[(x + 1) % self.nxC, (y - 1) % self.nyC] + \
                  self.gameState[(x - 1) % self.nxC, (y)     % self.nyC] + \
                  self.gameState[(x + 1) % self.nxC, (y)     % self.nyC] + \
                  self.gameState[(x - 1) % self.nxC, (y + 1) % self.nyC] + \
                  self.gameState[(x)     % self.nxC, (y + 1) % self.nyC] + \
                  self.gameState[(x + 1) % self.nxC, (y + 1) % self.nyC]

        # Reglas:
        #   - 1: Una celula muerta con 3 celulas vecinas vivas, revive
        #   - 2: Una celula viva con menos de 2 o mas de 3 vecinas vivas, muere
        if self.gameState[x, y] == 0 and n_neigh == 3:
            self.newGameState[x, y] = 1
        elif self.gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
            self.newGameState[x, y] = 0
        
        

    def draw(self, screen):

        self.draw_pause(screen)
        self.write_instructions(screen)
        self.newGameState = np.copy(self.gameState)

        for y in range(self.nxC):
            for x in range(self.nyC):
                if not self.pause:
                    self.update(x, y)

                # Creamos el poligono de cada celda a dibujar
                poly = [
                    ((x)     * self.dimCW, (y)     * self.dimCH),
                    ((x + 1) * self.dimCW, (y)     * self.dimCH),
                    ((x + 1) * self.dimCW, (y + 1) * self.dimCH),
                    ((x)     * self.dimCW, (y + 1) * self.dimCH),
                ]

                # Dibujamos la celda para cada par x e y
                color = self.cell_color[int(self.newGameState[x, y])]
                border = not self.newGameState[x, y]
                pygame.draw.polygon(screen, color, poly, border)
        # Actualizamos el estado
        self.gameState = np.copy(self.newGameState)
        
        for button in self.playing_buttons:
            button.draw(screen)

    def draw_pause(self, screen):

        if self.pause:
            color_pause = (255,0,0)
            text_pause = settings.pause_text[self.language][0]
        else:
            color_pause = (0,255,0)
            text_pause = settings.pause_text[self.language][1]

        text = self.font.render(text_pause, True, color_pause)
        w = self.width + (500 - text.get_width()) / 2
        h = (100 - text.get_height()) / 2
        screen.blit(text, (w, h))

    # Patron Acorn
    def draw_acorn(self):
    
        x = random.randint(0, self.nxC - 4)
        y = random.randint(0, self.nyC - 8)

        self.gameState[x:x+7,y:y+3] = settings.acorn

    # Automata palo 1x3
    def draw_stick(self):

        x = random.randint(0, self.nxC - 1)
        y = random.randint(0, self.nyC - 4)

        self.gameState[x,y:y+3] = settings.stick

    # Automata movil 3x3
    def draw_movil3x3(self):

        x = random.randint(0, self.nxC - 4)
        y = random.randint(0, self.nyC - 4)

        self.gameState[x:x+3,y:y+3] = settings.movil3x3

    # Automata movil 7x4
    def draw_movil7x4(self):

        x = random.randint(0, self.nxC - 8)
        y = random.randint(0, self.nyC - 5)

        self.gameState[x:x+7,y:y+4] = settings.movil7x4

    # Oscilador 13x13
    def draw_oscilator13x13(self):

        x = random.randint(0, self.nxC - 14)
        y = random.randint(0, self.nyC - 14)

        self.gameState[x:x+13,y:y+13] = settings.oscilator13x13

    # Oscilador 12x12
    def draw_oscilator12x12(self):

        x = random.randint(0, self.nxC - 13)
        y = random.randint(0, self.nyC - 13)

        self.gameState[x:x+12,y:y+12] = settings.oscilator12x12

    # Oscilador 10x3
    def draw_oscilator10x3(self):

        x = random.randint(0, self.nxC - 11)
        y = random.randint(0, self.nyC - 4)

        self.gameState[x:x+10,y:y+3] = settings.oscilator10x3

    # Oscilador 9x9
    def draw_oscilator9x9(self):

        x = random.randint(0, self.nxC - 10)
        y = random.randint(0, self.nyC - 10)

        self.gameState[x:x+9,y:y+9] = settings.oscilator9x9

    # Oscilador 6x6
    def draw_oscilator6x6(self):

        x = random.randint(0, self.nxC - 7)
        y = random.randint(0, self.nyC - 7)

        self.gameState[x:x+6,y:y+6] = settings.oscilator6x6

    # Oscilador 4x4
    def draw_oscilator4x4(self):

        x = random.randint(0, self.nxC - 5)
        y = random.randint(0, self.nyC - 5)

        self.gameState[x:x+4,y:y+4] = settings.oscilator4x4

    # Pistola 36x9
    def draw_gun36x9(self):

        x = random.randint(0, self.nxC - 10)
        y = random.randint(0, self.nyC - 37)

        self.gameState[x:x+9,y:y+36] = settings.gun36x9

    # Pistola 9x36
    def draw_gun9x36(self):

        x = random.randint(0, self.nxC - 37)
        y = random.randint(0, self.nyC - 10)

        self.gameState[x:x+36,y:y+9] = settings.gun9x36


    def write_instructions(self, screen):
        font = pygame.font.Font('CutiveMono-Regular.ttf',16)
        instruct = settings.instructions[self.language]
        text_height = (self.height - 150) / len(instruct)
        for i in range(len(instruct)):
            screen.blit(font.render(instruct[i], True, (255,255,255)),
                        (self.width + 50, 50 + (text_height * (i+1))))

    def change_language(self, language):
        self.language = language

    def load_buttons(self):
    
        self.playing_buttons.append(Button(self.width + 50,
                                           self.height - 50, 100, 40,
                                           function=self.change_language,
                                           params='english',
                                           colour=(27,142,207),
                                           text='ENGLISH'))
        self.playing_buttons.append(Button(self.width + self.text_width - 150,
                                           self.height - 50, 100, 40,
                                           function=self.change_language,
                                           params='spanish',
                                           colour=(27,142,207),
                                           text='SPANISH',
                                           highLighted=True))

if __name__ == '__main__':
    # Crear ventana de tamaño definido
    width, height = 1500, 1000
    text_width = 500
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Super-Game Of Life')
    # Color de fondo y pintar el fondo
    bg = 30, 30, 30
    screen.fill(bg)
    # Crear el juego
    game = Game(width - text_width, text_width, height, 50, 50, 'spanish')
    
    # Jugar
    while True:

        try:

            screen.fill(bg)
            time.sleep(0.1)
            game.event_handler()
            game.draw(screen)
            pygame.display.flip()

        except KeyboardInterrupt:
            sys.exit('keyboard interrupt')
