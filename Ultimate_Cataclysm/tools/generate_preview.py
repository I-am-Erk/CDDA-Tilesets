#!/usr/bin/env python3
"""
Generate preview for wielded/worn, item and moster sprites.

1. Generate items preview:
./generate_preview.py -i ../gfx -o preview.png --scale 2
                      --items rock sharp_rock

2. Generate wielded or worn preview:
./generate_preview.py -i ../gfx -o preview.png --scale 2
                      --overlays jeans rebar
                      --overlay-skin dark

3. Generate items preview with overlays (merge of --items and --overlay with the same id):
./generate_preview.py -i ../gfx -o preview.png --scale 2
                      --overlays-with-items maid_hat maid_dress stocking
                      --overlays-gender female --overlay-skin pink

4. Generate monsters preview:
./generate_preview.py -i ../gfx -o preview.png --scale 2
                      --monster mon_bear mon_zombear mon_zombie

5. Combine:
./generate_preview.py -i ../gfx -o preview.png --scale 2
                      --monster mon_bee mon_ant
                      --items 2x4 stick scrap
                      --overlays-with-items box_small box_medium box_large
                      --overlays jumpsuit
"""

import os
import argparse
import json
from pathlib import Path
import pyvips
import itertools
import sys
from math import ceil

def wrap(l):
    return l if type(l) is list else [l]


def flatten(l):
    return list(itertools.chain.from_iterable(l))


def chunked(l, chunk_size):
    return [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]


def deep_empty(l):
    for item in l:
        if not isinstance(item, list) or not deep_empty(item):
            return False
    return True


def map_fg(path, item):
    if type(item) is dict:
        id = item["sprite"]
    else:
        id = item
    return str(Path(path.parent, f"{id}.png"))


def parse_json_item(item):
    with open(item) as f:
        raw = wrap(json.load(f))
        w, h = [x for x in item.parts if x.startswith('pngs_')][0].split('_')[-1].split('x')
        res = [[{'id': j, 'fg': list(map(lambda x: map_fg(item, x), i['fg'])), 'w': w, 'h': h} for j in wrap(i['id'])] for i in raw]
        return flatten(res)


def find_simple(db, id):
    entry = next((i for i in db if i['id'] == id), None)
    if entry:
        images = [pyvips.Image.new_from_file(x, access='sequential') for x in entry['fg']]
        return pyvips.Image.arrayjoin(images)
    else:
        return None


def find_overlay(db, skin, gender, id):
    entry = next((i for i in db if i['id'].startswith(f'overlay_{gender}') and i['id'].endswith('_' + id)), None)
    if not entry:
        entry = next((i for i in db if i['id'].startswith(f'overlay_') and i['id'].endswith('_' + id)), None)
    if entry:
        images = [skin.composite2(pyvips.Image.new_from_file(x, access='sequential'), "VIPS_BLEND_MODE_OVER") for x in entry['fg']]
        return pyvips.Image.arrayjoin(images)
    else:
        return None


