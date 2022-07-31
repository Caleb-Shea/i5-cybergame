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
        self.window_rect = self.window.get_rect()
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
        self.arrow_rect.bottomleft = (0, self.HEIGHT)

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

        # This is used to determine which menu page we need to render
        self.p_page = None

        # Create buttons
        self.p_resume = pyg.Surface((500, 80))
        self.p_resume.fill(colors['indigo'])
        self.p_resume_rect = self.p_resume.get_rect(center=(self.WIDTH//2, 1/5*self.HEIGHT))
        text = fonts['zrnic26'].render('RESUME', True, colors['black'])
        self.p_resume.blit(text, text.get_rect(center=(250, 40)))

        self.p_eq = pyg.Surface((242, 270))
        self.p_eq.fill(colors['acq_bg'])
        self.p_eq_rect = self.p_eq.get_rect(topleft=self.p_resume_rect.move(0, 15).bottomleft)
        text = fonts['zrnic26'].render('EQ', True, colors['black'])
        self.p_eq.blit(text, text.get_rect(center=(121, 40)))

        self.p_credits = pyg.Surface((242, 80))
        self.p_credits.fill(colors['ops_bg'])
        self.p_credits_rect = self.p_credits.get_rect(topleft=self.p_eq_rect.move(15, 0).topright)
        text = fonts['zrnic26'].render('CREDITS', True, colors['lightgray'])
        self.p_credits.blit(text, text.get_rect(center=(121, 40)))

        self.p_options = pyg.Surface((242, 80))
        self.p_options.fill(colors['off_cyber_bg'])
        self.p_options_rect = self.p_options.get_rect(topleft=self.p_credits_rect.move(0, 15).bottomleft)
        text = fonts['zrnic26'].render('OPTIONS', True, colors['black'])
        self.p_options.blit(text, text.get_rect(center=(121, 40)))

        self.p_info = pyg.Surface((242, 80))
        self.p_info.fill(colors['def_cyber_bg'])
        self.p_info_rect = self.p_info.get_rect(topright=self.p_options_rect.move(0, 15).bottomright)
        text = fonts['zrnic26'].render('GAME INFO', True, colors['black'])
        self.p_info.blit(text, text.get_rect(center=(121, 40)))

        self.p_exit = pyg.Surface((500, 80))
        self.p_exit.fill(colors['ppl_bg'])
        self.p_exit_rect = self.p_exit.get_rect(topleft=self.p_eq_rect.move(0, 15).bottomleft)
        text = fonts['zrnic26'].render('EXIT', True, colors['black'])
        self.p_exit.blit(text, text.get_rect(center=(250, 40)))

        # Page specific init

        # Credits
        self.p_c = pyg.Surface((650, 600)).convert_alpha()
        self.p_c.fill(colors['gray'])
        self.p_c_rect = self.p_c.get_rect(center=(self.WIDTH/2, self.HEIGHT/2))

        # Render the header
        title = fonts['zrnic46'].render('CREDITS', True, colors['deepblue'])
        self.p_c.blit(title, title.get_rect(midtop=(325, 20)))
        pyg.draw.line(self.p_c, colors['deepblue'], (100, 80), (550, 80), 4)

        # Render the credits themselves
        credits = ['Michaela Kovalsky (Project Manager)',
                   'Caleb Shea (Development Lead)',
                   'Casey Landrum (Content, QA)',
                   '??? (Quality Analysis Tester)',
                   '??? (Graphic Designer)',
                   '??? (Content Creator)',
                   '??? (Story Planner)']

        for i, credit in enumerate(credits):
            surf = fonts['zrnic30'].render(credit, True, colors['black'])
            pos = (20, 120 + 50*i)
            self.p_c.blit(surf, pos)

        # Options
        self.p_o = pyg.Surface((650, 600)).convert_alpha()
        self.p_o.fill(colors['starwhite'])
        self.p_o_rect = self.p_o.get_rect(center=self.window_rect.center)

        # Game Info/Stats
        self.p_gi = pyg.Surface((650, 600)).convert_alpha()
        self.p_gi.fill(colors['black'])
        self.p_gi_rect = self.p_gi.get_rect(center=self.window_rect.center)

        # EQ
        # Music slider
        self.p_eq_music_rect = pyg.rect.Rect(0, 0, 200, 30)
        self.p_eq_music_rect.center = (self.p_eq_rect.centerx,
                                       self.p_eq_rect.y + 120)
        self.p_eq_music_knob = pyg.rect.Rect(0, 0, 20, 20)
        self.p_eq_music_knob.midright = self.p_eq_music_rect.midright

        m_text = fonts['zrnic20'].render('Music Volume', True, colors['black'])
        self.p_eq.blit(m_text, m_text.get_rect(topleft=(20, 80)))
        
        # Sound slider
        self.p_eq_sound_rect = pyg.rect.Rect(0, 0, 200, 30)
        self.p_eq_sound_rect.center = (self.p_eq_rect.centerx,
                                       self.p_eq_rect.y + 200)
        self.p_eq_sound_knob = pyg.rect.Rect(0, 0, 20, 20)
        self.p_eq_sound_knob.midright = self.p_eq_sound_rect.midright
        s_text = fonts['zrnic20'].render('Sound Volume', True, colors['black'])
        self.p_eq.blit(s_text, s_text.get_rect(topleft=(20, 160)))

        # Exit
        self.p_exit_confirm = pyg.Surface((800, 350))
        self.p_exit_confirm.fill(colors['ppl_bg'])
        self.p_exit_confirm_rect = self.p_exit_confirm.get_rect(center=self.window_rect.center)
        text = fonts['zrnic42'].render('Are you sure you want to quit?', True, colors['black'])
        self.p_exit_confirm.blit(text, text.get_rect(center=(400, 65)))

        self.p_exit_yes = pyg.Surface((200, 80))
        self.p_exit_yes.fill(colors['sand'])
        self.p_exit_yes_rect = self.p_exit_yes.get_rect(midtop=self.window_rect.center)
        text = fonts['zrnic30'].render("Yes I'm sure", True, colors['black'])
        self.p_exit_yes.blit(text, text.get_rect(center=(100, 40)))
                                    
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

        # --- Earth Locator init ---
        self.e_loc_rect = pyg.rect.Rect(0, 0, 60, 60)
        self.e_loc_E = fonts['zrnic24'].render('E', True, colors['black'])

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

    def render_back_arrow(self):
        """
        Description: Render a back arrow that will take us back to the main
                     menu. The image is static, and therefore is created in the
                     __init__ function.
        Parameters: None
        Returns: None
        """
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
        img = fonts['zrnic24'].render(f"Reputation: {game_info['Reputation']:,}", True, colors['starwhite'])
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
        img = fonts['zrnic24'].render(f"Cash: {game_info['Cash']:,}", True, colors['starwhite'])
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
        img = fonts['zrnic24'].render(f"Total Personnel: {game_info['Num Personnel']:,}", True, colors['starwhite'])
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

    def render_earth_loc(self, e_pos):
        """
        Description: Render a locator pointing towards the earth when the earth
                     is off the screen.
        Parameters:
            e_pos [tuple] -> Absolute position of the earth
        Returns: None
        """
        # Update rect position
        self.e_loc_rect.center = e_pos
        self.e_loc_rect.clamp_ip(self.window_rect)

        # Draw marker
        pyg.draw.circle(self.window, colors['white'], self.e_loc_rect.center,
                        self.e_loc_rect.width/2)
        self.window.blit(self.e_loc_E, self.e_loc_E.get_rect(center=self.e_loc_rect.center))

    def render_earth_menu(self):
        """
        Description: Render the earth's menu.
        Parameters: None
        Returns: None
        """
        self.window.blit(self.e_menu, (0, 0))

        # --- Stats ---
        # Budget
        img = fonts['zrnic26'].render(f"- Budget: {game_info['Budget']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 70)
        self.window.blit(img, rect)

        # Num Satellites
        img = fonts['zrnic26'].render(f"- Num Satellites: {game_info['Num Sats']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 100)
        self.window.blit(img, rect)

        # Num Personnel
        img = fonts['zrnic26'].render(f"- Num Personnel: {game_info['Num Personnel']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 130)
        self.window.blit(img, rect)

        # Max Budget
        img = fonts['zrnic26'].render(f"- Max Budget: {game_info['Max Budget']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 160)
        self.window.blit(img, rect)

        # Total Cash
        img = fonts['zrnic26'].render(f"- Total Cash Earned: {game_info['Total Cash']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 190)
        self.window.blit(img, rect)

        # Max Personnel
        img = fonts['zrnic26'].render(f"- Max Personnel: {game_info['Max Personnel']:,}", True, colors['starwhite'])
        rect = img.get_rect()
        rect.topleft = (50, 220)
        self.window.blit(img, rect)

    def render_hover_menu(self, obj):
        """
        Description: Render the menu that appears at the top of the screen when
                     the player hovers over a node/satellite.
        Parameters:
            obj [dict] -> A dict that contains the data for either a node or a
                          satellite, either one works because ~flexibility~
        Returns: None
        """
        name = fonts['zrnic42'].render(obj['name'], True, colors['white'])
        name_rect = name.get_rect(y=5)
        name_rect.centerx=self.WIDTH/2
        self.window.blit(name, name_rect)

        # Check for description because sats don't use them
        if 'desc' in obj.keys():
            desc = fonts['zrnic26'].render(obj['desc'], True, colors['white'])
            desc_rect = desc.get_rect(y=name_rect.bottom)
            desc_rect.centerx=self.WIDTH/2
            self.window.blit(desc, desc_rect)

    def render_pause_menu(self):
        """
        Description: Render the pause menu.
        Parameters: None
        Returns: None
        """
        self.window.blit(self.p_menu, (0, 0))

        if self.p_page == None:
            # Main pause menu
            self.window.blit(self.p_resume, self.p_resume_rect)
            self.window.blit(self.p_eq, self.p_eq_rect)
            self.window.blit(self.p_credits, self.p_credits_rect)
            self.window.blit(self.p_options, self.p_options_rect)
            self.window.blit(self.p_info, self.p_info_rect)
            self.window.blit(self.p_exit, self.p_exit_rect)

            # EQ
            pyg.draw.line(self.window, colors['black'],
                          self.p_eq_music_rect.midleft,
                          self.p_eq_music_rect.midright, 3)
            
            pyg.draw.circle(self.window, colors['blue'],
                            self.p_eq_music_knob.center,
                            self.p_eq_music_knob.width/2)
            
            pyg.draw.line(self.window, colors['black'],
                          self.p_eq_sound_rect.midleft,
                          self.p_eq_sound_rect.midright, 3)
            
            pyg.draw.circle(self.window, colors['blue'],
                            self.p_eq_sound_knob.center,
                            self.p_eq_sound_knob.width/2)

        elif self.p_page == 'credits':
            # Credits screen
            self.window.blit(self.p_c, self.p_c_rect)

        elif self.p_page == 'options':
            # Options menu
            self.window.blit(self.p_o, self.p_o_rect)

        elif self.p_page == 'info':
            # General game info screen
            self.window.blit(self.p_gi, self.p_gi_rect)
        
        elif self.p_page == 'exit':
            # Exit confirmation message
            self.window.blit(self.p_exit_confirm, self.p_exit_confirm_rect)
            self.window.blit(self.p_exit_yes, self.p_exit_yes_rect)
