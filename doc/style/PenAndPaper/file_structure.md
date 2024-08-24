# P&P repository file structure

- `pngs_overmap_48x48`: This folder contains almost all sprites. Details below.
- `pngs_backgrounds_48x48`: This folder should contain only background sprites, so players can change the brightness all together with one action, for all sprites including unknown terrains.
- `pngs_weather_96x96`: To achieve the effect of long diagonal strikes across many tiles, I had to use double-sized sprites (four times bigger in terms of area).
- `pngs_weather_unknown_48x48`: Unknown sky areas have similar sprites to the ground ones, but blue. All are here.
- `pngs_icons_96x96`, `pngs_icons-h_96x48`, `pngs_icons-v_48x96`: These three folders could be combined into one under different circumstances. However, the current rendering engine forced me to create additional sprites that have only half of the mission arrow sprite. The idea of the mission arrow sprite is a square patch of transparent film attached to the edge of the map. Maybe one day we can make it more obvious.
- `pngs_cursor_288x144`: A single cursor sprite, so players can easily change it later on the client side.

## Common overmap sprites

Most sprites fall into this category. It is important to remember that to keep the tileset’s characteristics and flexibility, all sprites must be separated into the actual image and the background, which is standard for all sprites. A JSON file combines everything together.

Many objects consist of more than one tile on the map. It is assumed that the survivor always draws them upright on the map. However, the game mechanics rotate objects, so these rotations must also be compensated in the JSON file.

To avoid creating JSON files from scratch each time or searching for them throughout the repository, I have tried to group them. Objects with the same dimensions on the map are placed in corresponding folders. The terrain is stored separately, as are objects related to granular visibility.

### 1x1 tile object

These objects usually consist of a foreground sprite and a JSON file. Ideally, objects that occupy a single tile should have at least a few variations. Since such objects often appear close to each other, repetition can diminish the handmade map effect.

```json
[
  {
    "id": [
      "animalpound", "animalpound_roof",
      "animalshelter", "animalshelter_roof"
    ],
    "fg": "animal_shelter",
    "bg": [
      { "weight": 1, "sprite": "bg_00" },
...
      { "weight": 1, "sprite": "bg_23" },
      { "weight": 1, "sprite": "bg_24" }
    ]
  }
]
```

I recommend always enclosing the sprite description in square brackets, as this will simplify adding and modifying the JSON file in the future.

Pay attention to the list of IDs - it is advisable to include roofs and basements. This will make it easier to navigate the map.

In this example, only one foreground sprite is used.

However, the background uses all 25 available variations. If there are multiple sprites for the foreground, a similar structure will need to be written. Never include the background in the final sprite. This will maintain the flexibility and size of the tileset.

In this example, the “rotates” attribute with the value false is omitted. This is the default value. It means that even if the object on the map is rotated with the “entrance” facing south, the sprite will still remain in the correct position.

### 1x2 tile object (this is vertical object when facing North)

I have tried to include templates in most folders with standard sizes, so you can use them for typical objects. I do not recommend using JSON files from other objects, as some objects have non-standard rotations or different sets of IDs.

```json
[
  {
    "//helper": [
      "    N   ", "    W   ", "    S   ", "    E   ",
      "_0_ 1 2 ", " 0 _1_2 ", " 0  1 2 ", " 0  1_2_",
      " 3      ", " 3      ", "_3_     ", " 3      "
    ],



    "id": [
      "template1x2_A"
    ],
    "rotates": true,
    "fg": [
      "template1x2_var_00", "template1x2_var_01", "template1x2_var_03", "template1x2_var_02"
    ],
    "bg": [
      { "weight": 1, "sprite": "bg_00" },
...
      { "weight": 1, "sprite": "bg_24" }
    ]
  },



  {
    "id": [
      "template1x2_B"
    ],
    "rotates": true,
    "fg": [
      "template1x2_var_03", "template1x2_var_02", "template1x2_var_00", "template1x2_var_01"
    ],
    "bg": [
      { "weight": 1, "sprite": "bg_00" },
...
      { "weight": 1, "sprite": "bg_24" }
    ]
  }
]
```

In this template, you can see three parts. The first part helps visually assess what will be described in the following two parts and is not necessary for the tileset to function.

It is assumed that our object consists of two tiles and by default looks as follows when facing north:

```
A
B
```

Looking at the helper section, you can see that tile A will receive the sprites with the numbers that are underlined when the object is rotated.

Accordingly, tile B will receive the non-underlined sprites (3, 2, 0, 1).

As you can see, four sprites had to be created for this object because it has vertical (N, S) and horizontal (W, E) orientations. Square objects can be represented with a single large image.

The correct names for the tiles (instead of A and B) need to be specified each time, there is no naming convention.

### Common terrain

Here are the sprites that form the main background of the map - forests, fields, rivers, etc. I want to remind you again about the variability of sprites. For example, I had to create more than 75 sprites for the forest to avoid it looking too repetitive.

### Granular

Sprites related to PR [#75236](https://github.com/CleverRaven/Cataclysm-DDA/pull/75236)
