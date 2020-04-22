# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:42:15 2020

@author: reill
"""

import pygame

WHITE = (255, 255, 255)


class Paddle(object):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dy = 0
        self.dt = 0
        self.score = 0


    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, [self.x, self.y, self.w, self.h])


    def update(self, dt):
        return None


    def score_update(self):
        self.score += 1


    def bound(self, screen_height):
        if self.y < 0:
            self.y = 0
        if self.y + self.h > screen_height:
            self.y = screen_height - self.h