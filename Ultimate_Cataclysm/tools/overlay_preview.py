#!/usr/bin/env python3
"""
Generate preview for overlay sprites

Example:
./overlay_preview.py maid_dress maid_hat -i ../gfx -o preview.png --scale 2
"""

import os
import argparse
import json
from pathlib import Path
import pyvips
import itertools
import sys
from math import ceil

parser = argparse.ArgumentParser(description='Generate preview for overlay sprites')
parser.add_argument('id', nargs='+', help='ids of items in preview')
parser.add_argument('-i', '--input', help='input path (gfx directory)', required=True)
parser.add_argument('-o', '--output', help='output path', default='output.png')
parser.add_argument('-s', '--scale', help='output image scale', default=2)
parser.add_argument('-gw', '--grid-width', help='maximum grid width of output image', default=9)
parser.add_argument('--gender', help='gender of a dummy', default='male', choices={'male', 'female'})
parser.add_argument('--skin', help='skin color of a dummy', default='rose', choices={'brown', 'dark', 'light', 'rose', 'tan'})

def wrap(l):
    return l if type(l) is list else [l]


def flatten(l):
    return list(itertools.chain.from_iterable(l))


def parse_json_item(item):
    with open(item) as f:
        raw = wrap(json.load(f))
        res = [[{'id': j, 'fg': str(Path(item.parent, f"{i['fg'][0]}.png"))} for j in wrap(i['id'])] for i in raw]
        return flatten(res)


def main():
    args = parser.parse_args()


    # output image configuration
    l = len(args.id)
    gridw = min(l, int(args.grid_width))
    gridh = ceil(l / gridw)

    print('\033[94m  ℹ  configuration:\n{}\033[0m'.format(
        '\n'.join(map(lambda x: ' ' * 9 + x, [
            f'output grid: {gridw}x{gridh}',
            f'scale: x{args.scale}']))))


    # generate items database
    print('\033[94m  ℹ  generating item database..\033[0m')
    items = flatten([parse_json_item(f) for f in Path(args.input).rglob('items/**/*.json')])

    # generate overlays database
    print('\033[94m  ℹ  generating overlays database..\033[0m')
    overlays = flatten([parse_json_item(f) for f in Path(args.input).rglob('overlay/**/*.json')])

    # find skin
    print('\033[94m  ℹ  searching for a skin for dummy..\033[0m')
    skin_map = {
        'brown': 'SKIN_MEDIUM',
        'dark': 'SKIN_DARK',
        'light': 'SKIN_LIGHT',
        'rose': 'SKIN_PINK',
        'tan': 'SKIN_TAN'
    }
    skin = None
    skin_req_id = f'overlay_{args.gender}_mutation_{skin_map[args.skin]}'
    for f in Path(args.input).rglob('overlay/skin/**/*.json'):
        with open(f) as s:
            raw = wrap(json.load(s))
            for skindef in raw:
                if skindef['id'] == skin_req_id:
                    skin = pyvips.Image.new_from_file(str(Path(f.parent, f"{skindef['fg'][0]}.png")), access='sequential')
    if not skin:
        print(f'\033[91m  ✘  error: requested skin \"{args.skin}\" for gender \"{args.gender}\" not found !\033[0m')
        sys.exit(1)


    # processing
    print('\033[94m  ℹ  processing output image..\033[0m')
    args_split = [args.id[i:i + gridw] for i in range(0, len(args.id), gridw)]
    err = False
    layers = []
    for subset in args_split:
        arr = []
        # paste overlay
        for id in subset:
            entry = next((i for i in overlays if i['id'].startswith(f'overlay_{args.gender}') and i['id'].endswith('_' + id)), None)
            if not entry:
                entry = next((i for i in overlays if i['id'].startswith(f'overlay_') and i['id'].endswith('_' + id)), None)
            if entry:
                image = pyvips.Image.new_from_file(entry['fg'], access='sequential')
                image = skin.composite2(image, "VIPS_BLEND_MODE_OVER")
                arr.append(image)
            else:
                print(f'\033[91m  ✘  error: overlay for \"{id}\" does not exist in the tileset !\033[0m')
                err = True

        # paste items
        for id in subset:
            entry = next((i for i in items if i['id'] == id), None)
            if entry:
                image = pyvips.Image.new_from_file(entry['fg'], access='sequential')
                arr.append(image)
            else:
                print(f'\033[91m  ✘  error: item with id \"{id}\" does not exist in the tileset !\033[0m')
                err = True

        
        layer_image = pyvips.Image.arrayjoin(arr, across=len(subset))
        layers.append(layer_image)

    if err:
        sys.exit(1)

    outimage = pyvips.Image.arrayjoin(layers, across=1, halign="centre")
    outimage = outimage.resize(args.scale, kernel='nearest')
    outimage.write_to_file(args.output)

if __name__ == "__main__":
    main()
