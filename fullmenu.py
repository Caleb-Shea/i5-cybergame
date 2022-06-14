import pygame as pyg

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
        self.image = self.image_base

        # Create tabs
        self.tab_names = ['ACQUISITIONS', 'OPS', 'INTEL', 'CYBER', 'PERSONNEL',
                          'EVENTS']
        self.tab_rects = []
        for i in range(len(self.tab_names)):
            x_size = self.rect.width//len(self.tab_names)
            rect = pyg.rect.Rect(i * x_size, 0, x_size, 50)
            self.tab_rects.append(rect)

        self.cur_tab = self.tab_names[1]

        self.channel = pyg.mixer.find_channel()

        # Tab specific initalization
        # --- Intel tab ---
        self.intel_bg_rect = pyg.rect.Rect(5, 52, 1250, 645)
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
        self.sats = fullmenu_data.sats
        self.hovered_sat = -1
        self.selected_sat = -1
        self.sat_rects = []
        for i in range(9):
            size = (250, 55)
            rect = pyg.rect.Rect((100, 100 + (500/9)*i), size)
            self.sat_rects.append(rect)

        # Static rects that only need to be made once
        self.acq_bg_rect = pyg.rect.Rect(5, 52, 1250, 645)
        self.acq_sel_rect = pyg.rect.Rect(100, 100, 250, 500)
        self.acq_info_rect = pyg.rect.Rect(380, 100, 800, 500)
        self.acq_pic_rect = pyg.rect.Rect(400, 150, 400, 400)
        self.acq_descbg_rect = pyg.rect.Rect(830, 110, 310, 480)
        self.acq_desc_rect = pyg.rect.Rect(840, 180, 290, 400)
        self.acq_button_rect = pyg.rect.Rect(840, 510, 290, 70)

        # --- Cyber tab ---
        self.cyber_def_rect = pyg.rect.Rect(5, 52, 630, 645)
        self.cyber_off_rect = pyg.rect.Rect(630, 52, 625, 645)
        self.cyber_def_header = pyg.rect.Rect(30, 60, 300, 70)
        self.cyber_off_header = pyg.rect.Rect(930, 60, 300, 70)

        # --- Ops tab ---

        # --- Personnel tab ---

        # --- Events tab ---


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
                if rect.move(10, 10).collidepoint(m_pos):
                    self.selected_sat = i
                    break
                if self.acq_descbg_rect.move(10, 10).collidepoint(m_pos):
                    break
                if self.acq_pic_rect.move(10, 10).collidepoint(m_pos):
                    break
            else:
                self.selected_sat = -1

            if self.selected_sat != -1:
                if is_click:
                    if self.acq_button_rect.move(10, 10).collidepoint(m_pos):
                        new_sat = self.sats[self.selected_sat]

                        game_info['num_sats'] += 1
                        game_info['cash'] -= new_sat['money_cost']
                        game_info['sats_owned'].append(new_sat)

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
            if i == self.hovered_sat or i == self.selected_sat:
                pyg.draw.rect(self.image, colors['yellow'], rect)
            else:
                pyg.draw.rect(self.image, colors['orange'], rect)

            # Draw the name of the satellite on it's own button
            list_text = fonts['zrnic26'].render(self.sats[i]['name'], True, colors['black'])
            self.image.blit(list_text, list_text.get_rect(center=rect.center))

        for i in range(9): # Divider lines
            pyg.draw.line(self.image, colors['lime'],
                         (100, 100 + (500/9)*i), (349, 100 + (500/9)*i), 3)
        # Border
        pyg.draw.rect(self.image, colors['lime'], (100, 100, 250, 500), 3)


        if self.selected_sat != -1: # If there is a selected satellite
            cur_sat = self.sats[self.selected_sat] # Get the info for the current satellite
            # Satellite image
            # Placeholder text
            pic_text = fonts['zrnic80'].render('SAT PICTURE', True, colors['black'])
            self.image.blit(pic_text, (420, 300))

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
        ...

    def render_cyber(self):
        """
        Description: Draw the menu for the cyber tab.
        Parameters: None
        Returns: None
        """
        # Draw bg
        pyg.draw.rect(self.image, colors['def_cyber_bg'], self.cyber_def_rect)
        pyg.draw.rect(self.image, colors['off_cyber_bg'], self.cyber_off_rect)
        # pyg.draw.rect(self.image, colors['babygreen'], self.cyber_def_header)
        # pyg.draw.rect(self.image, colors['babyblue'], self.cyber_off_header)

        def_header = fonts['zrnic36'].render('DEFENSIVE', True, colors['babygreen'])
        off_header = fonts['zrnic36'].render('OFFENSIVE', True, colors['babyblue'])

        self.image.blit(def_header, def_header.get_rect(midleft=self.cyber_def_header.midleft))
        self.image.blit(off_header, off_header.get_rect(midright=self.cyber_off_header.midright))

        pyg.draw.line(self.image, colors['babygreen'], self.cyber_def_header.bottomleft, self.cyber_def_header.bottomright, 5)
        pyg.draw.line(self.image, colors['babyblue'], self.cyber_off_header.bottomleft, self.cyber_off_header.bottomright, 5)


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
        placeholder = fonts['zrnic80'].render('UNDER CONSTRUCTION', True, colors['black'])
        placeholder_rect = placeholder.get_rect(center=self.rect.center).inflate(40, 40)
        pyg.draw.rect(self.image, colors['gray'], placeholder_rect)
        self.image.blit(placeholder, placeholder_rect.move(20, 20))

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

        # Switch tabs if the mouse clicks on one
        for rect, name in zip(self.tab_rects, self.tab_names):
            # If a tab is clicked on, select it
            # We move the rect because the mouse coords are absolute, but the
            # rect coords are based on the topleft of the menu
            if rect.move(10, 10).collidepoint(m_pos) and m_pressed[0]:
                self.cur_tab = name

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
        for rect, name in zip(self.tab_rects, self.tab_names):
            # Draw the tabs, highlighting the selected one
            if self.cur_tab == name:
                pyg.draw.rect(self.image, colors['darkgray'], rect)
            else:
                pyg.draw.rect(self.image, colors['gray'], rect)

            # Draw the text on top of the tab
            text = fonts['zrnic30'].render(name, True, colors['starwhite'])
            text_rect = text.get_rect(center=rect.center)
            self.image.blit(text, text_rect)

        # Draw lines separating each tab
        size = self.rect.width//len(self.tab_names)
        pyg.draw.line(self.image, colors['black'], (0, 50), (self.rect.right, 50))
        for i in range(1, len(self.tab_names)):
            pyg.draw.line(self.image, colors['darkgray'], (i*size, 0), (i*size, 50))

        # Draw a line under all the tabs
        pyg.draw.line(self.image, colors['ddarkgray'], (5, 52), (1254, 52), 5)

    def render(self):
        """
        Description: Render this menu on the screen, then render any tab
                     specific elements to the screen.
        Parameters: None
        Returns: None
        """
        # Clear the image of anything tab specific so objects don't persist
        self.image = self.image_base.copy()

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

        self.render_tabs()

        # Blit to the screen
        self.window.blit(self.image, self.rect)
