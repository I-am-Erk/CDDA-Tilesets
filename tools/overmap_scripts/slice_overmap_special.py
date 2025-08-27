#!/usr/bin/env python3

"""
See doc/how-to/overmap_special_slicing.md
"""

from PIL import Image

import argparse
import os


def ensure_absolute_path(path):
    if os.path.isabs(path):
        return path
    script_dir = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(script_dir, path))


args = argparse.ArgumentParser()
args.add_argument(
    "input_path",
    help="target file/directory location, if ran over a directory all .png files (excluding those in subdirectories) will be targetted",
    type=ensure_absolute_path,
)
args.add_argument(
    "--width",
    help="width of output pngs",
    type=int,
    default=32,
)
args.add_argument(
    "--height",
    help="height of output pngs",
    type=int,
    default=32,
)
args.add_argument(
    "-o",
    "--output",
    help="specify output path, defaults to target path",
    type=str,
    action="store",
    default="",
)
args.add_argument(
    "-so",
    "--slice-only",
    help="slice target file(s) without renaming",
    action="store_true",
)
args.add_argument(
    "-ta",
    "--target-all",
    help="slice unknown file(s) without renaming",
    action="store_true",
)
args.add_argument(
    "-sd", "--subdirectories", help="also run over subdirectories", action="store_true"
)
args_dict = vars(args.parse_args())

rename_dict = {
    "marina_0": "marina_5",
    "marina_1": "marina_4",
    "marina_2": "marina_3",
    "marina_3": "marina_2",
    "marina_4": "marina_1",
    "marina_5": "marina_10",
    "marina_6": "marina_9",
    "marina_7": "marina_8",
    "marina_8": "marina_7",
    "marina_9": "marina_6",
    "marina_10": "marina_15",
    "marina_11": "marina_14",
    "marina_12": "marina_13",
    "marina_13": "marina_12",
    "marina_14": "marina_11",
    "marina_15": "marina_20",
    "marina_16": "marina_19",
    "marina_17": "marina_18",
    "marina_18": "marina_17",
    "marina_19": "marina_16",
}


def shouldTargetFile(filename, total_sprites):
    if args_dict["target_all"]:
        return True
    for num in range(int(total_sprites)):
        potential_lookup = filename + "_" + str(num)
        if potential_lookup in rename_dict:
            return True
    return False


def shouldIgnore(image):
    extrema = image.convert("L").getextrema()
    # If it's all white or black
    if extrema == (0, 0) or extrema == (1, 1):
        return True
    if image.info.get("transparency", None) is not None:
        extrema = image.convert("A").getextrema()
        # Or fully transparent
        if extrema == (0, 0):
            return True
    return False


def cutPNG(path):
    source_image = Image.open(path)

    input_filename = os.path.splitext(os.path.basename(path))[0]
    rotate_before_saving = 0
    directionless_filename = input_filename
    direction = ""
    if directionless_filename.endswith("_north"):
        directionless_filename = directionless_filename[:-6]
        direction = "_north"
    if directionless_filename.endswith("_east"):
        source_image = source_image.rotate(90, expand=1)
        rotate_before_saving = 270
        directionless_filename = directionless_filename[:-5]
        direction = "_east"
    if directionless_filename.endswith("_south"):
        source_image = source_image.rotate(180, expand=1)
        rotate_before_saving = 180
        directionless_filename = directionless_filename[:-6]
        direction = "_south"
    if directionless_filename.endswith("_west"):
        source_image = source_image.rotate(270, expand=1)
        rotate_before_saving = 90
        directionless_filename = directionless_filename[:-5]
        direction = "_west"

    output_width = args_dict["width"]
    output_height = args_dict["height"]
    input_width, input_height = source_image.size

    if input_height == output_height and input_width == output_width:
        # Ignore images with the output dimensions
        return
    if input_height % output_height != 0 or input_width % output_width != 0:
        print(
            "Source file %s has pixel width and height %s, %s which isn't divisible by the provided output dimensions %s, %s"
            % (input_filename, input_width, input_height, output_width, output_height)
        )
        return

    images_per_row = input_width / args_dict["width"]
    total_sprites = images_per_row * (input_height / output_height)
    if not shouldTargetFile(directionless_filename, total_sprites):
        return

    output_directory = (
        os.path.dirname(path) if args_dict["output"] == "" else args_dict["output"]
    )
    for output_suffix in range(int(total_sprites)):
        column = output_suffix % images_per_row
        row = (output_suffix - column) / images_per_row

        left_x = column * output_width
        right_x = left_x + output_width
        top_y = row * output_height
        bottom_y = top_y + output_height

        output_image = source_image.crop((left_x, top_y, right_x, bottom_y))
        if not shouldIgnore(output_image):
            output_filename = input_filename + "_" + str(output_suffix)
            if not args_dict["slice_only"]:
                output_directionless_filename = (
                    directionless_filename + "_" + str(output_suffix)
                )
                if output_directionless_filename in rename_dict:
                    output_filename = (
                        rename_dict[output_directionless_filename] + direction
                    )
            if rotate_before_saving != 0:
                output_image = output_image.rotate(rotate_before_saving)
            output_image.save(os.path.join(output_directory, output_filename + ".png"))


if os.path.isdir(args_dict["input_path"]):
    for root, directories, filenames in os.walk(args_dict["input_path"]):
        # Delay cutting files until finding all source files in case we're outputting to the same directory
        paths = []
        for filename in filenames:
            if filename.endswith(".png"):
                paths.append(os.path.join(root, filename))
            # Skip unrecognised filetypes
        for path in paths:
            cutPNG(path)
        if not args_dict["subdirectories"]:
            break
elif args_dict["input_path"].endswith(".png"):
    cutPNG(args_dict["input_path"])
else:
    print("Unrecognised filetype, supported file types: '.png'")
