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

from game_info import game_info
from fullmenu import FullMenu
from helper_func import *
from node_data import *
from node import Node
from assets import *
from hud import HUD


def init_nodes():
    """
    Description: Create a dictionary that contains all the nodes the program
                 needs.
    Parameters: None
    Returns:
        node_dict [dict] -> The dict with all the nodes
    """
    # Create all nodes from node_data.py
    earth_nodes = pyg.sprite.Group()
    [earth_nodes.add(Node(data)) for data in main_data]
    gssap_nodes = pyg.sprite.Group()
    [gssap_nodes.add(Node(data)) for data in gssap_data]
    iss_nodes = pyg.sprite.Group()
    [iss_nodes.add(Node(data)) for data in iss_data]
    milstar_nodes = pyg.sprite.Group()
    [milstar_nodes.add(Node(data)) for data in milstar_data]
    aehf_nodes = pyg.sprite.Group()
    [aehf_nodes.add(Node(data)) for data in aehf_data]
    gps_nodes = pyg.sprite.Group()
    [gps_nodes.add(Node(data)) for data in gps_data]
    sbirs_nodes = pyg.sprite.Group()
    [sbirs_nodes.add(Node(data)) for data in sbirs_data]

    # Once all nodes have been made, init phase two
    for node in earth_nodes:
        node.phase_two_init(earth_nodes)
    for node in gssap_nodes:
        node.phase_two_init(gssap_nodes)
    for node in iss_nodes:
        node.phase_two_init(iss_nodes)
    for node in milstar_nodes:
        node.phase_two_init(milstar_nodes)
    for node in aehf_nodes:
        node.phase_two_init(aehf_nodes)
    for node in gps_nodes:
        node.phase_two_init(gps_nodes)
    for node in sbirs_nodes:
        node.phase_two_init(sbirs_nodes)

    node_dict = {'EARTH': earth_nodes, 'GSSAP': gssap_nodes, 'ISS': iss_nodes,
                 'MILSTAR': milstar_nodes, 'AEHF': aehf_nodes, 'GPS': gps_nodes,
                 'SBIRS': sbirs_nodes,

                 # These are included because although they use a different menu
                 # system, we still need to clear the screen
                 'OPS': [], 'PERSONNEL': [], 'INTEL': [], 'CYBER': [],
                 'ACQUISITIONS': [], 'EVENTS': []}

    return node_dict

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

def scroll_the_earth(earth, target, all_nodes, bg_stars):
    """
    Description: Scroll the screen until the earth is at the center.
    Parameters:
        earth [Node] -> A reference to earth
        target [tuple] -> Coords of the target point
        all_nodes [dict] -> A dictionary that contains all the nodes
        bg_stars [list] -> A list that contains the bg stars information.
    Returns:
        [bool] -> Return true if the earth has reached the center of the screen
    """

    # Calculate offsets
    x_offset = earth.rect.centerx - target[0]
    y_offset = earth.rect.centery - target[1]

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
        for node in all_nodes['EARTH']:
            node.rect.move_ip(x_move, y_move)

        for star in bg_stars:
            star['pos'][0] += x_move * .06*star['dist']
            star['pos'][1] += y_move * .06*star['dist']

        return False
    else:
        return True

