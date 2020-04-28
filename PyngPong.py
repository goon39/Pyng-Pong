# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:16:22 2020

@author: reill
"""

import pygame
import random
import sys
import os
from Paddle import Paddle
from Ball import Ball


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (57, 255, 20)

pygame.init()
pygame.font.init()

pd = pygame.display.Info()
SCREEN_WIDTH = pd.current_w - 200
SW = SCREEN_WIDTH / 2
SCREEN_HEIGHT = pd.current_h - 100
SH = SCREEN_HEIGHT / 2

type_font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 120)
over_font = pygame.font.SysFont(None, 200)
title_font = pygame.font.SysFont(None, 160)

#Option menu inputs
options = {'Color': ['White', 'Green'], 
           'Difficulty': ['Easy', 'Normal', 'Hard'],
           }
inputs = {'Color': None,
          'Difficulty': None}

#TODO: Add sound during movement
pygame.mixer.init()

pygame.display.set_caption('Pyng-Pong')
clock = pygame.time.Clock()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((pd.current_w / 2 - SW), (pd.current_h / 2 - SH))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)  # TODO: Resizable window

def text_objects(text, font_obj, color, antialias=True):
    textSurf = font_obj.render(text, antialias, color)
    return textSurf, textSurf.get_rect()


def button(msg, x, y, w, h, ic, ac, fs, itc=WHITE, atc=BLACK, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    text = pygame.font.SysFont("Courier", fs, bold=False)
    if x + w  > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        textSurf, textRect = text_objects(msg, text, atc)
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
        textSurf, textRect = text_objects(msg, text, itc)

    textRect.center = ( (x + (w/2)), (y + (h/2)) )
    screen.blit(textSurf, textRect)


def start_menu():

    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start = False
                    pygame.quit()
                    sys.exit()
        screen.fill(BLACK)
        titleSurf, titleRect = text_objects('PONG!', title_font, WHITE)
        titleRect.centerx = SW
        titleRect.centery = SH
        screen.blit(titleSurf, titleRect)

        button('Play', SW, SH + titleRect.getheight()*2, 150, 50, BLACK, WHITE, 48, action=game_loop)
        button('Options', SW - (150/2), SH + 200, 150, 50, BLACK, WHITE, 48, action=option_menu)
        pygame.display.update()
        clock.tick(15)


def option_menu():

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = False
                    pygame.quit()
                    sys.exit()
        screen.fill(BLACK)
        titleSurf, titleRect = text_objects('Options', title_font, WHITE)
        titleRect.centerx = SW
        titleRect.centery = titleRect.h / 2
        screen.blit(titleSurf, titleRect)

        optSurf, optRect = text_objects('Color', title_font, WHITE)
        optRect.w = 2 * SW / (len(options['Color']) + 1)
        optRect.centerx = 10
        optRect.centery = titleRect.bottom_left + 10
        screen.blit(optSurf, optRect)

        if inputs['Color'] == 'Green':
            button('Green', optRect.x + optRect.w + 10, optRect.y, optRect.w, optRect.h, BLACK, WHITE, 48, itc=GREEN, atc=GREEN)
        else:
            # msg, x, y, w, h, ic, ac, fs, itc=WHITE, atc=BLACK, action=None
            button('White', optRect.x + optRect.w + 10, optRect.y, optRect.w, optRect.h, BLACK, WHITE, 48)

        optSurf, optRect = text_objects('Difficulty', title_font, WHITE)
        optRect.w = 2 * SW / (len(options['Difficulty']) + 1)
        optRect.centerx = 10
        optRect.centery = titleRect.bottom_left + 10
        screen.blit(optSurf, optRect)

        if inputs['Difficulty'] == 'Easy':
            button('Green', optRect.x + optRect.w + 10, optRect.y, optRect.w, optRect.h, BLACK, WHITE, 48, itc=GREEN, atc=GREEN)
        else:
            # msg, x, y, w, h, ic, ac, fs, itc=WHITE, atc=BLACK, action=None
            button('White', optRect.x + optRect.w + 10, optRect.y, optRect.w, optRect.h, BLACK, WHITE, 48)
        

        for opt, o in enumerate(['Color', 'Difficulty']):
            optSurf, optRect = text_objects(opt, title_font, WHITE)
            optRect.w = 2 * SW / (len(options[opt]) + 1)
            optRect.centerx = 10
            optRect.centery = (o + 1) * (titleRect.bottom_left) + 10
            screen.blit(optSurf, optRect)
            for value, v in enumerate(options[opt]):
                if value != 'Green':
                    valueSurf, valueRect = text_objects(value, title_font, WHITE)
                    button(value, (v + 1) * optRect.w + 10, optRect.y, optRect.w, optRect.h, BLACK, WHITE
                else:
                    valueSurf, valueRect = text_objects(value, title_font, GREEN)
                valueRect.w = optRect.w
                valueRect.centerx = (v + 1) * optRect.w + 10
                valueRect.centery = optRect.centery
                screen.blit(valueSurf, valueRect)
                
       # button('Play', SW, SH + titleRect.h * 2, 150, 50, BLACK, WHITE, 48, action=game_loop)
      #  button('Options', SW - (150/2), SH + 200, 150, 50, BLACK, WHITE, 48, action=option_menu)
        pygame.display.update()
        clock.tick(15)    


def game_loop():

    player = Paddle(20, SH - 18, 6, 36)
    computer = Paddle(SCREEN_WIDTH - 20, SH - 18, 6, 36)
    ball = Ball(SW, SH, 6, 6)
    
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

        playerRect = player.draw(screen)
        computerRect = computer.draw(screen)
        ballRect = ball.draw(screen)

        p_scoreSurf, p_scoreRect = text_objects(str(player.score), score_font, WHITE)
        p_scoreRect.centerx = SW / 2
        p_scoreRect.centery = 36
        screen.blit(p_scoreSurf, p_scoreRect)

        c_scoreSurf, c_scoreRect = text_objects(str(computer.score), score_font, WHITE)
        c_scoreRect.centerx = 0.75 * SCREEN_WIDTH
        c_scoreRect.centery = 36
        screen.blit(c_scoreSurf, c_scoreRect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.update(-1, SCREEN_HEIGHT)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.update(1, SCREEN_HEIGHT)

        ball.update(SCREEN_HEIGHT)
        
        computer.update(0, SCREEN_HEIGHT, ball=ball)

        if state == 'start':
            startSurf, startRect = text_objects('Press ENTER to start', type_font, WHITE)
            startRect.centerx = SW
            startRect.centery = 52
            screen.blit(startSurf, startRect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = 'serve'
        elif state == 'serve':
            ball.reset()
            player.reset()
            computer.reset()
            if ball.last_score not in [0, 1]:
                direction = random.choice([-1, 1])
            elif ball.last_score == 0:
                direction = 1
            else:
                direction = -1
            ball.serve(direction)
            state = 'play'
        elif state == 'play':
            if ball.score(SCREEN_WIDTH, player, computer):
                if player.score == 1 or computer.score == 1:
                    state = 'over'
                else:
                    state = 'start'
                ball.x = -ball.w
                ball.y = -ball.h
            else:
                ball.collide_check(playerRect)
                ball.collide_check(computerRect)
        elif state == 'over':
            if player.score == 10:
                overSurf, overRect = text_objects('Player wins!', over_font, WHITE)
            else:
                overSurf, overRect = text_objects('Computer wins!', over_font, WHITE)
            overRect.centerx = SW
            overRect.centery = SH
            screen.blit(overSurf, overRect)
            replaySurf, replayRect = text_objects('Press ENTER to replay', type_font, WHITE)
            replayRect.centerx = SW
            replayRect.centery = 52
            screen.blit(replaySurf, replayRect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = 'start'
                    player.score = 0
                    computer.score = 0
            
                        
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()