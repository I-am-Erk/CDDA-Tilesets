import glob, os, shutil #pip install glob3
import numpy as np #pip install numpy
from PIL import Image
import sys

numberPrefixes = ["_0", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_8"]
seasonPrefixes = {
  "_season_autumn": [(230,227,171), (216,147,110), (163,100,92), (90,68,72)],
  "_season_winter": [(254,254,254), (203,200,218), (137,119,142), (90,68,72)],
  "_season_summer": [(255,216,148), (194,176,107), (83,138,106), (73,75,88)]
}
defaultColors = [(240,236,187), (181,175,105), (115,130,92), (95,76,53)]

def replaceColors(seasonFile, season):
    replacementColors = seasonPrefixes[season]
    img = Image.open(seasonFile).convert('RGB')
    data = np.array(img)
    currentColor = 0
    
    for color in defaultColors:
        data[(data == color).all(axis = -1)] = replacementColors[currentColor]
        currentColor = currentColor + 1

    return Image.fromarray(data, mode='RGB')


def transparent_background( img ):
    img = img.convert("RGBA")
    img_datas = img.getdata()
    newData = []
    for item in img_datas:
        if item[0] == 21 and item[1] == 19 and item[2] == 21:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

def change_colors():
    dirName = os.path.basename(os.getcwd())
    for file in glob.glob("*.png"):
        newFile = file
        prefix = ""
        if newFile.endswith(".png"):
            newFile = newFile[:-4]
            for number in numberPrefixes:
                if newFile.endswith(number):
                    newFile = newFile[:-2]
                    prefix = number
                    break

            for season in seasonPrefixes:
                seasonFile = f"{dirName}"
                seasonFile = seasonFile + season
                seasonFile = seasonFile + prefix
                seasonFile = seasonFile + ".png"
                shutil.copy2(file, seasonFile)
                img = replaceColors(seasonFile, season)
                transparent_background( img ).save(seasonFile, "PNG")

        new_name = f"{dirName}"+"_season_spring.png"
        os.rename(file,new_name)
        transparent_background( Image.open(new_name) ).save(new_name, "PNG")
        print(dirName)



rootdir = sys.argv[1]



for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == "generic.png":
            os.chdir(subdir)
            change_colors()
