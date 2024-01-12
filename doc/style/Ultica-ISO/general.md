# Ultica-ISO general style guide

## Necessary Digression

An isometric projection is a representation of three-dimensional objects on a plane, where the angles between the axes are equal and make up 120 degrees. In pixel art, such an image will not look very beautiful, as straight lines will feel broken. Therefore, a pseudo-isometric projection is used, where only two angles between the axes are equal to each other. However, in the future, it will be called isometric. You can read more details [here](https://en.wikipedia.org/wiki/Isometric_video_game_graphics).

## Ultimate Cataclysm inheritor

Ultica-ISO is an isometric tileset that has its roots in the standard Ultimate Cataclysm [(Ultica)](../UltimateCataclysm/summary.md) tileset and borrows a large number of resources from there. Primarily, the character and accompanying sprites, items, weapons, monsters and so on.

As a result of this approach, Ultica-ISO shares the main style guides with Ultica and also attempts to tie all objects in the game to real sizes. From the game documentation, we know not only the dimensions of one tile (1 meter by 1 meter), but also the approximate height of the z-level (3-4 meters). These features influenced the choice of the base sprite size.

Experiments at the very beginning of the tileset creation showed that it would be optimal to increase the legacy sprites from Ultica by two times, and then, assuming the character's height is approximately 1.75-1.8 meters, get the dimensions of the rhombus to be 48 by 24 pixels.

The height of the Z-level is composed of the space above the base plane (3 meters), and the thickness of the base (thickness of the soil, roof, floor – 0.37 meters) and amounts to (96 + 12) 108 pixels.

>[!NOTE] You can consider 1 pixel height to be equivalent to 1¼ inches or 3.125 cm.

Due to the fact that the tile is not square, as in classic orthogonal tilesets, the conjugation of four tiles has some peculiarities.

>[!NOTE] In fact, this means that a pixel on the horizontal plane should be drawn if more than half of it falls within the boundaries of the object, and left empty otherwise. However, pixels on vertical surfaces should be drawn in most cases.
