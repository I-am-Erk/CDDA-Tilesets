#!/usr/bin/env python3

"""
Renames automatic iterative names obtained by:
1. Importing the directional source files as sprite sheets with aseprite (Ctrl + I), using width = height = 32 pixels
2. Export (not sprite sheet) as <name_of_file>_0.png
Run in the same folder as the relevant sprites
Example usage:
py marinaCut.py
"""

from PIL import Image

import os


def rotateImage(path, degrees):
    image = Image.open(path)
    image = image.rotate(degrees)
    image.save(path)


rename_dict = {
    "marina_north_0": "marina_5_north",
    "marina_north_1": "marina_4_north",
    "marina_north_2": "marina_3_north",
    "marina_north_3": "marina_2_north",
    "marina_north_4": "marina_1_north",
    "marina_north_5": "marina_10_north",
    "marina_north_6": "marina_9_north",
    "marina_north_7": "marina_8_north",
    "marina_north_8": "marina_7_north",
    "marina_north_9": "marina_6_north",
    "marina_north_10": "marina_15_north",
    "marina_north_11": "marina_14_north",
    "marina_north_12": "marina_13_north",
    "marina_north_13": "marina_12_north",
    "marina_north_14": "marina_11_north",
    "marina_north_15": "marina_20_north",
    "marina_north_16": "marina_19_north",
    "marina_north_17": "marina_18_north",
    "marina_north_18": "marina_17_north",
    "marina_north_19": "marina_16_north",
    #
    "marina_east_0": "marina_5_east",
    "marina_east_1": "marina_4_east",
    "marina_east_2": "marina_3_east",
    "marina_east_3": "marina_2_east",
    "marina_east_4": "marina_1_east",
    "marina_east_5": "marina_10_east",
    "marina_east_6": "marina_9_east",
    "marina_east_7": "marina_8_east",
    "marina_east_8": "marina_7_east",
    "marina_east_9": "marina_6_east",
    "marina_east_10": "marina_15_east",
    "marina_east_11": "marina_14_east",
    "marina_east_12": "marina_13_east",
    "marina_east_13": "marina_12_east",
    "marina_east_14": "marina_11_east",
    "marina_east_15": "marina_20_east",
    "marina_east_16": "marina_19_east",
    "marina_east_17": "marina_18_east",
    "marina_east_18": "marina_17_east",
    "marina_east_19": "marina_16_east",
    #
    "marina_south_0": "marina_5_south",
    "marina_south_1": "marina_4_south",
    "marina_south_2": "marina_3_south",
    "marina_south_3": "marina_2_south",
    "marina_south_4": "marina_1_south",
    "marina_south_5": "marina_10_south",
    "marina_south_6": "marina_9_south",
    "marina_south_7": "marina_8_south",
    "marina_south_8": "marina_7_south",
    "marina_south_9": "marina_6_south",
    "marina_south_10": "marina_15_south",
    "marina_south_11": "marina_14_south",
    "marina_south_12": "marina_13_south",
    "marina_south_13": "marina_12_south",
    "marina_south_14": "marina_11_south",
    "marina_south_15": "marina_20_south",
    "marina_south_16": "marina_19_south",
    "marina_south_17": "marina_18_south",
    "marina_south_18": "marina_17_south",
    "marina_south_19": "marina_16_south",
    #
    "marina_west_0": "marina_5_west",
    "marina_west_1": "marina_4_west",
    "marina_west_2": "marina_3_west",
    "marina_west_3": "marina_2_west",
    "marina_west_4": "marina_1_west",
    "marina_west_5": "marina_10_west",
    "marina_west_6": "marina_9_west",
    "marina_west_7": "marina_8_west",
    "marina_west_8": "marina_7_west",
    "marina_west_9": "marina_6_west",
    "marina_west_10": "marina_15_west",
    "marina_west_11": "marina_14_west",
    "marina_west_12": "marina_13_west",
    "marina_west_13": "marina_12_west",
    "marina_west_14": "marina_11_west",
    "marina_west_15": "marina_20_west",
    "marina_west_16": "marina_19_west",
    "marina_west_17": "marina_18_west",
    "marina_west_18": "marina_17_west",
    "marina_west_19": "marina_16_west",
}

for root, directories, filenames in os.walk(os.getcwd()):
    for filename in filenames:
        basename, ext = os.path.splitext(filename)
        path = os.path.join(root, filename)
        # Only touch png files starting with marina_ and end with a number
        if ext == ".png" and basename.startswith("marina_") and basename[-1].isdigit():
            if basename in rename_dict:
                new_basename = rename_dict[basename]
                new_path = os.path.join(root, new_basename + ".png")
                os.rename(path, new_path)
                if new_basename.endswith("_east"):
                    rotateImage(new_path, 270)
                if new_basename.endswith("_south"):
                    rotateImage(new_path, 180)
                if new_basename.endswith("_west"):
                    rotateImage(new_path, 90)
    # Skip subdirectories
    break
