import pygame as pyg

from assets import *
from fullmenu_data import *
from helper_func import *


class FullMenu():
    def __init__(self, window):
        """
        Description: A class to represent a single node. The node has a parent,
                     children, and attributes used for purchasing, inspecting, and
                     learning about this node.
        Parameters:
            window [pyg.Surface] -> A reference to the screen.
        Returns: None
        """
        self.window = window

        self.rect = self.window.get_rect().inflate(-20, -20)
        self.image = pyg.Surface(self.rect.size).convert_alpha()
        self.image.fill(colors['fullmenu'])

        self.tab_names = ['ACQUISITIONS', 'OPS', 'PERSONNEL', 'INTEL', 'CYBER']
        self.tabs = []
        for i, tab in enumerate(self.tab_names):
            size = self.rect.width//len(self.tab_names)
            rect = pyg.rect.Rect(i * size, 0, size, 50)
            self.tabs.append(rect)

        self.cur_tab = self.tab_names[1]

        self.channel = pyg.mixer.find_channel()

    def update(self):
        """
        Description: Detect mouse clicks and update active tab.
        Parameters: None
        Returns: None
        """
        m_pos = pyg.mouse.get_pos()
        m_pressed = pyg.mouse.get_pressed()
        for rect, name in zip(self.tabs, self.tab_names):
            # If a tab is clicked on, select it
            # We move the rect because the mouse coords are absolute, but the
            # rect coords are based on the topleft of the menu
            if rect.move(10, 10).collidepoint(m_pos) and m_pressed[0]:
                self.cur_tab = name

                if not self.channel.get_busy():
                    self.channel.play(sounds['ui_click'])

    def render_select(self):
        """
        Description: Draw the selection menu on the left side of the screen.
        Parameters: None
        Returns: None
        """
        

    def render_tabs(self):
        """
        Description: Draw the tabs at the top of the screen.
        Parameters: None
        Returns: None
        """
        for rect, name in zip(self.tabs, self.tab_names):
            if self.cur_tab == name:
                pyg.draw.rect(self.image, colors['darkgray'], rect)
            else:
                pyg.draw.rect(self.image, colors['gray'], rect)

            text = fonts['zrnic30'].render(name, True, colors['starwhite'])
            text_rect = text.get_rect(center=rect.center)
            self.image.blit(text, text_rect)

        # Draw lines separating each tab
        size = self.rect.width//len(self.tab_names)
        pyg.draw.line(self.image, colors['black'], (0, 50), (self.rect.right, 50))
        for i in range(1, 5):
            pyg.draw.line(self.image, colors['darkgray'], (i*size, 0), (i*size, 50))

    def render(self):
        """
        Description: Render this menu on the screen.
        Parameters: None
        Returns: None
        """
        self.window.blit(self.image, self.rect)
        self.render_select()
        self.render_tabs()
