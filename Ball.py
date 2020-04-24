# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:53:08 2020

@author: reill
"""

import pygame
import random
import math


WHITE = (255, 255, 255)


class Ball(object):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dx = 0
        self.dy = 0
        self.v = 3
        self.rect = 0
        self.last_pos = ()
        self.last_score = -1
        self.start = (x, y)


    def draw(self, screen):
        self.rect = pygame.draw.rect(screen, WHITE, [self.x, self.y, self.w, self.h])
        return self.rect


    def update(self, screen_height):
        self.last_pos = (self.x, self.y)
        self.x += self.dx
        self.y += self.dy
        self.bound(screen_height)


    def reset(self):
        self.x = self.start[0]
        self.y = self.start[1]
        

    def collide_check(self, paddleRect):
       if self.rect.colliderect(paddleRect):
           self.dx = -1.01 * self.dx
           self.dy = -self.dy


    def bound(self, screen_height):
        if self.y < 0:
            self.y = 0
            self.dy = -self.dy
            # TODO: math for bouncing off walls
        if self.y + self.h > screen_height:
            self.y = screen_height - self.h
            self.dy = -self.dy
            # TODO: math for bouncing off wall


    def score(self, screen_width, paddle1, paddle2):
        if self.x <= 0:
            paddle2.score_update()
            self.last_score = 0
            return True
        elif self.x + self.w >= screen_width:
            paddle1.score_update()
            self.last_score = 1
            return True
        else:
            return False


    def serve(self, direction):
        # serve ball at random angle
        angle = random.randrange(-45, 45)
        self.dx = direction * self.v * abs(math.cos(math.radians(angle)))
        self.dy = direction * self.v * abs(math.sin(math.radians(angle)))
        return None