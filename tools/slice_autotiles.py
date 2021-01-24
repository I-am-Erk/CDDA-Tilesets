#!/usr/bin/env python3
"""
Slice an autotile image into individual images for usage in tileset definitions
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
    img = pyvips.Image.new_from_file(args.image)

    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)

    slices = []

    for y in range(0, img.height, args.size):
        for x in range(0, img.width, args.size):
            slices.append(img.crop(x, y, args.size, args.size))

    for suffix, position in MAPS[len(slices)].items():
        slices[position].pngsave(
            os.path.join(args.out, f'{args.tile}_{suffix}.png'))

    if args.no_json:
        return

    json_content = {
        "id": args.tile,
        "fg": f"{args.tile}_unconnected",
        "bg": "",
        "multitile": True,
        "additional_tiles": [
            {
                "id": "center",
                "fg": f"{args.tile}_center",
                "bg": "",
            }, {
                "id": "corner",
                "fg": [
                    f"{args.tile}_corner_nw",
                    f"{args.tile}_corner_sw",
                    f"{args.tile}_corner_se",
                    f"{args.tile}_corner_ne"],
                "bg": "",
            }, {
                "id": "t_connection",
                "fg": [
                    f"{args.tile}_t_connection_n",
                    f"{args.tile}_t_connection_w",
                    f"{args.tile}_t_connection_s",
                    f"{args.tile}_t_connection_e"],
                "bg": "",
            }, {
                "id": "edge",
                "fg": [
                    f"{args.tile}_edge_ns",
                    f"{args.tile}_edge_ew"],
                "bg": "",
            }, {
                "id": "end_piece",
                "fg": [
                    f"{args.tile}_end_piece_n",
                    f"{args.tile}_end_piece_w",
                    f"{args.tile}_end_piece_s",
                    f"{args.tile}_end_piece_e"],
                "bg": "",
            }, {
                "id": "unconnected",
                # two copies because multitiles are assumed to rotate
                "fg": [f"{args.tile}_unconnected", f"{args.tile}_unconnected"],
                "bg": ""
            }
        ]
    }

    tile_json_filename = os.path.join(args.out, f"{args.tile}.json")
    with open(tile_json_filename, "w") as tile_json_file:
        json.dump(json_content, tile_json_file, indent=2)
        tile_json_file.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slice an autotile image")
    parser.add_argument("tile", help="base name of the tile")
    parser.add_argument("size", type=int, help="tile size in pixels")
    parser.add_argument("image", help="path to autotile image")
    parser.add_argument("out", help="output path")
    parser.add_argument("--no-json", action='store_true',
                        help="disable json file generation")
    main(parser.parse_args())
