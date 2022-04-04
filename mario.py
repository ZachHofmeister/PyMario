import math

import pygame as pg
from entity import Entity
from animation import Animation, AnimationDict
# import spritesheet as ss
from vector import Vector


class Mario(Entity):
    def __init__(self, game, size, ul, image, entities):
        super().__init__(game, size, ul, image)
        self.entities = entities
        self.vel = Vector(0, 0)

    def update(self):
        self.gravity()
        self.ul += self.vel
        super().update()

    def draw(self):
        super().draw()

    def gravity(self):
        minY = math.inf
        entityY = 0
        for entity in self.entities.entities.sprites():
            if abs(entity.ul.x - self.ul.x) < self.size:  # raycast down
                if minY > entity.ul.y - self.ul.y > -(self.size/2):
                    minY = entity.ul.y - self.ul.y  # find closest entity
                    entityY = entity.ul.y
        if minY - self.size <= 0:
            self.vel.y = 0
            self.ul.y = entityY - self.size
        else:
            self.vel.y += 0.08

    def jump(self):
        print("jump")
        self.vel.y = -5
        self.ul.y -= 0.1

    def move(self, dir):
        self.vel.x = dir.x * 3

    def crouch(self):
        pass
