"""
A wargame simulation made by the i5 cyber element, with inspiration from the i5 intel element.

By: i5 Cyber element
"""

import pygame as pyg
import random
import math
import os

from node import Node
from fullmenu import FullMenu
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
        node = Node(window, data)
        earth_nodes.add(node)

    gssap_nodes = pyg.sprite.Group()
    for data in gssap_data:
        node = Node(window, data)
        gssap_nodes.add(node)

    iss_nodes = pyg.sprite.Group()
    for data in iss_data:
        node = Node(window, data)
        iss_nodes.add(node)

    milstar_nodes = pyg.sprite.Group()
    for data in milstar_data:
        node = Node(window, data)
        milstar_nodes.add(node)

    aehf_nodes = pyg.sprite.Group()
    for data in aehf_data:
        node = Node(window, data)
        aehf_nodes.add(node)

    gps_nodes = pyg.sprite.Group()
    for data in gps_data:
        node = Node(window, data)
        gps_nodes.add(node)

    sbirs_nodes = pyg.sprite.Group()
    for data in sbirs_data:
        node = Node(window, data)
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

def render_back_arrow(window, cur_center):
    """
    Description: Render a back arrow that will take us back to the main menu.
    Parameters:
        window [pyg.Surface] -> The surface to draw on
        cur_center [str] -> The name of the node currently in the center
    Returns: None
    """
    if cur_center != 'EARTH':
        arrow = fonts['zrnic48'].render("<--- EARTH", True, colors['white'])

        if cur_center in ['ACQUISITIONS', 'OPS', 'PERSONNEL', 'INTEL', 'CYBER']:
            window.blit(arrow, (20, HEIGHT - 65))
        else:
            window.blit(arrow, (20, 10))

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
    # all_nodes is a dictionary that holds every node
    all_nodes = init_nodes()
    cur_center = 'EARTH'

    # full_menu is an object that is used for Earth's menu
    full_menu = FullMenu(window)

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

            elif event.type == pyg.MOUSEBUTTONUP:
                if full_menu_active:
                    if event.pos[0] < 200 and event.pos[1] > HEIGHT - 60: # Will need to be changed
                        cur_center = 'EARTH'
                else:
                    if event.pos[0] < 200 and event.pos[1] < 100: # Will need to be changed
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

        # If the current center node doesn't use nodes (e.x. OPS or CYBER), use
        # a full screen menu
        if len(all_nodes[cur_center]) == 0:
            full_menu.update()
            full_menu.render()

        # Give the user a way back to the main screen
        render_back_arrow(window, cur_center)

        # Update the display, and don't exceed FPS
        pyg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    # Initalize pygame and create a window
    pyg.init()
    pyg.display.set_caption("Upgrade Tree")
    window = pyg.display.set_mode(flags=pyg.HWSURFACE | pyg.FULLSCREEN | pyg.DOUBLEBUF)
    WIDTH, HEIGHT = pyg.display.get_window_size()

    # Start the program
    main()