def main():
    # args and args validation
    parser = argparse.ArgumentParser(description='Generate preview for the game entities')

    ids_group = parser.add_argument_group('id selection')
    ids_group.add_argument('--items', nargs='+', help='id for items to preview')
    ids_group.add_argument('--overlays', nargs='+', help='id for wield/worn to preview')
    ids_group.add_argument('--overlays-with-items', nargs='+', help='id for wield/worn + same id items to preview')
    ids_group.add_argument('--monsters', nargs='+', help='id for mosters to preview')

    overlay_group = parser.add_argument_group('optional overlay options')
    overlay_group.add_argument('--overlay-gender', help='gender of a dummy', default='male', choices={'male', 'female'})
    overlay_group.add_argument('--overlay-skin', help='skin color of a dummy', default='rose', choices={'brown', 'dark', 'light', 'rose', 'tan'})

    base_group = parser.add_argument_group('base options')
    base_group.add_argument('-i', '--input', help='input path (gfx directory)', required=True)
    base_group.add_argument('-o', '--output', help='output path', default='output.png')
    base_group.add_argument('-s', '--scale', help='output image scale', default=2)
    base_group.add_argument('-gw', '--grid-width', help='maximum grid width of output image', default=9)

    args = parser.parse_args()

    if not args.items and not args.overlays and not args.overlays_with_items and not args.monsters:
        print(f'\033[91m  ✘  error: no input ids.\033[0m')
        sys.exit(1)


    # generate database
    print('\033[94m  ℹ  database construction:')
    print('       collecting items..')
    items = flatten([parse_json_item(f) for f in Path(args.input).rglob('items/**/*.json')])
    print('       collecting overlays..')
    overlays = flatten([parse_json_item(f) for f in Path(args.input).rglob('overlay/**/*.json')])
    print('       collecting monsters..\033[0m')
    monsters = flatten([parse_json_item(f) for f in Path(args.input).rglob('monsters/**/*.json')])

    # configuration
    conf = {
        'items': {
            'ids': args.items if args.items else []
        },
        'overlays': {
            'ids': args.overlays if args.overlays else []
        },
        'overitems': {
            'ids': args.overlays_with_items if args.overlays_with_items else []
        },
        'monsters': {
            'ids': args.monsters if args.monsters else []
        }
    }

    print('\033[94m  ℹ  configuration:\n{}\033[0m'.format(
        '\n'.join(map(lambda x: ' ' * 7 + x, [
            f'preview items: {len(conf["items"]["ids"]) + len(conf["overitems"]["ids"])}',
            f'preview overlay: {len(conf["overlays"]["ids"]) + len(conf["overitems"]["ids"])}',
            f'preview monsters: {len(conf["monsters"]["ids"])}'
            ]))))


    # find skin
    if conf['overlays']['ids'] or conf['overitems']['ids']:
        print('\033[94m  ℹ  searching for a skin for dummy..\033[0m')
        skin_map = {
            'brown': 'SKIN_MEDIUM',
            'dark': 'SKIN_DARK',
            'light': 'SKIN_LIGHT',
            'rose': 'SKIN_PINK',
            'tan': 'SKIN_TAN'
        }
        skin = None
        skin_req_id = f'overlay_{args.overlay_gender}_mutation_{skin_map[args.overlay_skin]}'
        for f in Path(args.input).rglob('overlay/skin/**/*.json'):
            with open(f) as s:
                raw = wrap(json.load(s))
                for skindef in raw:
                    if skindef['id'] == skin_req_id:
                        skin = pyvips.Image.new_from_file(str(Path(f.parent, f"{skindef['fg'][0]}.png")), access='sequential')
        if not skin:
            print(f'\033[91m  ✘  error: requested skin \"{args.overlay_skin}\" for gender \"{args.overlay_gender}\" not found !\033[0m')
            sys.exit(1)


    # processing
    print('\033[94m  ℹ  processing output image:')
    layers = []

    if conf['items']['ids']:
        print('\033[94m       items..')
        chunks = chunked(conf['items']['ids'], args.grid_width)
        for chunk in chunks:
            arr = []
            for id in chunk:
                image = find_simple(items, id)
                if image: arr.append(image)
                else: print(f'\033[93m  ⚠️  warning: item with id \"{id}\" does not exist in the tileset !\033[0m')
            if arr:
                layer_image = pyvips.Image.arrayjoin(arr, across=len(chunk))
                layers.append(layer_image)

    if conf['overlays']['ids']:
        print('\033[94m       overlays..')
        chunks = chunked(conf['overlays']['ids'], args.grid_width)
        for chunk in chunks:
            arr = []
            for id in chunk:
                image = find_overlay(overlays, skin, args.overlay_gender, id)
                if image: arr.append(image)
                else: print(f'\033[93m  ⚠️  warning: overlay for id \"{id}\" does not exist in the tileset !\033[0m')
            if arr:
                layer_image = pyvips.Image.arrayjoin(arr, across=len(chunk))
                layers.append(layer_image)

    if conf['overitems']['ids']:
        print('\033[94m       overlays with items..')
        chunks = chunked(conf['overitems']['ids'], args.grid_width)
        for chunk in chunks:
            arr = []
            for id in chunk:
                overlay_image = find_overlay(overlays, skin, args.overlay_gender, id)
                if not overlay_image: 
                    print(f'\033[93m  ⚠️  warning: overlay for id \"{id}\" does not exist in the tileset !\033[0m')

                item_image = find_simple(items, id)
                if not item_image: 
                    print(f'\033[93m  ⚠️  warning: item with id \"{id}\" does not exist in the tileset !\033[0m')

                if overlay_image and item_image:
                    arr.append(pyvips.Image.arrayjoin([overlay_image, item_image], across=1))
                elif overlay_image:
                    arr.append(overlay_image)
                elif item_image:
                    arr.append(item_image)
            if arr:
                layer_image = pyvips.Image.arrayjoin(arr, across=len(chunk))
                layers.append(layer_image)

    if conf['monsters']['ids']:
        print('\033[94m       monsters..')
        chunks = chunked(conf['monsters']['ids'], args.grid_width)
        for chunk in chunks:
            arr = []
            for id in chunk:
                image = find_simple(monsters, id)
                if image: arr.append(image)
                else: print(f'\033[93m  ⚠️  warning: monster with id \"{id}\" does not exist in the tileset !\033[0m')
            if arr:
                layer_image = pyvips.Image.arrayjoin(arr, across=len(chunk))
                layers.append(layer_image)

    print('\033[94m       writing..\033[0m')
    if layers:
        outimage = pyvips.Image.arrayjoin(layers, across=1, halign='centre', valign='centre')
        outimage = outimage.resize(args.scale, kernel='nearest')
        outimage.write_to_file(args.output)
    else:
        print(f'\033[93m  ⚠️  warning: no sprites to draw !\033[0m')


if __name__ == "__main__":
    main()
