import pygame as pyg
import random
import math

from game_info import game_info
from assets import *


class EarthSystem():
    def __init__(self):
        """
        Description: A class to represent earth and it's connected entities.
                     This class holds the earth itself, nodes connected to the
                     earth, satellites, and menu decorations.
        Parameters: None
        Returns: EarthSystem()
        """
        self.window = pyg.display.get_surface()

        # Init objects
        self.nodes = {}

        earth = pyg.Surface((130, 130)).convert_alpha()
        earth.fill(colors['clear'])
        pyg.draw.circle(earth, colors['white'], (65, 65), 65)
        self.nodes['EARTH'] = {'name': 'EARTH', 'surf': earth,
                               'rect': earth.get_rect(), 'desc': 'Home sweet home'}
        acq = pyg.Surface((100, 100)).convert_alpha()
        acq.fill(colors['clear'])
        pyg.draw.circle(acq, colors['cyan'], (50, 50), 50)
        self.nodes['ACQUISITIONS'] = {'name': 'ACQUISITIONS', 'surf': acq,
                                      'rect': acq.get_rect(), 'desc': 'Buy cool shit',
                                      'dist': 130, 'theta': 2*math.pi/5}
        cyber = pyg.Surface((100, 100)).convert_alpha()
        cyber.fill(colors['clear'])
        pyg.draw.circle(cyber, colors['cyan'], (50, 50), 50)
        self.nodes['CYBER'] = {'name': 'CYBER', 'surf': cyber,
                               'rect': cyber.get_rect(), 'desc': 'Attack and defend, virtually',
                               'dist': 130, 'theta': 4*math.pi/5}
        intel = pyg.Surface((100, 100)).convert_alpha()
        intel.fill(colors['clear'])
        pyg.draw.circle(intel, colors['cyan'], (50, 50), 50)
        self.nodes['INTEL'] = {'name': 'INTEL', 'surf': intel,
                               'rect': intel.get_rect(), 'desc': 'Hire James Bond for a bit',
                               'dist': 130, 'theta': 6*math.pi/5}
        ops = pyg.Surface((100, 100)).convert_alpha()
        ops.fill(colors['clear'])
        pyg.draw.circle(ops, colors['cyan'], (50, 50), 50)
        self.nodes['OPS'] = {'name': 'OPS', 'surf': ops,
                             'rect': ops.get_rect(), 'desc': 'Kill Nazis', 'dist': 130,
                             'theta': 8*math.pi/5}
        ppl = pyg.Surface((100, 100)).convert_alpha()
        ppl.fill(colors['clear'])
        pyg.draw.circle(ppl, colors['cyan'], (50, 50), 50)
        self.nodes['PERSONNEL'] = {'name': 'PERSONNEL', 'surf': ppl,
                                   'rect': ppl.get_rect(), 'desc': 'Buy people.',
                                   'dist': 130, 'theta': 10*math.pi/5}

        # A satellite is anything orbiting the earth but isn't connected to it
        self.sats = []

        # Init trackers
        self.selected = None
        self.hovered = None

        # Set initial positions
        self.nodes['EARTH']['rect'].center = self.window.get_rect().center
        """
        # Load images
        # Get the spritesheet for earth
        if self.data['name'] == 'EARTH':
            self.ss = images['earth_ss']
            self.ss_cur = 0
            self.ss_rects = []
            for j in range(4):
                for i in range(12):
                    x = i * 100
                    y = j * 100
                    self.ss_rects.append(pyg.rect.Rect(x, y, 100, 100))"""

    def get_hovered(self):
        """
        Description: If the `self.hovered` attribute exists, find what is
                     being hovered over, and return it.
        Parameters: None
        Returns:
            [dict] -> The hovered entity
        """
        # Loop through the nodes
        for node in self.nodes.values():
            if node['name'] == self.hovered:
                return node

        # Loop through the sats
        for sat in self.sats:
            if sat['name'] == self.hovered:
                return sat

    def spin(self):
        """
        Description: Spin the nodes and the sats around the earth.
        Parameters: None
        Returns: None
        """
        earth_rect = self.nodes['EARTH']['rect']

        # Nodes
        for node in self.nodes.values():
            if node['name'] == 'EARTH': continue
            node['theta'] += 0.001
            node['rect'].center = (earth_rect.centerx + node['dist'] * math.cos(node['theta']),
                                   earth_rect.centery + node['dist'] * math.sin(node['theta']))

        # Sats
        for sat in self.sats:
            sat['theta'] += 0.0015
            sat['rect'].center = (earth_rect.centerx + sat['dist'] * math.cos(sat['theta']),
                                  earth_rect.centery + sat['dist'] * math.sin(sat['theta']))

    def update(self, is_click=False):
        """
        Description: Update the position of everything, handle mouseclicks.
        Parameters:
            is_click [bool] -> True on the first frame of a mouseclick event
        Returns: None
        """
        # --- Handle mouse events ---
        m_pos = pyg.mouse.get_pos()
        m_pressed = pyg.mouse.get_pressed()

        # If the mouse is hovering over something, track that
        for node in self.nodes.values():
            if node['rect'].collidepoint(m_pos):
                self.hovered = node['name']
                break
        else:
            self.hovered = None

            for sat in self.sats:
                if sat['rect'].collidepoint(m_pos):
                    self.hovered = sat['name']
                    break
            else:
                self.hovered = None

        if is_click:
            for node in self.nodes.values():
                if self.hovered == node['name']:
                    if node['rect'].collidepoint(m_pos):
                        self.selected = node['name']
                        break
            else:
                self.selected = None

        # --- Satellite management ---
        # Add new sats if necessary
        while len(self.sats) < game_info['num_sats']:
            # Create a surface
            surf = pyg.Surface((30, 30)).convert_alpha()
            surf.fill(colors['sand'])

            # Create the sat's data
            dist = random.randint(300, 400)
            theta = random.random() * 2*math.pi

            # Name each individual satellite based on what type we're missing
            sat_names = ['GPS', 'ABD', 'SPI', 'MDef', 'ABCDE', 'IROOI', 'ICBM', 'B.O.L.L.S.', 'Nukes']
            for n in sat_names:
                if len([i for i in self.sats if i['name'] == n]) < game_info[f'Acq {n} Level']:
                    name = n
                    break
            else:
                # Failsafe
                name = 'UNKNOWN SATELLITE'

            # Create a new sat "instance"
            new_sat = {'name': name, 'surf': surf, 'rect': surf.get_rect(), 'dist': dist,
                       'theta': theta}
            self.sats.append(new_sat)

        # Spin nodes and sats
        self.spin()

    def render(self):
        """
        Description: Render the earth system including satellites.
        Parameters: None
        Returns: None
        """
        # Draw connection lines
        earth_center = self.nodes['EARTH']['rect'].center
        for node in self.nodes.values():
            # Draw straight lines to all the nodes
            pyg.draw.line(self.window, colors['gray'], earth_center, node['rect'].center)

        for sat in self.sats:
            # Draw a circular orbit for the satellites
            pyg.draw.circle(self.window, colors['gray'], earth_center, sat['dist'], 1)

        # Render nodes
        for node in self.nodes.values():
            if self.hovered == node['name']:
                # If we're hovering over a node, render it bigger
                self.window.blit(pyg.transform.smoothscale(node['surf'], node['rect'].inflate(10, 10).size), node['rect'].move(-5, -5))
            else:
                self.window.blit(node['surf'], node['rect'])

            # Draw the names of each node on each node
            if len(node['name']) < 6:
                f = fonts['zrnic24']
            else:
                f = fonts['zrnic18']
            name = f.render(node['name'], True, colors['black'])
            self.window.blit(name, name.get_rect(center=node['rect'].center))

        # Render satellites
        for sat in self.sats:
            if self.hovered == sat['name']:
                # If we're hovering over a node, render it bigger
                self.window.blit(pyg.transform.smoothscale(sat['surf'], sat['rect'].inflate(6, 6).size), sat['rect'].move(-3, -3))
            else:
                self.window.blit(sat['surf'], sat['rect'])
