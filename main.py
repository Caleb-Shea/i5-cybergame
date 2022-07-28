##!/usr/bin/env python # for some reason that I don't care to look into, this breaks on my computer
# coding=utf-8
"""
A wargaming simulation made by the i5 cyber element, with inspiration from the i5 intel element.

By: i5 Cyber element
"""

import datetime as dt
import pygame as pyg
import random
import math
import os

from earth_system import EarthSystem
from game_info import game_info
from fullmenu import FullMenu
from helper_func import *
from assets import *
from hud import HUD


def render_bg(bg_stars, bg_sprites):
    """
    Description: Render a faux starscape.
    Parameters:
        bg_stars [list] -> A list containing data for each star
        bg_sprites [list] -> A list containing data for each moving object
    Returns: None
    """
    window = pyg.display.get_surface()
    WIDTH, HEIGHT = pyg.display.get_window_size()

    for star in bg_stars:
        # Only render stars that are on screen
        if 0 < star['pos'][0] < WIDTH and 0 < star['pos'][1] < HEIGHT:
            # Draw each star using just one corner so it looks more realistic
            if star['corner'] == 1:
                pyg.draw.circle(window, colors['starwhite'], star['pos'], star['size'], draw_top_left=True)
            elif star['corner'] == 2:
                pyg.draw.circle(window, colors['starwhite'], star['pos'], star['size'], draw_top_right=True)
            elif star['corner'] == 3:
                pyg.draw.circle(window, colors['starwhite'], star['pos'], star['size'], draw_bottom_left=True)
            else:
                pyg.draw.circle(window, colors['starwhite'], star['pos'], star['size'], draw_bottom_right=True)

    for sprite in bg_sprites:
        if sprite['type'] == 'shooting_star':
            # Draw multiple circles to mimic a tail
            # Use lifetime so it fades away naturally
            for i in range(sprite['lifetime']*2):
                pos = sprite['pos'] - 0.05*i*sprite['vel']
                pyg.draw.circle(window, colors['starwhite'], pos, sprite['size'])

def new_shooting_star():
    """
    Description: Create a new shooting star somewhere near the viewing area.
    Parameters: None
    Returns:
        [dict] -> A dict holding the pos and vel of a new shooting star.
    """
    # Get the dimensions of the screen
    WIDTH, HEIGHT = pyg.display.get_window_size()
    # Find a position
    x = random.randint(-WIDTH, WIDTH*2)
    y = random.randint(-HEIGHT, HEIGHT*2)

    # Moves some farther away and brings some closer
    dist = random.random() + 0.6
    # Size, based on the distance
    size = 1.5*dist + random.random()

    # Create a random velocity vector
    vel = pyg.math.Vector2()
    vel.x = random.randint(10, 15) * random.choice([-1, 1]) * size
    vel.y = random.randint(10, 15) * random.choice([-1, 1]) * size

    # Give each star it's own lifetime
    lifetime = random.randint(15, 25)

    return {'type': 'shooting_star', 'pos': [x, y], 'vel': vel,
            'size': size, 'dist': dist, 'lifetime': lifetime}

def scroll_the_earth(earth_sys, target, bg_stars):
    """
    Description: Scroll the screen until the earth is at the center.
    Parameters:
        earth_sys [EarthSystem()] -> A reference to the EarthSystem instance
        target [tuple] -> Coords of the target point
        bg_stars [list] -> A list that contains the bg stars information.
    Returns:
        [bool] -> Return true if the earth has reached the center of the screen
    """

    # Calculate offsets
    x_offset = earth_sys.nodes['EARTH']['rect'].centerx - target[0]
    y_offset = earth_sys.nodes['EARTH']['rect'].centery - target[1]

    # Due to rounding errors in rect movement, we need to add 20 to the offset
    x_offset += math.copysign(20, x_offset)
    y_offset += math.copysign(20, y_offset)

    # Use a sigmoid function to collapse distances to a -1-1 range
    x_sig = -2/(1 + math.e**(-0.001 * x_offset)) + 1
    y_sig = -2/(1 + math.e**(-0.001 * y_offset)) + 1 # For performance, 3 could also work in place of e

    # Convert those values to amounts to move earth by
    x_move = x_sig * 100
    y_move = y_sig * 100

    # Move everything
    # We use 20 due to rounding errors somewhere. IDK tbh
    if abs(x_offset) > 20 or abs(y_offset) > 20:
        for node in earth_sys.nodes.values():
            node['rect'].move_ip(x_move, y_move)

        for star in bg_stars:
            star['pos'][0] += x_move * .06*star['dist']
            star['pos'][1] += y_move * .06*star['dist']

        return False
    else:
        return True

