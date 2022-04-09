import math

import pygame as pg
from entity import Entity
from animation import Animation, AnimationDict
# import spritesheet as ss
from vector import Vector
from util import clamp
from copy import copy


class Mario(Entity):
    def __init__(self, game, size, ul, image, entities):
        super().__init__(game, size, ul, image)
        self.entities = entities
        self.vel = Vector(0, 0)
        self.x_limits = (0, 0)  # left / right pos limits
        self.y_limits = (0, 0)  # above / below pos limits
        self.delta_x = 0;
        self.jumping = False

    def update(self):
        self.get_xy_limits()
        self.gravity()
        if self.jumping:
            self.jump()
        # update position
        old_x = self.ul.x
        self.ul += self.vel * self.game.deltaTime
        # clamp x to the walls, y to floor or ceiling
        self.clamp_xy_limits()
        self.delta_x = old_x
        super().update()

    def draw(self):
        super().draw()

    def get_xy_limits(self):
        self.x_limits = [0, self.screen.get_size()[0] - self.size]
        self.y_limits = [0, self.screen.get_size()[1] - self.size]
        for entity in self.entities.group.sprites():
            if abs(entity.ul.y - self.ul.y) < self.size:  # check if entity is within player Y range
                if self.ul.x >= entity.ul.x + self.size > self.x_limits[0]:
                    self.x_limits[0] = entity.ul.x + self.size
                elif self.ul.x <= entity.ul.x - self.size < self.x_limits[1]:  # below
                    self.x_limits[1] = entity.ul.x - self.size
            if abs(entity.ul.x - self.ul.x) < self.size:  # check if entity is within player X range
                if self.ul.y >= entity.ul.y + self.size > self.y_limits[0]:  # above
                    self.y_limits[0] = entity.ul.y + self.size
                elif self.ul.y <= entity.ul.y - self.size < self.y_limits[1]:  # below
                    self.y_limits[1] = entity.ul.y - self.size

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

    def crouch(self):
        pass
