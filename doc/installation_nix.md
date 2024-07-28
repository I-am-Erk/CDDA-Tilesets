# Nix Installation

Documentation of developing tileset with [Nix](https://nixos.org/). 

## Prerequisites

You will need:
- Python 3
- [Libvips](https://libvips.github.io/libvips/install.html)
- pyvips (install it via python pip: `pip install pyvips`) 

## Build

As this repository uses flakes, it's possible to build any of the tileset (not only UlitCa) using `nix build .#{name}` command. For example:

```sh
# This will build UltiCa
nix build .#UltimateCataclysm

# But this will build Mushroom Dream
nix build .#Mushroom-Dream
```

And the result will be in *result* directory, ready to put into the game. If you want to link the result to the different directory, use `--out-link {path}` argument.

## Devshell

Tileset flake also provide a simple devshell with python and vips to run tools such as `compose.py` or `generate_preview.py`.

```sh
# Enter the devshell
nix develop .

# This now works
python3 tools/compose.py --use-all gfx/UltimateCataclysm out
```

Or if you have [direnv](https://direnv.net/) enabled, it will automatically enter the devshell upon opening the repository.
