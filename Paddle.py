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

    def __init__(self, rect, options):
#        self.x = x
#        self.y = y
#        self.w = w
#        self.h = h
#        self.dy = 6
        self.rect = pygame.Rect(rect)
        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2((0, 1))
        self.score = 0
        self.start = self.rect.center
        self.paddle_speed = 25
        if options['Difficulty'] == 'Easy':
            self.AI_level = 0.8
        elif options['Difficulty'] == 'Hard':
            self.AI_level = 1.2
        else:
            self.AI_level = 1.0
        if options['Color'] == 'Green':
            self.color = pygame.Color('#00ff00')
        else:
            self.color = pygame.Color('#ffffff')


    def draw(self, screen):
        screen.fill(self.color, rect=self.rect)
        #pygame.draw.rect(screen, self.color, self.rect)


    def update(self, direction, border, delta, ball=None):
#        if not ball:
#            self.y += direction * self.dy
#        else:
#            if random.random() < self.AI_level:
#                if ball.dx > 0 and ball.x < self.x:
#                    if ball.y + ball.h / 2 > self.y + self.h / 2:
#                        speed = self.dy
#                    elif ball.y + ball.h / 2 < self.y + self.h / 2:
#                        speed = -self.dy
#                    else:
#                        speed = 0
#                    self.y += speed
#        self.bound(screen_height)
        if not ball:
            self.vector = pygame.Vector2((0, direction))
            v = self.vector * delta * self.paddle_speed
            self.center += v
            self.rect.move_ip(v)
        else:
            if ball.vector.x > 0 and ball.rect.x < self.rect.x:
                if ball.rect.centery > self.rect.centery:
                    speed = self.AI_level * self.paddle_speed
                elif ball.rect.centery < self.rect.centery:
                    speed = -1 * self.AI_level * self.paddle_speed
                else:
                    speed = 0
                v = self.vector * speed * delta
                self.center += v
                self.rect.move_ip(v)
        self.bound(border)


    def score_update(self):
        self.score += 1


    def bound(self, border):
#        if self.y < 0:
#            self.y = 0
#        if self.y + self.h > screen_height:
#            self.y = screen_height - self.h
#        border_rect = pygame.Rect(border)
#        clamp = border_rect.inflate(100, 0)
#        if clamp.y != self.rect.y:
#            self.center = pygame.Vector2(clamp.center)
#            self.vector.y = clamp.y
#            self.rect = clamp
        border_rect = pygame.Rect(border)
        rect = border_rect.inflate(100, 0)
        if not rect.contains(self.rect):
            clamp = self.rect.clamp(rect)
            self.center = pygame.Vector2(clamp.center)
            self.rect = clamp



    def reset(self):
#        self.x = self.start[0]
#        self.y = self.start[1]
        self.rect.center = self.start
        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2((0, 1))