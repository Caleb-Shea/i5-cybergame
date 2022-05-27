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

from fullmenu import FullMenu
from node import Node
from hud import HUD
from node_data import *
from assets import *
from helper_func import *


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
    for data in main_data:
        node = Node(data)
        earth_nodes.add(node)

    gssap_nodes = pyg.sprite.Group()
    for data in gssap_data:
        node = Node(data)
        gssap_nodes.add(node)

    iss_nodes = pyg.sprite.Group()
    for data in iss_data:
        node = Node(data)
        iss_nodes.add(node)

    milstar_nodes = pyg.sprite.Group()
    for data in milstar_data:
        node = Node(data)
        milstar_nodes.add(node)

    aehf_nodes = pyg.sprite.Group()
    for data in aehf_data:
        node = Node(data)
        aehf_nodes.add(node)

    gps_nodes = pyg.sprite.Group()
    for data in gps_data:
        node = Node(data)
        gps_nodes.add(node)

    sbirs_nodes = pyg.sprite.Group()
    for data in sbirs_data:
        node = Node(data)
        sbirs_nodes.add(node)

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


    node_dict = {'EARTH': earth_nodes,
                 'GSSAP': gssap_nodes,
                 'ISS': iss_nodes,
                 'MILSTAR': milstar_nodes,
                 'AEHF': aehf_nodes,
                 'GPS': gps_nodes,
                 'SBIRS': sbirs_nodes,

                 # These are included because although they use a different menu
                 # system, we still need to clear the screen
                 'OPS': [],
                 'PERSONNEL': [],
                 'INTEL': [],
                 'CYBER': [],
                 'ACQUISITIONS': []}

    return node_dict

def zoom_to(node, cur_center):
    """
    Description: Replace the menu nodes with the node map of the passed node.
    Parameters:
        node [Node()] -> The node to zoom in on
        cur_center [str] -> The name of the node currently in the center
    Returns: str -> The name of the node in the center
    """

    if node.data['name'] != cur_center:
        if node.data['is_zoomable']:
            return node.data['name']

    return cur_center

def render_bg(window, bg_star_coords):
    """
    Description: Render a faux starscape.
    Parameters:
    window [pyg.Surface] -> The surface to draw on
    bg_star_coords [list] -> A list containing coordinates and size data
    for each star
    Returns: None
    """
    for star in bg_star_coords:
        # Unpack the list
        x = star[0]
        y = star[1]
        size = star[2]
        corner = star[3]

        if corner == 1:
            pyg.draw.circle(window, colors['starwhite'], (x, y), size, draw_top_left=True)
        elif corner == 2:
            pyg.draw.circle(window, colors['starwhite'], (x, y), size, draw_top_right=True)
        elif corner == 3:
            pyg.draw.circle(window, colors['starwhite'], (x, y), size, draw_bottom_left=True)
        else:
            pyg.draw.circle(window, colors['starwhite'], (x, y), size, draw_bottom_right=True)

