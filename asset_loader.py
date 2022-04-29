import pygame as pyg
import os

from main import get_path

fonts = {'zrnic16': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 16),
         'zrnic24': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 24),
         'zrnic32': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 32),
         'zrnic48': pyg.font.Font(get_path(os.path.join('assets', 'fonts', 'zrnic.ttf')), 48)}

# Not actual files, this is C/P from another file of mine for future use
# node_images = {'bg_set_1': pyg.image.load(get_path(os.path.join('assets', 'imgs', 'background', 'bg_set_1.png'))),
#                'bg_set_2': pyg.image.load(get_path(os.path.join('assets', 'imgs', 'background', 'bg_set_2.png'))),
#                'bg_set_3': pyg.image.load(get_path(os.path.join('assets', 'imgs', 'background', 'bg_set_3.png'))),
#                'bg_set_4': pyg.image.load(get_path(os.path.join('assets', 'imgs', 'background', 'bg_set_4.png')))}
