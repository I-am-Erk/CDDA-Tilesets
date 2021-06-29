"""
Create recolored seasonal variations for sprites in all subfolders
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
}
DEFAULT_COLORS = [
    (240, 236, 187),
    (181, 175, 105),
    (115, 130, 92),
    (95, 76, 53),
]


def replace_colors(season_file: str, season: str) -> Image:
    """
    Load original sprite and tint it for the season
    """
    replacement_colors = SEASON_PREFIXES[season]
    img = Image.open(season_file).convert('RGB')
    data = numpy.array(img)
    current_color = 0

    for color in DEFAULT_COLORS:
        # We're iterating through each default (spring) color. We've used numpy
        # to turn the image into an array (var data). As we iterate through
        # each spring color we're also iterating through the replacement colors
        # array. We're basically mass replacing the default colors, starting
        # with the lightest and moving to the darkest. Afterwards we use numpy
        # to reconstruct the image. This method (replace_colors) is run for
        # each alternative season (summer, fall and winter).
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
            # Each item corresponds to a pixel. 21, 19, 21 is the background
            # color I used in my image editor when drawing the icons. If we
            # come across this color we are adding 255,255,255,0 (a transparent
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
            img = replace_colors(season_file, season)
            transparent_background(img).save(season_file, 'PNG')

        new_name = f'{dir_name}_season_spring.png'
        os.rename(filename, new_name)
        transparent_background(Image.open(new_name)).save(new_name, 'PNG')
        print(dir_name)


def walk(directory_name: str) -> None:
    """
    Search subdirectoriest that contain a generic.png and execute change_colors
    """
    for subdir, _, files in os.walk(directory_name):
        for file in files:
            if file == 'generic.png':
                os.chdir(subdir)
                change_colors()


if __name__ == '__main__':
    rootdir = sys.argv[1]
    walk(rootdir)
