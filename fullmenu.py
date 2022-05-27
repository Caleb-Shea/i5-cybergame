import pygame as pyg

import fullmenu_data
from assets import *
from helper_func import *


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
        self.image_base.fill(colors['fullmenu'])
        pyg.draw.rect(self.image_base, colors['rose'], ((0, 0), self.rect.size), 5) # On larger displays this breaks

        # self.image is the surface where everything happens, and self.image_base
        # is the surface that we keep plain for easy redrawing
        self.image = self.image_base

        # Create tabs
        self.tab_names = ['ACQUISITIONS', 'OPS', 'PERSONNEL',
                          'INTEL', 'CYBER', 'RESEARCH']
        self.tab_rects = []
        for i in range(len(self.tab_names)):
            x_size = self.rect.width//len(self.tab_names)
            rect = pyg.rect.Rect(i * x_size, 0, x_size, 50)
            self.tab_rects.append(rect)

        self.cur_tab = self.tab_names[1]

        self.channel = pyg.mixer.find_channel()

        # Tab specific initalization
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

    def update(self):
        """
        Description: Detect mouse clicks and update active tab.
        Parameters: None
        Returns: None
        """
        # Switch tabs if the mouse clicks on one
        m_pos = pyg.mouse.get_pos()
        m_pressed = pyg.mouse.get_pressed()
        for rect, name in zip(self.tab_rects, self.tab_names):
            # If a tab is clicked on, select it
            # We move the rect because the mouse coords are absolute, but the
            # rect coords are based on the topleft of the menu
            if rect.move(10, 10).collidepoint(m_pos) and m_pressed[0]:
                self.cur_tab = name

        # Handle tab specific updates
        # Pass mouse info so we don't have to get it more than once a frame
        if self.cur_tab == 'INTEL':
            self.update_intel(m_pos, m_pressed)

    def update_intel(self, m_pos, m_pressed):
        """
        Description: Handle events specific to the intel tab.
        Parameters: None
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
            for i, rect, brief in zip(range(len(self.cur_briefs)), self.brief_rects, self.cur_briefs):
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
        # Create buttons for each of the current briefs
        for brief, rect in zip(self.cur_briefs, self.brief_rects):
            # If it's expensive, make it a different color
            if brief['cost'] > 1500:
                c = colors['red']
            else:
                c = colors['darkgray']

            # If a brief is clicked and held, fade to black
            if self.selected_brief_id == self.cur_briefs.index(brief):
                c = colors['fullmenu'].lerp(c, 1 - min(self.brief_buy_timer/30, 1))

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
                cost = fonts['zrnic24'].render(f"Cost: {brief['cost']}", True, colors['black'])
                desc = word_wrap(brief['desc'], fonts['zrnic20'], colors['black'], ttrect.inflate(-25, 0))

                tt.blit(name, (20, 5))
                tt.blit(p2b, (32, 215))
                tt.blit(cost, (140, 170))
                tt.blit(desc, (20, 50))

                self.image.blit(tt, ttrect)

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

    def render(self):
        """
        Description: Render this menu on the screen.
        Parameters: None
        Returns: None
        """
        # Clear the image of anything tab specific so objects don't persist
        self.image = self.image_base.copy()

        # Render everything to self.image
        self.render_tabs()
        if self.cur_tab == 'INTEL':
            self.render_intel()

        # Blit to the screen
        self.window.blit(self.image, self.rect)
