"""
The sole purpose of this file is to load assets required.

Assets are grouped according to how they will be used, and stored as dicts
for easy access.
"""


import pygame as pyg
import os

pyg.font.init()

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

# Not actual files, this is C/P from another file of mine for future use
# node_images = {'bg_set_1': pyg.image.load(get_path(os.path.join('assets', 'imgs', 'background', 'bg_set_1.png'))),
#                'bg_set_2': pyg.image.load(get_path(os.path.join('assets', 'imgs', 'background', 'bg_set_2.png'))),
#                'bg_set_3': pyg.image.load(get_path(os.path.join('assets', 'imgs', 'background', 'bg_set_3.png'))),
#                'bg_set_4': pyg.image.load(get_path(os.path.join('assets', 'imgs', 'background', 'bg_set_4.png')))}
