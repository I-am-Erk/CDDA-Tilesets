#!/usr/bin/env python3
"""
Generate preview for wielded/worn, item and moster sprites.

1. Generate items preview:
./tools/generate_preview.py -i gfx -o preview.png --scale 2
                      --items rock sharp_rock

2. Generate wielded or worn preview:
./tools/generate_preview.py -i gfx -o preview.png --scale 2
                      --overlays jeans rebar --overlay-skin dark

3. Generate items preview with overlays (merge of --items and --overlay with the same id):
./tools/generate_preview.py -i gfx -o preview.png --scale 2
                      --overlays-with-items maid_hat maid_dress stocking
                      --overlays-gender female --overlay-skin pink

4. Generate monsters preview:
./tools/generate_preview.py -i gfx -o preview.png --scale 2
                      --monster mon_bear mon_zombear mon_zombie

5. Combine:
./tools/generate_preview.py -i gfx -o preview.png --scale 2
                      --monster mon_bee mon_ant
                      --items 2x4 stick scrap
                      --overlays-with-items box_small box_medium box_large
                      --overlays jumpsuit

6. Generate anything from path:
./tools/generate_preview.py -i gfx -o preview.png --scale 2
                      --from-path pngs_normal_32x_32/monsters
"""

import os
import argparse
import json
from pathlib import Path
import pyvips
import itertools
import sys
from functools import reduce
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


def res_or_warn(fun, warn):
    res = fun()
    if res:
        return res
    else:
        print(f'\033[93m  ⚠️  warning: {warn}\033[0m')
        return None


def map_img(item):
    return item["sprite"] if type(item) is dict else item


def parse_json_item(item):
    with open(item) as f:
        raw = wrap(json.load(f))
        w, h = [x for x in item.parts if x.startswith('pngs_')][0].split('_')[-1].split('x')
        res = [[{
            'id': j, 
            'fg': list(map(map_img, i['fg'])), 
            'bg': list(map(map_img, i['bg'])), 
            'w': w, 
            'h': h
        } for j in wrap(i['id'])] for i in raw]
        return flatten(res)


def get_img(images, id):
    return str(images[id])


def merge_fg_and_bg(images, fg, bg):
    if bg and fg:
        return [pyvips.Image.new_from_file(get_img(images, b), access='sequential')
                .composite2(pyvips.Image.new_from_file(get_img(images, f), access='sequential'), "VIPS_BLEND_MODE_OVER") 
                for f in fg for b in bg]
    elif fg:
        return [pyvips.Image.new_from_file(get_img(images, f), access='sequential') for f in fg]
    else:
        return []


def find_simple(images, db, id):
    entry = next((i for i in db if i['id'] == id), None)
    if entry:
        return merge_fg_and_bg(images, entry['fg'], entry['bg'])
    else:
        return None


def find_overlay(images, db, skin, gender, id):
    entry = next((i for i in db if i['id'].startswith(f'overlay_{gender}') and i['id'].endswith('_' + id)), None)
    if not entry:
        entry = next((i for i in db if i['id'].startswith(f'overlay_') and i['id'].endswith('_' + id)), None)
    if entry:
        images = [skin.composite2(pyvips.Image.new_from_file(get_img(images, x), access='sequential'), "VIPS_BLEND_MODE_OVER") for x in entry['fg']]
        return images
    else:
        return None


def pack_sprites(l, grid_size, fun):
    arr = []
    for id in l:
        res = fun(id)
        if res:
            arr.extend(res)

    layers = []
    if arr:
        chunks = chunked(arr, grid_size)
        for chunk in chunks:
            out = reduce(lambda img, new: img.join(new, 'horizontal', expand=True, align='centre'), chunk)
            layers.append(out)
    return layers


