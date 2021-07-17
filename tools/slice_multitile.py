#!/usr/bin/env python3
"""
Slice a multitile image into individual images for usage in tileset definitions
"""

import os
import argparse
import json
import pathlib
import pyvips


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
}


def main(args):
    args.height = args.height or args.width

    if args.tile is None:
        args.tile = pathlib.Path(args.image).stem\
            .replace('autotile_', '').replace('multitile_', '')\
            .replace('_autotile', '').replace('_multitile', '')  # TODO: regex

    output_dir = args.out or os.path.join(
        os.path.dirname(args.image), args.tile)

    img = pyvips.Image.new_from_file(args.image)

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    slices = []

    for y in range(0, img.height, args.height):
        for x in range(0, img.width, args.width):
            slices.append(img.crop(x, y, args.width, args.height))

    slicing_map = MAPS.get(len(slices))
    if slicing_map is None:
        raise Exception(
            'No slicing map that matches these sizes, '
            'did you forget to specify height?')

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
        "--background", dest='background',
        help="background sprite name")
    main(parser.parse_args())
