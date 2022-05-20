"""
The sole purpose of this file is to load assets required.

Assets are grouped according to how they will be used, and stored as dicts
for easy access.
"""


import pygame as pyg
import os

pyg.font.init()
pyg.mixer.pre_init(44100, -16, 2, 512)
pyg.mixer.init()

def get_path(path):
    """
    Description: Get the full path from a partial file path.
    Parameters:
        path [path-like-object] -> The partial path to get the full path from
    Returns:
        A path-like-object that contains a full path
    """
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, path)


fonts = {'zrnic14': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 14),
         'zrnic16': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 16),
         'zrnic24': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 24),
         'zrnic30': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 30),
         'zrnic32': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 32),
         'zrnic36': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 36),
         'zrnic48': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 48)}

sounds = {'ui_click': pyg.mixer.Sound(get_path(os.path.join('assets', 'sounds', 'ui_click.wav')))}

colors = {'clear': (  0,   0,   0,   0),
          'fullmenu': (  5,   0,  30,  150),
          'white': (255, 255, 255),
          'starwhite': (230, 230, 230),
          'gray': (120, 120, 120),
          'darkgray': ( 50,  50,  50),
          'space': (  0,   0,   7),
          'black': (  0,   0,   0),
          'red': (255,   0,   0),
          'orange': (220, 100,   5),
          'yellow': (255, 255,   0),
          'green': (  0, 255,   0),
          'lime': (120, 255,   0),
          'mint': (  0, 255, 170),
          'cyan': (  0, 255, 255),
          'skyblue': (  0, 110, 255),
          'blue': (  0,   0, 255),
          'deepblue': (  5,   0, 20),
          'indigo': ( 50,   0, 255),
          'purple': (128,   0, 255),
          'pink': (255,   0, 255),
          'rose': (255,   0,  80)}
