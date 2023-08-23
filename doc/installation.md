# Installation

## Stable

The easiest way to download the tileset would be from the latest release. It is a stable tileset build which you can safely put into the game and run.

1. Download the [latest release](https://github.com/I-am-Erk/CDDA-Tilesets/releases/latest) from the releases page (Not the source code !).
2. Extract archive once it's downloaded.
3. Put *UltimateCataclysm* folder from extracted files into your `cataclysmdda\gfx` folder. It should look like: `cataclysmdda\gfx\UltimateCataclysm`.

> ⚠ If you have "Missing "tile_config.json" file" error upon loading the tileset, this means that you have downloaded and extracted the source code, and **not** the tileset.

## Develop

The most up to date build of the tileset (per commit). Might be broken.

1. Locate the most recent commit that has a green check right next to it [here](https://github.com/I-am-Erk/CDDA-Tilesets/commits/master).
2. Click on the green check -> *"CI Build / CI Build" Details*
3. Find *Artifacts* drop-down menu, click on it, and then select the artifact.
4. Proceed with step 2 and 3 from stable installation.

> Red cross means that the build has failed and no artifacts were produced.

# Building

You will need:
- Python 3
- [Libvips](https://libvips.github.io/libvips/install.html)
- pyvips (install it via python pip: `pip install pyvips`) 

Once you have everything ready, you can build the tileset:
```sh
# Assuming that you are in the root of the tileset repository
$ python3 tools/compose.py gfx/UltimateCataclysm
```
