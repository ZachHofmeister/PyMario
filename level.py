import pygame as pg
from entity import Entity, Entities
from mario import Mario
from vector import Vector

class Level:
    def __init__(self, game, lvl_name, bg_color):
        self.game = game
        self.screen = game.screen
        self.name = lvl_name
        with open(f'levels/{lvl_name}') as schema_file:
            self.map_schema = schema_file.readlines()
        # self.back_image = pg.image.load(f'images/{back_image}')
        # back_rect = self.back_image.get_rect()
        # back_scale = (back_rect.width * (self.game.settings.screen_height / back_rect.height),
        #               self.game.settings.screen_height)
        # print(back_scale)
        # self.back_image = pg.transform.scale(self.back_image, back_scale)

        self.bg_color = bg_color

        block_sz = self.game.settings.screen_height / len(self.map_schema)
        print(block_sz)
        self.entities = Entities(self.game, self.map_schema, Vector(block_sz, block_sz))
        self.mario = Mario(self.game, Vector(block_sz, block_sz), Vector(100, 500), self.entities)

    def update(self):
        self.entities.update()
        self.mario.update()
        if self.mario.ul.x + (self.mario.size.x/2) > (self.screen.get_size()[0]/2):
            # when mario moves past middle of screen, move level
            # print (self.mario.ul.x + (self.mario.size/2) - (self.screen.get_size()[0]/2))
            self.entities.move(-Vector(self.mario.ul.x + (self.mario.size.x/2) - (self.screen.get_size()[0]/2), 0))
            self.mario.ul.x = (self.screen.get_size()[0]/2) - (self.mario.size.x/2)


    def draw(self):
        # rect = self.back_image.get_rect()
        # self.screen.blit(self.back_image, rect)
        self.screen.fill(self.bg_color)
        self.entities.draw()
        self.mario.draw()
