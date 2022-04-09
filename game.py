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

        # Clock used to cap FPS
        self.clock = pg.time.Clock()
        self.deltaTime = 0

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
            if e.type == pg.KEYUP:
                if e.key in dir_keys:
                    d = dir_keys[e.key]
                    if (d == LEFT and self.level.mario.vel.x <= 0) or (d == RIGHT and self.level.mario.vel.x >= 0):
                        self.level.mario.move(dirs[STOP])  # Stops, only if still moving the direction of key released
                    elif d == UP:
                        self.level.mario.jumping = False
            if e.type == pg.KEYDOWN:
                if e.key in dir_keys:
                    d = dir_keys[e.key]
                    if d == LEFT or d == RIGHT:
                        print(d)
                        self.level.mario.move(dirs[d])
                    elif d == UP:
                        # self.level.mario.jump()
                        self.level.mario.jumping = True
                    elif d == DOWN:
                        self.level.mario.crouch()
                # print(self.bg_color)

    def play(self):
        while not self.finished:
            self.check_events()
            self.update()
            self.draw()
            self.deltaTime = self.clock.tick(self.settings.fps)  # FPS cap
        print("GAME OVER! EXITING...")
        exit()
