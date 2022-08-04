from os import fsdecode
from signal import SIG_DFL
import pygame as pyg
import random
import math
import csv

from game_info import game_info
from helper_func import *
from assets import *


class Mission():
    def __init__(self, name):
        """
        Description: A class to represent one mission. This is it's own class
                     because the data held within a mission is too much for a
                     simple dict. This class will hold information such as
                     objectives, threats, dynamic events, real time game info,
                     etc.
        Parameters:
            name [str] -> The name of the mission to load data from
        Returns: Mission()
        """
        self.window = pyg.display.get_surface()

        # Find the appropriate mission dataset
        with open(get_path('ops_data.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['name'] == name:
                    self.raw_data = row
                    break
        
        # Process all the data
        self.process_data()
    
    def process_data(self):
        """
        Description: Process the csv data loaded in __init__
        Parameters: None
        Returns: None
        """
        """
        'name' -> The name of the mission
        'loc' -> The location of the mission
        'cost' -> A dict containing the different resources required to embark
        'rec_assets' -> The reccomended amount of assets to bring on the mission
        'game_area' -> How much area is needed to be created for the mission
        'target_pos' -> The grid coords that we need to maneuver to
        'start_pos' -> The starting position of the ground forces
        'friendlies' -> The type and grid coords of any friendly units
        'hostiles' -> The type and grid coords of any hostile units
        """
        self.name = self.raw_data['name']
        self.full_name = 'OPERATION ' + self.name

        self.loc = self.raw_data['loc']

        self.cost = self.raw_data['cost']
        if self.cost == 'None': self.cost = None

        self.rec_assets = self.raw_data['rec_assets']
        if self.rec_assets == 'None': self.rec_assets = None

        self.game_area = [int(i) for i in self.raw_data['game_area'].split('x')]
        
        self.target_pos = [int(i) for i in self.raw_data['target_pos'].split('x')]

        self.start_pos = [int(i) for i in self.raw_data['start_pos'].split('x')]

        # For each friendly force, determine it's specific data then store it
        if self.raw_data['friendlies'] == 'None':
            # If there is no friendly force, rename 'None' to None
            self.friendlies = None
        else:
            self.friendlies = []
            forces = self.raw_data['friendlies'].split('|')
            # Loop through each dataset
            for force in forces:
                # Split it up
                force_data = force.split(':')
                type = force_data[0]

                # Determine it's type
                if type == 'ground':
                    # Then parse it specificly to that type
                    coords = [int(i) for i in force_data[1].split('x')]

                    new_force = {'coords': coords}

                elif type == 'air':
                    coords = [int(i) for i in force_data[1].split('x')]

                    new_force = {'coords': coords}

                # These attributes will be consistent for all friendly forces
                new_force['type'] = type
                new_force['team'] = 'friendly'

                # Finally, store that data
                self.friendlies.append(new_force)

        # For each hostile force, determine it's specific data then store it
        if self.raw_data['hostiles'] == 'None':
            # If there is no friendly force, rename 'None' to None
            self.hostiles = None
        else:
            self.hostiles = []
            forces = self.raw_data['hostiles'].split('|')
            # Loop through each dataset
            for force in forces:
                # Split it up
                force_data = force.split(':')
                type = force_data[0]

                # Determine it's type
                if type == 'ground':
                    # Then parse it specificly to that type
                    coords = [int(i) for i in force_data[1].split('x')]

                    new_force = {'coords': coords}

                elif type == 'air':
                    coords = [int(i) for i in force_data[1].split('x')]

                    new_force = {'coords': coords}

                elif type == 'jam':
                    data = [int(i) for i in force_data[1].split('x')]
                    tl = data[:2]
                    size = data [2:]
                    rect = pyg.rect.Rect(tl, size)

                    new_force = {'rect': rect}

                # These attributes will be consistent for all friendly forces
                new_force['type'] = type
                new_force['team'] = 'hostile'

                # Finally, store that data
                self.hostiles.append(new_force)


class GameField():
    def __init__(self, mission):
        """
        Description: A class to represent the gameplay for a certain mission.
                     This class will be responsible for rendering the playing
                     field, handling user inputs, controlling the enemy via
                     a primative "ai", and basically doing it all.
        Parameters:
            mission [Mission()] -> The mission object to use to load and store
                                   mission data in
        Returns: GameFields()
        """
        self.window = pyg.display.get_surface()
        self.window_rect = self.window.get_rect()

        self.image = pyg.Surface(self.window_rect.size).convert_alpha()
        self.image.fill(colors['clear'])

        self.mission = mission

        # Grid size
        self.gridsize = 50

        # Scrolling offsets
        self.scroll_x = 0
        self.scroll_y = 0

        # Find the topleft corner
        self.topleft = (self.window_rect.width/2 - self.mission.game_area[0]*self.gridsize/2,
                        self.window_rect.height/2 - self.mission.game_area[1]*self.gridsize/2)

        # Update object positions to use absolute positions
        for obj in self.mission.friendlies + self.mission.hostiles:
            if obj['type'] == 'jam':
                tl = obj['rect'].topleft
                size = (obj['rect'].width * self.gridsize,
                        obj['rect'].height * self.gridsize)

                obj['rect'] = pyg.rect.Rect(self.g2a(tl), size)
            
            elif obj['type'] in ['ground', 'air']:
                obj['coords'] = self.g2a(obj['coords'])
    
    def g2a(self, coordpair):
        """
        Description: Convert a coord pair from grid values, to absolute values.
        Parameters:
            coordpair [tuple] -> A pair of grid coords
        Returns:
            [tuple] -> A pair of absolute coords
        """
        new_x = self.topleft[0] + coordpair[0]*self.gridsize + self.scroll_x
        new_y = self.topleft[1] + coordpair[1]*self.gridsize + self.scroll_y

        return (new_x, new_y)
    
    def update(self, m_rel):
        """
        Description: Handle mouse/keyboard events and perform logic.
        Parameters:
            m_rel [tuple] -> Mouse movement. This must be passed as an argument
                             because we can only call this once per frame, and
                             we already do in the main event loop
        Returns: None
        """
        # Mouse data
        m_pos = pyg.mouse.get_pos()
        m_pressed = pyg.mouse.get_pressed()

        # Scroll if the mouse is drug
        if m_pressed[0]:
            self.scroll_x += m_rel[0]
            self.scroll_y += m_rel[1]
        
        # Limit scrolling so half of the grid stays on screen always
        self.scroll_x = max(self.scroll_x, -self.window_rect.width/2)
        self.scroll_x = min(self.scroll_x, self.window_rect.width/2)

        self.scroll_y = max(self.scroll_y, -self.window_rect.height/2)
        self.scroll_y = min(self.scroll_y, self.window_rect.height/2)

        # Update draw coords
        for obj in self.mission.friendlies + self.mission.hostiles:
            if obj['type'] == 'jam':
                obj['d_rect'] = obj['rect'].move(self.scroll_x, self.scroll_y)

            elif obj['type'] in ['ground', 'air']:
                obj['d_coords'] = (obj['coords'][0] + self.scroll_x,
                                   obj['coords'][1] + self.scroll_y)

        # Check if the mouse is hovering over any object
        for obj in self.mission.friendlies + self.mission.hostiles:
            if obj['type'] == 'jam':
                if obj['d_rect'].collidepoint(m_pos):
                    self.hovered = obj
                    break
            else:
                if math.hypot(obj['d_coords'][0]-m_pos[0], obj['d_coords'][1]-m_pos[1]) < self.gridsize*0.5:
                    self.hovered = obj
                    break
        else:
            self.hovered = None

    def render_grid(self):
        """
        Description: Render a grid the size of the game area.
        Parameters: None
        Returns: None
        """
        scroll_tl = (self.topleft[0] + self.scroll_x, self.topleft[1] + self.scroll_y)

        # Horizontal lines
        for y in range(self.mission.game_area[1] + 1):
            pyg.draw.line(self.image, colors['babygreen'],
                          (scroll_tl[0], scroll_tl[1] + y*self.gridsize),
                          (scroll_tl[0] + self.mission.game_area[0]*self.gridsize, scroll_tl[1] + y*self.gridsize))

        # Vertical lines
        for x in range(self.mission.game_area[0] + 1):
            pyg.draw.line(self.image, colors['babygreen'],
                          (scroll_tl[0] + x*self.gridsize, scroll_tl[1]),
                          (scroll_tl[0] + x*self.gridsize, scroll_tl[1] + self.mission.game_area[1]*self.gridsize))

    def render_friendlies(self):
        """
        Description: Render any forces/tiles that are friendly to the player.
        Parameters: None
        Returns: None
        """
        for obj in self.mission.friendlies:
            if obj['type'] == 'ground':
                pyg.draw.circle(self.image, colors['babyblue'], obj['d_coords'], self.gridsize/2.5, 5)
      
            elif obj['type'] == 'air':
                start = (obj['d_coords'][0]-.3*self.gridsize, obj['d_coords'][1]-.3*self.gridsize)
                end = (obj['d_coords'][0]+.3*self.gridsize, obj['d_coords'][1]+.3*self.gridsize)
                pyg.draw.line(self.image, colors['babyblue'], start, end, 5)

                start = (obj['d_coords'][0]+.3*self.gridsize, obj['d_coords'][1]-.3*self.gridsize)
                end = (obj['d_coords'][0]-.3*self.gridsize, obj['d_coords'][1]+.3*self.gridsize)
                pyg.draw.line(self.image, colors['babyblue'], start, end, 5)

    def render_hostiles(self):
        """
        Description: Render any forces/tiles that are hostile to the player.
        Parameters: None
        Returns: None
        """
        for obj in self.mission.hostiles:
            if obj['type'] == 'ground':
                # Draw a circle for ground forces
                pyg.draw.circle(self.image, colors['rose'], obj['d_coords'], self.gridsize/2.5, 5)
        
            elif obj['type'] == 'air':
                # Draw an 'X' for air forces
                start = (obj['d_coords'][0]-.3*self.gridsize, obj['d_coords'][1]-.3*self.gridsize)
                end = (obj['d_coords'][0]+.3*self.gridsize, obj['d_coords'][1]+.3*self.gridsize)
                pyg.draw.line(self.image, colors['rose'], start, end, 5)

                start = (obj['d_coords'][0]+.3*self.gridsize, obj['d_coords'][1]-.3*self.gridsize)
                end = (obj['d_coords'][0]-.3*self.gridsize, obj['d_coords'][1]+.3*self.gridsize)
                pyg.draw.line(self.image, colors['rose'], start, end, 5)

            elif obj['type'] == 'jam':
                # Draw a filled in rectangle for jammed areas
                rect = pyg.rect.Rect(obj['d_rect'].topleft, obj['d_rect'].size)
                pyg.draw.rect(self.image, colors['clear_rose'], rect)
                pyg.draw.rect(self.image, colors['rose'], rect, 5)

    def render_hud(self):
        """
        Description: Render the ops-specific hud.
        Parameters: None
        Returns: None
        """
        # If we have are hovering over something, render a menu
        if self.hovered != None:
            if self.hovered['team'] == 'friendly':
                color = colors['babyblue']
            else:
                color = colors['rose']

            pyg.draw.rect(self.image, color, (0, 0, 200, 300))

    def render(self):
        """
        Description: Render the playing area.
        Parameters: None
        Returns: None
        """
        self.image.fill(colors['black'])

        self.render_grid()

        self.render_friendlies()

        self.render_hostiles()

        self.render_hud()

        self.window.blit(self.image, (0, 0))