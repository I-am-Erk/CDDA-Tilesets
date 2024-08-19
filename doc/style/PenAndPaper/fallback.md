# Fallback file structure and features

This file is used in cases where the game cannot find a suitable sprite for an object. It is also used to display `N`otes on the map. We will take advantage of this feature of the game in the future.

> [!NOTE]
> It is important that for proper display of `N`otes on the map, the file must have a transparent background.

## Structure of the file

The file consists of 16 blocks of 256 characters each, grouped by 16 in a row.
Those are ASCII symbols. One may think that you can use any of those symbols for notes, but it is wrong. The game gone far from pure ASCII and even if you managed to type `☺` to the note text it wouldn't appear on the map. As well as many other symbols. (This face probably woulld appear as double vertical lines)

So the player actually limited to very few symbols. Numbers, letters and punctuation symbols plus few more. However I recreate every ASCII symbol as hand written even if no one will see it.

Each block contains sybols for specific color. The first block is not displayed by the game and contains black-colored characters. I assume that since the game uses black as the default background color, no one expect writing black notes on the map.

I left this block almost unchanged, and it can be used as a reference to understand which character was in a particular colored block.

> [!TIP]
> Try not to change first block even if the developers enable the display of black color.

Then there are 9 blocks that appears as pens or pencil in game (thin opaque strokes).

| block number | name | RGB values and transparency |
|-|-|-|
| 2  | white      | `#FFFFFF` : `70%` |
| 3  | light gray | `#000000` : `50%` |
| 4  | dark gray  | `#000000` : `00%` |
| 5  | red        | `#800000` : `00%` |
| 6  | green      | `#226600` : `00%` |
| 7  | blue       | `#000066` : `00%` |
| 8  | cyan       | `#00665e` : `00%` |
| 9  | magenta    | `#660066` : `00%` |
| 10 | brown      | `#663300` : `00%` |

The last 6 blocks are for bright colors. My idea was to make the characters in these blocks look as if they were written with highlighters. Therefore, the characters are somewhat wider and semi-transparent.

| block number | name | RGB values and transparency |
|-|-|-|
| 11 | light red  | `#A83939` : `66%` |
| 12 | light green | `#91D94A` : `66%` |
| 13 | light blue | `#4A4Ad9` : `66%` |
| 14 | light cyan | `#4AD9D9` : `66%` |
| 15 | pink       | `#D94A9D` : `66%` |
| 16 | yellow     | `#CAD94A` : `66%` |

> [!NOTE]
> For those who familiar with HSB color space there are some hints:
> - highlighters have saturation 66% and brightnes 85%
> - pens have saturation 100% and brightnes 40%

## Fallback additional features

As I mentioned earlier, not all symbols are available to the player for marking on the map. Therefore, some ASCII symbols in the colored blocks have been changed to pictograms, lines, and other designations. Below are the symbols in the color blocks that are not available in the default view.

It is also worth noting that the dot symbol has been made significantly larger and more noticeable in all color blocks.

<table>
<tr><th>Pen or pencil</th><th>&nbsp;</th></tr>
<tr><td>

 dark gray   (`dg`) (<i>black pen actually</i>)
 
 dark cyan   (`C`)
 
 magenta     (`m`)
 
 brown       (`br`)

</td><td>

`no changes`

</td></tr>
<tr><td>

white       (`W`)

</td><td>

`<` : upstairs

`>` : downstairs

`-` : wide stroke

`=` : wide stroke

</td></tr>
<tr><td>

light gray  (`lg`) (<i>pencil</i>)

red         (`R`)

green       (`G`)

blue        (`B`)

</td><td>

  `+`   : verical line

  `-`   : horizontal line

 `1`-`9`  : corners, t-connections, x-connection

  `h`   : arrow left

  `j`   : arrow down

  `k`   : arrow up

  `l`   : arrow right


</td></tr>
</table>

<table>
<tr><th>Highlighters</th><th>&nbsp;</th></tr>
<tr><td>

light red   (`r`)

light green (`g`)

light blue  (`b`)

light cyan  (`c`)

pink        (`P`)

yellow      (<i>default</i>)

</td><td>

   `(`   : dead face
   
   `)`   : happy face
   
 `-`,`/`,`=` : wide strokes
 
   `@`   : human figurine

</td></tr>
</table>
