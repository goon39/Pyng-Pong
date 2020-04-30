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

pygame.mixer.init()
paddle_hit = pygame.mixer.Sound(os.path.join('.' , 'sound', 'ball_to_paddle.wav'))
score_sound = pygame.mixer.Sound(os.path.join('.', 'sound', 'score.wav'))
wall_hit = pygame.mixer.Sound(os.path.join('.', 'sound', 'ball_to_wall.wav'))

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
        #text_w = textRect.w
        #text_h = textRect.h
        pygame.draw.rect(screen, ac, (x, y, w, h))
        #pygame.draw.rect(screen, ac, (x, y, text_w, text_h))
        if click[0] == 1 and action != None:
            if len(inspect.getfullargspec(action).args) == 1:
                action(msg)
            else:
                action()
    else:
        textSurf, textRect = text_objects(msg, text_font, itc)
        #text_w = textRect.w
        #text_h = textRect.h
        pygame.draw.rect(screen, ic, (x, y, w, h))
        #pygame.draw.rect(screen, ic, (x, y, text_w, text_h))

    textRect.center = ( (x + (w/2)), (y + (h/2)) )
    screen.blit(textSurf, textRect)


def start_menu():

    start = True
    while start:
        start = game_exit()

        screen.fill(BLACK)
        titleSurf, titleRect = text_objects('PONG!', title_font, WHITE)
        titleRect.centerx = SW
        titleRect.centery = SH
        screen.blit(titleSurf, titleRect)

        button('Play', SW - len('Play') * 24, SH + titleRect.h + 20, len('Play') * 48, 48, BLACK, WHITE, 96, action=game_loop)
        button('Options', SW - len('Options') * 24, SH + titleRect.h + 100, len('Options') * 48, 48, BLACK, WHITE, 96, action=option_menu)
        pygame.display.update()
        clock.tick(60)


def option_menu():

    menu = True
    while menu:
        menu = game_exit()

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
            button('Green', optRect.x + optRect.w + 10, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, itc=GREEN, atc=GREEN, action=input_update)
        else:
            button('Green', optRect.x + optRect.w + 10, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, itc=GREEN, atc=GREEN, action=input_update)

        if inputs['Color'] == 'White' or not inputs['Color']:
            button('White', optRect.x + optRect.w + button_width + 20, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, itc=BLACK, atc=WHITE, action=input_update)
        else:
            button('White', optRect.x + optRect.w + button_width + 20, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, itc=WHITE, atc=BLACK, action=input_update)       

        optSurf, optRect = text_objects('Difficulty', title_font, WHITE)
        optRect.w = optSurf.get_width()
        optRect.x = 10
        optRect.centery = 2 * (titleRect.y + titleRect.h + 100)
        screen.blit(optSurf, optRect)

        button_width = (2 * SW - (optRect.w + optRect.x)) / len(options['Difficulty'])

        if inputs['Difficulty'] == 'Easy':
            button('Easy', optRect.x + optRect.w + 10, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, action=input_update, itc=BLACK, atc=WHITE)
        else:
            button('Easy', optRect.x + optRect.w + 10, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, action=input_update, itc=WHITE, atc=BLACK)

        if inputs['Difficulty'] == 'Normal' or not inputs['Difficulty']:
            # msg, x, y, w, h, ic, ac, fs, itc=WHITE, atc=BLACK, action=None
            button('Normal', optRect.x + optRect.w + button_width + 20, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, action=input_update, itc=BLACK, atc=WHITE)
        else:
            button('Normal', optRect.x + optRect.w + button_width + 20, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, action=input_update, itc=WHITE, atc=BLACK)

        if inputs['Difficulty'] == 'Hard':
            button('Hard', optRect.x + optRect.w + 2 * button_width + 30, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, action=input_update, itc=BLACK, atc=WHITE)
        else:
            button('Hard', optRect.x + optRect.w + 2 * button_width + 30, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, action=input_update, itc=WHITE, atc=BLACK)


        button('Back', SW - 50, optRect.y + optRect.h + 50, 100, 50, BLACK, WHITE, 48, action=start_menu)
        
        pygame.display.update()
        clock.tick(60)


