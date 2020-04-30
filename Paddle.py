# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:42:15 2020

@author: reill
"""

import pygame
import random

WHITE = (255, 255, 255)
GREEN = (57, 255, 20)


class Paddle(object):

    def __init__(self, x, y, w, h, options):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dy = 6
        self.score = 0
        self.rect = 0
        self.start = (x, y)
        if options['Difficulty'] == 'Easy':
            self.AI_level = 0.4
        elif options['Difficulty'] == 'Hard':
            self.AI_level = 0.8
        else:
            self.AI_level = 0.6
        if options['Color'] == 'Green':
            self.color = GREEN
        else:
            self.color = WHITE

    def draw(self, screen):
        self.rect = pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h])
        return self.rect


    def update(self, direction, screen_height, ball=None):
        if not ball:
            self.y += direction * self.dy
        else:
            if random.random() < self.AI_level:
                if ball.dx > 0 and ball.x < self.x:
                    if ball.y + ball.h / 2 > self.y + self.h / 2:
                        speed = self.dy
                    elif ball.y + ball.h / 2 < self.y + self.h / 2:
                        speed = -self.dy
                    else:
                        speed = 0
                    self.y += speed
        self.bound(screen_height)


    def score_update(self):
        self.score += 1


    def bound(self, screen_height):
        if self.y < 0:
            self.y = 0
        if self.y + self.h > screen_height:
            self.y = screen_height - self.h


    def reset(self):
        self.x = self.start[0]
        self.y = self.start[1]