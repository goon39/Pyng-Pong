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

    def __init__(self, rect, options):
        #self.x = x
        #self.y = y
        #self.w = w
        #self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2()
       # self.dx = 0
      #  self.dy = 0
        #self.v = 5
        #self.rect = 0
        self.last_pos = ()
        self.last_score = -1
        self.start = self.rect.center
        if options['Color'] == 'Green':
            self.color = pygame.Color(GREEN)
        else:
            self.color = pygame.Color(WHITE)
        if options['Difficulty'] == 'Easy':
            #self.cor = 1.03
            self.speed = 10
        elif options['Difficulty'] == 'Hard':
            #self.cor = 1.07
            self.speed = 50
        else:
            #self.cor = 1.05
            self.speed = 30


    def draw(self, screen):
        #self.rect = pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h])
        #return self.rect
        screen.fill(self.color, self.rect)


    def update(self, delta, border):
#        self.last_pos = (self.x, self.y)
#        self.x += self.dx
#        self.y += self.dy
#        wall = self.bound(screen_height)
#        return wall
        self.center += self.vector * self.speed * delta
        wall = self.bound(border)
        return wall


    def reset(self):
        #self.x = self.start[0]
        #self.y = self.start[1]
        self.rect.center = self.start
        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2()
        

    def collide_check(self, paddleRect):
#        if (self.y < paddleRect.y + paddleRect.h) and (self.y + self.h > paddleRect.y):
#            if (paddleRect.x < self.x < paddleRect.x + paddleRect.w):
#                self.dx = -self.cor * self.dx
#                self.dy = self.cor * self.dy
#                if self.dx > 0:
#                    self.x += self.w
#                else:
#                    self.x += -self.w
#                return True
#        else:
#            return False
        if self.rect.colliderect(paddleRect):
            if self.vector.x < 0:
                self.rect.left = paddleRect.right
            else:
                self.rect.right = paddleRect.left
            self.center.x = self.rect.centerx
            self.vector = (pygame.Vector2(self.rect.center) - paddleRect.center).normalize()
            return True
        else:
            return False


    def bound(self, border):
#        if self.y < 0:
#            self.y = 0
#            self.dy = -self.dy
#            return True
#        elif self.y + self.h > screen_height:
#            self.y = screen_height - self.h
#            self.dy = -self.dy
#            return True
#        else:
#            return False
        rect = border.inflate(100, 0)
        clamp = self.rect.clamp(rect)

        if clamp.y != self.rect.y:
            self.center = pygame.Vector2(clamp.center)
            self.vector.y -= self.vector.y
            self.rect = clamp
            return True
        else:
            return False


    def score(self, screen_width, paddle1, paddle2):
#        if self.x <= 0:
#            paddle2.score_update()
#            self.last_score = 0
#            return True
#        elif self.x + self.w >= screen_width:
#            paddle1.score_update()
#            self.last_score = 1
#            return True
#        else:
#            return False
        if self.rect.right < paddle1.left:
            paddle2.score_update()
            self.last_score = 0
            return True
        elif self.rect.left > paddle2.right:
            paddle1.score_update()
            self.last_score = 1
            return True
        else:
            return False


    def serve(self, direction):
        # serve ball at random angle
#        angle = random.randrange(-45, 45)
#        self.dx = direction * self.v * abs(math.cos(math.radians(angle)))
#        self.dy = direction * self.v * abs(math.sin(math.radians(angle)))
        if direction < 0:
            angle = random.randint(-45, -135)
        else:
            angle = random.randint(45, 135)
        self.vector = pygame.Vector2.from_polar(1, angle)
        