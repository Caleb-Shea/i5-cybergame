import pygame as pyg
import random
import csv

from game_info import game_info
from helper_func import *
from assets import *


class Ticker():
    def __init__(self):
        """
        Description: A class to represent a news ticker. This class will allow
                     the player to see 'real world' events that they can choose
                     to interact with or ignore.
        Parameters: None
        Returns: Ticker()
        """
        # Grab window attributes
        self.window = pyg.display.get_surface()
        self.WIDTH, self.HEIGHT = pyg.display.get_window_size()

        # Create a base that we will copy over self.image to make life easy
        self.image_base = pyg.Surface((600, 40)).convert_alpha()
        self.rect = self.image_base.get_rect(midbottom=(self.WIDTH//2, self.HEIGHT))

        # Draw the image base
        self.image_base.fill(colors['ticker_bg']) # BG
        pyg.draw.rect(self.image_base, colors['gray'], ((80, 0), (self.rect.width-80, 40)), 3) # Border
        pyg.draw.rect(self.image_base, colors['babyblue'], ((0, 0), (80, self.rect.height))) # 'NEWS' BG
        news_text = fonts['zrnic30'].render('NEWS:', True, colors['black']) # 'NEWS' text
        news_rect = news_text.get_rect(midleft=(5, self.rect.height/2))
        self.image_base.blit(news_text, news_rect)

        self.image = self.image_base.copy()

        # Load all event information
        self.events = []
        self.load_events()

        self.unused_events = self.events[:]
        self.used_events = []
        self.cur_event = None

    def load_events(self):
        """
        Description: Read all the events from the ticker_events.csv file, and
                     organize them in a useful way.
        Parameters: None
        Returns: None
        """
        with open(get_path('ticker_events.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.events.append(row)

    def new_event(self, date):
        """
        Description: Choose a new available event and store it.
        Parameters:
            date [datetime.date] -> Today's date
        Returns: None
        """
        available_events = []

        # Check for pre-requisites
        for event in self.unused_events:
            if event['pre_req'] == 'None':
                available_events.append(event)
                continue

            # The pre-req for any given event is the ID of the pre-req
            elif event['pre_req'] in [e['ID'] for e in self.used_events]:
                available_events.append(event)
                continue

            # Some events have level requirements
            for tag in ['Cyber Def', 'Cyber Off', 'Acq GPS']:
                if event['pre_req'].startswith(tag):
                    lvl_req = int(event['pre_req'].split()[-1])

                    # Check tag specific level requirement
                    if tag == 'Cyber Def':
                        if game_info['Cyber Def Level'] >= lvl_req:
                            available_events.append(event)
                    elif tag == 'Acq GPS':
                        if game_info['Acq GPS Level'] >= lvl_req:
                            available_events.append(event)

        if len(available_events) > 0:
            # Get the new event, remove it from the list of available events and
            # add it to the list of seen events
            self.cur_event = random.choice(available_events)
            self.used_events.append(self.cur_event)
            self.unused_events.remove(self.cur_event)

            # Get a timestamp for which day the user first saw the event
            self.cur_event['Date Seen'] = date

            # Add the event to game_info
            game_info['Reels Seen'].append(self.cur_event)

            # Store the event
            self.event_text = fonts['zrnic20'].render(self.cur_event['event'], True, colors['black'])
            self.event_rect = self.event_text.get_rect()

    def update(self):
        """
        Description: Update the ticker.
        Parameters: None
        Returns: None
        """
        ...

    def render_event(self):
        """
        Description: Render the current event.
        Parameters: None
        Returns: None
        """
        if self.cur_event != None:
            self.event_rect.midleft = (93, self.rect.height//2)
            self.image.blit(self.event_text, self.event_rect)

    def render(self):
        """
        Description: Render the ticker onto the screen.
        Parameters: None
        Returns: None
        """
        # Clear the image of anything tab specific so objects don't persist
        self.image = self.image_base.copy()

        self.render_event()

        # Blit to the screen
        self.window.blit(self.image, self.rect)
