import pygame as pyg

from game_info import game_info
from ticker import Ticker
from helper_func import *
from assets import *


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
        self.WIDTH, self.HEIGHT = pyg.display.get_window_size()

        # Create a news/event ticker
        self.ticker = Ticker()

        # --- Back arrow init ---
        text = fonts['zrnic48'].render("<--- EARTH", True, colors['starwhite'])
        # Create a surface big enough for the text and a border
        self.arrow = pyg.Surface(text.get_rect().inflate(16, -2).size).convert_alpha()
        self.arrow.fill(colors['hud_bg'])

        # Position the text in the middle of the surface
        self.arrow.blit(text, (8, -1))
        self.arrow_rect = self.arrow.get_rect()
        pyg.draw.rect(self.arrow, colors['rose'], self.arrow_rect, 2)

        # The below code creates images that are static, and therefore are
        # created only once

        # --- Earth menu init ---
        self.e_menu = pyg.Surface(self.window.get_rect().size).convert_alpha()
        self.e_menu.fill(colors['clear'])

        # Render the menu headings
        text = fonts['zrnic42'].render("STATS:", True, colors['starwhite'])
        self.e_menu.blit(text, (30, 20))

        # --- Pause menu init ---
        self.p_menu = pyg.Surface(self.window.get_rect().size).convert_alpha()
        self.p_menu.fill(colors['pause_menu'])

        # Create buttons
        self.p_resume = pyg.Surface((500, 80))
        self.p_resume.fill(colors['intel_bg'])
        self.p_resume_rect = self.p_resume.get_rect(center=(self.WIDTH//2, 2/5*self.HEIGHT))
        text = fonts['zrnic26'].render('RESUME', True, colors['lightgray'])
        self.p_resume.blit(text, text.get_rect(center=(250, 40)))

        self.p_options = pyg.Surface((242, 80))
        self.p_options.fill(colors['off_cyber_bg'])
        self.p_options_rect = self.p_options.get_rect(topleft=self.p_resume_rect.move(0, 15).bottomleft)
        text = fonts['zrnic26'].render('OPTIONS', True, colors['black'])
        self.p_options.blit(text, text.get_rect(center=(121, 40)))

        self.p_info = pyg.Surface((242, 80))
        self.p_info.fill(colors['def_cyber_bg'])
        self.p_info_rect = self.p_info.get_rect(topright=self.p_resume_rect.move(0, 15).bottomright)
        text = fonts['zrnic26'].render('GAME INFO', True, colors['black'])
        self.p_info.blit(text, text.get_rect(center=(121, 40)))

        self.p_exit = pyg.Surface((500, 80))
        self.p_exit.fill(colors['acq_bg'])
        self.p_exit_rect = self.p_exit.get_rect(topleft=self.p_options_rect.move(0, 15).bottomleft)
        text = fonts['zrnic26'].render('EXIT', True, colors['lightgray'])
        self.p_exit.blit(text, text.get_rect(center=(250, 40)))

        # --- Vignette init ---
        # Left side
        vig1_points = [(0, 0), (0, self.HEIGHT), (self.WIDTH//3, self.HEIGHT),
                       (self.WIDTH//4, self.HEIGHT//1.6), (self.WIDTH//4, self.HEIGHT//3),
                       (self.WIDTH//3, 0), (0, 0)]
        self.vignette_l = pyg.Surface(self.window.get_rect().size).convert_alpha()
        self.vignette_l.fill(colors['clear'])
        pyg.draw.polygon(self.vignette_l, colors['vignette'], vig1_points)
        pyg.draw.polygon(self.vignette_l, colors['vignette_b'], vig1_points, 10)

        # Right side
        vig2_points = [(self.WIDTH, 0), (self.WIDTH, self.HEIGHT), (2*self.WIDTH//3, self.HEIGHT),
                       (3*self.WIDTH//4, self.HEIGHT//1.6), (3*self.WIDTH//4, self.HEIGHT//3),
                       (2*self.WIDTH//3, 0), (self.WIDTH, 0)]
        self.vignette_r = pyg.Surface(self.window.get_rect().size).convert_alpha()
        self.vignette_r.fill(colors['clear'])
        pyg.draw.polygon(self.vignette_r, colors['vignette'], vig2_points)
        pyg.draw.polygon(self.vignette_r, colors['vignette_b'], vig2_points, 10)

    def render_vignette(self, side):
        """
        Description: Render a vignette on either side of the screen. For
                     dramatic purposes.
        Parameters:
            side [str] -> The side of the screen to render a vignette on.
                          Options are 'left', 'right', and 'both'
                          If side is not 'left' or 'right', it will render both
        Returns: None
        """
        if side != 'right':
            self.window.blit(self.vignette_l, (0, 0))

        if side != 'left':
            self.window.blit(self.vignette_r, (0, 0))

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
        # Create an object specifially for the text that will be rendered
        date_str = date.strftime("%d %B, %Y")
        img = fonts['zrnic24'].render(date_str, True, colors['starwhite'])
        rect = img.get_rect()
        rect.bottomright = (self.WIDTH - 7, self.HEIGHT - 6)

        # Create a bg that is slightly bigger than the text
        date_bg = pyg.Surface(rect.inflate(15, 10).size).convert_alpha()
        date_bg.fill(colors['hud_bg'])
        dbg_rect = date_bg.get_rect()
        dbg_rect.bottomright = (self.WIDTH, self.HEIGHT)

        # Render the bg, a border, and the text
        self.window.blit(date_bg, dbg_rect)
        pyg.draw.rect(self.window, colors['rose'], dbg_rect, width=1)
        self.window.blit(img, rect)

    def render_reputation(self):
        """
        Description: Render current amount of reputation the player has, right
                     above the current time.
        Parameters: None
        Returns: None
        """
        # Create an object specifially for the text that will be rendered
        img = fonts['zrnic24'].render(f"Reputation: {game_info['reputation']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.bottomright = (self.WIDTH - 7, self.HEIGHT - 46)

        # Create a bg that is slightly bigger than the text
        date_bg = pyg.Surface(rect.inflate(15, 10).size).convert_alpha()
        date_bg.fill(colors['hud_bg'])
        dbg_rect = date_bg.get_rect()
        dbg_rect.bottomright = (self.WIDTH, self.HEIGHT - 40)

        # Render the bg, a border, and the text
        self.window.blit(date_bg, dbg_rect)
        pyg.draw.rect(self.window, colors['rose'], dbg_rect, width=1)
        self.window.blit(img, rect)

    def render_cash(self):
        """
        Description: Render current amount of cash the player has, right above
                     the current reputation.
        Parameters: None
        Returns: None
        """
        # Create an object specifially for the text that will be rendered
        img = fonts['zrnic24'].render(f"Cash: {game_info['cash']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.bottomright = (self.WIDTH - 7, self.HEIGHT - 86)

        # Create a bg that is slightly bigger than the text
        date_bg = pyg.Surface(rect.inflate(15, 10).size).convert_alpha()
        date_bg.fill(colors['hud_bg'])
        dbg_rect = date_bg.get_rect()
        dbg_rect.bottomright = (self.WIDTH, self.HEIGHT - 80)

        # Render the bg, a border, and the text
        self.window.blit(date_bg, dbg_rect)
        pyg.draw.rect(self.window, colors['rose'], dbg_rect, width=1)
        self.window.blit(img, rect)

    def render_personnel(self):
        """
        Description: Render current amount of total personnel the player has,
        right above the current amount of cash.
        Parameters: None
        Returns: None
        """
        # Create an object specifially for the text that will be rendered
        img = fonts['zrnic24'].render(f"Total Personnel: {game_info['num_personnel']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.bottomright = (self.WIDTH - 7, self.HEIGHT - 126)

        # Create a bg that is slightly bigger than the text
        date_bg = pyg.Surface(rect.inflate(15, 10).size).convert_alpha()
        date_bg.fill(colors['hud_bg'])
        dbg_rect = date_bg.get_rect()
        dbg_rect.bottomright = (self.WIDTH, self.HEIGHT - 120)

        # Render the bg, a border, and the text
        self.window.blit(date_bg, dbg_rect)
        pyg.draw.rect(self.window, colors['rose'], dbg_rect, width=1)
        self.window.blit(img, rect)

    def render_earth_menu(self):
        """
        Description: Render the earth's menu.
        Parameters: None
        Returns: None
        """
        self.window.blit(self.e_menu, (0, 0))

        # --- Stats ---
        # Budget
        img = fonts['zrnic26'].render(f"- Budget: {game_info['budget']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 70)
        self.window.blit(img, rect)

        # Num Satellites
        img = fonts['zrnic26'].render(f"- Num Satellites: {game_info['num_sats']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 100)
        self.window.blit(img, rect)

        # Num Personnel
        img = fonts['zrnic26'].render(f"- Num Personnel: {game_info['num_personnel']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 130)
        self.window.blit(img, rect)

        # Max Budget
        img = fonts['zrnic26'].render(f"- Max Budget: {game_info['max_budget']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 160)
        self.window.blit(img, rect)

        # Total Cash
        img = fonts['zrnic26'].render(f"- Total Cash Earned: {game_info['total_cash']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 190)
        self.window.blit(img, rect)

        # Max Personnel
        img = fonts['zrnic26'].render(f"- Max Personnel: {game_info['max_personnel']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 220)
        self.window.blit(img, rect)

    def render_pause_menu(self):
        """
        Description: Render the pause menu.
        Parameters: None
        Returns: None
        """
        self.window.blit(self.p_menu, (0, 0))
        self.window.blit(self.p_resume, self.p_resume_rect)
        self.window.blit(self.p_options, self.p_options_rect)
        self.window.blit(self.p_info, self.p_info_rect)
        self.window.blit(self.p_exit, self.p_exit_rect)
