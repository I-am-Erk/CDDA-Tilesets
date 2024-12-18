#!/usr/bin/python

import os, glob, sys, time
from gimpfu import *
"""
This script uses GIMP 2.10 to turn a flat flag sprite (e.g. "national_flag_var_chinese_flag_scratch") into three contextual sprites.
-"postup" for hanging flags on walls
-"hoisted" for hanging flags on flagpoles
-"", for a dropped flag variant item
"""
def process(infile):
    file_split = os.path.split(infile)
    dir = file_split[0]
    save_dir = normal_path(os.path.join(dir, "output"))
    base_name = file_split[1][:-4]
    file_load = normal_path(infile)
    file_hoisted_save = normal_path(os.path.join(save_dir,base_name+"_hoisted.png"))
    file_item_save = normal_path(os.path.join(save_dir,base_name+".png"))
    file_postup_save = normal_path(os.path.join(save_dir,base_name+"_postup.png"))

    file_hoisted_shading = normal_path(os.path.join(dir,"shading/flag_hoisted_shading.png"))
    file_postup_shading = normal_path(os.path.join(dir,"shading/flag_postup_shading.png"))
    file_item_shadow = normal_path(os.path.join(dir,"shading/flag_item_shadow.png"))
    
    #create the image
    img=pdb.gimp_file_load(file_load, file_load)

    #post_up
    pdb.gimp_image_select_rectangle(img, 0, 4, 5, 5, 18)
    pdb.gimp_floating_sel_anchor(pdb.gimp_selection_float(pdb.gimp_image_get_active_layer(img), 0, 1))
    pdb.gimp_image_select_rectangle(img, 0, 9, 5, 15, 18)
    pdb.gimp_floating_sel_anchor(pdb.gimp_selection_float(pdb.gimp_image_get_active_layer(img), 0, 2))
    pdb.gimp_image_select_rectangle(img, 0, 24, 5, 5, 18)
    pdb.gimp_floating_sel_anchor(pdb.gimp_selection_float(pdb.gimp_image_get_active_layer(img), 0, 1))
    
    postup_shading = pdb.gimp_file_load_layer(img, file_postup_shading)
    pdb.gimp_image_insert_layer( img, postup_shading, None, -1)
    pdb.gimp_image_merge_down( img, postup_shading, 0)
    pdb.file_png_save(img, img.layers[0], file_postup_save, file_postup_save, 0, 9, 0, 0, 0, 0, 0)

    pdb.gimp_image_delete(img)
    #hoisted
    img=pdb.gimp_file_load(file_load, file_load)

    offsetx=[8,12,16,20,24,28]
    offsety=[1,2,3,2,1,2]

    for i in range(0,6):
        pdb.gimp_image_select_rectangle(img, 0, offsetx[i], 5, 4, 18)
        pdb.gimp_floating_sel_anchor(pdb.gimp_selection_float(pdb.gimp_image_get_active_layer(img), 0, offsety[i]))

    shading = pdb.gimp_file_load_layer(img, file_hoisted_shading)
    pdb.gimp_image_insert_layer( img, shading, None, -1)
    pdb.gimp_image_merge_down( img, shading, 0)
    pdb.file_png_save(img, img.layers[0], file_hoisted_save, file_hoisted_save, 0, 9, 0, 0, 0, 0, 0)

    #item
    activeLayer = img.layers[0]
    pdb.plug_in_map_object(
    img, activeLayer, 0, 
    0.5, 0.5, 1.0, 
    0.455, 0.5, -0.06, 
    0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 
    -24.0, -5.0, -40.0, 
    2, (0,0,0), 
    0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 
    0.3, 1.0, 0.5, 0.5, 27.0, 
    0, 0, 0, 1, 
    0.0, 0.0, 0.0, 0.0, 0.0, 
    activeLayer, activeLayer, activeLayer, activeLayer, activeLayer, activeLayer, activeLayer, activeLayer);
    pdb.plug_in_threshold_alpha(img, img.layers[0], 93.4)
    shadow = pdb.gimp_file_load_layer(img, file_item_shadow)
    pdb.gimp_image_insert_layer( img, shadow, None, -1)
    pdb.gimp_image_merge_down( img, shadow, 0)

    pdb.file_png_save(img, img.layers[0], file_item_save, file_item_save, 0, 9, 0, 0, 0, 0, 0)
    pdb.gimp_image_delete(img)
def normal_path(path):
    return path.replace("\\","/")

def run(directory):
    start=time.time()
    for infile in glob.glob(os.path.join(directory, '*.png')):
        process(infile)
    end=time.time()
    
if __name__ == "__main__":
    run("../scratch/UltimateCataclysm/items/flags")