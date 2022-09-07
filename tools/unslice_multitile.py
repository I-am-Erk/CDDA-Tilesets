#!/usr/bin/env python3
'''
Combine a set of multitile sprites into 4x4 grid
'''

import argparse
import os
import pyvips
import numpy as np

from slice_multitile import MAPS


def main(args):
    multitile_dict = {}

    width = None
    height = None
    id_map = MAPS["iso"] if args.iso else MAPS[16]
    for suffix, position in id_map.items():
        sprite = pyvips.Image.new_from_file(os.path.join(args.path, f'{args.tile}_{suffix}.png'))

        if args.iso:
            if sprite.width % 4 != 0:
                raise Exception(
                    'Only width values multiples of 4 are supported in ISO mode.')
            if 2 * sprite.height < sprite.width:
                raise Exception(
                    'ISO sprite height must be at least half sprite width.')
            if width is None:
                width = sprite.width
                height = sprite.height
            elif width != sprite.width or height != sprite.height:
                raise Exception(
                    f'Expecting sprites of equal size. '
                    f'Got {sprite.width}x{height != sprite.height}, expected {width}x{height}.')

        multitile_dict[position] = sprite

    if args.iso:
        extra_height = height - width // 2
        output_img = pyvips.Image.new_from_array(
            np.full(shape=(width * 2 + extra_height, width * 4, 4),
                    fill_value=0, dtype=np.uint8),
            interpretation="rgb")

        dx = width // 2
        dy = width // 4

        index = 0
        for row in range(7):
            per_row = min(row, 6 - row) + 1
            half_offsets = (8 - 2 * per_row) // 2
            x_offset = half_offsets * dx
            y_offset = row * dy
            for col in range(per_row):
                output_img = output_img.composite(
                    multitile_dict[index], mode="over", x=x_offset + col * width, y=y_offset)
                index += 1

    else:
        output_img = pyvips.Image.arrayjoin(
            [multitile_dict[i] for i in range(16)], across=4)

    output_img.pngsave(os.path.join(args.path, f'{args.tile}_multitile.png'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Combine a set of multitile sprites')
    parser.add_argument('tile', help='base name of the tile')
    parser.add_argument('--path',
                        required=False,
                        default=".",
                        help='path to the directory of the tile')
    parser.add_argument(
        "--iso", action='store_true',
        help="unslice to isometric autotile")
    main(parser.parse_args())
