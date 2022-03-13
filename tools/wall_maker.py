#!/usr/bin/env python3

"""Wall maker"""
# FIXME: missing purpose of module in doc

import os
import sys
import tempfile

import argparse
import requests
from PIL import Image

sys.path.append("pixray")
import pixray  # noqa pylint: disable=C0413

parser = argparse.ArgumentParser()
# FIXME: missing argument descriptions
parser.add_argument(
    'name', type=str,
    help=""
)
parser.add_argument(
    'palette', type=str,
    help=""
)
parser.add_argument(
    'prompt', type=str,
    help=""
)


def generate_horizontal(name, prompt, palette, overlay_url):
    """Generate horizontal"""
    # FIXME: missing meaningful doc

    overlay_temp_filename = os.path.join(tempfile.gettempdir(), 'overlay.png')

    config = {
        'prompt': f"{prompt} #pixelart",
        'drawer': "pixel",
        'size': [32, 32],
        'pixel_size': [32, 32],
        'iterations': 90,
        'filters': "wallpaper,lookup",
        'palette': f"{palette}.png",
        'overlay_image': overlay_temp_filename,
        'overlay_every': 20,
        'overlay_alpha': 0,
        'overlay_offset': 5,
        'output_name': f"{name}_edge_ew1.png"
    }

    canvas = Image.new('RGBA', (36, 32))
    image = Image.open(config['output_name'])
    # same height as `image`
    mask = Image.new('RGBA', (2, 32), color=(1., 1., 1., .25))

    # download overlay
    img_data = requests.get(overlay_url).content
    with open(overlay_temp_filename, 'wb') as handler:
        handler.write(img_data)

    # step 1
    pixray.run(**config)

    overlay_image = Image.open(overlay_temp_filename)
    canvas.paste(overlay_image, box=(2, 0))
    # left edge
    canvas.paste(image.crop((0, 0, 2, 32)), (0, 0), mask=mask)
    # right edge
    canvas.paste(image.crop((30, 0, 32, 32)), (32, 32), mask=mask)

    canvas.save(f"{name}_ew_transparencymap.png")

    # step 2
    config = {
        'size': [36, 32],
        'pixel_size': [36, 32],
        'filters': "wallpaper",
        'palette': f"{name}_edge_ew.png",
        'overlay_image': f"{name}_ew_transparencymap.png"
    }
    pixray.run(**config)

    image = Image.open(f"{name}_edge_ew.png").crop((2, 0, 32, 32))
    image.save(f"{name}_edge_ew2.png")

    config['output_name'] = f"{name}_edge_ew3.png"

    pixray.run(**config)


if __name__ == '__main__':
    URL = "https://raw.githubusercontent.com/I-am-Erk/CDDA-Tilesets/precursor-sprites-for-pixray/pixray/wall_ew_transmap2.png"  # noqa pylint: disable=C0301

    args = parser.parse_args()

    generate_horizontal(args.name, args.prompt, args.palette, URL)
    sys.exit()
