import pygame as pg
from pygame.sprite import Sprite, Group
from vector import Vector


class Entity(Sprite):
    def __init__(self, game, size, ul, image):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.size = size
        self.ul = ul
        self.image = pg.transform.scale(image, size.tuple())
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x, self.rect.y = self.ul.x, self.ul.y

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def move(self, delta_vector):
        self.ul += delta_vector


class AnimatedEntity(Entity):
    def __init__(self, game, size, ul, anim_dict):
        super().__init__(game, size, ul, anim_dict.image())
        self.anim_dict = anim_dict
        self.xdir = 1

    def draw(self, hflip=False):
        self.screen.blit(pg.transform.flip(self.anim_dict.image(), hflip, False), self.rect)

    def anim_switch_to(self, key):
        self.anim_dict.switch_to(key)
        self.image = self.anim_dict.image()
        self.rect = self.image.get_rect()

    def anim_has_key(self, key): self.anim_dict.has_key(key)
    def anim_keys(self): return self.anim_dict.keys()
    def anim_is_expired(self): return self.anim_dict.is_expired()
    def anim_reset(self): self.anim_dict.reset()
    def anim_image(self): return self.anim_dict.image()


class ContainerEntity(Entity):
    def __init__(self, game, size, ul, image, entity_char):
        super().__init__(game, size, ul, image)
        self.entity_char = entity_char


class Entities:
    char_dict = {
        'X': {'class': Entity, 'img': pg.image.load('images/Ground_Brick.png')},
        'B': {'class': Entity, 'img': pg.image.load('images/Red_Brick.png')},
        'M': {'class': Entity, 'img': pg.image.load('images/Red_Brick.png')},
        'S': {'class': Entity, 'img': pg.image.load('images/Red_Brick.png')},
        'R': {'class': Entity, 'img': pg.image.load('images/Stair_Brick.png')},
        '?': {'class': Entity, 'img': pg.image.load('images/Item_Brick.png')},
        'V': {'class': Entity, 'img': pg.image.load('images/Invisible_Block.png')}
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
                    props = Entities.char_dict[char]
                    self.group.add(props['class'](self.game, self.size, Vector(x, y).vmul(self.size), props['img']))
        # add invisible barrier to end of level
        for y, line in enumerate(self.map_schema):
            props = Entities.char_dict['V']
            self.group.add(props['class'](self.game, self.size, Vector(largest_x-1, y).vmul(self.size), props['img']))  # largest_x-1 for \n char

    def create_entity(self, char, game, size, ul, image):
        if char == 'X':
            return Entity(game, size, ul, image)


    def update(self):
        for entity in self.group.sprites():
            entity.update()

    def draw(self):
        for entity in self.group.sprites():
            entity.draw()

    def move(self, delta_vector):
        for entity in self.group.sprites():
            entity.move(delta_vector)

