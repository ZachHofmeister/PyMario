import math

import pygame as pg
from entity import Entity, AnimatedEntity
from animation import Animation, AnimationDict
# import spritesheet as ss
from vector import Vector
from util import clamp
from copy import copy

class Mario(AnimatedEntity):
    MARIO = 0
    SUPER_MARIO = 1
    FIRE_MARIO = 2
    SUPER_DUCK = 3
    FIRE_DUCK = 4
    PREFIXES = {MARIO: '', SUPER_MARIO: 'super_', FIRE_MARIO: 'fire_', SUPER_DUCK: 'super_', FIRE_DUCK: 'fire_'}
    SCALES = {MARIO: Vector(1, 1), SUPER_MARIO: Vector(1, 2), FIRE_MARIO: Vector(1, 2), SUPER_DUCK: Vector(1, 1.25), FIRE_DUCK: Vector(1, 1.25)}

    def __init__(self, game, size, ul, entities):
        sz = (Mario.SCALES[Mario.MARIO].vmul(size)).tuple()
        sz2 = (Mario.SCALES[Mario.SUPER_MARIO].vmul(size)).tuple()
        duck = (Mario.SCALES[Mario.SUPER_DUCK].vmul(size)).tuple()
        mario_anims = AnimationDict(
            {
                'idle': Animation([pg.image.load(f'images/mario/mario.gif')], scale=sz),
                'walk': Animation([pg.image.load(f'images/mario/mario_walk_{i}.gif') for i in range(3)], scale=sz),
                'jump': Animation([pg.image.load(f'images/mario/mario_jump.gif')], scale=sz),
                'climb': Animation([pg.image.load(f'images/mario/mario_climb_{i}.gif') for i in range(2)], scale=sz),
                'skid': Animation([pg.image.load(f'images/mario/mario_skid.gif')], scale=sz, is_loop=False),
                'swim': Animation([pg.image.load(f'images/mario/mario_swim_{i}.gif') for i in range(4)], scale=sz),
                'dead': Animation([pg.image.load(f'images/mario/mario_dead.gif')], scale=sz),

                'super_idle': Animation([pg.image.load(f'images/super_mario/super_mario.gif')], scale=sz2),
                'super_walk': Animation([pg.image.load(f'images/super_mario/super_mario_walk_{i}.gif') for i in range(3)], scale=sz2),
                'super_jump': Animation([pg.image.load(f'images/super_mario/super_mario_jump.gif')], scale=sz2),
                'super_climb': Animation([pg.image.load(f'images/super_mario/super_mario_climb_{i}.gif') for i in range(2)], scale=sz2),
                'super_skid': Animation([pg.image.load(f'images/super_mario/super_mario_skid.gif')], scale=sz2, is_loop=False),
                'super_swim': Animation([pg.image.load(f'images/super_mario/super_mario_swim_{i}.gif') for i in range(6)], scale=sz2),
                'super_duck': Animation([pg.image.load(f'images/super_mario/super_mario_duck.gif')], scale=duck),

                'fire_idle': Animation([pg.image.load(f'images/fire_mario/fire_mario.gif')], scale=sz2),
                'fire_walk': Animation(
                    [pg.image.load(f'images/fire_mario/fire_mario_walk_{i}.gif') for i in range(3)], scale=sz2),
                'fire_jump': Animation([pg.image.load(f'images/fire_mario/fire_mario_jump.gif')], scale=sz2),
                'fire_climb': Animation(
                    [pg.image.load(f'images/fire_mario/fire_mario_climb_{i}.gif') for i in range(2)], scale=sz2),
                'fire_skid': Animation([pg.image.load(f'images/fire_mario/fire_mario_skid.gif')], scale=sz2, is_loop=False),
                'fire_swim': Animation(
                    [pg.image.load(f'images/fire_mario/fire_mario_swim_{i}.gif') for i in range(6)], scale=sz2),
                'fire_duck': Animation([pg.image.load(f'images/fire_mario/fire_mario_duck.gif')], scale=duck),
                'fire_fireball': Animation([pg.image.load(f'images/fire_mario/fire_mario_fireball.gif')], scale=sz2, is_loop=False),
            },
            'idle'
        )
        super().__init__(game, size, ul, mario_anims)
        self.entities = entities
        self.vel = Vector(0, 0)
        self.x_limits = (0, 0)  # left / right pos limits
        self.y_limits = (0, 0)  # above / below pos limits
        self.jumping = False
        self.ducking = False
        self.state = Mario.SUPER_MARIO
        self.anim_key = 'idle'
        self.last_x_vel = 1

    def update(self):
        self.get_xy_limits()
        print(self.y_limits)
        self.gravity()
        if self.jumping:
            self.jump()
        # update position
        self.ul += self.vel * self.game.deltaTime
        # cancel x movement if ducking
        if self.ducking:
            self.ul.x -= self.vel.x * self.game.deltaTime
        if self.vel.x != 0:
            self.last_x_vel = self.vel.x
        # clamp x to the walls, y to floor or ceiling
        self.clamp_xy_limits()
        # animation states
        if self.ducking:
            self.anim_switch_to('duck')
        elif not self.is_grounded():
            self.anim_switch_to('jump')
        elif self.vel.x != 0:
            self.anim_switch_to('walk')
        else:
            self.anim_switch_to('idle')
        super().update()

    def draw(self):
        super().draw(hflip=self.last_x_vel < 0)

    def get_xy_limits(self):
        self.x_limits = [0, self.screen.get_size()[0] - self.cur_sz().x]
        self.y_limits = [0, self.screen.get_size()[1] - self.cur_sz().y]
        for entity in self.entities.group.sprites():
            if abs(entity.ul.y - self.ul.y) < self.cur_sz().y:  # check if entity is within player Y range
                if self.ul.x >= entity.ul.x + entity.size.x > self.x_limits[0]:  # left
                    self.x_limits[0] = entity.ul.x + entity.size.x
                elif self.ul.x <= entity.ul.x - self.cur_sz().x < self.x_limits[1]:  # right
                    self.x_limits[1] = entity.ul.x - self.cur_sz().x
            if abs(entity.ul.x - self.ul.x) < self.cur_sz().x:  # check if entity is within player X range
                if self.ul.y >= entity.ul.y - entity.size.y > self.y_limits[0]:  # above
                    self.y_limits[0] = entity.ul.y + entity.size.y
                elif self.ul.y <= entity.ul.y - self.cur_sz().y < self.y_limits[1]:  # below
                    self.y_limits[1] = entity.ul.y - self.cur_sz().y

    def clamp_xy_limits(self):
        old_ul = copy(self.ul)
        self.ul.x = clamp(self.ul.x, self.x_limits[0], self.x_limits[1])
        self.ul.y = clamp(self.ul.y, self.y_limits[0], self.y_limits[1])
        # if clamp stopped movement in y direction, zero the y velocity (not for x)
        if old_ul.y != self.ul.y:
            self.vel.y = 0

    def is_grounded(self):
        return self.ul.y == self.y_limits[1]

    def gravity(self):
        if not self.is_grounded():
            self.vel.y += self.game.settings.gravity

    def jump(self):
        if self.is_grounded():
            self.vel.y = -self.game.settings.player_jump_mag

    def move(self, dir):
        self.vel.x = dir.x * self.game.settings.player_speed

    def toggle_duck(self):
        if not self.ducking and self.state == Mario.MARIO:
            return
        self.ducking = not self.ducking
        self.change_state(self.state + 2 if self.ducking else self.state - 2)

    def change_state(self, new_state):
        last_sz = self.cur_sz()
        self.state = new_state
        self.ul.y -= self.cur_sz().y - last_sz.y
        self.anim_update_state()

    def anim_switch_to(self, key):
        super().anim_switch_to(f'{self.cur_prefix()}{key}')
        self.anim_key = key

    def anim_update_state(self):
        super().anim_switch_to(f'{self.cur_prefix()}{self.anim_key}')

    def cur_sz(self):
        return Mario.SCALES[self.state].vmul(self.size)

    def cur_prefix(self):
        return Mario.PREFIXES[self.state]
