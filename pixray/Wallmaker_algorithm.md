# Generate starting horizontal wall:

Specify text `prompt`, `palette` (PNG file), output file `name`.
Apply the following pixray settings:

```python
drawer=pixel
prompt="[prompt] #pixelart"
size=[32,32]
pixel_size=[32,32]
iterations=90
filters=wallpaper,lookup
wallpaper_type=horizontal
palette=[palette.png]
overlay_image=https://raw.githubusercontent.com/I-am-Erk/CDDA-Tilesets/precursor-sprites-for-pixray/pixray/wall_ew_transmap2.png
overlay_every=20
overlay_alpha=0
overlay_offset=5
output_name=[name]_edge_ew1.png

```

Later on we will want to be able to specify a different overlay_image to allow other wall styles to generate. This is for Ultica.

# Generate 2 variant horizontal walls.
1. take the transparency used in step 1 (https://raw.githubusercontent.com/I-am-Erk/CDDA-Tilesets/precursor-sprites-for-pixray/pixray/wall_ew_transmap2.png). 
- Add the last 2 pixels from the right edge of name_edge_ew1.png and append them to the left side of a new overlay. 
- Likewise take the 2 pixels from the left and append them to the right, creating a 36x32 image.
-  Add an alpha overlay of the 2 right edge pixels and 2 left pixels in place at alpha 25. The result should look like https://raw.githubusercontent.com/I-am-Erk/CDDA-Tilesets/precursor-sprites-for-pixray/pixray/eldritch_wall_frame_2.png
-  save this output as [name]_ew_transparencymap.png
2. Adjust settings for pixray:
- turn off `filters=wallpaper`
- replace size and pixel_size with [36,32]
- use [name]_edge_ew.png as the palette
- use [name]_ew_transparencymap.png as the overlay_image
3. Crop resulting image by 2px on each side to a 32x32 output.
4. Save file as [name]_edge_ew2.png
5. Run pixray again with same settings and the post-pixray crop, but output file as [name]_edge_ew3.png


Vertical wall algorithm pending