def main():
    # Get references to the window and it's size
    window = pyg.display.get_surface()
    WIDTH, HEIGHT = pyg.display.get_window_size()

    # all_nodes is a dictionary that holds every node
    all_nodes = init_nodes()
    cur_center = 'EARTH'

    # Grab a reference to the earth
    for node in all_nodes['EARTH']:
        if node.data['name'] == 'EARTH':
            earth = node
            break

    # full_menu is an object that is used for Earth's menu
    full_menu = FullMenu()

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
    full_menu_active = False
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
    pyg.time.set_timer(add_shooting_star, 5000) # 5 sec

    # Sounds
    ui_channel = pyg.mixer.find_channel()
    soundtrack_channel = pyg.mixer.find_channel()

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
                        is_paused = False

                elif event.type == pyg.MOUSEBUTTONUP:
                    # HUD buttons
                    if hud.p_resume_rect.collidepoint(event.pos):
                        is_paused = False

                    elif hud.p_options_rect.collidepoint(event.pos):
                        ...

                    elif hud.p_info_rect.collidepoint(event.pos):
                        ...

                    elif hud.p_exit_rect.collidepoint(event.pos):
                        terminate()

            # Rendering
            window.fill(colors['space'])
            render_bg(bg_stars, bg_sprites)

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

                elif event.key == pyg.K_SPACE:
                    game_info['cash'] += 90000000000000000000
                    game_info['reputation'] += 20
                    game_info['num_personnel'] += 200
                    game_info['Staff Assignments']['Unassigned'] += 100
                    game_info['Staff Assignments']['Cyber'] += 50
                    game_info['Staff Assignments']['Intel'] += 20
                    game_info['Staff Assignments']['Ops'] += 10
                    game_info['Staff Assignments']['Acquisitions'] += 30

                elif event.key == pyg.K_e:
                    if cur_center == 'EARTH':
                        done_scrolling = False

            elif event.type == pyg.KEYUP:
                if event.key == pyg.K_ESCAPE:
                    if cur_center == 'EARTH':
                        is_paused = True
                    else:
                        cur_center = 'EARTH'

                        # Deselect all nodes
                        for node in all_nodes[cur_center]:
                            node.is_hovered = False

            elif event.type == pyg.MOUSEBUTTONDOWN:
                ui_channel.queue(sounds['down_click'])
                full_menu.update(True) # We pass True because we are calling update() due to a mouse event

            elif event.type == pyg.MOUSEMOTION:
                # If the mouse is over a node, detect that
                for node in all_nodes[cur_center]:
                    if math.dist(event.pos, node.rect.center) <= node.radius:
                        node.is_hovered = True
                    else:
                        node.is_hovered = False

            elif event.type == pyg.MOUSEBUTTONUP:
                ui_channel.queue(sounds['up_click'])
                full_menu.update(True) # We pass True because we are calling update() due to a mouse event

                # If we click on a node
                for node in all_nodes[cur_center]:
                    if node.is_hovered and m_rel == (0, 0):
                        node.is_selected = True # Select it

                        # Check if the node we clicked on has a menu
                        if node.data['name'] != cur_center:
                            if node.data['is_zoomable']:
                                cur_center = node.data['name']

                        # Set the appropriate tab
                        full_menu.cur_tab = cur_center

                        # If we clicked on earth, scroll the earth
                        if node.data['name'] == 'EARTH':
                            done_scrolling = False
                    else:
                        node.is_selected = False
                        # If we drag while holding the earth, don't come back
                        if node.data['name'] == 'EARTH':
                            done_scrolling = True

                # Back arrow
                if hud.arrow_rect.collidepoint(event.pos):
                    cur_center = 'EARTH'
                    # Deselect all nodes
                    for node in all_nodes[cur_center]:
                        node.is_hovered = False

                # Ticker
                if hud.ticker.rect.collidepoint(event.pos):
                    cur_center = 'EVENTS' # Clumsy workaround for old node system
                    full_menu.cur_tab = 'EVENTS'

            # Custom event handling
            elif event.type == new_day:
                date = date + dt.timedelta(days=1)

            elif event.type == new_news_event:
                hud.ticker.new_event(date)

            elif event.type == new_soundtrack:
                # soundtrack_channel.queue(sounds[f'soundtrack{random.randint(1, 1)}'])
                soundtrack_channel.queue(sounds['soundtrack1'])

            elif event.type == add_shooting_star:
                bg_sprites.append(new_shooting_star())

        # Handle held down keys and mouse movement
        event_keys = pyg.key.get_pressed()
        m_pressed = pyg.mouse.get_pressed()
        m_rel = pyg.mouse.get_rel()
        # Move all the nodes/stars if the mouse is dragged
        if m_pressed[0] and not full_menu_active:
            for node in all_nodes[cur_center]: # Move nodes
                node.rect.x += m_rel[0]
                node.rect.y += m_rel[1]
            for obj in bg_stars + bg_sprites: # Move bg objets, but less
                obj['pos'][0] += m_rel[0] * .06*obj['dist']
                obj['pos'][1] += m_rel[1] * .06*obj['dist']

        # Determine whether or not the full menu should be showing
        if cur_center in ['ACQUISITIONS', 'OPS', 'PERSONNEL', 'INTEL', 'CYBER', 'EVENTS']:
            full_menu_active = True
        else:
            full_menu_active = False

        # Keep scrolling until the earth is centered
        if not done_scrolling:
            # If the earth is selected, scroll to the right of the screen to
            # make room for the vignette menu
            if earth.is_selected:
                target = (3/5*WIDTH, HEIGHT/2)
            else:
                target = (WIDTH/2, HEIGHT/2)

            done_scrolling = scroll_the_earth(earth, target, all_nodes, bg_stars)

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

        # Update and render all the nodes
        for node in all_nodes[cur_center]:
            node.update()
            node.render()

        # If the earth is selected, render it's menu
        if earth.is_selected:
            hud.render_vignette('left')
            hud.render_earth_menu()

        # If a node is hovered over, render it's menu
        for node in all_nodes[cur_center]:
            if node.is_hovered:
                node.render_menu()
                break

        # If the full menu is active, update/render it
        if full_menu_active:
            full_menu.update()
            full_menu.render()

        # Render HUD elements
        if cur_center != 'EARTH':
            hud.render_back_arrow(full_menu_active)
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
