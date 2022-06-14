"""
This file is meant to hold helper functions that are used often and across
several files.

terminate()
get_path(path)
play_sound(sound, channel=None)
word_wrap(text, font, color, rect)
num_to_roman(num)
debug_render(value)
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

def word_wrap(text, font, color, rect):
    """
    Description: Word wrap a long string into the boundries of a given rect.
    Parameters:
        text [str] -> The text to wrap
        font [pyg.font.Font] -> The font object to use
        color [pyg.Color or tuple] -> The color of the text
        rect [pyg.rect.Rect] -> The rect to use as boundries for wrapping
    Returns:
        [pyg.Surface] -> A surface containing the wrapped text

    Credit:
        Adapts some code from https://stackoverflow.com/a/49433498
    """
    surf = pyg.Surface(rect.size).convert_alpha()
    surf.fill((0, 0, 0, 0))

    words = text.split()

    lines = []
    while len(words) > 0:
        # Get as many words as will fit within the rect
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > rect.width:
                break

        # Add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # Render the lines onto surf
    x, y = 0, 0
    for line in lines:
        line = font.render(line, True, color)
        surf.blit(line, (x, y))
        y += line.get_rect().height * 1.1

    return surf

def num_to_roman(num):
    """
    Description: Convert an integer to roman numeral format.
    Parameters:
        num [int] -> The number to convert
    Returns:
        [str] -> A string containing the roman numeral notation

    Credit:
        Copied from https://stackoverflow.com/a/47713392
    """
    ROMAN = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
             (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"),
             (4, "IV"), (1, "I")]
    result = ""
    for (arabic, roman) in ROMAN:
        (factor, num) = divmod(num, arabic)
        result += roman * factor
    return result

def debug_render(value):
    """
    Description: Render a given value on the screen for debugging purposes.
    Parameters:
        value [almost anything] -> The thing to render
    Returns: None
    """
    window = pyg.display.get_surface()

    font_name = pyg.font.get_default_font()
    font = pyg.font.SysFont(font_name, 24)
    image = font.render(f"{value}", True, (255, 255, 255))
    rect = image.get_rect(topleft=(0, 0))
    bg = pyg.Surface(rect.inflate(20, 20).size)
    bg.fill((0, 0, 0))

    window.blit(bg, rect.move(-10, -10))
    window.blit(image, rect)
