#!/usr/bin/env python3
"""
Slice a multitile image into individual images for usage in tileset definitions
"""

import os
import argparse
import json
import pathlib
import numpy as np

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


MAPS = {
    48: {
        'unconnected': 10,
        'center': 11,
        'edge_ns': 3,  # |
        'edge_ew': 2,  # -
        # clockwise order
        'corner_ne': 1,  # ↗
        'corner_se': 9,  # ↘
        'corner_sw': 8,  # ↙
        'corner_nw': 0,  # ↖
        't_connection_n': 24,
        't_connection_e': 26,
        't_connection_s': 25,
        't_connection_w': 27,
        'end_piece_n': 16,
        'end_piece_e': 19,
        'end_piece_s': 18,
        'end_piece_w': 17,
    },
    16: {
        'unconnected': 0,
        'center': 10,
        'edge_ns': 8,  # |
        'edge_ew': 2,  # -
        # clockwise order
        'corner_ne':  7,  # ↗
        'corner_se': 15,  # ↘
        'corner_sw': 13,  # ↙
        'corner_nw':  5,  # ↖
        't_connection_n':  6,
        't_connection_e': 11,
        't_connection_s': 14,
        't_connection_w': 9,
        'end_piece_n':  4,
        'end_piece_e':  3,
        'end_piece_s': 12,
        'end_piece_w':  1,
    },
    "iso": {
        'unconnected': 6,
        'center': 8,
        'edge_ns': 13,  # |
        'edge_ew': 1,  # -
        # clockwise order
        'corner_ne':  2,  # ↗
        'corner_se': 9,  # ↘
        'corner_sw': 14,  # ↙
        'corner_nw':  7,  # ↖
        't_connection_n':  4,
        't_connection_e': 5,
        't_connection_s': 12,
        't_connection_w': 11,
        'end_piece_n':  10,
        'end_piece_e':  0,
        'end_piece_s': 15,
        'end_piece_w':  3,
    },
}

OUTPUT_ORDER = [
    'unconnected', 'end_piece_w', 'edge_ew', 'end_piece_e',
    'end_piece_n', 'corner_nw', 't_connection_n', 'corner_ne',
    'edge_ns', 't_connection_w', 'center', 't_connection_e',
    'end_piece_s', 'corner_sw', 't_connection_s', 'corner_se'
]


def main(args):
    args.height = args.height or args.width

    if args.tile is None:
        args.tile = pathlib.Path(args.image).stem\
            .replace('autotile_', '').replace('multitile_', '')\
            .replace('_autotile', '').replace('_multitile', '')  # TODO: regex

    rearrange = None
    rearrange_bottom = False
    if args.rearrange_top is not None and args.rearrange_bottom is not None:
        raise Exception(
            "Can only use one of --rearrange-top and rearrange-bottom.")
    rearrange = args.rearrange_top or args.rearrange_bottom
    rearrange_bottom = args.rearrange_bottom is not None

    if rearrange is not None and rearrange < args.height:
        raise Exception(
            f"Can't rearrange with a height smaller than the original sprite height ({args.height}). Got {rearrange}.")

    output_dir = args.out or os.path.join(
        os.path.dirname(args.image), args.tile)

    img = pyvips.Image.new_from_file(args.image)

    slices = extract_slices(img, args.width, args.height, args.iso)

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    slicing_map = MAPS.get("iso") if args.iso else MAPS.get(len(slices))
    if slicing_map is None:
        raise Exception(
            'No slicing map that matches these sizes, '
            'did you forget to specify height?')

    if rearrange is not None:
        img_out = pyvips.Image.new_from_array(
            np.full(shape=(rearrange * 4, args.width * 4, 4),
                    fill_value=1, dtype=np.uint8),
            interpretation="rgb")

        for col in range(4):
            for row in range(4):
                sprite = slices[slicing_map[OUTPUT_ORDER[col + 4 * row]]]
                y_offset = rearrange - args.height if rearrange_bottom else 0
                img_out = img_out.draw_image(sprite, col * args.width, row * rearrange + y_offset)

        img_out.pngsave(
            os.path.join(output_dir, f'{args.tile}_multitile_rearranged.png'))
    else:
        for suffix, position in slicing_map.items():
            slices[position].pngsave(
                os.path.join(output_dir, f'{args.tile}_{suffix}.png'))

        if args.no_json:
            return

        json_content = {  # double quotes here to make copying easier
            "id": args.tile,
            "fg": f"{args.tile}_unconnected",
            "multitile": True,
            "additional_tiles": [
                {
                    "id": "center",
                    "fg": f"{args.tile}_center",
                }, {
                    "id": "corner",
                    "fg": [
                        f"{args.tile}_corner_nw",
                        f"{args.tile}_corner_sw",
                        f"{args.tile}_corner_se",
                        f"{args.tile}_corner_ne"],
                }, {
                    "id": "t_connection",
                    "fg": [
                        f"{args.tile}_t_connection_n",
                        f"{args.tile}_t_connection_w",
                        f"{args.tile}_t_connection_s",
                        f"{args.tile}_t_connection_e"],
                }, {
                    "id": "edge",
                    "fg": [
                        f"{args.tile}_edge_ns",
                        f"{args.tile}_edge_ew"],
                }, {
                    "id": "end_piece",
                    "fg": [
                        f"{args.tile}_end_piece_n",
                        f"{args.tile}_end_piece_w",
                        f"{args.tile}_end_piece_s",
                        f"{args.tile}_end_piece_e"],
                }, {
                    "id": "unconnected",
                    # two copies because multitiles are assumed to rotate
                    "fg": [f"{args.tile}_unconnected", f"{args.tile}_unconnected"],
                }
            ]
        }

        if args.background is not None:
            json_content['bg'] = args.background
            for array in json_content['additional_tiles']:
                array['bg'] = args.background

        tile_json_filename = os.path.join(output_dir, f"{args.tile}.json")
        with open(tile_json_filename, "w") as tile_json_file:
            json.dump(json_content, tile_json_file, indent=2)
            tile_json_file.write("\n")


