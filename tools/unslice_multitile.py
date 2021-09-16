#!/usr/bin/env python3
'''
Combine a set of multitile sprites into 4x4 grid
'''

import argparse
import pyvips

from slice_multitile import MAPS


def main(args):
    multitile_dict = {}

    for suffix, position in MAPS[16].items():
        sprite = pyvips.Image.new_from_file(f'{args.tile}_{suffix}.png')
        multitile_dict[position] = sprite

    output_img = pyvips.Image.arrayjoin(
        [multitile_dict[i] for i in range(16)], across=4)
    output_img.pngsave(f'{args.tile}_multitile.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Combine a set of multitile sprites')
    parser.add_argument('tile', help='base name of the tile')
    main(parser.parse_args())
