# How to use this overmap tileset
*This section is moslty for players*

To get the most out of this tileset, it’s important to understand that it requires more player interaction.

By default, the color indication on the map is quite minimal, and this is intentional. It allows the player to mark points of interest and danger zones on the map themselves. Just as we make notes on a real map, the player is expected to add some information manually.

Of course, the game has an Autonotes feature, and I have tried to ensure that these notes match the style of what the player can add manually. This way, manual notes and Autonotes are meant to complement each other.

Let's take a closer look:
![screensho](./images/notes_screenshot.png)

As you can see here there are some notes:
1) Yellow "Home" above three buildings. This note is made out of four different notes. These are common notes the player can write using `N` key.
(`H:`,`o:`,`m:` and `e:` - notes values. As you can see only `:` is used to define the map glyph, and the color is default yellow.
2) Below `Home` there is a green stroke. It can be achieved by the note `-:g;`. The stroke of highlighers (bright colors) are relatively wide.
3) The black `X` mark on the road was made manually.
4) But the brown circle right near the pencil is autonote (*dead vegetables*)
5) The grey circle on the road (*burned ground*) is also an autonote. So you can see that manual and autonotes are quite the same.
6) Light green face is `):g;`. As you can notice, you have to put one symbol at a time on the map.
7) But there is anoter type of notes that spreads around a central point. It is a red diagonal strokes around the magenta `o`. This indicates a danger zone. It would be great if we can create other long notes like this.
8) The red line around the red tack is a set of notes you can ~~painfully~~ draw by numbers and `+` / `-` symbols.

Full set of symbols can be found [here](./fallback.md#fallback-additional-features)

## Additinal info

You can change several aspects of this overmap tileset on the client side (but of course, you have to do it each time after a tileset update).

- cursor (pencil by default)
- brightness/saturation of background as well

You can download a couple of cursors from here:
- [Orange semitransparent protractor](./images/cursor_protractor.png) - This was the first cursor. It has a couple of nice features: the ruler on the protractor is relatively accurate and almost equal to real centimeters/inches, and it has a couple of “handmade ticks” for 100 and 200 meters/yards(?). But this one can be confusing.
- [Classic small red circle](./images/cursor_circle.png) - Can be used if you prefer a cursor that doesn’t span across several tiles.

> [!WARNING]
> You should save it as `cursor.png` in `%GAME% \gfx\PenAndPaper\`. Save original `cursor.png` somewhere just in case.

To change brightness/saturation of the tileset use any image editor and adjust those files.
