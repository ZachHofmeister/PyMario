import sys

import pygame as pg
from settings import Settings


class Game:
    def __init__(self):
        # Init pygame
        pg.init()
        pg.display.set_caption("Super Wario Game")

        # Instantiate helper objects
        self.settings = Settings()

        # Init self variables
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = list(self.settings.bg_color)
        self.finished = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.bg_color)
        pg.display.flip()

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.finished = True
            elif e.type == pg.KEYDOWN:
                # if e.key == pg.K_1:
                #     self.bg_color[0] += 10
                # elif e.key == pg.K_2:
                #     self.bg_color[0] -= 10
                # elif e.key == pg.K_3:
                #     self.bg_color[1] += 10
                # elif e.key == pg.K_4:
                #     self.bg_color[1] -= 10
                # elif e.key == pg.K_5:
                #     self.bg_color[2] += 10
                # elif e.key == pg.K_6:
                #     self.bg_color[2] -= 10
                print(self.bg_color)

    def play(self):
        while not self.finished:
            self.check_events()
            self.update()
            self.draw()
        print("GAME OVER! EXITING...")
        exit()
