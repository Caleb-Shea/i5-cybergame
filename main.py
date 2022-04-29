#!/usr/bin/env python3
"""
An upgrade tree simulation.

By: Caleb Shea
"""

import pygame as pyg
import random
import math
import os

from colors import colors
from node_data import node_data

os.environ['SDL_VIDEO_CENTERED'] = '1'

FPS = 30


class Node(pyg.sprite.Sprite):
    """
    A class to represent a single node.
    """
    def __init__(self, window, data):
        super().__init__()

        self.window = window

        self.data = data
        self.parent = self.data['parent']

        self.radius = 50 + (3 - (self.data['generation'] * 5))

        self.image = pyg.Surface((self.radius * 2, self.radius * 2)).convert_alpha()
        self.image.fill(colors['clear'])
        pyg.draw.circle(self.image, colors[self.data['color']], (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect()

        self.is_hovered = False
        self.is_selected = False
        self.is_bought = False

        self.name_img = fonts['zrnic24'].render(self.data['name'], True, colors['darkgray'])
        self.name_rect = self.name_img.get_rect()

    def phase_two_init(self, nodes):
        """
        Description: Initalize parts of the node that cannot be initalized
                     without more information, specifially the complete list
                     of nodes.
        Parameters:
            nodes [pyg.sprite.Group] -> The complete lists of nodes.
        Returns: None
        """
        self.nodes = nodes
        self.get_children(self.nodes)

        for node in nodes:
            if self.parent == node.data['name']:
                self.parent = node

        if self.parent == None:
            # If center node, center on the screen
            if self.data['name'] == 'CENTER':
                self.rect.center = (WIDTH//2, HEIGHT//2)
                # The center has a theta so it's children don't overlap
                self.theta = random.random() * (4 * math.pi)
        else:
            # Otherwise, center on parent
            self.theta = self.parent.theta

            if self.data['generation'] > 1:
                num_sibs = len(self.parent.children) + 1
                self.theta += (2 * math.pi) / num_sibs * int(self.data['name'][-1])
                self.theta += math.pi # Additional rotation to face the non-central nodes away from the center
            else:
                num_sibs = len(self.parent.children)
                self.theta += (2 * math.pi) / num_sibs * int(self.data['name'][-1])

            self.dist = 200 - 10*(self.data['generation']**1.7)
            self.rect.center = (self.parent.rect.centerx + self.dist * math.cos(self.theta),
                                self.parent.rect.centery + self.dist * math.sin(self.theta))

    def get_children(self, nodes):
        """
        Description: Create a list of this node's children.
        Parameters:
            nodes [pyg.sprite.Group] -> The complete lists of nodes.
        Returns: None
        """
        self.children = []
        for child in self.data['children']:
            for node in nodes:
                if node.data['name'] == child:
                    self.children.append(node)

    def draw_connections(self):
        """
        Description: Draw lines between this node and it's children.
        Parameters: None
        Returns: None
        """
        for child in self.children:
            pyg.draw.aaline(window, colors['gray'],
                          self.rect.center, child.rect.center) # Use arcs later

    def update(self):
        """
        Description: Spin this node around the central node.
                     Set is_hovered and is_selected booleans.
                     Position text.
        Parameters: None
        Returns: None
        """
        if self.parent != None:
            self.theta += 0.0015
            self.rect.center = (self.parent.rect.centerx + self.dist * math.cos(self.theta),
                                self.parent.rect.centery + self.dist * math.sin(self.theta))

        m_pos = pyg.mouse.get_pos()
        if math.dist(m_pos, self.rect.center) <= self.radius:
            self.is_hovered = True
            # pyg.transform.smoothscale(self.image, (2 * (self.radius + 3), 2 * (self.radius + 3)))
        else:
            self.is_hovered = False
            # pyg.transform.smoothscale(self.image, (2 * self.radius, 2 * self.radius))

        self.name_rect.center = self.rect.center

    def render(self):
        """
        Description: Render this node on the screen.
        Parameters: None
        Returns: None
        """
        self.draw_connections()
        if self.is_bought:
            # self.window.blit(self.glow_img, self.rect)
            pyg.draw.circle(self.window, colors['yellow'], self.rect.center, self.radius * 1.1)
        self.window.blit(self.image, self.rect)
        self.window.blit(self.name_img, self.name_rect)


def terminate():
    """
    Description: Cleanly exit the program.
    Parameters: None
    Returns: None
    """
    pyg.quit()
    raise SystemExit()

def get_path(path):
    """
    Description: Get the full path from a partial file path.
    Parameters:
        path [path-like-object] -> The partial path to get the full path from
    Returns:
        A path-like-object that contains a full path
    """
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, path)

def play_sound(sound):
    """
    Description: Play a sound out of any available channel.
    Parameters:
        sound [sound file] -> The sound to play
    Returns: None
    """
    se_channel = pyg.mixer.find_channel()
    se_channel.play(sound)

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
    nodes = pyg.sprite.Group()
    for data in node_data:
        node = Node(window, data)
        nodes.add(node)

    for node in nodes:
        node.phase_two_init(nodes)

    bg_star_coords = []
    for i in range(10000):
        x = random.randint(-WIDTH, 2 * WIDTH)
        y = random.randint(-HEIGHT, 2 * HEIGHT)
        size = random.random() + 1.5
        corner = random.randint(1, 4)

        bg_star_coords.append([x, y, size, corner])


    clock = pyg.time.Clock()

    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                terminate()

            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_BACKQUOTE:
                    terminate()
                elif event.key == pyg.K_SPACE:
                    ...

            elif event.type == pyg.KEYUP:
                if event.key == pyg.K_LSHIFT:
                    for di in dice_info:
                        di.show_stats = False

            elif event.type == pyg.MOUSEBUTTONDOWN:
                for node in nodes:
                    if math.dist(event.pos, node.rect.center) <= node.radius:
                        node.is_bought = True


        event_keys = pyg.key.get_pressed()
        mouse_keys = pyg.mouse.get_pressed()
        m_rel = pyg.mouse.get_rel()
         # Move the nodes if a key is pressed
        if event_keys[pyg.K_LEFT] or event_keys[pyg.K_a]:
            for node in nodes:
                node.rect.x += 15
            for star in bg_star_coords:
                star[0] += 1.5
        if event_keys[pyg.K_RIGHT] or event_keys[pyg.K_d]:
            for node in nodes:
                node.rect.x -= 15
            for star in bg_star_coords:
                star[0] -= 1.5
        if event_keys[pyg.K_UP] or event_keys[pyg.K_w]:
            for node in nodes:
                node.rect.y += 15
            for star in bg_star_coords:
                star[1] += 1.5
        if event_keys[pyg.K_DOWN] or event_keys[pyg.K_s]:
            for node in nodes:
                node.rect.y -= 15
            for star in bg_star_coords:
                star[1] -= 1.5
        if mouse_keys[0]:
            for node in nodes:
                node.rect.x += m_rel[0]
                node.rect.y += m_rel[1]
            for star in bg_star_coords:
                star[0] += m_rel[0] * .1
                star[1] += m_rel[1] * .1


        window.fill(colors['black'])
        render_bg(window, bg_star_coords)

        for node in nodes:
            node.update()
            node.render()

        pyg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pyg.mixer.pre_init(44100, -16, 2, 512)
    pyg.mixer.init()
    pyg.init()
    pyg.display.set_caption("Upgrade Tree")
    window = pyg.display.set_mode(flags=pyg.HWSURFACE | pyg.FULLSCREEN | pyg.DOUBLEBUF)
    WIDTH, HEIGHT = pyg.display.get_window_size()

    # Import assets after initalizing pygame
    from asset_loader import *

    main()