def main():
    # Get references to the window and it's size
    window = pyg.display.get_surface()
    window_rect = window.get_rect()
    WIDTH, HEIGHT = pyg.display.get_window_size()

    # Audio
    ui_channel = pyg.mixer.find_channel()
    soundtrack_channel = pyg.mixer.find_channel()

    # full_menu is an object that is used for Earth's menu
    full_menu = FullMenu(ui_channel)

    # This holds all the information needed for earth's system
    earth_sys = EarthSystem()

    # The HUD
    hud = HUD()

    # Create the background star effect
    bg_stars = []
    for i in range(10000):
        # Coords
        x = random.randint(-WIDTH, 2 * WIDTH)
        y = random.randint(-HEIGHT, 2 * HEIGHT)
        # Moves some stars farther away and brings some closer
        dist = random.random() + 0.5
        # Size, based on the distance
        size = 1.5*dist + random.random()
        # Which corner of the circle to render (creats a more interesting shape)
        corner = random.randint(1, 4)

        bg_stars.append({'pos': [x, y], 'dist': dist, 'size': size, 'corner': corner})

    # This is for everything that is part of the background but isn't a star
    bg_sprites = []

    # Trackers
    done_scrolling = True
    is_paused = False
    got_payday = False

    # Timekeeping
    clock = pyg.time.Clock()
    FPS = 60

    date = dt.date.today()

    # Custom events
    new_day = pyg.USEREVENT + 1
    pyg.time.set_timer(new_day, 5000) # 5 sec
    new_news_event = pyg.USEREVENT + 2
    pyg.time.set_timer(new_news_event, 2000) # 2 sec
    new_soundtrack = pyg.USEREVENT + 3
    pyg.time.set_timer(new_soundtrack, 300000) # 5 min
    add_shooting_star = pyg.USEREVENT + 4
    pyg.time.set_timer(add_shooting_star, 7000) # 7 sec

    while True:
        # Pause menu
        if is_paused:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    terminate()

                elif event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_BACKQUOTE:
                        terminate()

                elif event.type == pyg.KEYUP:
                    if event.key == pyg.K_ESCAPE:
                        if hud.p_page != None:
                            hud.p_page = None
                        else:
                            is_paused = False

                elif event.type == pyg.MOUSEBUTTONDOWN:
                    ui_channel.queue(audio['down_click'])

                elif event.type == pyg.MOUSEBUTTONUP:
                    ui_channel.queue(audio['up_click'])

                    # Main menu navigation
                    if hud.p_page == None:
                        if hud.p_resume_rect.collidepoint(event.pos):
                            is_paused = False

                        elif hud.p_eq_rect.collidepoint(event.pos):
                            pass

                        elif hud.p_credits_rect.collidepoint(event.pos):
                            hud.p_page = 'credits'

                        elif hud.p_options_rect.collidepoint(event.pos):
                            hud.p_page = 'options'

                        elif hud.p_info_rect.collidepoint(event.pos):
                            hud.p_page = 'info'

                        elif hud.p_exit_rect.collidepoint(event.pos):
                            terminate()

            # Rendering
            window.fill(colors['space'])
            render_bg(bg_stars, bg_sprites)

            earth_sys.spin()
            earth_sys.render()

            # Render essential hud elements
            hud.render_time(date)
            hud.render_reputation()
            hud.render_cash()
            hud.ticker.render()

            hud.render_pause_menu()

            # Update the screen
            pyg.display.flip()
            clock.tick(FPS)

            # Don't run the rest of the while loop
            continue

        # Handle all events
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                terminate()

            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_BACKQUOTE:
                    terminate()

                # Testing purposes
                elif event.key == pyg.K_SPACE:
                    game_info['cash'] += 900000000000000
                    game_info['reputation'] += 20
                    game_info['num_personnel'] += 200
                    game_info['Staff Assignments']['Unassigned'] += 100
                    game_info['Staff Assignments']['Cyber'] += 50
                    game_info['Staff Assignments']['Intel'] += 20
                    game_info['Staff Assignments']['Ops'] += 30
                    game_info['Staff Assignments']['Acquisitions'] += 10

                # Scroll to the earth
                elif event.key == pyg.K_e:
                    done_scrolling = False

            elif event.type == pyg.KEYUP:
                if event.key == pyg.K_ESCAPE:
                    # FullMenu --> EarthSystem --> Pause Menu
                    if full_menu.cur_tab == None:
                        is_paused = True
                    else:
                        full_menu.cur_tab = None

                    # Deselect all nodes
                    earth_sys.hovered = None
                    earth_sys.selected = None

            elif event.type == pyg.MOUSEBUTTONDOWN:
                # Play sfx only when the left or right button is clicked
                if event.button in [1, 3]:
                    if not ui_channel.get_busy():
                        ui_channel.play(audio['down_click'])
                full_menu.update(event.button)

            elif event.type == pyg.MOUSEBUTTONUP:
                # Play sfx only when the left or right button is clicked
                if event.button in [1, 3]:
                    # Only play the up_click sound after the down_click sound
                    if ui_channel.get_sound() == audio['down_click']:
                        ui_channel.queue(audio['up_click'])
                if full_menu.cur_tab == None:
                    earth_sys.update(True) # We pass True because we are calling update() due to a mouse event

                # Back arrow
                if hud.arrow_rect.collidepoint(event.pos):
                    earth_sys.selected = None

                # # Ticker
                # if hud.ticker.rect.collidepoint(event.pos):
                #     full_menu.cur_tab = 'EVENTS'

            # --- Custom event handling ---
            elif event.type == new_day:
                date = date + dt.timedelta(days=1)

            elif event.type == new_news_event:
                hud.ticker.new_event(date)

            elif event.type == new_soundtrack:
                soundtrack_channel.queue(audio[f'soundtrack{random.randint(1, 1)}'])

            elif event.type == add_shooting_star:
                bg_sprites.append(new_shooting_star())

        # Handle held down keys and mouse movement
        event_keys = pyg.key.get_pressed()
        m_pressed = pyg.mouse.get_pressed()
        m_rel = pyg.mouse.get_rel()
        # Move all the nodes/stars if the mouse is dragged
        if m_pressed[0] and full_menu.cur_tab == None:
            for node in earth_sys.nodes.values(): # Move nodes
                node['rect'].x += m_rel[0]
                node['rect'].y += m_rel[1]
            for obj in bg_stars + bg_sprites: # Move bg objets, but less
                obj['pos'][0] += m_rel[0] * .06*obj['dist']
                obj['pos'][1] += m_rel[1] * .06*obj['dist']

        # Determine if the fullmenu should be rendered
        # If we have selected a node that has a menu
        if earth_sys.selected in ['ACQUISITIONS', 'CYBER', 'INTEL', 'OPS',
                                  'PERSONNEL']:
            # And there isn't another tab already selected
            if full_menu.cur_tab == None:
                # Set the cur_tab
                full_menu.cur_tab = earth_sys.selected

                # Update hovering trackers
                earth_sys.hovered = None
        else:
            # If we don't have a selected node, we don't render the fullmenu
            full_menu.cur_tab = None

        # If we click on the earth locator, scroll to the earth
        m_pos = pyg.mouse.get_pos()
        if hud.e_loc_rect.collidepoint(m_pos) and m_pressed[0]:
            done_scrolling = False

        # If we click on the earth, move the earth so it's in the open area
        if earth_sys.selected == 'EARTH':
            done_scrolling = False

        # Keep scrolling until the earth is centered
        if not done_scrolling:
            # If the earth is selected, scroll to the right of the screen to
            # make room for the vignette menu
            if earth_sys.selected == 'EARTH':
                target = (3/5*WIDTH, HEIGHT/2)
            else:
                target = (WIDTH/2, HEIGHT/2)

            done_scrolling = scroll_the_earth(earth_sys, target, bg_stars)

            # Cancel scroll if we click
            if m_pressed[0] and (m_rel[0]>0 or m_rel[1]>0):
                done_scrolling = True

        # Update the shooting stars
        for sprite in bg_sprites:
            if sprite['type'] == 'shooting_star':
                if sprite['lifetime'] == 0:
                    bg_sprites.remove(sprite)

                sprite['pos'][0] += sprite['vel'][0]
                sprite['pos'][1] += sprite['vel'][1]

                sprite['lifetime'] -= 1

        # Payday is the first of every month
        if date.day == 1 and not got_payday:
            game_info['budget'] = 10000 * game_info['reputation']
            game_info['cash'] += game_info['budget']
            got_payday = True
        # Reset tracker
        elif date.day == 2:
            got_payday = False

        # Render the background
        window.fill(colors['space'])
        render_bg(bg_stars, bg_sprites)

        # Update the earth system
        if full_menu.cur_tab == None:
            earth_sys.update()
        else:
            earth_sys.spin()
        earth_sys.render()

        # If the earth is selected and we're on the main screen, render the menu
        if earth_sys.selected == 'EARTH':
            hud.render_vignette('left')
            hud.render_earth_menu()

        # If the full menu is active, update/render it
        if full_menu.cur_tab != None:
            full_menu.update()
            full_menu.render()

        # Render HUD elements
        if earth_sys.selected not in [None, 'EARTH']:
            hud.render_back_arrow()
        if earth_sys.hovered != None:
            hud.render_hover_menu(earth_sys.get_hovered())
        if not window_rect.colliderect(earth_sys.nodes['EARTH']['rect']):
            hud.render_earth_loc(earth_sys.nodes['EARTH']['rect'].center)
        hud.render_time(date)
        hud.render_personnel()
        hud.render_cash()
        hud.render_reputation()
        hud.ticker.render()

        # Update the display, but don't exceed FPS
        pyg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    # Initalize pygame and create a window
    pyg.init()
    pyg.display.set_caption("i5 CYBERGAME")
    pyg.display.set_mode(flags=pyg.HWSURFACE | pyg.FULLSCREEN | pyg.DOUBLEBUF)

    # Start the program
    main()