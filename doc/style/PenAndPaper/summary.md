# Pen And Paper Overmap Style Guide

<p align="right"><a href="./summary.ua-UA.md"><img alt="Static Badge" src="https://img.shields.io/badge/lang-UA-blue"></a></p>

The overall style of this tileset is to give the map a hand-drawn effect. The following features of the map in the game should be considered:

1. The map should be done in a consistent style; sprites of the same type should not differ significantly from each other.
2. The more variety in the sprites, the better - this creates the feeling of a lively drawing.
3. Given the limited visual resources, try to show important objects and territory boundaries to the player. The more understandable at first glance, the better.
4. The map is designed for high-resolution screens and does not adhere to the concept of displaying sprites in pixel art style.

## General Aspects

1. Sprites should be transparent; the map background is added in the corresponding JSON file.
2. It is assumed that the player first draws on the map with a pencil in places where they are unsure. Objects they are sure of are drawn with a pen of the corresponding color.
3. The main color for roads and specialized buildings is a black pen.
4. The main color for secondary objects is a brown pen. For example, residential houses within the city are represented by the symbol `^`, and meadows with tall grass in the fields are brown sprites.
5. Try to draw sprites so that no more than 10 strokes are used per tile.
6. If it is possible to convey the logic and idea so that some tiles remain empty but the map is still readable, strive to do so.

## Specific Features

- [Used Colors and Pens properties](./colors.md)
- [Fallback file usage](./fallback.md)
- [How to use map](./usage.md)
- [File structure in repository](./file_structure.md)
- [Workflow to contribute](./workflow.md)
