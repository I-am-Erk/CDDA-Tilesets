# Windows wrappers for common tools

For detailed info please go to the [common tools](./common_tools.md) section.

We understand that people wants to participate in tilesets and not all of them are familiar with programmers tools and envirionments. To optimize artists time and workflow we provide some wrappers that provide some automation with preferred interactions (double-clicking and drag-and-drop).

Those wrappers may have less functionality but in most cases their results ara acceptable.

## Infrastructure building tools

// TODO: Do not forget to change this section when 'updtset.cmd' is divided.

### 1) Installation

To work with tilesets and test them in game you need a tileset repository clone on your drive and the game itself. You may refer [this](../installation_windows.md) page for details.

Current `updtset.cmd` wrapper written for **Windows Command shell** and supposed to run on every Windows version since Windows XP, till Windows 11 23H2. However [this](https://www.statista.com/statistics/265033/proportion-of-operating-systems-used-on-the-online-gaming-platform-steam/) statiscic means that old Windows versions can be excluded and script overwritten on **Powershell**.

At this time installation of necessary environment tools tied together with preparation steps and composing process.

The installation tool is `updtset.cmd` at first runs it will install:
- Python
- necessary Python modules (pyvips and numpy)
- necessary VIPS library and binaries

`git_symlinks.cmd` is a small script that run commands necessary for symlinks to work in the repository. However there is another way to do so describen [here](../how-to/Cloning_symlinks_on_windows.md).

### 2) Preparation

*There are some additional small scripts that also written for **Windows Command shell** and later must be rewritten on **Python** as **Powershell** does not support drag-and-drop over ps1 files.*

`set_game_path.cmd` is a subtool that can be run separately from `updtset.cmd` and will set environment variable pointing to the game. If you want to check your modified/added sprites in game tools need to know where the game is.

`set_tileset.cmd` - this subtool will fix a tileset for future composing runs. It is helpful if you like to work on one tileset only.

`set_vips_path.cmd` - subtool that allows you to define another `libvips` location.

All this wrappers can be launched by drag-and-drop appropriate folder over them. They will check if that folder have correct files (game executable, libvips binary) and set according Windows user environment variable.

## Slicer

Slicer wrapper `slicemt.py` is a wrapper for the [common tools](./common_tools.md) and will do the most repeating process - slice source files and compose tileset. But of course it cannot do some difficult task such as multivarian multitile slicing or animation making.

However if you need to slice multitile and check the result in game you can do the following:

1) Create a shortcut for the `slicemt.py` on your desktop
2) Create `source` subfolder in the object folder inside a tileset repository
3) Export png file from your graphic editor to this `source` folder and name this multitile source accordingly.
4) Drag-and-drop `source` folder over said shortcut.

You will receive 16 [^1] sprites and json file that will be used for composing. You may leave `source` folder in the repository as it is ignored in PR process. ([example with screenshots](https://github.com/I-am-Erk/CDDA-Tilesets/pull/2249#issue-2046838285))

Under the hood there is a following process:

1) The script (slicemt.py) will try to check if there is a `source` folder to work on. In case it was launched from CLI inside `object folder` it will try to find `source` folder one level deeper.
2) If script can find a folder with `png` in the beginning and `NxM` in the following it will suppose that it runs in tileset repository and `NxM` are sprite dimensions. This will allow to make an assumption where is `updtset.cmd` is located.

    Otherwise script will stop working.

3) Script will try to make four different checks. Each check will try to find source files with special name pattern. But you do not need to provide all of them. I will use `t_floor` as example tile name.
    - **Slicing variants**

        The pattern is `*_var*.png` so you can provide following files: *t_floor_var_1.png* or *t_floor_variants.png* each file will be sliced to 16 [^1] separate files and each file will have a name t_floor_var_XX.png, where XX is a number from 00 to 15.

        If you provide more than one source file (for example *t_floor_var_1.png* and *t_floor_var_2.png*) you receive 32 files numbered from 00 to 31.

        In this and only in this case (slicing variants) you may provide source file with a name different from object name (t_floor). It can be used if you want to have variants for subtile.

        Providing source file named `t_floor_unconnected_variants.png` will produce variants named `t_floor_unconnected_var_XX.png`.

        Running this script over same `source` folder with only one variant source file two (or more) times will produce separate images with names numbered from 00 to 31 (or even more). So each run will append existing set of variants.

        Do not forget to empty `object folder` for each slice run.

    - **Slicing simple multitile**

        Second pattern is `object name`+`.png` so for our example it will check for `t_floor.png` in `source` folder and treat it as multitile source.

        Slicing this source will provide 16 [^1] named as multitile sub tiles and json file (`t_floor.json`).

        This is the most common usage of this wrapper.

    - **Slicing transparent multitile**

        Third pattern is `object name`+`_t*.png` so you can provide names like `t_floor_transparent.png`, `t_floor_trans.png` or even `t_floor_t.png`. Resulting set will be named as `t_floor_transparent` and consists from 16 subtile images and json file.

        This pattern/name useful for high objects and game can swap them in close proximity to the player.

        Please read [this](https://github.com/CleverRaven/Cataclysm-DDA/blob/master/doc/TILESET.md#optional-transparent-variant) doc.

    - **Seasonal multitiles**

        Same as simple multitile, but pattern is:

            object_name_winter*.png
            object_name_spring*.png
            object_name_summer*.png
            object_name_autumn*.png

        Resulting sets will have names like `t_floor_season_winter` etc.

    - **Seasonal transparent multitile**

        Everything is similar to previous sections, except pattern.
        `objectname_seasonname_t*.png` - t_floor_winter_t.png will work.

    After slicing script will run `updtset.cmd` with Tileset name guessed from the path.

## Composer

Just run `updtset.cmd` for now.
