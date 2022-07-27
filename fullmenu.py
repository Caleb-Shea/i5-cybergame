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
        self.briefs = fullmenu_data.intel_briefs
        self.hovered_brief = -1
        self.selected_brief = -1
        self.brief_rects = []
        for i in range(len(self.briefs)):
            x = 50
            y = 80 + 100*i
            # 2nd column
            if y+100 > self.rect.bottom:
                y -= self.rect.height - 100
                x = 660
            # Break once we're out of screen
            if y+100 > self.rect.bottom and x == 660:
                break

            rect = pyg.rect.Rect((x, y), (550, 70))
            self.brief_rects.append(rect)

        self.intel_bg_rect = pyg.rect.Rect(5, 50, 1250, 645)

        # --- Acquisitions tab ---
        self.sats = fullmenu_data.acq_data
        self.hovered_sat = -1
        self.selected_sat = -1
        self.sat_rects = []
        for i in range(len(self.sats)):
            rect = pyg.rect.Rect((80, 100 + (500/len(self.sats))*i), (250, 55))
            self.sat_rects.append(rect)

        self.acq_bg_rect = pyg.rect.Rect(5, 50, 1250, 645)
        self.acq_sel_rect = pyg.rect.Rect(80, 100, 250, 500)
        self.acq_info_rect = pyg.rect.Rect(380, 100, 800, 500)
        self.acq_pic_rect = pyg.rect.Rect(400, 120, 400, 350)
        self.acq_descbg_rect = pyg.rect.Rect(830, 110, 310, 480)
        self.acq_desc_rect = pyg.rect.Rect(840, 180, 290, 400)
        self.acq_button_rect = pyg.rect.Rect(840, 510, 290, 70)
        self.acq_stats_rect = pyg.rect.Rect(400, 485, 400, 100)

        # --- Cyber tab ---
        self.cyber_def_level = 0
        self.cyber_off_level = 0

        self.cyber_attr = {'MDef': 0, 'System Monitoring': 0, 'Updates': 0,
                           'Funding': 0, 'White Hat': 0}
        self.cyber_graph_inc = 50

        self.cyber_def_level_cost = 1000
        self.cyber_def_rep_increase = 10

        self.cyber_map_rect = pyg.rect.Rect(650, 150, 550, 380)
        self.cyber_map = pyg.Surface(self.cyber_map_rect.size)
        self.cyber_map.blit(images['world_map'], (0, 0))

        self.cyber_def_rect = pyg.rect.Rect(5, 50, 630, 645)
        self.cyber_def_header = pyg.rect.Rect(30, 60, 300, 60)
        self.cyber_def_up_rect = pyg.rect.Rect(215, 590, 300, 60)
        self.cyber_graph_rect = pyg.rect.Rect(25, 150, 580, 400)
        self.cyber_off_rect = pyg.rect.Rect(630, 50, 625, 645)
        self.cyber_off_header = pyg.rect.Rect(930, 60, 300, 60)

        # --- Ops tab ---
        self.ops_bg_rect = pyg.rect.Rect(5, 50, 1250, 645)

        self.ops_map_rect = pyg.rect.Rect(80, 80, 1100, 540)
        self.ops_map = pyg.Surface(self.ops_map_rect.size)
        self.ops_map.blit(images['world_map_big'], (0, 0))

        self.ops_map_targets = []
        self.ops_map_hitlist = [(200, 260), (360, 250), # North America
                                (335, 480), (380, 370), # South America
                                (565, 225), # Europe
                                (650, 340), # Africa
                                (690, 235), (820, 315), (1000, 255)] # Asia

        # --- Personnel tab ---
        self.ppl_bg_rect = pyg.rect.Rect(5, 50, 1250, 645)

        self.ppl_bar_rect = pyg.rect.Rect(50, 120, 910, 200)
        self.ppl_bar = pyg.Surface(self.ppl_bar_rect.size)

        # Legend objects
        self.ppl_legend_rect = pyg.rect.Rect(980, 120, 230, 200)
        self.ppl_legend = pyg.Surface(self.ppl_legend_rect.size)
        self.ppl_legend.fill(colors['pink'])

        # Create the legend for the bar
        for i, job in enumerate(list(game_info['Staff Assignments'].keys())):
            # Draw the color for each job
            job_color = colors[f'ppl_legend_{job}']
            rect = pyg.rect.Rect(10, 10 + 40*i, 20, 20)

            pyg.draw.rect(self.ppl_legend, job_color, rect)

            # Draw the text for each job
            text = fonts['zrnic20'].render(job, True, colors['black'])
            self.ppl_legend.blit(text, rect.move(30, -2))

        # Hiring menu
        self.ppl_hiring_rect = pyg.rect.Rect(60, 350, 700, 280)
        self.ppl_hiring = pyg.Surface(self.ppl_hiring_rect.size)

        self.ppl_hiring_selecter = pyg.Surface((200, 280))
        self.ppl_hiring_selecter.fill(colors['white'])

        self.ppl_hiring_pic = pyg.Surface((300, 280))
        self.ppl_hiring_pic.fill(colors['gray'])
        # Pic placeholder text
        text = fonts['zrnic48'].render('PICTURE', True, colors['deepblue'])
        self.ppl_hiring_pic.blit(text, text.get_rect(center=(150, 140)))

        self.ppl_hiring_info = pyg.Surface((200, 280))
        self.ppl_hiring_info.fill(colors['darkgray'])

        self.ppl_hiring.blit(self.ppl_hiring_selecter, (0, 0))
        self.ppl_hiring.blit(self.ppl_hiring_pic, (200, 0))
        self.ppl_hiring.blit(self.ppl_hiring_info, (500, 0))

        # Picture
        self.ppl_pic_rect = pyg.rect.Rect(780, 360, 410, 260)
        self.ppl_pic = pyg.Surface(self.ppl_pic_rect.size)
        self.ppl_pic.fill(colors['ddarkgray'])

        # Placeholder text
        text = fonts['zrnic48'].render('PICTURE', True, colors['lightgray'])
        cent = (self.ppl_pic_rect.width//2, self.ppl_pic_rect.height//2)
        self.ppl_pic.blit(text, text.get_rect(center=cent))

        # --- Events tab ---
        self.events_bg_rect = pyg.rect.Rect(5, 50, 1250, 645)
        self.events_reel_rect = pyg.rect.Rect(80, 80, 1100, 520)

        self.events_scroll = 0

    def update_intel(self, m_pos, m_pressed, button):
        """
        Description: Handle events specific to the intel tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            button [int/None] -> The id of mouse button pressed. Only passes the
                                 button on the first frame
        Returns: None
        """
        # Detect hovering
        for i, rect in enumerate(self.brief_rects):
            if rect.move(10, 10).collidepoint(m_pos):
                # We move the rect because these rects are not based on the
                # main window
                self.hovered_brief = i
                break
        else:
            self.hovered_brief = -1

        # Detect clicks
        if m_pressed[0]:
            for i, rect in enumerate(self.brief_rects):
                if abs(self.selected_brief - i) == 1:
                    continue
                # If we clicked on a rect
                if rect.move(10, 10).collidepoint(m_pos):
                    self.selected_brief = i
                    break
            else: # If we didn't break from the loop, deselect
                self.selected_brief = -1

    def render_intel(self):
        """
        Description: Draw the menu for the intel tab.
        Parameters: None
        Returns: None
        """
        # Draw bg
        pyg.draw.rect(self.image, colors['intel_bg'], self.intel_bg_rect)

        # Draw each brief
        sel_rect = None
        sel_brief = None
        for i, rect in enumerate(self.brief_rects): # Rects
            if i == self.selected_brief: # Selected rect
                sel_rect = rect.inflate(0, 200)
                sel_brief = self.briefs[i]
            elif i == self.hovered_brief:
                pyg.draw.rect(self.image, colors['purple'], rect) # Hovered color
            else:
                pyg.draw.rect(self.image, colors['pink'], rect) # Unselected color

            # Draw the name
            name = fonts['zrnic32'].render(self.briefs[i]['name'], True, colors['black'])
            self.image.blit(name, name.get_rect(center=rect.center))

        # Draw the selected rect after the other rects so it's on top
        if sel_rect != None:
            pyg.draw.rect(self.image, colors['purple'], sel_rect)

            # Attend button
            sel_buy = pyg.rect.Rect(0, 0, 530, 50)
            sel_buy.bottom = sel_rect.bottom - 10
            sel_buy.centerx = sel_rect.centerx
            pyg.draw.rect(self.image, colors['red'], sel_buy)

            # Attend text
            attend = fonts['zrnic26'].render('Attend Brief', True, colors['black'])
            self.image.blit(attend, attend.get_rect(center=sel_buy.center))

            # Render brief name
            name = fonts['zrnic32'].render(sel_brief['name'], True, colors['black'])
            self.image.blit(name, name.get_rect(center=sel_rect.center))

    def update_acq(self, m_pos, m_pressed, button):
        """
        Description: Handle events specific to the acquisitions tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            button [int/None] -> The id of mouse button pressed. Only passes the
                                 button on the first frame
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
                # or the picture or the stats graphic
                if self.acq_descbg_rect.move(10, 10).collidepoint(m_pos):
                    break
                if self.acq_pic_rect.move(10, 10).collidepoint(m_pos):
                    break
                if self.acq_stats_rect.move(10, 10).collidepoint(m_pos):
                    break
            else: # If we didn't break from the loop, deselect
                self.selected_sat = -1

            # If there is a selected satellite
            if self.selected_sat != -1:
                # And we clicked on it
                if button != None:
                    if self.acq_button_rect.move(10, 10).collidepoint(m_pos):
                        new_sat = self.sats[self.selected_sat]
                        # If we have the money, purchase the satellite
                        if game_info['cash'] >= new_sat['money_cost']:
                            game_info['num_sats'] += 1
                            game_info[f'Acq {new_sat["name"]} Level'] += 1
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

            # Stats
            pyg.draw.rect(self.image, colors['cyan'], self.acq_stats_rect)

            # Buy button
            pyg.draw.rect(self.image, colors['pink'], self.acq_button_rect)

            # Cost of satellite
            cash_cost = fonts['zrnic26'].render(f"Purchase: {self.sats[self.selected_sat]['money_cost']:,}", True, colors['black'])
            self.image.blit(cash_cost, cash_cost.get_rect(center=self.acq_button_rect.center))

    def update_cyber(self, m_pos, m_pressed, button):
        """
        Description: Handle events specific to the cyber tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            button [int/None] -> The id of mouse button pressed. Only passes the
                                 button on the first frame
        Returns: None
        """
        # --- Defensive ---
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
        if button == 1:
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

        # --- Offensive ---
        if button == 3:
            self.cyber_map.blit(images['world_map_NA'], (0, 0))

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

        # --- Offensive ---
        self.image.blit(self.cyber_map, self.cyber_map_rect)

    def update_ops(self, m_pos, m_pressed, button):
        """
        Description: Handle events specific to the ops tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            button [int/None] -> The id of mouse button pressed. Only passes the
                                 button on the first frame
        Returns: None
        """
        if button == 3:
            self.ops_map_targets.append(random.choice(self.ops_map_hitlist))

    def render_ops(self):
        """
        Description: Draw the menu for the operations tab.
        Parameters: None
        Returns: None
        """
        # Draw bg
        pyg.draw.rect(self.image, colors['ops_bg'], self.ops_bg_rect)

        # Render the map
        self.image.blit(self.ops_map, self.ops_map_rect)

        # Render markers for available points
        for point in self.ops_map_targets:
            self.image.blit(images['map_marker'], point)

    def update_personnel(self, m_pos, m_pressed, button):
        """
        Description: Handle events specific to the personnel tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            button [int/None] -> The id of mouse button pressed. Only passes the
                                 button on the first frame
        Returns: None
        """
        ...

    def render_personnel(self):
        """
        Description: Draw the menu for the personnel tab.
        Parameters: None
        Returns: None
        """
        # Draw bg
        pyg.draw.rect(self.image, colors['ppl_bg'], self.ppl_bg_rect)

        # Render the legend
        self.image.blit(self.ppl_legend, self.ppl_legend_rect)

        # Draw a bar for each job that is proportional to the amount of people
        # assigned to that specific job
        start_x = 0
        for job in list(game_info['Staff Assignments'].keys()):
            job_color = colors[f'ppl_legend_{job}']

            # Calculate the width of the segment that represents one job
            width = game_info['Staff Assignments'][job]/game_info['num_personnel']*self.ppl_bar_rect.width

            # Add 2 to the width to prevent round-error gaps between bars
            rect = pyg.rect.Rect(start_x, 0, width + 2, self.ppl_bar_rect.height)
            pyg.draw.rect(self.ppl_bar, job_color, rect)

            # Draw the number of people currently assigned to a job
            text = fonts['zrnic20'].render(f"{game_info['Staff Assignments'][job]} People", True, colors['black'])
            self.ppl_bar.blit(text, text.get_rect(center=rect.center))

            # Keep track of where the next segment should start
            start_x += width

        # Render the finished bar graph
        self.image.blit(self.ppl_bar, self.ppl_bar_rect)

        # Render hiring menu
        self.image.blit(self.ppl_hiring, self.ppl_hiring_rect)

        # Render the picture
        self.image.blit(self.ppl_pic, self.ppl_pic_rect)

    def update_events(self, m_pos, m_pressed, button):
        """
        Description: Handle events specific to the events tab.
        Parameters:
            m_pos [tuple] -> The current position of the mouse
            m_pressed [tuple] -> Contains booleans that represent the mouse
                                 buttons
            button [int/None] -> The id of mouse button pressed. Only passes the
                                 button on the first frame
        Returns: None
        """
        # Handle scrolling for all the different events
        if button == 4:
            self.events_scroll = min(self.events_scroll + 50, 0)
        elif button == 5:
            self.events_scroll = max(self.events_scroll - 50, -50*(len(game_info['Reels Seen'])-1))

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
            rect = pyg.rect.Rect(self.events_reel_rect.inflate(-40, 0).x,
                                 self.events_reel_rect.inflate(0, -40).y + 50*i + self.events_scroll,
                                 self.events_reel_rect.inflate(-40, 0).width, 50)

            # If we are about to draw a reel that goes past the alloted space,
            # don't render it. Also break for efficiency
            if rect.bottom > self.events_reel_rect.bottom:
                break
            if rect.top < self.events_reel_rect.top:
                continue

            # If it's a special reel, color the bg differently
            if reel['has_menu_highlight'] == 'True':
                pyg.draw.rect(self.image, colors['sand'], rect)

            # Draw a line separating each reel
            pyg.draw.line(self.image, colors['black'], rect.topleft, rect.topright, 2)
            pyg.draw.line(self.image, colors['black'], rect.bottomleft, rect.bottomright, 2)

            # Render and draw the text that goes in each rect
            text = fonts['zrnic30'].render(reel['event'], True, colors['black'])
            self.image.blit(text, text.get_rect(center=rect.center))

            # Render a timestamp in the bottom right corner
            timestamp = fonts['zrnic16'].render(reel['Date Seen'].strftime("%d %B"), True, colors['gray'])
            self.image.blit(timestamp, timestamp.get_rect(bottomright=rect.move(-5, -2).bottomright))

        # Draw border around the newsreel
        pyg.draw.rect(self.image, colors['red_sand'], self.events_reel_rect, 20)

    def update(self, button=None):
        """
        Description: Detect mouse clicks and update active tab.
        Parameters:
            button [int/None] -> The id of mouse button pressed. Only passes the
                                 button on the first frame
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
            self.update_intel(m_pos, m_pressed, button)
        elif self.cur_tab == 'ACQUISITIONS':
            self.update_acq(m_pos, m_pressed, button)
        elif self.cur_tab == 'CYBER':
            self.update_cyber(m_pos, m_pressed, button)
        elif self.cur_tab == 'OPS':
            self.update_ops(m_pos, m_pressed, button)
        elif self.cur_tab == 'PERSONNEL':
            self.update_personnel(m_pos, m_pressed, button)
        elif self.cur_tab == 'EVENTS':
            self.update_events(m_pos, m_pressed, button)

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
                # We use self.tab_rects to allow for flexibility with new tabs
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
