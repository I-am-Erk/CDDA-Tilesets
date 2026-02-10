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
    "sand_pit_0": "sand_pit_NW",
    "sand_pit_1": "sand_pit_N",
    "sand_pit_2": "sand_pit_NE",
    "sand_pit_3": "sand_pit_W",
    "sand_pit_4": "sand_pit_M",
    "sand_pit_5": "sand_pit_E",
    "sand_pit_6": "sand_pit_SW",
    "sand_pit_7": "sand_pit_S",
    "sand_pit_8": "sand_pit_SE",
    #
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
    #
    "cloverleaf_5": "hw_clover_leaf_0_-5",
    "cloverleaf_14": "hw_clover_leaf_-3_-4",
    "cloverleaf_15": "hw_clover_leaf_-2_-4",
    "cloverleaf_16": "hw_clover_leaf_-1_-4",
    "cloverleaf_17": "hw_clover_leaf_0_-4",
    "cloverleaf_18": "hw_clover_leaf_1_-4",
    "cloverleaf_19": "hw_clover_leaf_2_-4",
    "cloverleaf_20": "hw_clover_leaf_3_-4",
    "cloverleaf_21": "hw_clover_leaf_4_-4",
    "cloverleaf_25": "hw_clover_leaf_-4_-3",
    "cloverleaf_26": "hw_clover_leaf_-3_-3",
    "cloverleaf_27": "hw_clover_leaf_-2_-3",
    "cloverleaf_28": "hw_clover_leaf_-1_-3",
    "cloverleaf_29": "hw_clover_leaf_0_-3",
    "cloverleaf_30": "hw_clover_leaf_1_-3",
    "cloverleaf_32": "hw_clover_leaf_3_-3",
    "cloverleaf_33": "hw_clover_leaf_4_-3",
    "cloverleaf_34": "hw_clover_leaf_5_-3",
    "cloverleaf_37": "hw_clover_leaf_-4_-2",
    "cloverleaf_38": "hw_clover_leaf_-3_-2",
    "cloverleaf_40": "hw_clover_leaf_-1_-2",
    "cloverleaf_41": "hw_clover_leaf_0_-2",
    "cloverleaf_42": "hw_clover_leaf_1_-2",
    "cloverleaf_43": "hw_clover_leaf_2_-2",
    "cloverleaf_45": "hw_clover_leaf_4_-2",
    "cloverleaf_46": "hw_clover_leaf_5_-2",
    "cloverleaf_49": "hw_clover_leaf_-4_-1",
    "cloverleaf_50": "hw_clover_leaf_-3_-1",
    "cloverleaf_51": "hw_clover_leaf_-2_-1",
    "cloverleaf_52": "hw_clover_leaf_-1_-1",
    "cloverleaf_56": "hw_clover_leaf_3_-1",
    "cloverleaf_57": "hw_clover_leaf_4_-1",
    "cloverleaf_58": "hw_clover_leaf_5_-1",
    "cloverleaf_61": "hw_clover_leaf_-4_0",
    "cloverleaf_62": "hw_clover_leaf_-3_0",
    "cloverleaf_63": "hw_clover_leaf_-2_0",
    "cloverleaf_64": "hw_clover_leaf_-1_0",
    "cloverleaf_67": "hw_clover_leaf_2_0",
    "cloverleaf_69": "hw_clover_leaf_4_0",
    "cloverleaf_70": "hw_clover_leaf_5_0",
    "cloverleaf_71": "hw_clover_leaf_6_0",
    "cloverleaf_72": "hw_clover_leaf_-5_1",
    "cloverleaf_73": "hw_clover_leaf_-4_1",
    "cloverleaf_74": "hw_clover_leaf_-3_1",
    "cloverleaf_75": "hw_clover_leaf_-2_1",
    "cloverleaf_76": "hw_clover_leaf_-1_1",
    "cloverleaf_79": "hw_clover_leaf_2_1",
    "cloverleaf_80": "hw_clover_leaf_3_1",
    "cloverleaf_81": "hw_clover_leaf_4_1",
    "cloverleaf_82": "hw_clover_leaf_5_1",
    "cloverleaf_85": "hw_clover_leaf_-4_2",
    "cloverleaf_86": "hw_clover_leaf_-3_2",
    "cloverleaf_87": "hw_clover_leaf_-2_2",
    "cloverleaf_88": "hw_clover_leaf_-1_2",
    "cloverleaf_91": "hw_clover_leaf_2_2",
    "cloverleaf_92": "hw_clover_leaf_3_2",
    "cloverleaf_93": "hw_clover_leaf_4_2",
    "cloverleaf_94": "hw_clover_leaf_5_2",
    "cloverleaf_97": "hw_clover_leaf_-4_3",
    "cloverleaf_98": "hw_clover_leaf_-3_3",
    "cloverleaf_100": "hw_clover_leaf_-1_3",
    "cloverleaf_103": "hw_clover_leaf_2_3",
    "cloverleaf_105": "hw_clover_leaf_4_3",
    "cloverleaf_106": "hw_clover_leaf_5_3",
    "cloverleaf_109": "hw_clover_leaf_-4_4",
    "cloverleaf_110": "hw_clover_leaf_-3_4",
    "cloverleaf_111": "hw_clover_leaf_-2_4",
    "cloverleaf_112": "hw_clover_leaf_-1_4",
    "cloverleaf_113": "hw_clover_leaf_0_4",
    "cloverleaf_114": "hw_clover_leaf_1_4",
    "cloverleaf_115": "hw_clover_leaf_2_4",
    "cloverleaf_116": "hw_clover_leaf_3_4",
    "cloverleaf_117": "hw_clover_leaf_4_4",
    "cloverleaf_118": "hw_clover_leaf_5_4",
    "cloverleaf_122": "hw_clover_leaf_-3_5",
    "cloverleaf_123": "hw_clover_leaf_-2_5",
    "cloverleaf_124": "hw_clover_leaf_-1_5",
    "cloverleaf_125": "hw_clover_leaf_0_5",
    "cloverleaf_126": "hw_clover_leaf_1_5",
    "cloverleaf_127": "hw_clover_leaf_2_5",
    "cloverleaf_128": "hw_clover_leaf_3_5",
    "cloverleaf_129": "hw_clover_leaf_4_5",
    "cloverleaf_130": "hw_clover_leaf_5_5",
    "cloverleaf_138": "hw_clover_leaf_1_6",
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