def main():
    # Get references to the window and it's size
    window = pyg.display.get_surface()
    WIDTH, HEIGHT = pyg.display.get_window_size()

    # all_nodes is a dictionary that holds every node
    all_nodes = init_nodes()
    cur_center = 'EARTH'

    # full_menu is an object that is used for Earth's menu
    full_menu = FullMenu()

    # The HUD
    hud = HUD()

    # Create the background star effect
    bg_star_coords = []
    for i in range(10000):
        x = random.randint(-WIDTH, 2 * WIDTH)
        y = random.randint(-HEIGHT, 2 * HEIGHT)
        size = random.random() + 1.5
        corner = random.randint(1, 4)

        bg_star_coords.append([x, y, size, corner])

    # Timekeeping
    clock = pyg.time.Clock()
    FPS = 60

    date = dt.date.today()

    # Custom events
    new_day = pyg.USEREVENT + 1
    pyg.time.set_timer(new_day, 5000)

    # Sounds
    ui_channel = pyg.mixer.find_channel()

    while True:
        # Determine whether or not the full menu is showing
        if cur_center in ['ACQUISITIONS', 'OPS', 'PERSONNEL', 'INTEL', 'CYBER']:
            full_menu_active = True
        else:
            full_menu_active = False

        # Handle all events
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                terminate()

            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_BACKQUOTE:
                    terminate()
                elif event.key == pyg.K_SPACE:
                    ...

            elif event.type == pyg.KEYUP:
                if event.key == pyg.K_ESCAPE:
                    if cur_center != 'EARTH':
                        cur_center = 'EARTH'

            elif event.type == pyg.MOUSEBUTTONDOWN:
                ui_channel.queue(sounds['down_click'])

            elif event.type == pyg.MOUSEBUTTONUP:
                ui_channel.queue(sounds['up_click'])

                if hud.arrow_rect.collidepoint(event.pos):
                    cur_center = 'EARTH'

                for node in all_nodes[cur_center]:
                    if node.is_selected and m_rel == (0, 0):
                        if math.dist(event.pos, node.rect.center) <= node.radius:
                            cur_center = zoom_to(node, cur_center)
                            full_menu.cur_tab = cur_center # Select the tab that we clicked on
                        else:
                            node.is_selected = False

                    # If a node is clicked on, select it
                    if node.is_hovered:
                        if math.dist(event.pos, node.rect.center) <= node.radius:
                            node.is_selected = True
            elif event.type == new_day:
                date = date + dt.timedelta(days=1)


        # Handle held down keys and mouse movement
        event_keys = pyg.key.get_pressed()
        mouse_keys = pyg.mouse.get_pressed()
        m_rel = pyg.mouse.get_rel()
        # Move all the nodes/stars if a key is pressed
        if event_keys[pyg.K_LEFT] or event_keys[pyg.K_a]:
            for node in all_nodes[cur_center]:
                node.rect.x += 15
            if not full_menu_active: # Find a better way to do this
                for star in bg_star_coords:
                    star[0] += 1.5 # Move the nodes less for a parallax effect
        if event_keys[pyg.K_RIGHT] or event_keys[pyg.K_d]:
            for node in all_nodes[cur_center]:
                node.rect.x -= 15
            if not full_menu_active:
                for star in bg_star_coords:
                    star[0] -= 1.5
        if event_keys[pyg.K_UP] or event_keys[pyg.K_w]:
            for node in all_nodes[cur_center]:
                node.rect.y += 15
            if not full_menu_active:
                for star in bg_star_coords:
                    star[1] += 1.5
        if event_keys[pyg.K_DOWN] or event_keys[pyg.K_s]:
            for node in all_nodes[cur_center]:
                node.rect.y -= 15
            if not full_menu_active:
                for star in bg_star_coords:
                    star[1] -= 1.5
        # Move all the nodes/stars if the mouse is dragged
        if mouse_keys[0]:
            for node in all_nodes[cur_center]:
                node.rect.x += m_rel[0]
                node.rect.y += m_rel[1]
            if not full_menu_active:
                for star in bg_star_coords:
                    star[0] += m_rel[0] * .1
                    star[1] += m_rel[1] * .1

        # Render the background
        window.fill(colors['space'])
        render_bg(window, bg_star_coords)

        # Update and render all the nodes
        for node in all_nodes[cur_center]:
            node.update()
            node.render()

        # If a node is selected, render it's menu
        for node in all_nodes[cur_center]:
            if node.is_selected:
                node.render_menu()
                break

        # If the current center node doesn't use nodes (e.x. OPS or CYBER),
        # use a full screen menu
        if len(all_nodes[cur_center]) == 0:
            full_menu.update()
            full_menu.render()

        # Render HUD elements
        if cur_center != 'EARTH':
            hud.render_back_arrow(full_menu_active)
        hud.render_time(date)

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
