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
        '?': 'Item_Brick.png',
        'V': 'Invisible_Block.png'
    }

    def __init__(self, game, map_schema, block_sz):
        self.game = game
        self.map_schema = map_schema
        self.size = block_sz
        self.group = Group()
        self.create_entities()

    def create_entities(self):
        largest_x = 0
        for y, line in enumerate(self.map_schema):
            if len(line) > largest_x:
                largest_x = len(line)
            for x, char in enumerate(line):
                if char in Entities.char_dict:
                    self.group.add(Entity(self.game, self.size, Vector(x, y) * self.size, Entities.char_dict[char]))
        # add invisible barrier to end of level
        for y, line in enumerate(self.map_schema):
            self.group.add(Entity(self.game, self.size, Vector(largest_x-1, y) * self.size, Entities.char_dict['V']))  # largest_x-1 for \n char

    def update(self):
        for entity in self.group.sprites():
            entity.update()

    def draw(self):
        for entity in self.group.sprites():
            entity.draw()

    def move(self, delta_vector):
        for entity in self.group.sprites():
            entity.move(delta_vector)


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

    def move(self, delta_vector):
        self.ul += delta_vector
