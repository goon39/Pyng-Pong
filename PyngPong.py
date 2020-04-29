# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:16:22 2020

@author: reill
"""

import pygame
import random
import sys
import os
import inspect
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

    text_font = pygame.font.SysFont(None, fs, bold=False)
    if x + w  > mouse[0] > x and y + h > mouse[1] > y:
        textSurf, textRect = text_objects(msg, text_font, atc)
        text_w = textSurf.get_width()  # TODO: Update to textRect.w/h
        text_h = textSurf.get_height()
        #pygame.draw.rect(screen, ac, (x, y, text_w, text_h))
       # pygame.draw.rect(screen, ac, (x, y, text_w, text_h))
        if click[0] == 1 and action != None:
            if len(inspect.getfullargspec(action).args) == 1:
                action(msg)
            else:
                action()
    else:
        textSurf, textRect = text_objects(msg, text_font, itc)
        text_w = textSurf.get_width()
        text_h = textSurf.get_height()
        #pygame.draw.rect(screen, ic, (x, y, text_w, text_h))

    textRect.center = ( (x + (text_w/2)), (y + (text_h/2)) )
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

        button('Play', SW - len('Play') * 24, SH + titleRect.h + 20, len('Play') * 48, 48, BLACK, WHITE, 96, action=game_loop)
        button('Options', SW - len('Options') * 24, SH + titleRect.h + 100, len('Options') * 48, 48, BLACK, WHITE, 96, action=option_menu)
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
        optRect.w = optSurf.get_width()
        optRect.x = 10
        optRect.centery = titleRect.y + titleRect.h + 100
        screen.blit(optSurf, optRect)
        
        button_width = (2 * SW - (optRect.w + optRect.x)) / len(options['Color'])

        if inputs['Color'] == 'Green':
            button('Green', optRect.x + optRect.w + 10, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, itc=GREEN, atc=GREEN)
        else:
            button('Green', optRect.x + optRect.w + 10, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, itc=GREEN, atc=GREEN)

        if inputs['Color'] == 'White' or not inputs['Color']:
            button('White', optRect.x + optRect.w + button_width + 20, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, itc=WHITE, atc=BLACK)
        else:
            button('White', optRect.x + optRect.w + button_width + 20, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, itc=WHITE, atc=BLACK)       

        optSurf, optRect = text_objects('Difficulty', title_font, WHITE)
        optRect.w = optSurf.get_width()
        optRect.x = 10
        optRect.centery = 2 * (titleRect.y + titleRect.h + 100)
        screen.blit(optSurf, optRect)

        button_width = (2 * SW - (optRect.w + optRect.x)) / len(options['Difficulty'])

        if inputs['Difficulty'] == 'Easy':
            button('Easy', optRect.x + optRect.w + 10, optRect.y, optRect.w, optRect.h, BLACK, WHITE, 48, action=input_update)
        else:
            button('Easy', optRect.x + optRect.w + 10, optRect.y, optRect.w, optRect.h, WHITE, BLACK, 48, action=input_update, itc=WHITE, atc=BLACK)

        if inputs['Difficulty'] == 'Hard':
            button('Hard', optRect.x + optRect.w + 2 * button_width + 30, optRect.y, optRect.w, optRect.h, BLACK, WHITE, 48, action=input_update)
        else:
            button('Hard', optRect.x + optRect.w + 2 * button_width + 30, optRect.y, optRect.w, optRect.h, WHITE, BLACK, 48, action=input_update, itc=WHITE, atc=BLACK)

        if inputs['Difficulty'] == 'Normal' or not inputs['Difficulty']:
            # msg, x, y, w, h, ic, ac, fs, itc=WHITE, atc=BLACK, action=None
            button('Normal', optRect.x + optRect.w + button_width + 20, optRect.y, optRect.w, optRect.h, BLACK, WHITE, 48, action=input_update)
        else:
            button('Normal', optRect.x + optRect.w + button_width + 20, optRect.y, optRect.w, optRect.h, WHITE, BLACK, 48, action=input_update, itc=WHITE, atc=BLACK)

        button('Back', SW - 50, optRect.y + optRect.h + 50, 100, 50, BLACK, WHITE, 48, action=start_menu)
        

#        for opt, o in enumerate(['Color', 'Difficulty']):
#            optSurf, optRect = text_objects(opt, title_font, WHITE)
#            optRect.w = 2 * SW / (len(options[opt]) + 1)
#            optRect.centerx = 10
#            optRect.centery = (o + 1) * (titleRect.bottom_left) + 10
#            screen.blit(optSurf, optRect)
#            for value, v in enumerate(options[opt]):
#                if value != 'Green':
#                    valueSurf, valueRect = text_objects(value, title_font, WHITE)
#                    button(value, (v + 1) * optRect.w + 10, optRect.y, optRect.w, optRect.h, BLACK, WHITE
#                else:
#                    valueSurf, valueRect = text_objects(value, title_font, GREEN)
#                valueRect.w = optRect.w
#                valueRect.centerx = (v + 1) * optRect.w + 10
#                valueRect.centery = optRect.centery
#                screen.blit(valueSurf, valueRect)
                
       # button('Play', SW, SH + titleRect.h * 2, 150, 50, BLACK, WHITE, 48, action=game_loop)
      #  button('Options', SW - (150/2), SH + 200, 150, 50, BLACK, WHITE, 48, action=option_menu)
        pygame.display.update()
        clock.tick(15)


def input_update(value):

    for key in options.keys():
        if value in options[key]:
            inputs[key] = value
                        


def game_loop():

    player = Paddle(20, SH - 18, 6, 36, inputs)
    computer = Paddle(SCREEN_WIDTH - 20, SH - 18, 6, 36, inputs)
    ball = Ball(SW, SH, 6, 6, inputs)
    
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


def main():

    start_menu()


if __name__ == "__main__":
    main()