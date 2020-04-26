# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:42:15 2020

@author: reill
"""

import pygame
import time
import random

WHITE = (255, 255, 255)


class Paddle(object):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dy = 6
        self.score = 0
        self.rect = 0
        self.start = (x, y)
        self.AI_on_after = time.time()
        self.P_AI_fail = 0.1  # Probability of failure
        self.T_AI_fail = 0.5  # Delay in reaction time
        self.next_fail_decision_T = time.time()


    def draw(self, screen):
        self.rect = pygame.draw.rect(screen, WHITE, [self.x, self.y, self.w, self.h])
        return self.rect


    def update(self, direction, screen_height, computer=False, ball_pos=None, ball_speed=None):
        if not computer:
            self.y += direction * self.dy
        else:
            if ball_speed[0] > 0 and ball_pos[0] < self.x:
                if time.time() > self.next_fail_decision_T:
                    if random.random() <= self.P_AI_fail:
                        self.AI_on_after = time.time() + self.T_AI_fail
                    self.next_fail_decision_T = time.time() + self.T_AI_fail
                if time.time() > self.AI_on_after:
                    speed = 0
                else:
                    speed = self.dy
                if ball_pos[1] < self.y:
                    self.y += -speed
                elif ball_pos[1] > self.y + self.h:
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