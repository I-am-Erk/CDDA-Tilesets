# Overmap special slicing

Script located at /tools/slice_overmap_special.py
Example sources can be found in /templates/overmap/

This script exists to make spriting large specials easier by automatically slicing and renaming the sprites from a larger spritesheet, ignoring any completely white/black/transparent sprites.

## Editing spritesheets / Using the script

Grab the template file(s) (or existing source file(s) for your tileset), modify them to your liking then run slice_overmap_special.py targetting the modified spritesheet or folder containing multiple.
If your tileset uses non 32x32 overmap sprites you will need to adjust the spritesheet's scale if using a template and use the --width and --height arguements when running the script.

## Adding spritesheets / Extending the script

For non-directional OMTs you need to provide one template png while for directional OMTs you will need to provide 4.
Then you need to add to the scripts rename_dict correlating each used sprite in the spritesheet to the correct id (dropping rotation for both if relevant), where the initial iteration starts from 0 at the top leftmost sprite, working across and then down eg:
0  1  2  3
4  5  6  7
8  9  10 11
This matches the order mod_tilesets use.
