import enum
import pygame as pyg
import random
import math
import csv

from os import path

from game_info import game_info
from helper_func import *
from assets import *


class MissionData():
    def __init__(self, name):
        """
        Description: A class to represent one mission. This is it's own class
                     because the data held within a mission is too much for a
                     simple dict. This class will hold information such as
                     objectives, threats, dynamic events, real time game info,
                     etc.
        Parameters:
            name [str] -> The name of the mission to load data from
        Returns: MissionData()
        """
        self.window = pyg.display.get_surface()

        # Find the appropriate mission dataset
        with open(get_path('ops_data.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['name'] == name:
                    self.raw_data = row
                    break
        
        # Locate the data from the csv file
        if self.raw_data['name'] == 'TEST':
            self.csv_layers = {}

            # Each map three layers, load each of them into their own layer
            for layer in ['ground', 'air', 'space']:
                with open(get_path(path.join('assets', 'mapdata', 'TEST', f'map_{layer}.csv')), 'r') as f:
                    reader = csv.reader(f)
                    
                    # Track each row
                    data = []
                    for row in reader:
                        data.append(row)
                
                # Store all the layer data in one dict
                self.csv_layers[layer] = data

        # Process all the data
        self.process_data()
    
    def process_data(self):
        """
        Description: Process the csv data loaded in __init__
        Parameters: None
        Returns: None
        """

        # 'name' -> The name of the mission
        # 'loc' -> The location of the mission
        # 'cost' -> A dict containing the different resources required to embark
        # 'rec_assets' -> The reccomended amount of assets to bring on the mission
        # 'game_area' -> How much area is needed to be created for the mission

        # Process self.raw_data
        self.name = self.raw_data['name']
        self.full_name = 'OPERATION ' + self.name

        self.loc = self.raw_data['loc']

        self.cost = self.raw_data['cost']
        if self.cost == 'None': self.cost = None

        self.rec_assets = self.raw_data['rec_assets']
        if self.rec_assets == 'None': self.rec_assets = None

        self.game_area = [int(i) for i in self.raw_data['game_area'].split('x')]

        # Process self.csv_layers
        self.layers = {'ground': [], 'air': [], 'space': []}

        for layer in self.layers.keys():
            for j, row in enumerate(self.csv_layers[layer]):
                for i, tile in enumerate(row):
                    # Determine what kind of tile we're looking at by the tile number
                    if tile in ['0', '1', '2', '3', '4', '10', '11', '12', '13',
                                '14', '20', '21', '22']:
                        type = 'jam'
                        team = 'hostile'
                    elif tile in ['9']:
                        type = 'tank'
                        team = 'hostile'
                    elif tile in ['19']:
                        type = 'plane'
                        team = 'hostile'
                    elif tile in ['39']:
                        type = 'tank'
                        team = 'friendly'
                    elif tile in ['49']:
                        type = 'plane'
                        team = 'friendly'

                    # '-1' indicates an empty tile, so if we get one of these,
                    # move on to the next tile
                    elif tile == '-1':
                        continue

                    # Create the tile
                    rect = pyg.rect.Rect(50*i, 50*j, 50, 50)
                    surf = tilesets[self.name][int(tile)]

                    # Store as a dict
                    obj = {'rect': rect, 'surf': surf, 'type': type, 'team': team}

                    # Put the new object in the appropriate layer
                    if type in ['jam']:
                        self.layers['space'].append(obj)
                    elif type in ['plane']:
                        self.layers['air'].append(obj)
                    elif type in ['tank']:
                        self.layers['ground'].append(obj)

class GameField():
    def __init__(self, mission):
        """
        Description: A class to represent the gameplay for a certain mission.
                     This class will be responsible for rendering the playing
                     field, handling user inputs, controlling the enemy via
                     a primative "ai", and basically doing it all.
        Parameters:
            mission [MissionData()] -> The mission object to use to load and store
                                       mission data in
        Returns: GameField()
        """
        self.window = pyg.display.get_surface()
        self.window_rect = self.window.get_rect()

        self.image = pyg.Surface(self.window_rect.size).convert_alpha()
        self.image.fill(colors['clear'])

        self.mission = mission

        # Grid size
        # This is always 50, but we use a variable for readability
        self.gridsize = 50

        # Find the topleft corner
        self.topleft = (self.window_rect.width/2 - self.mission.game_area[0]*self.gridsize/2,
                        self.window_rect.height/2 - self.mission.game_area[1]*self.gridsize/2)

        # Scrolling offsets
        self.scroll_x = 0
        self.scroll_y = 0

        for layer in ['ground', 'air', 'space']:
            for obj in self.mission.layers[layer]:
                obj['rect'].move_ip(self.topleft[0], self.topleft[1])

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
        self.scroll_x = max(self.scroll_x, -self.window_rect.width)
        self.scroll_x = min(self.scroll_x, self.window_rect.width)

        self.scroll_y = max(self.scroll_y, -self.window_rect.height)
        self.scroll_y = min(self.scroll_y, self.window_rect.height)

        # Update draw coords
        for layer in ['ground', 'air', 'space']:
            for obj in self.mission.layers[layer]:
                obj['d_rect'] = obj['rect'].move(self.scroll_x, self.scroll_y)
       
        # Check if the mouse is hovering over any object
        # Combine all the layers so we only need one for loop
        objs = self.mission.layers['space'] + self.mission.layers['air'] + self.mission.layers['ground']
        for obj in objs:
            if obj['d_rect'].collidepoint(m_pos):
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

    def render_layers(self):
        """
        Description: Render the different layers that make up the mission.
        Parameters: None
        Returns: None
        """

        for layer in ['ground', 'air', 'space']:
            for obj in self.mission.layers[layer]:
                self.image.blit(obj['surf'], obj['d_rect'])

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

        self.render_layers()

        self.render_grid()

        self.render_hud()

        self.window.blit(self.image, (0, 0))