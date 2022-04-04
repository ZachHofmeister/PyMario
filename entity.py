import pygame as pg
from pygame.sprite import Sprite, Group
from vector import Vector


class Entities:
    char_dict = {
        'X': 'Ground_Brick.png',
        'B': 'Red_Brick.png',
        'M': 'Red_Brick.png',
        'S': 'Red_Brick.png',
        'R': 'Stair_Brick.png',
        '?': 'Item_Brick.png'
    }

    def __init__(self, game, map_schema, block_sz):
        self.game = game
        self.map_schema = map_schema
        self.size = block_sz
        self.entities = Group()
        self.create_entities()

    def create_entities(self):
        for y, line in enumerate(self.map_schema):
            for x, char in enumerate(line):
                if char in Entities.char_dict:
                    self.entities.add(Entity(self.game, self.size, Vector(x, y) * self.size, Entities.char_dict[char]))

    def update(self):
        for entity in self.entities.sprites():
            entity.update()

    def draw(self):
        for entity in self.entities.sprites():
            entity.draw()


class Entity(Sprite):
    def __init__(self, game, size, ul, image):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.size = size
        self.ul = ul
        self.image = pg.transform.scale(pg.image.load(f'images/{image}'), (size, size))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x, self.rect.y = self.ul.x, self.ul.y

    def draw(self):
        self.screen.blit(self.image, self.rect)
