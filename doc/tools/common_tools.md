# Common tools (scripts)

These are the tools that works the same way on every operating system.

They supposed to run in shell environment and if you afraid doing so please refer [Windows wrappers](./windows_wrappers.md) documentation.

## add_outline.py

// TODO: Add some info about add_outline.py

## compose.py

Please refer [main CDDA documentation](https://github.com/CleverRaven/Cataclysm-DDA/blob/master/doc/TILESET.md#composepy) about this tool.

## generate_preview.py

// TODO: Add some info about generate_preview.py

// TODO: Add link to how-to/preview section

## recolor_season_variants.py

// TODO: Add some info about recolor_season_variants.py

## Slicers
### slice_multitile.py

// TODO: Add some info about slice_multitile.py

### slice_variants.py

// TODO: Add some info about slice_variants.py

### ultica_build_flags.py

This script uses GIMP to take in flag-like textures in `scratch\UltimateCataclysm\items\flags` and create contextual versions of those same flags, specifically:
- "postup", a drooped version for hanging flags on walls
- "hoisted", a waving version for hanging flags on flagpoles
- "", a crumpled version for a dropped flag variant item

To run, install GIMP, put flag textures in the above directory (along with an `output` folder), and run ultica_build_flags.cmd
Flag textures should be offset by 2x5 and have a size of 28x18 to appear correctly
Outputted flags must be moved manually to the appropriate `gfx` directory
If script runtime is too slow, move unneeded flags from `scratch` folder

### unslice_multitile.py

// TODO: Add some info about unslice_multitile.py
