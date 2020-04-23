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

type_font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 120)

#TODO: Add sound during movement
pygame.mixer.init()

pygame.display.set_caption('Pyng-Pong')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)  # TODO: Resizable window

def text_objects(text, font_obj, color, antialias=True):
    textSurf = font_obj.render(text, antialias, color)
    return textSurf, textSurf.get_rect()


def main():

    state = 'start'
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

        p_scoreSurf, p_scoreRect = text_objects(str(player.score), score_font, WHITE)
        p_scoreRect.centerx = SW / 2
        p_scoreRect.centery = 36
        screen.blit(p_scoreSurf, p_scoreRect)

        c_scoreSurf, c_scoreRect = text_objects(str(computer.score), score_font, WHITE)
        c_scoreRect.centerx = 0.75 * SCREEN_WIDTH
        c_scoreRect.centery = 36
        screen.blit(c_scoreSurf, c_scoreRect)

        if state == 'start':
            startSurf, startRect = text_objects('Press ENTER to start', type_font, WHITE)
            startRect.centerx = SW
            startRect.centery = 52
            screen.blit(startSurf, startRect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = 'serve'
        elif state == 'serve':
            if ball.last_score not in [0, 1]:
                direction = random.choice([-1, 1])
            elif ball.last_score == 0:
                direction = 1
            else:
                direction = -1
            ball.serve(direction)
            state = 'play'
        elif state == 'play':
            
                        
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()