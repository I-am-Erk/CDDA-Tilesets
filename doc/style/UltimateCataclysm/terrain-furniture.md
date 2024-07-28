# Terrain & Furniture

## Walls and floors are 32x32, other things may vary

// TODO: add terrain example image

Again, you should size things accordingly to their size in the world.

## Keep color value level in medium range

// TODO: add image with color levels explanation

It's important to keep the value level of background objects (terrain, furniture) at about 60-80, because it helps define foreground entities (e.g. monsters) better.

# Keep table surfaces consistent

When drawing something similar to a table keep in mind that currently table surfaces usually occupy the top 19 pixels of a tile, and items may be optimized to look placed in that area.
