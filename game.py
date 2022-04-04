import sys

import pygame as pg
from settings import Settings
from level import Level
from vector import Vector

LEFT, RIGHT, UP, DOWN, STOP = 'left', 'right', 'up', 'down', 'stop'

dirs = {LEFT: Vector(-1, 0),
        RIGHT: Vector(1, 0),
        STOP: Vector(0, 0)}

dir_keys = {pg.K_LEFT: LEFT, pg.K_a: LEFT,
            pg.K_RIGHT: RIGHT, pg.K_d: RIGHT,
            pg.K_UP: UP, pg.K_w: UP, pg.K_SPACE: UP,
            pg.K_DOWN: DOWN, pg.K_s: DOWN}

class Game:
    def __init__(self):
        # Init pygame
        pg.init()
        pg.display.set_caption("Super Mario Game")

        # Instantiate helper objects
        self.settings = Settings()

        # Init self variables
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = list(self.settings.bg_color)
        self.finished = False

        # Init sub classes
        self.level = Level(self, 'level_loc.txt', self.bg_color)

    def update(self):
        self.level.update();

    def draw(self):
        self.level.draw();
        pg.display.flip()

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.finished = True
            elif e.type == pg.KEYDOWN:
                if e.key in dir_keys:
                    d = dir_keys[e.key]
                    if d == LEFT or d == RIGHT:
                        self.level.mario.move(dirs[d])
                    elif d == UP:
                        self.level.mario.jump()
                    elif d == DOWN:
                        self.level.mario.crouch()
            elif e.type == pg.KEYUP:
                if e.key in dir_keys:
                    d = dir_keys[e.key]
                    if d == LEFT or d == RIGHT:
                        self.level.mario.move(dirs[STOP])
                # print(self.bg_color)

    def play(self):
        while not self.finished:
            self.check_events()
            self.update()
            self.draw()
        print("GAME OVER! EXITING...")
        exit()
