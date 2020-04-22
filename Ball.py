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
        self.last_pos = ()


    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, [self.x, self.y, self.w, self.h])


    def update(self, dt):
        return None
        

    def collide_check(self, paddle):
        return None


    def bound(self, screen_height):
        if self.y < 0:
            self.y = 0
            # TODO: math for bouncing off walls
        if self.y + self.h > screen_height:
            self.y = screen_height - self.h
            # TODO: math for bouncing off wall


    def score(self, screen_width, paddle1, paddle2):
        if self.x <= 0:
            paddle1.score_update()
            return True
        elif self.x + self.w >= screen_width:
            paddle2.score_update()
            return True
        else:
            return False


    def serve(self, direction):
        # serve ball at random angle
        return None