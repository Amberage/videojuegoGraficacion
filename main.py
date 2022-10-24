# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 07:26:42 2022

@author: Alejandro
"""

import os
import sys
import math
import random
import pygame

ancho = 900
altura = 720

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode( (ancho, altura) )
pygame.display.set_caption('Proyecto | Equipo: GNU Bash')

class BG:

    def __init__(self, x):
        self.width = ancho
        self.height = altura
        self.x = x
        self.y = 0
        self.texturas()
        self.show()
        self.sonidos()

    def update(self, dx):
        self.x += dx
        if self.x <= -ancho:
            self.x = ancho
            
    def sonidos(self):
        path = os.path.join('assets/sonidos/escenario.wav')
        self.sound = pygame.mixer.Sound(path)
        

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def texturas(self):
        path = os.path.join('assets/imagenes/background.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

class Jugador:

    def __init__(self):
        self.width = 60
        self.height = 60
        self.x = 10
        self.y = 520
        self.texture_num = 0
        self.dy = 3
        self.gravity = 1.2
        self.onground = True
        self.jumping = False
        self.jump_stop = 450
        self.falling = False
        self.fall_stop = self.y
        self.texturas()
        self.sonidos()
        self.show()

    def update(self, loops):
        # Inicio salto
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()
        
        # Caida
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fall_stop:
                self.stop()

        # Caminando
        elif self.onground and loops % 4 == 0:
            self.texture_num = (self.texture_num + 1) % 3
            self.texturas()
        

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def texturas(self):
        path = os.path.join(f'assets/imagenes/jugador_{self.texture_num}.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def sonidos(self):
        path = os.path.join('assets/sonidos/jump.wav')
        self.sound = pygame.mixer.Sound(path)

    def jump(self):
        self.sound.play()
        self.jumping = True
        self.onground = False

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop(self):
        self.falling = False
        self.onground = True

class Cactus:

    def __init__(self, x):
        self.width = 50
        self.height = 60
        self.x = x
        self.y = 520
        self.texturas()
        self.show()

    def update(self, dx):
        self.x += dx

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def texturas(self):
        path = os.path.join('assets/imagenes/cactus.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

class Collision:

    def between(self, obj1, obj2):
        distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
        return distance < 35

class Score:

    def __init__(self, hs):
        self.hs = hs
        self.act = 0
        self.font = pygame.font.SysFont('monospace', 18)
        self.color = (0, 0, 0)
        self.sonidos()
        self.show()

    def update(self, loops):
        self.act = loops // 10
        self.check_hs()
        self.check_sound()

    def show(self):
        self.lbl = self.font.render(f'PUNTUACION {self.hs} {self.act}', 1, self.color)
        lbl_width = self.lbl.get_rect().width
        screen.blit(self.lbl, (ancho - lbl_width - 10, 10))

    def sonidos(self):
        path = os.path.join('assets/sonidos/point.wav')
        self.sound = pygame.mixer.Sound(path)

    def check_hs(self):
        if self.act >= self.hs:
            self.hs = self.act

    def check_sound(self):
        if self.act % 100 == 0 and self.act != 0:
            self.sound.play()

class Game:

    def __init__(self, hs=0):
        self.bg = [BG(x=0), BG(x=ancho)]
        self.jugador = Jugador()
        self.obstacles = []
        self.collision = Collision()
        self.score = Score(hs)
        self.speed = 3
        self.playing = False
        self.sonidos()
        self.set_labels()
        self.spawn_cactus()

    def set_labels(self):
        big_font = pygame.font.SysFont('monospace', 24, bold=True)
        small_font = pygame.font.SysFont('monospace', 18)
        self.big_lbl = big_font.render(f'FIN DEL JUEGO', 1, (0, 0, 0))
        self.small_lbl = small_font.render(f'PRESIONE R PARA REINICIAR', 1, (0, 0, 0))

    def sonidos(self):
        path = os.path.join('assets/sonidos/die.wav')
        self.sound = pygame.mixer.Sound(path)

    def start(self):
        self.playing = True

    def over(self):
        self.sound.play()
        screen.blit(self.big_lbl, (ancho // 2 - self.big_lbl.get_width() // 2, altura // 4))
        screen.blit(self.small_lbl, (ancho // 2 - self.small_lbl.get_width() // 2, altura // 2))
        self.playing = False

    def tospawn(self, loops):
        return loops % 100 == 0

    def spawn_cactus(self):
        # list with cactus
        if len(self.obstacles) > 0:
            prev_cactus = self.obstacles[-1]
            x = random.randint(prev_cactus.x + self.jugador.width + 84, ancho + prev_cactus.x + self.jugador.width + 84)

        # Lista vacia
        else:
            x = random.randint(ancho + 100, 1000)

        # Crear un nuevo cactus
        cactus = Cactus(x)
        self.obstacles.append(cactus)

    def restart(self):
        self.__init__(hs=self.score.hs)

def main():

    # I. de objetos
    game = Game()
    jugador = game.jugador

    # I. de variables
    clock = pygame.time.Clock()
    loops = 0
    over = False

    # Loop de inicio del juego
    while True:

        if game.playing:

            loops += 1

            # Background
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()

            # Iniciar jugador
            jugador.update(loops)
            jugador.show()

            # Cactus
            if game.tospawn(loops):
                game.spawn_cactus()

            for cactus in game.obstacles:
                cactus.update(-game.speed)
                cactus.show()

                # Colision
                if game.collision.between(jugador, cactus):
                   over = True
            
            if over:
                game.over()

            # Puntucacion
            game.score.update(loops)
            game.score.show()

        # Eventos del teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not over:
                        if jugador.onground:
                            jugador.jump()

                        if not game.playing:
                            game.start()

                if event.key == pygame.K_r:
                    game.restart()
                    jugador = game.jugador
                    loops = 0
                    over = False

        clock.tick(80)
        pygame.display.update()

main()