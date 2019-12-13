#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pygame
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(BASE_DIR, "material/Pi.mp3"))
pygame.mixer.music.set_volume(0.7)
bullet_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/bullet.wav"))
bullet_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/game_over.wav"))
me_down_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/enemy1_down.wav"))
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/enemy1_down.wav"))
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/enemy1_down.wav"))
enemy3_down_sound.set_volume(0.2)