def iso_mask(width, height):
    mask = np.full(shape=(height, width, 4), fill_value=1, dtype=np.uint8)

    mid_x = width / 2
    mid_y = height / 2

    for iy, ix in np.ndindex(mask.shape[0:2]):
        dx = (mid_x - ix) if ix < mid_x else ix + 1 - mid_x
        dy = (mid_y - iy) if iy < mid_y else iy + 1 - mid_y
        dist = dx + 2 * dy
        if dist > height + 1:
            mask[iy, ix, :] = 0
            pass

    return mask


def extract_slices(img, width, height, iso):
    slices = []

    if iso:
        if width % 2 != 0 or height % 2 != 0:
            raise Exception(
                'Only even width and height values are supported in ISO mode.')
        if width != 2 * height:
            raise Exception(
                'Only tiles with a width:height ration 2:1 are supported in ISO mode.')
        if img.width != 4 * width or img.height != 4 * height:
            raise Exception(
                f"Unexpected image size. Expected {4 * width}x{4 * height}, got {img.width}x{img.height}."
            )

        mask = iso_mask(width, height)

        dx = width / 2
        dy = height / 2
        for row in range(7):
            per_row = min(row, 6 - row) + 1
            half_offsets = (8 - 2 * per_row) / 2
            x_offset = half_offsets * dx
            y_offset = row * dy
            for col in range(per_row):
                s = img.crop(x_offset + col * width, y_offset, width, height)
                masked = s.numpy() * mask
                slices.append(pyvips.Image.new_from_array(masked, interpretation="rgb"))

    else:
        for y in range(0, img.height, height):
            for x in range(0, img.width, width):
                slices.append(img.crop(x, y, width, height))

    return slices


if __name__ == "__main__":
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
        "--no-json", action='store_true',
        help="disable json file generation")
    parser.add_argument(
        "--iso", action='store_true',
        help="slice iso multitile")
    parser.add_argument(
        "--background", dest='background',
        help="background sprite name")
    parser.add_argument(
        "--rearrange-top", type=int,
        help="re-arrange to multitile with the given sprite height; "
             "if iso, bring into ortho format; aligns at the top")
    parser.add_argument(
        "--rearrange-bottom", type=int,
        help="re-arrange to multitile with the given sprite height; "
             "if iso, bring into ortho format; aligns at the bottom")

    main(parser.parse_args())
