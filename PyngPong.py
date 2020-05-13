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

fps = 60
delta = clock.tick(fps) / 1000

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

        print_to_screen('PONG!', title_font, SW, SH, color=WHITE)

        button('Play', SW - len('Play') * 24, SH + 100, len('Play') * 48, 48, BLACK, WHITE, 96, action=game_loop)
        button('Options', SW - len('Options') * 24, SH + 180, len('Options') * 48, 48, BLACK, WHITE, 96, action=option_menu)
        pygame.display.update()
        clock.tick(60)


def option_menu():

    menu = True
    while menu:
        menu = game_exit()

        screen.fill(BLACK)

        opt_width, opt_height = title_font.size('Options')
        print_to_screen('Options', title_font, SW, 100, color=WHITE)

        color_width, color_height = title_font.size('Color')
        print_to_screen('Color', title_font, 10 + color_width / 2, opt_height + 100, color=WHITE)

        button_width = (2 * SW - (60 + color_width)) / len(options['Color'])

        if inputs['Color'] == 'Green':
            #button('Green', optRect.x + optRect.w + 10, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, itc=GREEN, atc=GREEN, action=input_update)
            button('Green', 20 + color_width, opt_height + 100, button_width, color_height, WHITE, BLACK, 48, itc=GREEN, atc=GREEN, action=input_update)
        else:
            #button('Green', optRect.x + optRect.w + 10, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, itc=GREEN, atc=GREEN, action=input_update)
            button('Green', 20 + color_width, opt_height + 100, button_width, color_height, BLACK, WHITE, 48, itc=GREEN, atc=GREEN, action=input_update)

        if inputs['Color'] == 'White' or not inputs['Color']:
            #button('White', optRect.x + optRect.w + button_width + 20, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, itc=BLACK, atc=WHITE, action=input_update)
            button('White', 2 * color_width + 10, opt_height + 100, button_width, color_height, WHITE, BLACK, 48, itc=BLACK, atc=WHITE, action=input_update)
        else:
            #button('White', optRect.x + optRect.w + button_width + 20, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, itc=WHITE, atc=BLACK, action=input_update)
            button('White', 2 * color_width + 10, opt_height + 100, button_width, color_height, BLACK, WHITE, 48, itc=WHITE, atc=BLACK, action=input_update)

        diff_width, diff_height = title_font.size('Difficulty')
        print_to_screen('Difficulty', title_font, 10 + diff_width / 2, opt_height + color_height + 200, color=WHITE)

        button_width = (2 * SW - (80 + diff_width)) / len(options['Difficulty'])

        if inputs['Difficulty'] == 'Easy':
            #button('Easy', optRect.x + optRect.w + 10, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, action=input_update, itc=BLACK, atc=WHITE)
            button('Easy', 20 + diff_width, opt_height + color_height + 200, button_width, diff_height, WHITE, BLACK, 48, action=input_update, itc=BLACK, atc=WHITE)
        else:
            #button('Easy', optRect.x + optRect.w + 10, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, action=input_update, itc=WHITE, atc=BLACK)
            button('Easy', 20 + diff_width, opt_height + color_height + 200, button_width, diff_height, BLACK, WHITE, 48, action=input_update, itc=WHITE, atc=BLACK)

        if inputs['Difficulty'] == 'Normal' or not inputs['Difficulty']:
            #button('Normal', optRect.x + optRect.w + button_width + 20, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, action=input_update, itc=BLACK, atc=WHITE)
            button('Normal', 30 + diff_width + button_width, opt_height + color_height + 200, button_width, diff_height, WHITE, BLACK, 48, action=input_update, itc=BLACK, atc=WHITE)
        else:
            #button('Normal', optRect.x + optRect.w + button_width + 20, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, action=input_update, itc=WHITE, atc=BLACK)
            button('Normal', 30 + diff_width + button_width, opt_height + color_height + 200, button_width, diff_height, BLACK, WHITE, 48, action=input_update, itc=WHITE, atc=BLACK)

        if inputs['Difficulty'] == 'Hard':
            #button('Hard', optRect.x + optRect.w + 2 * button_width + 30, optRect.y, button_width, optRect.h, WHITE, BLACK, 48, action=input_update, itc=BLACK, atc=WHITE)
            button('Hard', 40 + diff_width + 2 * button_width, opt_height + color_height + 200, button_width, diff_height, WHITE, BLACK, 48, action=input_update, itc=BLACK, atc=WHITE)
        else:
            #button('Hard', optRect.x + optRect.w + 2 * button_width + 30, optRect.y, button_width, optRect.h, BLACK, WHITE, 48, action=input_update, itc=WHITE, atc=BLACK)
            button('Hard', 40 + diff_width + 2 * button_width, opt_height + color_height + 200, button_width, diff_height, BLACK, WHITE, 48, action=input_update, itc=WHITE, atc=BLACK)


        #button('Back', SW - 50, optRect.y + optRect.h + 50, 100, 50, BLACK, WHITE, 48, action=start_menu)
        back_width, back_height = pygame.font.SysFont(None, 48).size('Back')
        button('Back', SW - back_width / 2, SCREEN_HEIGHT - back_height - 10, back_width, back_height, BLACK, WHITE, 48, action=start_menu)
        
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


