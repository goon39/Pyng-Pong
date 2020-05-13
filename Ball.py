# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:53:08 2020

@author: reill
"""

import pygame
import random
import math


WHITE = (255, 255, 255, 0)
GREEN = (57, 255, 20)


class Ball(object):

    def __init__(self, rect, options):
        #self.x = x
        #self.y = y
        #self.w = w
        #self.h = h
        self.rect = pygame.Rect(rect)
        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2()
       # self.dx = 0
      #  self.dy = 0
        #self.v = 5
        #self.rect = 0
        self.last_pos = ()
        self.last_score = -1
        self.start = self.rect.center
        self.speed = 6
        if options['Color'] == 'Green':
            self.color = pygame.Color('#00ff00')
        else:
            self.color = pygame.Color('#ffffff')
        if options['Difficulty'] == 'Easy':
            self.cor = 1.03
        elif options['Difficulty'] == 'Hard':
            self.cor = 1.07
        else:
            self.cor = 1.05


    def draw(self, screen):
        #self.rect = pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h])
        #return self.rect
        #screen.fill(self.color, rect=self.rect)
        pygame.draw.rect(screen, self.color, self.rect)


    def update(self, delta, border):
#        self.last_pos = (self.x, self.y)
#        self.x += self.dx
#        self.y += self.dy
#        wall = self.bound(screen_height)
#        return wall
        self.center += self.vector * self.speed * delta
        #self.rect.x += self.vector.x * self.speed * delta
        #self.rect.y += self.vector.y * self.speed * delta
        v = self.vector * self.speed * delta
        self.rect.move_ip(v)
        print(self.rect)
        #self.rect = pygame.Rect((self.center.x - self.rect.w, self.center.y - self.rect.h, self.rect.w, self.rect.h))
        wall = self.bound(border)
        return wall


    def reset(self):
        #self.x = self.start[0]
        #self.y = self.start[1]
        self.rect.center = self.start
        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2()
        

    def collide_check(self, paddle):
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
        if self.rect.colliderect(paddle):
            if self.vector.x < 0:
                self.rect.left = paddle.rect.right
            else:
                self.rect.right = paddle.rect.left
            self.center.x = self.rect.centerx
            self.vector = self.cor * (pygame.Vector2(self.rect.center) - paddle.rect.center).normalize()
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
        border_rect = pygame.Rect(border)
        rect = border_rect.inflate(100, 0)
        clamp = self.rect.clamp(rect)

        if clamp.y != self.rect.y:
            self.center = pygame.Vector2(clamp.center)
            self.vector.y -= self.vector.y
            self.rect = clamp
            return True
        else:
            return False
#        border_rect = pygame.Rect(border)
#        rect = border_rect.inflate(100, 0)
#        if not rect.contains(self.rect):
#            clamp = self.rect.clamp(rect)
#            self.center = pygame.Vector2(clamp.center)
#            self.vector.y = -self.vector.y
#            self.rect = clamp
#            return True
#        else:
#            return False


    def score(self, paddle1, paddle2):
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
        if self.rect.right < paddle1.rect.left:
            paddle2.score_update()
            self.last_score = 0
            return True
        elif self.rect.left > paddle2.rect.right:
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
            angle = random.randint(135, 245)
        else:
            angle = random.randint(-45, 45)
        self.vector.from_polar((1, math.radians(angle)))
        