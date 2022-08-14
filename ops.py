import pygame as pyg
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
        # 'objective' -> The objective(s) of the mission
        # 'cost' -> A dict containing the different resources required to embark
        # 'rec_assets' -> The reccomended amount of assets to bring on the mission
        # 'game_area' -> How much area is needed to be created for the mission

        # Process self.raw_data
        self.name = self.raw_data['name']
        self.full_name = 'OPERATION ' + self.name

        self.loc = self.raw_data['loc']

        self.objectives = self.raw_data['objective'].split('|')

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
                    elif tile in ['40', '41', '42', '50', '52', '60', '61', '62']:
                        type = 'city_border'
                        team = 'passive'
                    elif tile in ['43', '51', '53', '63']:
                        type = 'city'
                        team = 'passive'

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
                    elif type in ['tank', 'city_border', 'city']:
                        self.layers['ground'].append(obj)

class GameField():
    def __init__(self, mission, assets):
        """
        Description: A class to represent the gameplay for a certain mission.
                     This class will be responsible for rendering the playing
                     field, handling user inputs, controlling the enemy via
                     a primative "ai", and basically doing it all.
        Parameters:
            mission [MissionData()] -> The mission object to use to load and store
                                       mission data in
            assets [dict] -> The assets the player chooses to bring with them
        Returns: GameField()
        """
        self.window = pyg.display.get_surface()
        self.window_rect = self.window.get_rect()

        self.image = pyg.Surface(self.window_rect.size).convert_alpha()
        self.image.fill(colors['clear'])

        self.mission = mission

        # Mouse trackers
        self.hovered = None
        self.selected = None

        # Grid size
        # This is always 50, but we use a variable for readability
        self.gridsize = 50

        # Find the topleft corner
        self.topleft = (self.window_rect.width/2 - self.mission.game_area[0]*self.gridsize/2,
                        self.window_rect.height/2 - self.mission.game_area[1]*self.gridsize/2)

        # Scrolling offsets
        self.scroll_x = 0
        self.scroll_y = 0

        # Set inital positions to be aligned with the grid
        for layer in ['ground', 'air', 'space']:
            for obj in self.mission.layers[layer]:
                obj['rect'].move_ip(self.topleft[0], self.topleft[1])
        
        # --- Player data ---
        self.p_max_actions = 5
        self.p_actions = self.p_max_actions
        self.p_assets = assets

        # --- Enemy data ---
        ...

        # --- HUD init ---
        # A list of important coords to render at
        self.imp_coords = {
            'name': (self.window_rect.left+120, self.window_rect.bottom-80),
            'pic': ()
        }

        # The coords of the area at the bottom of the screen
        trap_coords = [
            self.window_rect.bottomleft,
            self.window_rect.bottomright,
            (self.window_rect.right-100,self.window_rect.bottom-80),
            (self.window_rect.left+100,self.window_rect.bottom-80)
        ]
        
        # The coords for the game info at the topleft of the screen
        info_coords = [
            self.window_rect.topleft,
            (self.window_rect.left+310, self.window_rect.top),
            (self.window_rect.left+255, self.window_rect.top+105),
            (self.window_rect.left, self.window_rect.top+175)
        ]
        
        # Friendly
        self.f_hud = pyg.Surface(self.window_rect.size).convert_alpha()
        self.f_hud.fill(colors['clear'])
        pyg.draw.polygon(self.f_hud, colors['ops_f_half'], trap_coords)

        # Hostile
        self.h_hud = pyg.Surface(self.window_rect.size).convert_alpha()
        self.h_hud.fill(colors['clear'])
        pyg.draw.polygon(self.h_hud, colors['ops_h_half'], trap_coords)

        # Passive
        self.p_hud = pyg.Surface(self.window_rect.size).convert_alpha()
        self.p_hud.fill(colors['clear'])
        pyg.draw.polygon(self.p_hud, colors['ops_p_half'], trap_coords)

        # Game info
        self.info_hud = pyg.Surface(self.window_rect.size).convert_alpha()
        self.info_hud.fill(colors['clear'])
        pyg.draw.polygon(self.info_hud, colors['ops_f_half'], info_coords)
        pyg.draw.polygon(self.info_hud, colors['ops_friendly'], info_coords, 5)
        
        # Label text
        text = fonts['zrnic42'].render('OBJECTIVES', True, colors['starwhite'])
        text = pyg.transform.rotate(text, 15.8)      
        self.info_hud.blit(text, (5, 77))

        # Render objectives
        for y, item in enumerate(self.mission.objectives):
            # Check boxes
            box = pyg.rect.Rect(8, 8+30*y, 20, 20)
            pyg.draw.rect(self.info_hud, colors['starwhite'], box, 3)
            
            # Objective text
            if item == 'elim': fulltext = 'Eliminate all enemy forces'
            elif item == '0loss': fulltext = 'Have 0 casulties'
            elif item.endswith('loss'): fulltext = f'Have less than {item.split("loss")[0]} casulties'
            elif item == 'savecivs': fulltext = 'Save all civilians'

            text = fonts['zrnic20'].render(fulltext, True, colors['black'])
            self.info_hud.blit(text, box.move(26, -2))

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
        
        # Limit scrolling so we don't lose the grid
        self.scroll_x = max(self.scroll_x, -self.window_rect.width/1.5)
        self.scroll_x = min(self.scroll_x, self.window_rect.width/1.5)

        self.scroll_y = max(self.scroll_y, -self.window_rect.height/1.5)
        self.scroll_y = min(self.scroll_y, self.window_rect.height/1.5)

        # Update draw coords
        for layer in ['ground', 'air', 'space']:
            for obj in self.mission.layers[layer]:
                obj['d_rect'] = obj['rect'].move(self.scroll_x, self.scroll_y)

        # Check if the mouse is hovering over any object
        # Combine all the layers so we only need one for loop
        objs = self.mission.layers['space'] + self.mission.layers['air'] + self.mission.layers['ground']
        
        # We don't want to render hud sections for city borders
        objs = [i for i in objs if i['type'] != 'city_border']

        for obj in objs:
            if obj['d_rect'].collidepoint(m_pos):
                self.hovered = obj
                break
        else:
            self.hovered = None
        
        # Check if we clicked on something
        if m_pressed[0]:
            for obj in objs:
                if obj['d_rect'].collidepoint(m_pos):
                    self.selected = obj
                    break
            else: # If we didn't break from the loop, deselect
                self.selected = None
        
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
        # Render topleft info screen
        self.image.blit(self.info_hud, (0, 0))

        # If we have are hovering over something, render a menu
        if self.hovered or self.selected:
            if self.hovered: obj = self.hovered
            else: obj = self.selected

            # Draw the main area at the bottom of the screen
            if obj['team'] == 'friendly':
                self.image.blit(self.f_hud, (0, 0))
            elif obj['team'] == 'hostile':
                self.image.blit(self.h_hud, (0, 0))
            elif obj['team'] == 'passive':
                self.image.blit(self.p_hud, (0, 0))
        
            # Render the text for the name of the obj
            name = fonts['zrnic48'].render(f"Type: {obj['type']}", True, colors['white'])
            self.image.blit(name, self.imp_coords['name'])

        
        # If, while we have the select menu open, we hover over a different
        # object, render a smaller menu over the hover object
        if self.hovered != None and self.hovered != self.selected:
            ...

    def render(self):
        """
        Description: Render the playing area.
        Parameters: None
        Returns: None
        """
        self.image.fill(colors['black'])
        self.image.blit(images['bigbigmap'], (self.scroll_x-300, self.scroll_y-300))

        self.render_layers()

        self.render_grid()

        self.render_hud()

        self.window.blit(self.image, (0, 0))
