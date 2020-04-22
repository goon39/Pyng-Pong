# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:16:22 2020

@author: reill
"""

import pygame
import random
import sys
from Paddle import Paddle
from Ball import Ball


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.font.init()

pd = pygame.display.Info()
SCREEN_WIDTH = pd.current_w - 200
SW = SCREEN_WIDTH / 2
SCREEN_HEIGHT = pd.current_h - 100
SH = SCREEN_HEIGHT / 2

#TODO: Add sound during movement
pygame.mixer.init()

pygame.display.set_caption('Pyng-Pong')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)  # TODO: Resizable window

def text_objects(text, font_obj, color):
    textSurf = font_obj.render(text, True, color)
    return textSurf, textSurf.get_rect()


def main():

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)

        player = Paddle(20, SH - 18, 6, 36)
        computer = Paddle(SCREEN_WIDTH - 20, SH - 18, 6, 36)
        ball = Ball(SW, SH, 6, 6)

        player.draw(screen)
        computer.draw(screen)
        ball.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()