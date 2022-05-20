"""
This file is meant to hold helper functions that are used often and across
several files.

terminate()
get_path(path)
play_sound(sound)
"""


import pygame as pyg
import os


def terminate():
    """
    Description: Cleanly exit the program.
    Parameters: None
    Returns: None
    """
    pyg.quit()
    raise SystemExit()

def get_path(path):
    """
    Description: Get the full path from a partial file path.
    Parameters:
        path [path-like-object] -> The partial path to get the full path from
    Returns:
        [path-like-object] -> The full path
    """
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, path)

def play_sound(sound, channel=None):
    """
    Description: Play a sound out of any available channel.
    Parameters:
        sound [sound file] -> The sound to play
    Returns: None
    """
    if channel == None:
        channel = pyg.mixer.find_channel()

    try:
        channel.play(sound)
    except Exception as e:
        print(repr(e))
        print("Too many sounds being playeds")
        terminate()
