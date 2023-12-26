# Installation

You can select a different tileset than the one included with the game. You have two options: stable or latest. The stable version is tested and reliable, while the latest version is updated frequently and may have new features or bug fixes.

## Stable

The easiest way to download the tileset would be from the latest release. It is a stable tileset build which you can safely put into the game and run.

1. Download the [latest release](https://github.com/I-am-Erk/CDDA-Tilesets/releases/latest) from the releases page (Not the source code !).
2. Extract archive once it's downloaded.
3. Put *UltimateCataclysm* folder from extracted files into your `cataclysmdda\gfx` folder. It should look like: `cataclysmdda\gfx\UltimateCataclysm`.

> [!WARNING]
> If you have "Missing "tile_config.json" file" error upon loading the tileset, this means that you have downloaded and extracted the source code, and **not** the tileset.

## Develop

The most up to date build of the tileset (per commit). Might be broken.

1. Locate the most recent commit that has a green check right next to it [here](https://github.com/I-am-Erk/CDDA-Tilesets/commits/master).
2. Click on the green check -> *"CI Build / CI Build" Details*
3. Find *Artifacts* drop-down menu, click on it, and then select the artifact.
4. Proceed with step 2 and 3 from stable installation.

> [!NOTE]
> Red cross means that the build has failed and no artifacts were produced.

# Building

To create your own tileset, test new sprites, or contribute to the project, please follow the instructions for your operating system:

- For Linux, macOS, or other Unix-like systems, see [this guide](./installation_nix.md).
- For Windows, see [this guide](./installation_windows.md).

These guides will help you set up the required tools and steps to build the tileset from the source files.