def main():
    # args and args validation
    parser = argparse.ArgumentParser(description='Generate preview for the game entities')

    ids_group = parser.add_argument_group('id selection')
    ids_group.add_argument('--items', nargs='+', help='id for items to preview')
    ids_group.add_argument('--overlays', nargs='+', help='id for wield/worn to preview')
    ids_group.add_argument('--overlays-with-items', nargs='+', help='id for wield/worn + same id items to preview')
    ids_group.add_argument('--monsters', nargs='+', help='id for mosters to preview')
    ids_group.add_argument('--from-path', nargs='+', help='get ids from jsons in given path')

    overlay_group = parser.add_argument_group('optional overlay options')
    overlay_group.add_argument('--overlay-gender', help='gender of a dummy', default='male', choices={'male', 'female'})
    overlay_group.add_argument('--overlay-skin', help='skin color of a dummy', default='rose', choices={'brown', 'dark', 'light', 'rose', 'tan'})

    base_group = parser.add_argument_group('base options')
    base_group.add_argument('-i', '--input', help='input path (gfx directory)', required=True)
    base_group.add_argument('-o', '--output', help='output path', default='output.png')
    base_group.add_argument('-s', '--scale', help='output image scale', type=int, default=2)
    base_group.add_argument('-gw', '--grid-width', help='maximum grid width of output image', type=int, default=9)

    args = parser.parse_args()

    if not args.items and not args.overlays and not args.overlays_with_items and not args.monsters and not args.from_path:
        print(f'\033[91m  ✘  error: no input ids.\033[0m')
        sys.exit(1)


    # generate database
    print('\033[94m  ℹ  database construction:\033[0m')
    print('       collecting images..')
    images = dict([(f.stem, f) for f in Path(args.input).rglob('**/*.png')])
    print('       collecting items..')
    items = flatten([parse_json_item(f) for f in Path(args.input).rglob('items/**/*.json')])
    print('       collecting overlays..')
    overlays = flatten([parse_json_item(f) for f in Path(args.input).rglob('overlay/**/*.json')])
    print('       collecting monsters..')
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

    if args.from_path:
        for p in args.from_path:
            gathered = flatten([parse_json_item(f) for f in Path(args.input).rglob(f'{p}/**/*.json')])
            for data in gathered:
                if data['id'].startswith('mon'):
                    conf['monsters']['ids'].append(data['id'])
                elif data['id'].startswith('overlay'):
                    conf['overlays']['ids'].append(data['id'])
                else:
                    conf['items']['ids'].append(data['id'])

    print('\033[94m  ℹ  configuration:\n\033[0m{}'.format(
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
                        skin = pyvips.Image.new_from_file(get_img(images, skindef['fg'][0]), access='sequential')
        if not skin:
            print(f'\033[91m  ✘  error: requested skin \"{args.overlay_skin}\" for gender \"{args.overlay_gender}\" not found !\033[0m')
            sys.exit(1)


    # processing
    print('\033[94m  ℹ  processing output image:\033[0m')
    layers = []

    if conf['items']['ids']:
        print('       items..')
        layers.extend(pack_sprites(conf['items']['ids'], args.grid_width,
                      lambda id: res_or_warn(lambda: find_simple(images, items, id), 
                                             f"overlay for id \"{id}\" does not exist in the tileset !")))

    if conf['overlays']['ids']:
        print('       overlays..')
        gender = args.overlay_gender
        layers.extend(pack_sprites(conf['overlays']['ids'], args.grid_width,
                      lambda id: res_or_warn(lambda: find_overlay(images, overlays, skin, gender, id), 
                                             f"overlay for id \"{id}\" does not exist in the tileset !")))

    if conf['monsters']['ids']:
        print('       monsters..')
        layers.extend(pack_sprites(conf['monsters']['ids'], args.grid_width,
                      lambda id: res_or_warn(lambda: find_simple(images, monsters, id),
                                             f"monster with id \"{id}\" does not exist in the tileset !")))

    if conf['overitems']['ids']:
        print('       overlays with items..')
        def _pack_overitem(id):
            overlay_images = find_overlay(images, overlays, skin, args.overlay_gender, id)
            if not overlay_images: 
                print(f'\033[93m  ⚠️  warning: overlay for id \"{id}\" does not exist in the tileset !\033[0m')

            item_images = find_simple(images,items, id)
            if not item_images: 
                print(f'\033[93m  ⚠️  warning: item with id \"{id}\" does not exist in the tileset !\033[0m')
            if overlay_images and item_images:
                image = pyvips.Image.arrayjoin(overlay_images)
                image = image.join(pyvips.Image.arrayjoin(item_images), 'vertical')
                return [image]
            elif overlay_images:
                return overlay_images
            elif item_images:
                return item_images

        layers.extend(pack_sprites(conf['overitems']['ids'], args.grid_width, _pack_overitem))

    print('       writing..')
    if layers:
        outimage = reduce(lambda img, new: img.join(new, 'vertical', expand=True, align='centre'), layers)
        outimage = outimage.resize(args.scale, kernel='nearest')
        outimage.write_to_file(args.output)
    else:
        print(f'\033[93m  ⚠️  warning: no sprites to draw !\033[0m')


if __name__ == "__main__":
    main()
