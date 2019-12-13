#! /usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
import pygame
class SmallEnemy(pygame.sprite.Sprite):
    energy = 1
    def __init__(self, bg_size):
        super(SmallEnemy, self).__init__()
        self.image = pygame.image.load("material/image/enemy.png")
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 2
        self.energy = SmallEnemy.energy
        self.rect.left, self.rect.top = (
            randint(0, self.width - self.rect.width),  randint(-5 * self.rect.height, -5),
        )
        self.active = True
        self.destroy_images = []
        self.destroy_images.extend(
            [
                pygame.image.load("material/image/enemy_down.png"),
                pygame.image.load("material/image/enemy_down.png"),
                pygame.image.load("material/image/enemy_down.png"),
                pygame.image.load("material/image/enemy_down.png")
            ]
        )
    def move(self,speed = 10):
        if self.rect.top < self.height:
            #self.rect.top += self.speed
            self.rect.top += int(speed / 2)
        else:
            self.reset()
    def reset(self):
        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width), randint(-5 * self.rect.height, 0))
        self.active = True
class MidEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super(MidEnemy, self).__init__()
        self.image = pygame.image.load("material/image/enemy.png")
class BigEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super(BigEnemy, self).__init__()
        self.image = pygame.image.load("material/image/enemy.png")