def print_to_screen(msg, font, cx, cy, color=None):

    if not color:
        if inputs['Color'] == 'Green':
            mySurf, myRect = text_objects(msg, font, GREEN)
        else:
            mySurf, myRect = text_objects(msg, font, WHITE)
    else:
        mySurf, myRect = text_objects(msg, font, color)
    myRect.center = (cx, cy)
    screen.blit(mySurf, myRect)


def update_and_draw(player, computer, ball, keys):

    player.draw(screen)
    computer.draw(screen)
    ball.draw(screen)
    
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.update(-1, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), delta)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.update(1, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), delta)

    wall_bound = ball.update(delta, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    if wall_bound:
        wall_hit.play()
        wall_bound = False 

    computer.update(0, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), delta, ball=ball)
    

def start_state(keys):

    print_to_screen('Press ENTER to start', type_font, SW, 52)

    if keys[pygame.K_RETURN]:
        state = 'serve'
    else:
        state = 'start'
    return state


def serve_state(ball, player, computer):

    state = 'serve'
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
    return state


def play_state(ball, player, computer):

    state = 'play'
    if ball.score(player, computer):
        score_sound.play()
        if player.score == 10 or computer.score == 10:
            state = 'over'
        else:
            state = 'start'
    else:
        collide = ball.collide_check(player)
        if collide:
            paddle_hit.play()
            collide = False
        
        collide = ball.collide_check(computer)
        if collide:
            paddle_hit.play()
            collide = False
    return state


def over_state(ball, player, computer, keys):

    state = 'over'
    if player.score == 10:
        print_to_screen(screen, 'Player wins!', over_font, SW, SH)
    elif computer.score == 10:
        print_to_screen(screen, 'Computer wins!', over_font, SW, SH)

    print_to_screen(screen, 'Press ENTER to replay', type_font, SW, 52)

    if keys[pygame.K_RETURN]:
        state = 'start'
        player.score = 0
        computer.score = 0
    return state


def game_loop():

    player = Paddle((20, SH - 18, 6, 36), inputs)
    computer = Paddle((SCREEN_WIDTH - 20, SH - 18, 6, 36), inputs)
    ball = Ball((SW - 3, SH - 3, 6, 6), inputs)
    
    state = 'start'
    running = True
    while running:
        running = game_exit()

        screen.fill(BLACK)

        keys = pygame.key.get_pressed()

        update_and_draw(player, computer, ball, keys)

        print_to_screen(str(player.score), score_font, SW/2, 36)
        print_to_screen(str(computer.score), score_font, 0.75*SCREEN_WIDTH, 36)

        if state == 'start':
            state = start_state(keys)
        elif state == 'serve':
            state = serve_state(ball, player, computer)
        elif state == 'play':
            play_state(ball, player, computer)
        elif state == 'over':
            over_state(ball, player, computer, keys)

        pygame.display.update()
        #pygame.display.flip()
        clock.tick(60)


def main():

    start_menu()


if __name__ == "__main__":
    main()