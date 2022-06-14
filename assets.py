"""
The sole purpose of this file is to load assets required.

Assets are grouped according to how they will be used, and stored as dicts
for easy access.
"""


import pygame as pyg
from pygame.font import Font
from pygame.mixer import Sound
import os

from helper_func import get_path


pyg.font.init()
pyg.mixer.pre_init(44100, -16, 2, 512)
pyg.mixer.init()

fonts = {'zrnic14': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 14),
         'zrnic16': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 16),
         'zrnic20': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 20),
         'zrnic24': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 24),
         'zrnic26': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 26),
         'zrnic30': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 30),
         'zrnic32': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 32),
         'zrnic36': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 36),
         'zrnic42': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 42),
         'zrnic48': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 48),
         'zrnic80': Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 80)}

sounds = {'up_click': Sound(get_path(os.path.join('assets', 'sounds', 'up_click.wav'))),
          'down_click': Sound(get_path(os.path.join('assets', 'sounds', 'down_click.wav')))}

sounds['down_click'].set_volume(.75)

colors = {'clear': pyg.Color(  0,   0,   0,   0),
          'hud_bg': pyg.Color(  5,   0,  30, 230),
          'ticker_bg': pyg.Color(220, 220, 220),
          'vignette': pyg.Color( 50,  50, 100, 150),
          'vignette_b': pyg.Color(  0,   0,   0, 200),
          'intel_bg': pyg.Color(  5,   0,  30, 150),
          'acq_bg': pyg.Color(220,  60,  30,  30),
          'def_cyber_bg': pyg.Color(200, 240, 200,  50),
          'off_cyber_bg': pyg.Color(140, 210, 240,  50),
          'white': pyg.Color(255, 255, 255),
          'starwhite': pyg.Color(230, 230, 230),
          'lightgray': pyg.Color(200, 200, 200),
          'gray': pyg.Color(120, 120, 120),
          'darkgray': pyg.Color( 50,  50,  50), # Maybe switch to '25%white' etc
          'ddarkgray': pyg.Color( 30,  30,  30),
          'space': pyg.Color(  0,   0,   7),
          'black': pyg.Color(  0,   0,   0),
          'red': pyg.Color(255,   0,   0),
          'orange': pyg.Color(220, 100,   5),
          'yellow': pyg.Color(255, 255,   0),
          'babygreen': pyg.Color(200, 240, 200),
          'green': pyg.Color(  0, 255,   0),
          'lime': pyg.Color( 80, 255,   0),
          'mint': pyg.Color(  0, 255, 170),
          'cyan': pyg.Color(  0, 255, 255),
          'babyblue': pyg.Color(140, 210, 240),
          'skyblue': pyg.Color(  0, 110, 255),
          'blue': pyg.Color(  0,   0, 255),
          'deepblue': pyg.Color(  5,   0, 20),
          'indigo': pyg.Color( 50,   0, 255),
          'purple': pyg.Color(128,   0, 255),
          'pink': pyg.Color(255,   0, 255),
          'rose': pyg.Color(255,   0,  80)}
