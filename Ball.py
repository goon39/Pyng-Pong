# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:53:08 2020

@author: reill
"""

import pygame
import random
import math


WHITE = (255, 255, 255)
GREEN = (57, 255, 20)


class Ball(object):

    def __init__(self, x, y, w, h, options):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dx = 0
        self.dy = 0
        self.v = 5
        self.rect = 0
        self.last_pos = ()
        self.last_score = -1
        self.start = (x, y)
        if options['Color'] == 'Green':
            self.color = GREEN
        else:
            self.color = WHITE
        if options['Difficulty'] == 'Easy':
            self.cor = 1.03
        elif options['Difficulty'] == 'Hard':
            self.cor = 1.07
        else:
            self.cor = 1.05


    def draw(self, screen):
        self.rect = pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h])
        return self.rect


    def update(self, screen_height):
        self.last_pos = (self.x, self.y)
        self.x += self.dx
        self.y += self.dy
        wall = self.bound(screen_height)
        return wall


    def reset(self):
        self.x = self.start[0]
        self.y = self.start[1]
        

    def collide_check(self, paddleRect):
        if (self.y < paddleRect.y + paddleRect.h) and (self.y + self.h > paddleRect.y):
            if (paddleRect.x < self.x < paddleRect.x + paddleRect.w):
                self.dx = -self.cor * self.dx
                self.dy = self.cor * self.dy
                if self.dx > 0:
                    self.x += self.w
                else:
                    self.x += -self.w
                return True
        else:
            return False


    def bound(self, screen_height):
        if self.y < 0:
            self.y = 0
            self.dy = -self.dy
            return True
        elif self.y + self.h > screen_height:
            self.y = screen_height - self.h
            self.dy = -self.dy
            return True
        else:
            return False


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