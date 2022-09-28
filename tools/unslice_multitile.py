#!/usr/bin/env python3
'''
Combine a set of multitile sprites into 4x4 or 5x5 grid grid
'''

import argparse
import os
import math
import numpy as np

from slice_multitile import MAPS, MAPS_ISO

try:
    vips_path = os.getenv("LIBVIPS_PATH")
    if vips_path is not None and vips_path != "":
        os.environ["PATH"] += ";"+os.path.join(vips_path, "bin")
    import pyvips
    Vips = pyvips
except ImportError:
    import gi
    gi.require_version('Vips', '8.0')  # NoQA
    from gi.repository import Vips


def main(args):
    multitile_dict = {}

    width = None
    height = None
    num_sprites = 25 if os.path.isfile(os.path.join(args.path, f'{args.tile}_unconnected_faceN.png')) else 16
    template_size = math.isqrt(num_sprites)

    id_map = MAPS_ISO[num_sprites] if args.iso else MAPS[num_sprites]
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
            np.full(shape=(width // 2 * template_size + extra_height, width * template_size, 4),
                    fill_value=0, dtype=np.uint8),
            interpretation="rgb")

        dx = width // 2
        dy = width // 4

        double_size = 2 * template_size
        index = 0
        for row in range(double_size - 1):
            per_row = min(row, double_size - 2 - row) + 1
            half_offsets = (double_size - 2 * per_row) // 2
            x_offset = half_offsets * dx
            y_offset = row * dy
            for col in range(per_row):
                output_img = output_img.composite(
                    multitile_dict[index], mode="over", x=x_offset + col * width, y=y_offset)
                index += 1

    else:
        output_img = pyvips.Image.arrayjoin(
            [multitile_dict[i] for i in range(num_sprites)], across=template_size)

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
