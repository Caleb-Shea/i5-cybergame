import pygame as pyg
import random

import fullmenu_data
from helper_func import *
from game_info import *
from assets import *


class FullMenu():
    def __init__(self):
        """
        Description: A class to represent a full screen type menu. This type of
                     menu is used for the nodes connected directly to the Earth,
                     such as OPS, ACQUISITIONS, and CYBER, among others.
        Parameters: None
        Returns: FullMenu()
        """
        self.window = pyg.display.get_surface()

        # Create the image for the full menu
        self.rect = self.window.get_rect().inflate(-20, -20)
        self.image_base = pyg.Surface(self.rect.size).convert_alpha()
        self.image_base.fill(colors['clear'])
        pyg.draw.rect(self.image_base, colors['rose'], ((0, 0), self.rect.size), 5) # On larger displays this breaks

        # self.image is the surface where everything happens, and self.image_base
        # is the surface that we keep plain for easy redrawing
        self.image = self.image_base.copy()

        # Create tabs
        self.tab_names = ['ACQUISITIONS', 'OPS', 'INTEL', 'CYBER', 'PERSONNEL',
                          'EVENTS']
        self.tab_rects = []
        for i in range(len(self.tab_names)):
            x_size = self.rect.width//len(self.tab_names) - 20
            rect = pyg.rect.Rect(i * x_size, 0, x_size, 50)
            self.tab_rects.append(rect)

        # We must have a selected tab for the first frame of rendering
        self.cur_tab = self.tab_names[0]

        # Tab specific initalization
        # --- Intel tab ---
        self.intel_bg_rect = pyg.rect.Rect(5, 50, 1250, 645)
        self.hovered_brief_id = -1
        self.selected_brief_id = -1
        self.brief_buy_timer = 0
        self.num_briefs_to_show = 8
        self.num_briefs_per_col = (self.rect.height - 200) // 150 + 1
        self.cur_briefs = fullmenu_data.briefs[:self.num_briefs_to_show]
        self.all_briefs = fullmenu_data.briefs[self.num_briefs_to_show:]
        # Create all the rects needed
        self.brief_rects = []
        for i in range(len(self.cur_briefs)):
            size = (360, 100)
            rect = pyg.rect.Rect((0, 0), size)
            self.brief_rects.append(rect)

        # --- Acquisitions tab ---
        self.sats = fullmenu_data.acq_data
        self.hovered_sat = -1
        self.selected_sat = -1
        self.sat_rects = []
        for i in range(9):
            size = (250, 55)
            rect = pyg.rect.Rect((80, 100 + (500/9)*i), size)
            self.sat_rects.append(rect)

        self.acq_bg_rect = pyg.rect.Rect(5, 50, 1250, 645)
        self.acq_sel_rect = pyg.rect.Rect(80, 100, 250, 500)
        self.acq_info_rect = pyg.rect.Rect(380, 100, 800, 500)
        self.acq_pic_rect = pyg.rect.Rect(400, 120, 400, 350)
        self.acq_descbg_rect = pyg.rect.Rect(830, 110, 310, 480)
        self.acq_desc_rect = pyg.rect.Rect(840, 180, 290, 400)
        self.acq_button_rect = pyg.rect.Rect(840, 510, 290, 70)

        # --- Cyber tab ---
        self.cyber_def_level = 1
        self.cyber_off_level = 1

        self.cyber_attr = {'MDef': 0, 'System Monitoring': 0, 'Updates': 0,
                           'Funding': 0, 'White Hat': 0}
        self.cyber_graph_inc = 50

        self.cyber_def_level_cost = 1000
        self.cyber_def_rep_increase = 10

        # Static rects
        self.cyber_def_rect = pyg.rect.Rect(5, 50, 630, 645)
        self.cyber_def_header = pyg.rect.Rect(30, 60, 300, 60)
        self.cyber_def_up_rect = pyg.rect.Rect(215, 590, 300, 60)
        self.cyber_graph_rect = pyg.rect.Rect(25, 150, 580, 400)
        self.cyber_off_rect = pyg.rect.Rect(630, 50, 625, 645)
        self.cyber_off_header = pyg.rect.Rect(930, 60, 300, 60)
        self.cyber_threats_rect = pyg.rect.Rect(20, 150, 580, 480)

        # --- Ops tab ---
        self.ops_bg_rect = pyg.rect.Rect(5, 50, 1250, 645)

        # --- Personnel tab ---
        self.ppl_bg_rect = pyg.rect.Rect(5, 50, 1250, 645)

        # --- Events tab ---
        self.events_bg_rect = pyg.rect.Rect(5, 50, 1250, 645)
        self.events_reel_rect = pyg.rect.Rect(80, 80, 1100, 520)

    def update_intel(self, m_pos, m_pressed, is_click):
        """
        Description: Handle events specific to the intel tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            is_click [bool] -> True on the first frame of a mouseclick event
        Returns: None
        """
        # Set the positions of the brief buttons
        for i, rect in enumerate(self.brief_rects):
            if i%2 == 1:
                rect.x = 200
            else:
                rect.x = 100
            rect.x += i // self.num_briefs_per_col * 420

            rect.y = 150*(i % self.num_briefs_per_col) + 75

        # Handle mouse clicks
        if m_pressed[0]:
            # Check if any briefs have been clicked on
            for i, rect in enumerate(self.brief_rects):
                # We move the rect because the mouse coords are absolute, but the
                # rect coords are based on the topleft of the menu
                if rect.move(10, 10).collidepoint(m_pos):
                    if i == self.selected_brief_id:
                        self.selected_brief_id == -1
                    else:
                        self.selected_brief_id = i

            if self.selected_brief_id == -1: # Do nothing
                pass
            elif self.brief_buy_timer >= 30: # Click and hold to purchase the brief
                self.cur_briefs.pop(self.selected_brief_id)
                if len(self.all_briefs) > 0:
                    self.cur_briefs.append(self.all_briefs.pop(0))
                self.brief_buy_timer = 0
            else:
                self.brief_buy_timer += 1 # Increment timer

        else:
            # If the mouse isn't pressed, reset
            self.selected_brief_id = -1
            self.brief_buy_timer = 0

        # Handle mouse hovering
        self.hovered_brief_id = -1
        for i, rect in zip(range(len(self.cur_briefs)), self.brief_rects):
            if rect.move(10, 10).collidepoint(m_pos):
                self.hovered_brief_id = i

    def render_intel(self):
        """
        Description: Draw the menu for the intel tab.
        Parameters: None
        Returns: None
        """
        # Draw bg
        pyg.draw.rect(self.image, colors['intel_bg'], self.intel_bg_rect)

        # Create buttons for each of the current briefs
        for brief, rect in zip(self.cur_briefs, self.brief_rects):
            # If it's expensive, make it a different color
            if brief['cost'] > 1500:
                c = colors['red']
            else:
                c = colors['darkgray']

            # If a brief is clicked and held, fade to black
            if self.selected_brief_id == self.cur_briefs.index(brief):
                c = colors['intel_bg'].lerp(c, 1 - min(self.brief_buy_timer/30, 1))

            pyg.draw.rect(self.image, c, rect)

            # Draw the text on top of the brief button
            text = fonts['zrnic24'].render(brief['name'], True, colors['starwhite'])
            text_rect = text.get_rect(center=rect.center)
            self.image.blit(text, text_rect)

        # Loop again for the tooltips so they are always on top
        for brief, rect in zip(self.cur_briefs, self.brief_rects):
            # If hovered, draw a tooltip
            if self.hovered_brief_id == self.cur_briefs.index(brief):
                tt = pyg.Surface((250, 250)).convert_alpha()
                ttrect = tt.get_rect()
                ttrect.midleft = rect.midright

                # Set the bg color
                tt.fill(colors['clear'])
                tt.fill(colors['lightgray'], (15, 0, 250 - 15, 250))

                # Draw an arrow pointing towards the brief
                pyg.draw.polygon(tt, colors['lightgray'], [(0 , 125),
                                                           (15, 110),
                                                           (15, 140)])

                # Text
                name = fonts['zrnic24'].render(brief['name'], True, colors['black'])
                p2b = fonts['zrnic24'].render('Click and Hold to Buy', True, colors['black'])
                cost = fonts['zrnic24'].render(f"Cost: {brief['cost']:,}", True, colors['black'])
                desc = word_wrap(brief['desc'], fonts['zrnic20'], colors['black'], ttrect.inflate(-25, 0))

                tt.blit(name, (20, 5))
                tt.blit(p2b, (32, 215))
                tt.blit(cost, (140, 170))
                tt.blit(desc, (20, 50))

                self.image.blit(tt, ttrect)

    def update_acq(self, m_pos, m_pressed, is_click):
        """
        Description: Handle events specific to the acquisitions tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            is_click [bool] -> True on the first frame of a mouseclick event
        Returns: None
        """
        # Detect hovering
        for i, rect in enumerate(self.sat_rects):
            if rect.move(10, 10).collidepoint(m_pos):
                # We move the rect because these rects are not based on the
                # main window
                self.hovered_sat = i
                break
        else:
            self.hovered_sat = -1

        # Detect clicks
        if m_pressed[0]:
            for i, rect in enumerate(self.sat_rects):
                # If we clicked on a rect
                if rect.move(10, 10).collidepoint(m_pos):
                    self.selected_sat = i
                    break
                # Don't deselect the satellite if we clicked on the description
                # or the picture
                if self.acq_descbg_rect.move(10, 10).collidepoint(m_pos):
                    break
                if self.acq_pic_rect.move(10, 10).collidepoint(m_pos):
                    break
            else: # If we didn't break from the loop, deselect
                self.selected_sat = -1

            # If there is a selected satellite
            if self.selected_sat != -1:
                # And we clicked on it
                if is_click:
                    if self.acq_button_rect.move(10, 10).collidepoint(m_pos):
                        new_sat = self.sats[self.selected_sat]
                        # If we have the money, purchase the satellite
                        if game_info['cash'] >= new_sat['money_cost']:
                            game_info['num_sats'] += 1
                            game_info['Acq GPS Level'] += 1
                            game_info['cash'] -= new_sat['money_cost']
                            game_info['sats_owned'].append(new_sat)

                            new_sat['money_cost'] = int(round(new_sat['money_cost'] * 1.15, -1))

    def render_acq(self):
        """
        Description: Draw the menu for the acquisitions tab.
        Parameters: None
        Returns: None
        """
        pyg.draw.rect(self.image, colors['acq_bg'], self.acq_bg_rect)
        pyg.draw.rect(self.image, colors['lightgray'], self.acq_sel_rect)
        pyg.draw.rect(self.image, colors['blue'], self.acq_info_rect)
        pyg.draw.rect(self.image, colors['gray'], self.acq_pic_rect)
        pyg.draw.rect(self.image, colors['lightgray'], self.acq_descbg_rect)

        for i, rect in enumerate(self.sat_rects): # Rects
            # Draw the button itself
            if i==self.hovered_sat or i==self.selected_sat:
                pyg.draw.rect(self.image, colors['yellow'], rect) # Selected color
            else:
                pyg.draw.rect(self.image, colors['orange'], rect) # Unselected color

            # Draw the name of the satellite, and it's level, on it's own button
            sat_name = self.sats[i]['name']
            sat_title = sat_name + " Lvl:" + str(game_info[f'Acq {sat_name} Level'])
            list_text = fonts['zrnic26'].render(sat_title, True, colors['black'])
            self.image.blit(list_text, list_text.get_rect(center=rect.center))

        for i in range(9): # Divider lines
            pyg.draw.line(self.image, colors['lime'],
                         (80, 100 + (500/9)*i), (329, 100 + (500/9)*i), 3)
        # Border
        pyg.draw.rect(self.image, colors['lime'], (80, 100, 250, 500), 3)

        # If there is a selected satellite
        if self.selected_sat != -1:
            cur_sat = self.sats[self.selected_sat] # Get the info for the current satellite
            # Satellite image
            # -- Placeholder text
            pic_text = fonts['zrnic80'].render('SAT PICTURE', True, colors['black'])
            self.image.blit(pic_text, pic_text.get_rect(center=self.acq_pic_rect.center))

            # Name
            name_text = fonts['zrnic42'].render(cur_sat['name'], True, colors['black'])
            self.image.blit(name_text, (840, 115))

            # Draw a line under the name
            pyg.draw.line(self.image, colors['cyan'], (835, 170), (1135, 170), 3)

            # Description
            desc = word_wrap(cur_sat['desc'], fonts['zrnic30'],
                             colors['black'], self.acq_desc_rect)
            self.image.blit(desc, self.acq_desc_rect)

            # Buy button
            pyg.draw.rect(self.image, colors['pink'], self.acq_button_rect)

            # Cost of satellite
            cash_cost = fonts['zrnic26'].render(f"Purchase: {self.sats[self.selected_sat]['money_cost']:,}", True, colors['black'])
            self.image.blit(cash_cost, cash_cost.get_rect(center=self.acq_button_rect.center))

    def update_cyber(self, m_pos, m_pressed, is_click):
        """
        Description: Handle events specific to the cyber tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            is_click [bool] -> True on the first frame of a mouseclick event
        Returns: None
        """
        # Tooltip rendering
        if self.cyber_def_up_rect.move(10, 10).collidepoint(m_pos):
            # Show a tooltip for upgrading defence
            self.cyber_inflate_def_up = True

        elif not self.cyber_def_up_rect.inflate(80, 60).move(10, -20).collidepoint(m_pos):
            # Hide the tooltip when the mouse leaves the inflated rect
            self.cyber_inflate_def_up = False

        def upgrade_random_attr():
            """
            We call this chunk of code twice, so this function exists to cut
            down on repeated code.
            """
            # Upgrade defensive capabilities
            self.cyber_def_level += 1
            game_info['Cyber Def Level'] += 1
            game_info['reputation'] += self.cyber_def_rep_increase
            game_info['cash'] -= self.cyber_def_level_cost

            # Choose a random attribute to level up
            attr = random.choice(list(self.cyber_attr.keys()))
            # attr = list(self.cyber_attr.keys())[1]
            self.cyber_attr[attr] += 1

            # Increase the cost of future upgrades
            self.cyber_def_level_cost = int(round(self.cyber_def_level_cost * 1.2, -1))

        # If the user clicks
        if m_pressed[0] and is_click:
            # And clicks on the defensive upgrade button
            if self.cyber_inflate_def_up:
                if self.cyber_def_up_rect.inflate(80, 60).move(10, -20).collidepoint(m_pos):
                    # And has the available resources
                    if game_info['cash'] >= self.cyber_def_level_cost:
                        upgrade_random_attr()
            else:
                if self.cyber_def_up_rect.collidepoint(m_pos):
                    # And has the available resources
                    if game_info['cash'] >= self.cyber_def_level_cost:
                        upgrade_random_attr()

        # Adjust graph increment if necessary
        max_attr = max(list(self.cyber_attr.values()))
        if max_attr > 6:
            # 6 levels is the point when the default increment exceeds the
            # graph area. Use // so the max bar height is variable
            self.cyber_graph_inc = 300 // max_attr

    def render_cyber(self):
        """
        Description: Draw the menu for the cyber tab.
        Parameters: None
        Returns: None
        """
        # Draw bg
        pyg.draw.rect(self.image, colors['def_cyber_bg'], self.cyber_def_rect)
        pyg.draw.rect(self.image, colors['off_cyber_bg'], self.cyber_off_rect)

        # Draw header text
        def_header = fonts['zrnic36'].render('DEFENSIVE', True, colors['babygreen'])
        off_header = fonts['zrnic36'].render('OFFENSIVE', True, colors['babyblue'])
        self.image.blit(def_header, def_header.get_rect(midleft=self.cyber_def_header.midleft))
        self.image.blit(off_header, off_header.get_rect(midright=self.cyber_off_header.midright))

        # Draw capability levels
        def_level = fonts['zrnic26'].render(f'Level: {self.cyber_def_level}', True, colors['babygreen'])
        off_level = fonts['zrnic26'].render(f'Level: {self.cyber_off_level}', True, colors['babyblue'])
        self.image.blit(def_level, def_level.get_rect(midright=self.cyber_def_header.midright))
        self.image.blit(off_level, off_level.get_rect(midleft=self.cyber_off_header.midleft))

        # Draw header underline
        pyg.draw.line(self.image, colors['babygreen'], self.cyber_def_header.bottomleft, self.cyber_def_header.bottomright, 5)
        pyg.draw.line(self.image, colors['babyblue'], self.cyber_off_header.bottomleft, self.cyber_off_header.bottomright, 5)

        # --- Defensive ---
        # pyg.draw.rect(self.image, colors['babygreen'], self.cyber_threats_rect)

        # Draw bar graph background
        pyg.draw.rect(self.image, colors['lightgray'], self.cyber_graph_rect)

        # Draw unit lines for the graph
        for y in range(self.cyber_graph_rect.height//self.cyber_graph_inc + 1):
            pyg.draw.line(self.image, colors['babygreen'],
                         (self.cyber_graph_rect.left, self.cyber_graph_rect.bottom-y*self.cyber_graph_inc),
                         (self.cyber_graph_rect.right, self.cyber_graph_rect.bottom-y*self.cyber_graph_inc))

        # Draw the bars
        for i, attr in enumerate(list(self.cyber_attr.keys())):
            # Get coords of each bar
            x = 120 + 100*i
            y = self.cyber_graph_inc * self.cyber_attr[attr]

            # Create and draw a rect that holds the bounds of each bar
            rect = pyg.rect.Rect(x-20, self.cyber_graph_rect.bottom-y, 50, y)
            pyg.draw.rect(self.image, colors['ddarkgray'], rect)

            # Render the bar title that goes on top of each bar
            text = fonts['zrnic16'].render(str(attr), True, colors['black'])
            text = pyg.transform.rotate(text, 45)
            self.image.blit(text, text.get_rect(bottomleft=(rect.x, self.cyber_graph_rect.bottom-y)))

        # Draw the graph border
        pyg.draw.rect(self.image, colors['white'], self.cyber_graph_rect.inflate(14, 14), 7)

        # Draw upgrade button
        if self.cyber_inflate_def_up:
            # Draw an enlarged button that has more information
            pyg.draw.rect(self.image, colors['red'], self.cyber_def_up_rect.inflate(80, 60).move(0, -30))
            # Draw text
            def_up_text = fonts['zrnic24'].render('Upgrade Defense', True, colors['black'])
            self.image.blit(def_up_text, def_up_text.get_rect(midtop=self.cyber_def_up_rect.move(0, -55).midtop))

            # Purchase info
            info_text = fonts['zrnic20'].render(f'${self.cyber_def_level_cost:,} -> {self.cyber_def_rep_increase:,} Rep', True, colors['black'])
            self.image.blit(info_text, info_text.get_rect(center=self.cyber_def_up_rect.center))
        else:
            # Draw a normal upgrade button
            pyg.draw.rect(self.image, colors['red'], self.cyber_def_up_rect)
            # Upgrade text
            def_up_text = fonts['zrnic26'].render('Upgrade Defense', True, colors['black'])
            self.image.blit(def_up_text, def_up_text.get_rect(center=self.cyber_def_up_rect.center))

    def update_ops(self, m_pos, m_pressed, is_click):
        """
        Description: Handle events specific to the ops tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            is_click [bool] -> True on the first frame of a mouseclick event
        Returns: None
        """
        ...

    def render_ops(self):
        """
        Description: Draw the menu for the operations tab.
        Parameters: None
        Returns: None
        """
        placeholder = fonts['zrnic80'].render('UNDER CONSTRUCTION', True, colors['black'])
        placeholder_rect = placeholder.get_rect(center=self.rect.center).inflate(40, 40)
        pyg.draw.rect(self.image, colors['babyblue'], placeholder_rect)
        self.image.blit(placeholder, placeholder_rect.move(20, 20))

    def update_personnel(self, m_pos, m_pressed, is_click):
        """
        Description: Handle events specific to the personnel tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            is_click [bool] -> True on the first frame of a mouseclick event
        Returns: None
        """
        ...

    def render_personnel(self):
        """
        Description: Draw the menu for the personnel tab.
        Parameters: None
        Returns: None
        """
        placeholder = fonts['zrnic80'].render('UNDER CONSTRUCTION', True, colors['black'])
        placeholder_rect = placeholder.get_rect(center=self.rect.center).inflate(40, 40)
        pyg.draw.rect(self.image, colors['lightgray'], placeholder_rect)
        self.image.blit(placeholder, placeholder_rect.move(20, 20))

    def update_events(self, m_pos, m_pressed, is_click):
        """
        Description: Handle events specific to the events tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            is_click [bool] -> True on the first frame of a mouseclick event
        Returns: None
        """
        ...

    def render_events(self):
        """
        Description: Draw the menu for the events tab.
        Parameters: None
        Returns: None
        """
        # Draw background
        pyg.draw.rect(self.image, colors['events_bg'], self.events_bg_rect)

        # Draw newsreel bg
        pyg.draw.rect(self.image, colors['events_reel'], self.events_reel_rect)

        # Draw each seen reel to the screen
        for i, reel in enumerate(reversed(game_info['Reels Seen'])):
            rect = pyg.rect.Rect(self.events_reel_rect.inflate(-40, -40).x,
                                 self.events_reel_rect.inflate(-40, -40).y + 50*i,
                                 self.events_reel_rect.inflate(-40, -40).width, 50)

            # If we are about to draw a reel that goes past the alloted space,
            # don't render it. Also break for efficiency
            if rect.bottom > self.events_reel_rect.bottom:
                break

            # If it's a special reel, color the bg differently
            if reel['has_menu_highlight'] == 'True':
                pyg.draw.rect(self.image, colors['sand'], rect)
                pyg.draw.line(self.image, colors['black'], rect.topleft, rect.topright, 2)

            # Draw a line separating each reel
            pyg.draw.line(self.image, colors['black'], rect.bottomleft, rect.bottomright, 2)

            # Render and draw the text that goes in each rect
            text = fonts['zrnic30'].render(reel['event'], True, colors['black'])
            self.image.blit(text, text.get_rect(center=rect.center))

            # Render a timestamp in the bottom right corner
            timestamp = fonts['zrnic16'].render(reel['Date Seen'].strftime("%d %B"), True, colors['gray'])
            self.image.blit(timestamp, timestamp.get_rect(bottomright=rect.move(-5, -2).bottomright))

        # Draw border around the newsreel
        pyg.draw.rect(self.image, colors['red_sand'], self.events_reel_rect, 20)

    def update(self, is_click=False):
        """
        Description: Detect mouse clicks and update active tab.
        Parameters:
            is_click [bool] -> True if this function is being called because of
                               a mouse click, false otherwise
        Returns: None
        """
        m_pos = pyg.mouse.get_pos()
        m_pressed = pyg.mouse.get_pressed()

        # Tracker to keep track if we have moved on to a rect that is right of
        # the currently selected tab
        right_of_sel = False

        # Switch tabs if the mouse clicks on one
        for rect, name in zip(self.tab_rects, self.tab_names):
            # If a tab is clicked on, select it
            # We move the rect because the mouse coords are absolute, but the
            # rect coords are based on the topleft of the menu
            if self.cur_tab == name:
                # The selected tab has a larger rect that is moved slightly to
                # the right, so the mouse collisions must reflect that
                cur_rect = rect.inflate(20*len(self.tab_rects), 0).move(10*len(self.tab_rects), 0).move(10, 10)

                # If the user clicked on the current tab, don't do anything
                if cur_rect.collidepoint(m_pos) and m_pressed[0]:
                    break

                # Update the position tracker
                right_of_sel = True
            else:
                # Move all collision rects to the right once we've passed the
                # larger selected rect
                if right_of_sel:
                    rect = rect.move(20*len(self.tab_rects), 0)
                # If the user clicks on a different tab, switch to it
                if rect.move(10, 10).collidepoint(m_pos) and m_pressed[0]:
                    self.cur_tab = name
                    break

        # Handle tab specific updates
        # Pass mouse info so we don't have to get it more than once a frame
        if self.cur_tab == 'INTEL':
            self.update_intel(m_pos, m_pressed, is_click)
        elif self.cur_tab == 'ACQUISITIONS':
            self.update_acq(m_pos, m_pressed, is_click)
        elif self.cur_tab == 'CYBER':
            self.update_cyber(m_pos, m_pressed, is_click)
        elif self.cur_tab == 'OPS':
            self.update_ops(m_pos, m_pressed, is_click)
        elif self.cur_tab == 'PERSONNEL':
            self.update_personnel(m_pos, m_pressed, is_click)
        elif self.cur_tab == 'EVENTS':
            self.update_events(m_pos, m_pressed, is_click)

    def render_tabs(self):
        """
        Description: Draw the tabs at the top of the screen.
        Parameters: None
        Returns: None
        """
        # Tracker to keep track if we have moved on to a rect that is right of
        # the currently selected tab
        right_of_sel = False
        for rect, name in zip(self.tab_rects, self.tab_names):
            # Draw the tabs, highlighting the selected one
            if self.cur_tab == name:
                # We want the selected tab to be bigger than the others
                rect = rect.inflate(20*len(self.tab_rects), 0).move(10*len(self.tab_rects), 0)

                # Update position tracker
                right_of_sel = True

                pyg.draw.rect(self.image, colors['darkgray'], rect)
            else:
                # Due to the larger selected tab, we must move all the tabs that
                # are right of the tab over
                if right_of_sel:
                    rect = rect.move(20*len(self.tab_rects), 0)

                pyg.draw.rect(self.image, colors['gray'], rect)

            # Draw the text on top of the tab
            text = fonts['zrnic30'].render(name, True, colors['starwhite'])
            self.image.blit(text, text.get_rect(center=rect.center))

            # Draw divider lines
            pyg.draw.line(self.image, colors['darkgray'], (rect.right-1, 0), (rect.right-1, 50))

    def render(self):
        """
        Description: Render this menu on the screen, then render any tab
                     specific elements to the screen.
        Parameters: None
        Returns: None
        """
        # Clear the image of anything tab specific so objects don't persist
        self.image = self.image_base.copy()

        self.render_tabs()
        # Render everything to self.image
        if self.cur_tab == 'INTEL':
            self.render_intel()
        elif self.cur_tab == 'ACQUISITIONS':
            self.render_acq()
        elif self.cur_tab == 'CYBER':
            self.render_cyber()
        elif self.cur_tab == 'OPS':
            self.render_ops()
        elif self.cur_tab == 'PERSONNEL':
            self.render_personnel()
        elif self.cur_tab == 'EVENTS':
            self.render_events()

        # Blit to the screen
        self.window.blit(self.image, self.rect)
