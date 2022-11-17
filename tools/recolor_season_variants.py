"""
Create recolored seasonal variations for sprites in all subfolders for HollowMoon tileset.

Usage:
[0] Create a PNG sprite in any consistent palette allowed by HollowMoon tileset.
    For transparency use background color allowed by HM tileset, it will be replaced
    by the script with true transparency.
[1] Create a subfolder and name it using target file's name (for example 't_dirt').
    Name should correspond to how the game names relevant object (terrain, furniture, etc.).
[2] Name your source PNG file <season>.png (for example summer.png) where <season>
    corresponds to the palette you used to create the sprite.
    If you used a spring palette you can also call it 'generic.png'.
[3] Place the file in the created subfolder and run the script.
    Script will also target subfolders so you can run it for the whole tileset folder.
"""
import sys
import os
import shutil

import glob  # pip install glob3
import numpy  # pip install numpy  # TODO: versions

from PIL import Image


NUMBER_PREFIXES = ['_0', '_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8']
SEASON_PREFIXES = {
    '_season_autumn': [
        (230, 227, 171),
        (216, 147, 110),
        (163, 100, 92),
        (90, 68, 72),
    ],
    '_season_winter': [
        (254, 254, 254),
        (203, 200, 218),
        (137, 119, 142),
        (90, 68, 72),
    ],
    '_season_summer': [
        (255, 216, 148),
        (194, 176, 107),
        (83, 138, 106),
        (73, 75, 88),
    ],
    '_season_spring': [
        (240, 236, 187),
        (181, 175, 105),
        (115, 130, 92),
        (95, 76, 53),
    ],
}

def replace_colors(season_file: str, season: str, source_season: str) -> Image:
    """
    Load original sprite and tint it for the season
    """
    replacement_colors = SEASON_PREFIXES[season]
    img = Image.open(season_file).convert('RGB')
    data = numpy.array(img)
    current_color = 0

    assert source_season.endswith('.png')
    source_season = source_season[:-4]
    if source_season == 'generic':
        source_season = 'spring'
    source_colors = SEASON_PREFIXES[f'_season_{source_season}']

    for color in source_colors:
        # We're iterating through each color relevant to the source file's season.
        # We've used numpy to turn the image into an array (var data). As we iterate
        # through each color we're also iterating through the replacement colors
        # array. We're basically mass replacing the source colors, starting
        # with the lightest and moving to the darkest. Afterwards we use numpy
        # to reconstruct the image. This method (replace_colors) is run for
        # each season (spring, summer, fall and winter).
        # https://github.com/I-am-Erk/CDDA-Tilesets/pull/628/files#r639298118
        data[(data == color).all(axis=-1)] = replacement_colors[current_color]
        current_color = current_color + 1

    return Image.fromarray(data, mode='RGB')


def transparent_background(img: Image) -> Image:
    """
    Apply transparent background to the image
    """
    img = img.convert('RGBA')
    img_data = img.getdata()

    new_data = []
    for item in img_data:
        if item[0] == 21 and item[1] == 19 and item[2] == 21:
            # Each item corresponds to a pixel. 21, 19, 21 is the RGB background
            # color I used in my image editor when drawing the icons (HTML: 151315).
            # If we come across this color we are adding 255,255,255,0 (a transparent
            # pixel) to new_data. Otherwise we are adding the pixel as is to
            # new_data. At the end it is reconstructed with transparency where
            # the background color used to be. Obviously not very efficient
            # https://github.com/I-am-Erk/CDDA-Tilesets/pull/628/files#r639307434
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img


def change_colors():
    """
    Genarate variations for all *.png files in current folder
    """
    dir_name = os.path.basename(os.getcwd())  # TODO: make it an argument
    for filename in glob.glob('*.png'):
        new_file = filename
        prefix = ''

        assert new_file.endswith('.png')
        new_file = new_file[:-4]

        for number in NUMBER_PREFIXES:
            if new_file.endswith(number):
                new_file = new_file[:-2]
                prefix = number
                break

        for season in SEASON_PREFIXES:
            season_file = f'{dir_name}{season}{prefix}.png'
            # FIXME: do not create a copy and overwrite it,
            # tint in memory and save instead
            shutil.copy2(filename, season_file)
            img = replace_colors(season_file, season, filename)
            transparent_background(img).save(season_file, 'PNG')
            print(f'Created: {season_file}')

        # variants are created, remove the source
        os.remove(filename)
        print(f'Removed: {filename} in {dir_name}')


def walk(directory_name: str) -> None:
    """
    Search subdirectories that contain either a generic.png (spring colors)
    or <season>.png (<season> palette) and execute change_colors
    """
    file_types = ['generic.png', 'spring.png', 'summer.png', 'autumn.png', 'winter.png']
    for subdir, _, files in os.walk(directory_name):
        for file in files:
            if file in file_types:
                os.chdir(subdir)
                change_colors()


if __name__ == '__main__':
    rootdir = sys.argv[1]
    walk(rootdir)
