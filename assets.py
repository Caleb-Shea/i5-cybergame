"""
The sole purpose of this file is to load assets required.

Assets are grouped according to how they will be used, and stored as dicts
for easy access.
"""

import pygame as pyg
from pygame.font import Font
from pygame.mixer import Sound
from os import path

from helper_func import get_path


pyg.font.init()
pyg.mixer.pre_init(44100, -16, 2, 512)
pyg.mixer.init()

# Load all the colors
colors = {'clear': pyg.Color(  0,   0,   0,   0),
          'hud_bg': pyg.Color(  5,   0,  30, 230),
          'pause_menu': pyg.Color(  0,  10,  50, 200),
          'ticker_bg': pyg.Color(220, 220, 220),
          'vignette': pyg.Color( 50,  50, 100, 150),
          'vignette_b': pyg.Color(  0,   0,   0, 200),

          'intel_bg': pyg.Color(  5,   0,  30, 150),
          'acq_bg': pyg.Color(205, 255,   0,  20),
          'ops_bg': pyg.Color( 60,  60,  60, 100),
          'def_cyber_bg': pyg.Color(200, 240, 200,  50),
          'off_cyber_bg': pyg.Color(140, 210, 240,  50),
          'events_bg': pyg.Color(220,  10,  200,  30),
          'events_reel': pyg.Color(220, 220, 200),
          'ppl_bg': pyg.Color(40, 200, 230,  30),
          'ppl_legend_Intel': pyg.Color(255,   0,   0),
          'ppl_legend_Ops': pyg.Color(  0,   0, 255),
          'ppl_legend_Cyber': pyg.Color(255, 255,   0),
          'ppl_legend_Acquisitions': pyg.Color(  0, 255,   0),
          'ppl_legend_Unassigned': pyg.Color(128,   0, 255),

          'ops_friendly': pyg.Color(140, 190, 240),
          'ops_f_half': pyg.Color(140, 190, 240, 180),
          'ops_hostile': pyg.Color(240, 140, 140),
          'ops_h_half': pyg.Color(240, 140, 140, 180),
          'ops_passive': pyg.Color(180, 180, 180),
          'ops_p_half': pyg.Color(180, 180, 180, 180),

          'white': pyg.Color(255, 255, 255),
          'starwhite': pyg.Color(230, 230, 230),
          'lightgray': pyg.Color(200, 200, 200),
          'gray': pyg.Color(120, 120, 120),
          'darkgray': pyg.Color( 50,  50,  50), # Maybe switch to '25%white' etc
          'ddarkgray': pyg.Color( 30,  30,  30),
          'black': pyg.Color(  0,   0,   0),
          'space': pyg.Color(  0,   0,   7),
          'pink': pyg.Color(255,   0, 255),
          'rose': pyg.Color(255,   0,  80),
          'clear_rose': pyg.Color(255,   0,  80,  30),
          'red': pyg.Color(255,   0,   0),
          'red_sand': pyg.Color(200, 120, 100),
          'orange': pyg.Color(220, 100,   5),
          'yellow': pyg.Color(255, 255,   0),
          'sand': pyg.Color(240, 230, 150),
          'lime': pyg.Color( 80, 255,   0),
          'babygreen': pyg.Color(200, 240, 200),
          'green': pyg.Color(  0, 255,   0),
          'mint': pyg.Color(  0, 255, 170),
          'cyan': pyg.Color(  0, 255, 255),
          'babyblue': pyg.Color(140, 210, 240),
          'skyblue': pyg.Color(  0, 110, 255),
          'blue': pyg.Color(  0,   0, 255),
          'deepblue': pyg.Color(  5,   0, 20),
          'indigo': pyg.Color( 50,   0, 255),
          'purple': pyg.Color(128,   0, 255)}

# Load fonts in various sizes
fonts = {'zrnic14': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 14),
         'zrnic16': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 16),
         'zrnic18': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 18),
         'zrnic20': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 20),
         'zrnic24': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 24),
         'zrnic26': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 26),
         'zrnic30': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 30),
         'zrnic32': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 32),
         'zrnic36': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 36),
         'zrnic42': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 42),
         'zrnic46': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 46),
         'zrnic48': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 48),
         'zrnic80': Font(get_path(path.join('assets', 'fonts', 'zrnic.ttf')), 80)}

# Load audio files
audio = {'up_click': Sound(get_path(path.join('assets', 'audio', 'up_click.wav'))),
         'down_click': Sound(get_path(path.join('assets', 'audio', 'down_click.wav'))),
         'soundtrack1': Sound(get_path(path.join('assets', 'audio', 'soundtrack', 'Empty Head.mp3'))),
         'ui_error': Sound(get_path(path.join('assets', 'audio', 'ui_error.flac')))}

# Adjust volume levels
audio['down_click'].set_volume(.75)
audio['soundtrack1'].set_volume(.25)
audio['ui_error'].set_volume(.15)

# Load any images needed by the program
images = {'earth_ss': pyg.image.load(get_path(path.join('assets', 'images', 'earth.png'))),
          'world_map': pyg.image.load(get_path(path.join('assets', 'images', 'world_map.png'))),
          'world_map_NA': pyg.image.load(get_path(path.join('assets', 'images', 'world_map_NA.png'))),
          'world_map_big': pyg.image.load(get_path(path.join('assets', 'images', 'world_map_big.png'))),
          'map_marker': pyg.image.load(get_path(path.join('assets', 'images', 'map_marker.png'))),
          'GPS': pyg.image.load(get_path(path.join('assets', 'images', 'sats', 'gps.png'))),
          'MDef': pyg.image.load(get_path(path.join('assets', 'images', 'sats', 'mdef.png'))),
          'Nukes': pyg.image.load(get_path(path.join('assets', 'images', 'sats', 'nuke.png'))),
          'ICBM': pyg.image.load(get_path(path.join('assets', 'images', 'sats', 'icbm.png')))}

# Load the tilesets for the ops missions
test_raw = pyg.image.load(get_path(path.join('assets', 'mapdata', 'TEST', 'tileset.png')))
test = []
for y in range(0, test_raw.get_rect().height, 50):
    for x in range(0, test_raw.get_rect().width, 50):
        # Create a 50x50 surface and pre-fill it
        surf = pyg.Surface((50, 50))
        surf.fill(colors['clear'])

        # Blit the portion of the tilesheet we want
        surf.blit(test_raw, (0, 0), pyg.rect.Rect(x, y, 50, 50))

        test.append(surf)

tilesets = {'TEST': test}

# Clean up namespace
del test_raw, test, surf