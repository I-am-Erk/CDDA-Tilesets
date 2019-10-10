#!/usr/bin/env python3
"""
Slice an autotile image into individual images for usage in tileset definitions
"""

import os
import argparse
import json
import pathlib
import pyvips

parser = argparse.ArgumentParser(description="Slice an autotile image")
parser.add_argument("tile", help="base name of the tile")
parser.add_argument("size", type=int, help="tile size in pixels")
parser.add_argument("image", help="path to autotile image")
parser.add_argument("out", help="output path")


def main():
    args = parser.parse_args()
    img = pyvips.Image.new_from_file(args.image)

    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)

    slices = []

    for y in range(0, img.height, args.size):
        for x in range(0, img.width, args.size):
            slices.append(img.crop(x, y, args.size, args.size))

    parts = {
        f"{args.tile}_unconnected.png": 10,
        f"{args.tile}_center.png": 11,
        f"{args.tile}_edge_ns.png": 3,
        f"{args.tile}_edge_ew.png": 2,
        f"{args.tile}_corner_nw.png": 0,
        f"{args.tile}_corner_sw.png": 8,
        f"{args.tile}_corner_se.png": 9,
        f"{args.tile}_corner_ne.png": 1,
        f"{args.tile}_t_connection_n.png": 24,
        f"{args.tile}_t_connection_w.png": 27,
        f"{args.tile}_t_connection_s.png": 25,
        f"{args.tile}_t_connection_e.png": 26,
        f"{args.tile}_end_piece_n.png": 16,
        f"{args.tile}_end_piece_w.png": 17,
        f"{args.tile}_end_piece_s.png": 18,
        f"{args.tile}_end_piece_e.png": 19
    }

    for path, index in parts.items():
        slices[index].pngsave(os.path.join(args.out, path))

    json_content = {
        "id": args.tile,
        "multitile": True,
        "fg": [f"{args.tile}_unconnected"],
        "bg": [],
        "additional_tiles": [
            {
                "id": "center",
                "bg": [],
                "fg": [f"{args.tile}_center"]
            },
            {
                "id": "corner",
                "bg": [],
                "fg": [f"{args.tile}_corner_nw",  f"{args.tile}_corner_sw",  f"{args.tile}_corner_se", f"{args.tile}_corner_ne"]
            },
            {
                "id": "t_connection",
                "bg": [],
                "fg": [f"{args.tile}_t_connection_n", f"{args.tile}_t_connection_w", f"{args.tile}_t_connection_s", f"{args.tile}_t_connection_e"]
            },
            {
                "id": "edge",
                "bg": [],
                "fg": [f"{args.tile}_edge_ns", f"{args.tile}_edge_ew"]
            },
            {
                "id": "end_piece",
                "bg": [],
                "fg": [f"{args.tile}_end_piece_n", f"{args.tile}_end_piece_w", f"{args.tile}_end_piece_s", f"{args.tile}_end_piece_e"]
            },
            {
                "bg": [],
                "id": "unconnected",
                "fg": [f"{args.tile}_unconnected"]
            }
        ]
    }

    with open(os.path.join(args.out, f"{args.tile}.json"), "w") as tile_json_file:
        json.dump(json_content, tile_json_file, indent = 2)

if __name__ == "__main__":
    main()
