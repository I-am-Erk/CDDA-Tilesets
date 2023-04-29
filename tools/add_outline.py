#!/usr/bin/env python3
"""
Add black outline to all sprites in a folder
"""
import os
import glob
import argparse
import numpy as np
from PIL import Image

BLANK = np.array([0, 0, 0, 0])
BLACK = np.array([0, 0, 0, 255])


def is_outline(table: np.array, col: int, row: int) -> bool:
    """
    Determine if the point belongs to the outline
    """
    up = table[row - 1, col, :]
    down = table[row + 1, col, :]
    left = table[row, col - 1, :]
    right = table[row, col + 1, :]

    for side in [left, right, up, down]:
        if (side != BLACK).any() & (side != BLANK).any():
            return True

    return False


def draw_outline(data: np.array) -> None:
    """
    Add outline to the pixels array in-place
    """
    for i in range(1, 30):
        for j in range(1, 30):
            if (data[j, i, :] == BLANK).any():
                if is_outline(data, i, j):
                    data[j, i, :] = BLACK


def main(args: argparse.Namespace) -> None:
    """
    Add outlines to all *.png images in the args.folder
    """
    for filename in glob.glob(os.path.join(args.folder, '*.png')):
        with Image.open(
                os.path.join(os.getcwd(), filename)).convert('RGBA') as img:
            data = np.array(img)
            draw_outline(data)
            Image.fromarray(data, mode='RGBA').save(filename, 'PNG')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add black outline around a sprite")
    parser.add_argument(
        "folder",
        help="path to the folder of images to edit")
    main(parser.parse_args())

