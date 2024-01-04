# Creating mod tilesheet using existing tools

If you want to create a quite extended mod for CDDA and it'll be shipped separately from the main game you need a composed tilesheet.

It is not a problem for mods with a couple of sprites, but if you have a lot of sprites better to use existing tools.

## Creating a dummy tileset

First of all you need to create a dummy tileset in the tileset repository and receiving folder in your game.

- Create a `my_mod` folder under `CDDA-Tilesets\gfx` (tilesets repository)
- Create a `my_mod` folder under `Cataclysm\gfx` (your game folder)

Now you need to create some files in repository.
Go to `CDDA-Tilesets\gfx\my_mod\` and create `tileset.txt` and add the following content:

```txt
#my_mod

NAME: my_mod_name
VIEW: my_mod_view
JSON: tile_config.json
TILESET: tiles.png
```

As you can see name and view should be somehow related to your mod name, but actually they can be abything but existing tilesets names.

Copy `fallback.png` from any other existing tileset into your `CDDA-Tilesets\gfx\my_mod\` folder. It is needed only to be checked once and you will delete it later.

Lets assume that you have a number of sprites and sprites size are: x=32 and y=48. Put all of them into the folder and name this folder: `pngs_my_mod_sprites_32x48`.

Now you need to create the final file: `tile_info.json` with following content:

```json
[
  {
    "pixelscale": 1,
    "width": 1,
    "height": 1
  },
  {
    "my_mod_sprites.png": { "sprite_width": 32, "sprite_height": 48 }
  }
]
```

## Composing the "tileset"

Use `updtset.cmd` tool as usual (you may refer to this [doc](../tools/windows_wrappers.md#composer)). Your new dummy tileset will appear in the list of source tilesets available for composing.

If you did everything right you will get the composed tileset in your game directory `Cataclysm\gfx\my_mod`.

You will get:
| file | purpose |
|--|--|
| :bar_chart:fallback.png | to be deleted |
| :bar_chart:my_mod_sprites.png | your composed tilesheet |
| :memo:tile_config.json | you need to fix it a bit |
| :memo:tileset.txt | to be deleted |

Check my_mod_sprites.png - this file should contain all your sprites.

## Fixing the json

Resulting `tile_config.json` supposed to be for a full tileset, so you need to fix it first. Open it in any text editor, copy all content and past it here: [CDDA json linter](https://dev.narc.ro/cataclysm/format.html) and press "LINT" button below.

Now this file content can be easily readable. You will get something like this:

```json
{
  "tile_info": [
    ...
  ],
  "tiles-new": [
    {
      "file": "my_mod_sprites.png",
      "//": "range from 1 to X",
      "sprite_width": 32,
      "sprite_height": 48,
      "sprite_offset_x": 0,
      "sprite_offset_y": 0,
      "tiles": [
        ...
      ]
    },
    {
      "file": "fallback.png",
      "tiles": [],
      "ascii": [
        ...
      ]
    }
  ]
}
```
