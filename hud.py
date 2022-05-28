import pygame as pyg

from assets import *
from helper_func import *


class HUD():
    def __init__(self):
        """
        Description: A class to control and keep track of all the elements
                     within the HUD. All functions render directly onto the
                     main screen.
        Parameters: None
        Returns: HUD()
        """
        # Create a reference to the main window and it's size meaurements
        self.window = pyg.display.get_surface()
        self.WIDTH, self.HEIGHT = self.window.get_rect().size

        # Back arrow init
        text = fonts['zrnic48'].render("<--- EARTH", True, colors['starwhite'])
        # Create a surface big enough for the text and a border
        self.arrow = pyg.Surface(text.get_rect().inflate(16, -2).size).convert_alpha()
        self.arrow.fill(colors['hud_bg'])

        # Position the text in the middle of the inflation
        self.arrow.blit(text, (8, -1))
        self.arrow_rect = self.arrow.get_rect()
        pyg.draw.rect(self.arrow, colors['rose'], self.arrow_rect, 2)

    def render_back_arrow(self, full_menu_active):
        """
        Description: Render a back arrow that will take us back to the main
                     menu. The image is static, and therefore is created in the
                     __init__ function.
        Parameters:
            full_menu_active [bool] -> Is the full menu currently being shown?
        Returns: None
        """
        # If we're looking at a full menu, the arrow needs to be on the bottom
        if full_menu_active:
            self.arrow_rect.bottomleft = (0, self.HEIGHT)
            self.window.blit(self.arrow, self.arrow_rect)
        else:
            # Otherwise it should be on the top
            self.arrow_rect.topleft = (0, 0)
            self.window.blit(self.arrow, self.arrow_rect)

    def render_time(self, date):
        """
        Description: Render the current date in the format "DD MM, YYYY".
        Parameters:
            date [dt.date] -> The current in-game date
        Returns: None
        """
        date_str = date.strftime("%d %B, %Y")
        img = fonts['zrnic24'].render(date_str, True, colors['starwhite'])
        rect = img.get_rect()
        rect.bottomright = (self.WIDTH - 7, self.HEIGHT - 6)

        date_bg = pyg.Surface(rect.inflate(15, 10).size).convert_alpha()
        date_bg.fill(colors['hud_bg'])
        dbg_rect = date_bg.get_rect()
        dbg_rect.bottomright = (self.WIDTH, self.HEIGHT)

        self.window.blit(date_bg, dbg_rect)
        pyg.draw.rect(self.window, colors['rose'], dbg_rect, width=1)
        self.window.blit(img, rect)
