#!/usr/bin/env python3

"""

Renames automatic iterative names obtained by:
1. Importing sprite sheet (Ctrl + I) in cloverleaf.aseprite, using width = height = 32 pixels
2. Export (not sprite sheet) as cloverleaf_0

Run in the same folder as the relevant sprites
Deletes all other .png files starting with "cloverleaf_" in the working directory!

Example usage:
py cloverleafRename.py

"""

import os

rename_dict = {
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
    "cloverleaf_138": "hw_clover_leaf_1_6"
}

for root, directories, filenames in os.walk(os.getcwd()):
    for filename in filenames:
        basename, ext = os.path.splitext(filename)
        path = os.path.join(root, filename)
        # Only touch png files starting with cloverleaf_
        if ext == ".png" and basename.startswith("cloverleaf_"):
            if basename in rename_dict:
                new_path = os.path.join(root, rename_dict[basename] + ".png")
                os.rename(path, new_path)
            else:
                # Delete extra sprites from the spritesheet that aren't wanted
                os.remove(path)
    # Skip subdirectories
    break
