#!/usr/bin/env python3
'''
Slice multitiles of arbitrary size into numbered variants.
'''

import argparse
import os
import pathlib

from slice_multitile import iso_mask

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
    args.height = args.height or args.width

    if args.tile is None:
        args.tile = pathlib.Path(args.image).stem \
            .replace('autotile_', '').replace('multitile_', '') \
            .replace('_autotile', '').replace('_multitile', '')  # TODO: regex

    output_dir = args.out or os.path.join(
        os.path.dirname(args.image), args.tile)

    img = pyvips.Image.new_from_file(args.image)

    slices = extract_slices(img, args.width, args.height, args.iso)

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    for i, sl in enumerate(slices):
        out_idx = i
        while args.append and os.path.isfile(os.path.join(output_dir, f'{args.tile}_{out_idx:02d}.png')):
            out_idx += 1
        sl.pngsave(
            os.path.join(output_dir, f'{args.tile}_{out_idx:02d}.png'))


def extract_slices(img, width, height, iso):
    try:
        if not img.hasalpha():
            img = img.addalpha()
        if img.get_typeof('icc-profile-data') != 0:
            img = img.icc_transform('srgb')
    except Vips.Error as vips_error:
        raise Exception('%s', vips_error)

    slices = []

    template_size_x = img.width // width
    template_size_y = img.height // height
    if img.width != template_size_x * width or img.height != template_size_y * height:
        raise Exception(
            f"Unexpected image size. Expecting integer multiple of tile size."
        )

    if iso:
        if width % 2 != 0 or height % 2 != 0:
            raise Exception(
                'Only even width and height values are supported in ISO mode.')
        if width != 2 * height:
            raise Exception(
                'Only tiles with a width:height ration 2:1 are supported in ISO mode.')

        mask = iso_mask(width, height)

        dx = width / 2
        dy = height / 2
        double_size = 2 * template_size_x
        for row in range(double_size - 1):
            per_row = min(row, double_size - 2 - row) + 1
            half_offsets = (double_size - 2 * per_row) / 2
            x_offset = half_offsets * dx
            y_offset = row * dy
            for col in range(per_row):
                s = img.crop(x_offset + col * width, y_offset, width, height)
                masked = s.numpy() * mask
                slices.append(pyvips.Image.new_from_array(masked, interpretation="srgb"))

    else:
        for y in range(0, img.height, height):
            for x in range(0, img.width, width):
                slices.append(img.crop(x, y, width, height))

    return slices


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Slice a multitile image")
    parser.add_argument(
        "image",
        help="path to the multitile image that will be sliced")
    parser.add_argument(
        "width", type=int,
        help="tile width in pixels")
    parser.add_argument(
        "height", type=int,
        nargs='?',
        help="tile height in pixels, defaults to tile width")
    parser.add_argument(
        "--tile", dest="tile",
        help="base name of the tile, defaults to the image name"
             " without .png, autotile_ and/or multitile_ parts")
    parser.add_argument(
        "--out", dest="out",
        help="output directory path, "
             "defaults to the tile name in the directory of the image")
    parser.add_argument(
        "--iso", action='store_true',
        help="slice iso multitile")
    parser.add_argument(
        "--append", action='store_true',
        help="do not overwrite numbered sprites, write with increased IDs")

    main(parser.parse_args())
