# Windows Wrappers for Common Tools

For more detailed information, please refer to the [Common Tools](./common_tools.md) section.

We understand that artists may want to participate in tilesets, but not everyone is familiar with programmer's tools and environments. To optimize artists' time and workflow, we provide some wrappers that offer automation with preferred interactions such as double-clicking and drag-and-drop.

These wrappers might have less functionality, but in most cases, their results are acceptable.

## Infrastructure Building Tools

// TODO: Remember to update this section when 'updtset.cmd' is divided.

### 1) Installation

To work with tilesets and test them in the game, you need a clone of the tileset repository on your drive and download the game itself. You can refer to [this](../installation_windows.md) page for details.

The current `updtset.cmd` wrapper is written for the **Windows Command Shell** and is supposed to run on every Windows version from Windows XP to Windows 11 23H2. However, according to [this](https://www.statista.com/statistics/265033/proportion-of-operating-systems-used-on-the-online-gaming-platform-steam/) statistic, older Windows versions can be excluded and the script can be rewritten in **Powershell**.

At this time, the installation of necessary environment tools is tied together with preparation steps and the composing process.

The installation tool `updtset.cmd` will install the following on its first run:
- Python
- Necessary Python modules (pyvips and numpy)
- Necessary VIPS library and binaries

`git_symlinks.cmd` is a small script that runs commands necessary for symlinks to work in the repository. However, there is another method described [here](../how-to/Cloning_symlinks_on_windows.md).

### 2) Preparation

*There are some additional small scripts that are also written for the **Windows Command Shell** and should be rewritten in **Python** later, as **Powershell** does not support drag-and-drop over ps1 files.*

`set_game_path.cmd` is a subtool that can be run separately from `updtset.cmd` and will set an environment variable pointing to the game. If you want to check your modified/added sprites in the game, tools need to know where the game is.

`set_tileset.cmd` - This subtool will fix a tileset for future composing runs. It is helpful if you prefer to work on only one tileset.

`set_vips_path.cmd` - This subtool allows you to define another `libvips` location.

All these wrappers can be launched by dragging and dropping the appropriate folder over them. They will check if that folder has the correct files (game executable, libvips binary) and set the corresponding Windows user environment variable.
Here's the revised version with improved style and grammar:

## Slicer

The Slicer wrapper, `slicemt.py`, is a wrapper for the [common tools](./common_tools.md) and performs the most repetitive process - slicing source files and composing tilesets. However, it cannot perform complex tasks such as multivariate multitile slicing or animation creation.

If you need to slice multitiles and check the result in the game, you can do the following:

1) Create a shortcut for `slicemt.py` on your desktop.
2) Create a `source` subfolder in the `object folder` inside a tileset repository.
3) Export a png file from your graphic editor to this `source` folder and name this multitile source accordingly.
4) Drag-and-drop the `source` folder over the said shortcut.

You will receive 16  sprites and a json file that will be used for composing. You may leave the `source` folder in the repository as it is ignored in the PR process. ([example with screenshots](https://github.com/I-am-Erk/CDDA-Tilesets/pull/2249#issue-2046838285))

Under the hood, the following process occurs:

1) The script (`slicemt.py`) will try to check if there is a `source` folder to work on. If it was launched from the CLI inside the `object folder`, it will try to find the `source` folder one level deeper.
2) If the script can find a folder with `png` at the beginning and `NxM` following, it will assume that it runs in a tileset repository and `NxM` are sprite dimensions. This will allow it to make an assumption about where `updtset.cmd` is located.

    Otherwise, the script will stop working.

3) The script will try to make four different checks. Each check will try to find source files with a special name pattern. But you do not need to provide all of them. I will use `t_floor` as an example tile name.
    - **Slicing Variants**

        The pattern is `*_var*.png` so you can provide following files: *t_floor_var_1.png* or *t_floor_variants.png* each file will be sliced into 16  separate files and each file will have a name t_floor_var_XX.png, where XX is a number from 00 to 15.

        If you provide more than one source file (for example *t_floor_var_1.png* and *t_floor_var_2.png*) you will receive 32 files numbered from 00 to 31.

        In this and only in this case (slicing variants), you may provide a source file with a name different from the object name (t_floor). It can be used if you want to have variants for a subtile.

        Providing a source file named `t_floor_unconnected_variants.png` will produce variants named `t_floor_unconnected_var_XX.png`.

        Running this script over the same `source` folder with only one variant source file two (or more) times will produce separate images with names numbered from 00 to 31 (or even more). So each run will append the existing set of variants.

        Do not forget to empty the `object folder` for each slice run.

    - **Slicing Simple Multitile**

        The second pattern is `object name`+`.png` so for our example, it will check for `t_floor.png` in the `source` folder and treat it as a multitile source.

        Slicing this source will provide 16 named as multitile sub-tiles and a json file (`t_floor.json`).

        This is the most common usage of this wrapper.

    - **Slicing Transparent Multitile**

        The third pattern is `object name`+`_t*.png` so you can provide names like `t_floor_transparent.png`, `t_floor_trans.png` or even `t_floor_t.png`. The resulting set will be named as `t_floor_transparent` and consists of 16 subtile images and a json file.

        This pattern/name is useful for high objects and the game can swap them in close proximity to the player.

        Please read [this](https://github.com/CleverRaven/Cataclysm-DDA/blob/master/doc/TILESET.md#optional-transparent-variant) document.

    - **Seasonal Multitiles**

        Same as simple multitile, but the pattern is:

            object_name_winter*.png
            object_name_spring*.png
            object_name_summer*.png
            object_name_autumn*.png

        Resulting sets will have names like `t_floor_season_winter`, etc.

    - **Seasonal Transparent Multitiles**

        Everything is similar to the previous sections, except for the pattern.
        `objectname_seasonname_t*.png` - `t_floor_winter_t.png` will work.

    After slicing, the script will run `updtset.cmd` with the tileset name inferred from the path.

## Composer

For now, simply run `updtset.cmd`.
