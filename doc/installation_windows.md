# Windows guide

Guide for Windows users, without touching the Command Line.

## Install requirements

**Python**

Install Python 3 from [python.org](https://www.python.org/downloads/windows/).

During installation, check "Add Python to PATH".

**libvips**

Download the latest libvips distribution from [libvips.github.io](https://libvips.github.io/libvips/install.html)
(get vips-dev-w64-web-#.#.#.zip NOT vips-dev-w64-all-#.#.#.zip).

Extract the files somewhere.

**Cataclysm-DDA game**

The easiest way to get the game is to use the [CDDA Game Launcher](https://github.com/Fris0uman/CDDA-Game-Launcher/releases).
With the launcher, install the latest **experimental** release.

## Setting up paths

For composing tilesets, some path must be known to the respective scripts.
This section describes the most easy drag & drop approach.

In `CDDA-Tilesets`, go into folder `tools`.

1. Copy `set_game_path.cmd` into the game's folder, and double-click it.  
OR: Drag & drop the game folder onto `set_game_path.cmd`.
   > Note: This sets the environmental variable `CDDA_PATH`.

2. Copy `set_vips_path.cmd` into the vips folder (e.g. `C:\vips-dev-x.xx`), and double-click it.  
OR: Drag & drop the vips folder onto `set_vips_path.cmd`.
   > Note: This sets the environmental variable `LIBVIPS_PATH`.

3. Optional: To set a tileset to compose permanently, double-click `set_tileset.cmd` and select the desired tileset.  
If not set permanently, the update script will allow for interactive selection of a tileset.
   > Note: This sets the environmental variable `CDDA_TILESET`.

After these steps, it might be necessary to restart the computer.

## Compose and update tileset

In `tools`, double-click `updtset.cmd`.

You will be prompted to select a tileset (unless it was set permanently).
At the first run, `pyvips` will be installed automatically.

If something goes wrong, read the script's output carefully!
