### Autotiles

Autotiles, referred to in CDDA game code as "multitiles", are tiles that display differently
depending on their relationship to other sprites in the group. Water is a classic example: drawing
water as an autotile allows it to display as a single body with edges, instead of either individual
little puddles, or a large blue expanse with no shoreline.

![Water autotile](image/t_water_sh_autotile.png)

To simplify drawing these tiles, we use a template with an 8x6 grid of all the tile boundary types
in a predictable order. Transparency allows overlapping the same tiles on different backgrounds, so
we don't have to redraw the water boundaries for dirt, grass, rock, etc. - we draw the water once,
and the transparent edges allow it to overlap dirt, grass, rock, and so on.

This template shows the standard arrangement of tile borders:

![Autotile Template](image/autotile_template_grid.png)

Black space indicates background, and white is the shape of the furniture or terrain. The sixteen
tiles in the top-left 4x4 block contain the basic boundary shapes - these are the most important
ones to draw.

Both terrain and furniture tiles may use this template. Terrain like grass or fences:

![Tall grass terrain](image/t_grass_tall_autotile.png)
![Fence terrain](image/t_fence_autotile.png)

and furniture like bathtubs or benches:

![Bathtub furniture](image/f_bathtub_autotile.png)
![Table furniture](image/f_bench_autotile.png)

Currently, there are only a few of these tiles supported in CDDA, although some day it would be nice
to have all of them available. With the current tile support there are two ways you might use an
autotile, demonstrated by the bench and table autotiles. What we're missing is the ability to draw
different types of *diagonal* connections. Without that, we have to represent things that are likely
to have diagonal connections or unlikely to have them in different ways.

These break down into a few parts as recognized by the game.

- **corner**: These attach two adjacent tiles perpendicular to the tile in question.
- **edge**: These tiles connected either on the top-bottom or left-right sides, in a straight line.
- **unconnected**: This is a tile just hanging out alone, unconnected to its neighbors.
- **center**: This is a 4-way intersection tile, connected on all sides.
- **end_piece**: These tiles are connected only on one side.
- **t_connection**: These are the 3-way intersection tiles.

![Autotile part labels](image/f_bench_autotile_labels.png)


#### Things like benches

![Autotile: bench](image/f_bench_autotile.png)

The bench autotile is an example of an autotile that we don't really expect to be displayed double-thick most of the time. Generally you're going to draw a bench like this:
```
.....
bbbbb
.....
```
rather than like this:
```
bb.bb
bb.bb
bb.bb
```

For this reason, the **t_connection** and **center** art for the bench are drawn as 3-way and 4-way intersections.


#### Things like tables

![Autotile: table](image/f_table_autotile.png)

The table autotile is an example of a tile you would often expect to be drawn double-thick,
connecting to itself. While you might also draw it one tile wide, two or more tiles of contiguous
table are common. For this reason you can't assume there's an edge visible on a **t_connection** or
**center** tile. Consider the center tile in a table like this, represented by a capital T amidst
lower case:

```
.....
.ttt.
.tTt.
.ttt.
.....
```

That **center** tile can't be drawn as a 4-way intersection, or there would be holes in the table.
It has to be drawn as a flat contiguous tabletop. Likewise the **t_intersection** tiles (the middle
piece of each edge section) should be assumed to connect diagonally as well, again to prevent holes
in the table.


### Slicing autotiles

Before an autotile template can be used by the game, it needs to be sliced up into individual tiles.
We use the `tools/slice_autotiles.py` script to achieve this.

To run the script, you will need [python](https://python.org) installed, as well as the libvips
graphic library. Something like these commands should suffice to install them on Ubuntu:

```
$ sudo apt install python3-pip libvips
$ pip3 install pyvips
```

If all goes well, you should be able to run the `slice_autotiles.py` script and see the usage note:

```
$ tools/slice_autotiles.py
usage: slice_autotiles.py [-h] [--no-json] tile size image out
slice_autotiles.py: error: the following arguments are required: tile, size, image, out
```

So if you have created a `mud_autotile.png` image, using the autotile template above, you can tell
the script to slice it into 32x32-pixel tiles with a command like this:

```
$ tools/slice_autotiles.py mud 32 mud_autotile.png mud_tiles
```

This will create a `mud_tiles` folder with separate images for each tile in the template, along with
a JSON file with connection data, for example:

- mud.json
- mud_center.png
- mud_corner_ne.png
- mud_corner_nw.png
- mud_corner_se.png
- mud_corner_sw.png
- mud_edge_ew.png
- mud_edge_ns.png
- mud_end_piece_e.png
- mud_end_piece_n.png
- mud_end_piece_s.png
- mud_end_piece_w.png
- mud_t_connection_e.png
- mud_t_connection_n.png
- mud_t_connection_s.png
- mud_t_connection_w.png
- mud_unconnected.png