def input_update(value):

    for key in options.keys():
        if value in options[key]:
            inputs[key] = value


def game_exit():

    opt=True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            opt = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                opt = False
                pygame.quit()
                sys.exit()
    return opt


def game_loop():

    player = Paddle(20, SH - 18, 6, 36, inputs)
    computer = Paddle(SCREEN_WIDTH - 20, SH - 18, 6, 36, inputs)
    ball = Ball(SW, SH, 6, 6, inputs)
    
    state = 'start'
    running = True
    while running:
        running = game_exit()

        screen.fill(BLACK)

        playerRect = player.draw(screen)
        computerRect = computer.draw(screen)
        ballRect = ball.draw(screen)

        if inputs['Color'] == 'Green':
            p_scoreSurf, p_scoreRect = text_objects(str(player.score), score_font, GREEN)
        else:
            p_scoreSurf, p_scoreRect = text_objects(str(player.score), score_font, WHITE)
        p_scoreRect.centerx = SW / 2
        p_scoreRect.centery = 36
        screen.blit(p_scoreSurf, p_scoreRect)

        if inputs['Color'] == 'Green':
            c_scoreSurf, c_scoreRect = text_objects(str(computer.score), score_font, GREEN)
        else:
            c_scoreSurf, c_scoreRect = text_objects(str(computer.score), score_font, WHITE)
        c_scoreRect.centerx = 0.75 * SCREEN_WIDTH
        c_scoreRect.centery = 36
        screen.blit(c_scoreSurf, c_scoreRect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.update(-1, SCREEN_HEIGHT)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.update(1, SCREEN_HEIGHT)

        wall_bound = ball.update(SCREEN_HEIGHT)
        if wall_bound:
            wall_hit.play()
            wall_bound = False
        
        computer.update(0, SCREEN_HEIGHT, ball=ball)

        if state == 'start':
            if inputs['Color'] == 'Green':
                startSurf, startRect = text_objects('Press ENTER to start', type_font, GREEN)
            else:
                startSurf, startRect = text_objects('Press ENTER to start', type_font, WHITE)
            startRect.centerx = SW
            startRect.centery = 52
            screen.blit(startSurf, startRect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                state = 'serve'
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_RETURN:
#                    state = 'serve'
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
                score_sound.play()
                if player.score == 10 or computer.score == 10:
                    state = 'over'
                else:
                    state = 'start'
                ball.x = -ball.w
                ball.y = -ball.h
                ball.dx = 0
                ball.dy = 0
            else:
                collide = ball.collide_check(playerRect)
                if collide:
                    paddle_hit.play()
                    collide = False
                
                collide = ball.collide_check(computerRect)
                if collide:
                    paddle_hit.play()
                    collide = False
        elif state == 'over':
            if player.score == 10:
                if inputs['Color'] == 'Green':
                    overSurf, overRect = text_objects('Player wins!', over_font, GREEN)
                else:
                    overSurf, overRect = text_objects('Player wins!', over_font, WHITE)
            elif computer.score == 10:
                if inputs['Color'] == 'Green':
                    overSurf, overRect = text_objects('Computer wins!', over_font, GREEN)
                else:
                    overSurf, overRect = text_objects('Computer wins!', over_font, WHITE)
            overRect.centerx = SW
            overRect.centery = SH
            screen.blit(overSurf, overRect)
            
            if inputs['Color'] == 'Green':
                replaySurf, replayRect = text_objects('Press ENTER to replay', type_font, GREEN)
            else:
                replaySurf, replayRect = text_objects('Press ENTER to replay', type_font, WHITE)
            replayRect.centerx = SW
            replayRect.centery = 52
            screen.blit(replaySurf, replayRect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                state = 'start'
                player.score = 0
                computer.score = 0
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_RETURN:
#                    state = 'start'
#                    player.score = 0
#                    computer.score = 0
                                 
        pygame.display.update()
        clock.tick(60)


def main():

    start_menu()


if __name__ == "__main__":
    main()