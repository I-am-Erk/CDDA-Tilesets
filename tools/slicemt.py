"""
Slice a multitile source image into individual images and put them in the parent folder
Uses path to detect tile name, dimentions, tileset name etc
Intended to run in a cloned tileset repository

I think it can be run only on Windows.
"""

import sys
import os
import fnmatch
import time
import subprocess
from pathlib import Path
from slice_multitile import main as  mt_slicer
from slice_variants  import main as var_slicer

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class sliceargs:
  def __init__(self, image, width , height, tile, out):
    self.image   = image
    self.width   = width
    self.height  = height
    self.tile    = tile
    self.out     = out
    self.no_json = False
    self.append           = True
    self.iso              = False
    self.rearrange_top    = None
    self.rearrange_bottom = None
    self.background       = None


def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press Enter to exit.")
    sys.exit(-1)


def CheckAffectedFiles(ArgPath,ArgTime):
  NumberOfFiles = 0
  for root, dirs, files in os.walk(ArgPath):
    for name in files:
      filename = os.path.join(root, name)
      if os.stat(filename).st_mtime > ArgTime:
        NumberOfFiles += 1
  print('Number of affected files : ' + str(NumberOfFiles))
  print()


sys.excepthook = show_exception_and_exit

# Set working path
if len(sys.argv) < 2:
  FullPath = os.getcwd()
else:
  FullPath = sys.argv[1]

PathHead, PathTail = os.path.split(FullPath)
if PathTail != 'source':
  FullPath += '\\source'
print(f'Will work on : {bcolors.OKCYAN}' + FullPath + f'{bcolors.ENDC}')

# Set tile name
PathDetails = FullPath.split('\\')
CurrentTileName = PathDetails[-2]
print(f'Tile name is : {bcolors.OKCYAN}' + CurrentTileName + f'{bcolors.ENDC}')
# TODO: Probably should check it it looks like a tile name

# Check if working path contains tile dimentions, set them
PathLevel = fnmatch.filter(PathDetails,'*pngs*x*')
if len(PathLevel) > 0:
  LevelParts = PathLevel[0].split('_')
  Dimensions = LevelParts[-1]
  DimX = Dimensions.split('x')[0]
  DimY = Dimensions.split('x')[1]
else:
  print(f'{bcolors.FAIL}Check folder. It has to be cloned repository.{bcolors.ENDC}')
  quit()
print(f'Dimentions   : {bcolors.OKCYAN}' + DimX + ' x ' + DimY + f'{bcolors.ENDC}')

# Set current tileset name
TilesetName = PathDetails[PathDetails.index('gfx')+1]
print(f'Tileset name : {bcolors.OKCYAN}' + TilesetName + f'{bcolors.ENDC}')
print('')

# Set updtset.cmd path
UpdateCmd = '\\'.join(PathDetails[:PathDetails.index('gfx')]) + '\\tools\\updtset.cmd ' + TilesetName
UpdatePath = '\\'.join(PathDetails[:PathDetails.index('gfx')]) + '\\tools\\'

OutPath = FullPath + '\\..\\'

# Detect source files for variants
StartTime = time.time()
Patterns = [ '*_var*.png' ]
print('1) Searching for variants :')
for Pattern in Patterns:
  print(f'  {bcolors.OKBLUE}' + Pattern + f'{bcolors.ENDC}')
  for File in Path(FullPath).glob(Pattern):
    PathHead, PathTail = os.path.split(File)
    print(f'    found    : {bcolors.OKGREEN}' + PathTail + f'{bcolors.ENDC}')
    ResultName = PathTail.split('.')[0].split('_var')[0]+'_var'
    print('    result   : ' + ResultName)
    Args = sliceargs(
      File,       # image name
      int(DimX),  # width
      int(DimY),  # height
      ResultName, # resulting filenames
      OutPath     # out path
    )
    var_slicer(Args)
CheckAffectedFiles( FullPath+'\\..\\', StartTime )

# Detect source files for simple multitile
StartTime = time.time()
Patterns  = [ CurrentTileName +'.png' ]
print('2) Searching for simple multitile :')
for Pattern in Patterns:
  print(f'  {bcolors.OKBLUE}' + Pattern + f'{bcolors.ENDC}')
  for File in Path(FullPath).glob(Pattern):
    PathHead, PathTail = os.path.split(File)
    print(f'    found    : {bcolors.OKGREEN}' + PathTail + f'{bcolors.ENDC}')
    ResultName = CurrentTileName
    print('    result   : ' + ResultName)
    Args = sliceargs(
      File,       # image name
      int(DimX),  # width
      int(DimY),  # height
      ResultName, # resulting filenames
      OutPath     # out path
    )
    JsonCheck = OutPath + ResultName + '.json'
    if (os.path.exists(JsonCheck)) :
      print(f'{bcolors.WARNING}    ignoring : ' + ResultName + '.json' + f'{bcolors.ENDC}')
      Args.no_json = True
    mt_slicer(Args)
CheckAffectedFiles( FullPath+'\\..\\', StartTime )

# Detect source files for transparent multitile
StartTime = time.time()
Patterns = [ CurrentTileName +'_t*.png' ]
print('3) Searching for transparent multitile :')
for Pattern in Patterns:
  print(f'  {bcolors.OKBLUE}' + Pattern + f'{bcolors.ENDC}')
  for File in Path(FullPath).glob(Pattern):
    PathHead, PathTail = os.path.split(File)
    print(f'    found    : {bcolors.OKGREEN}' + PathTail + f'{bcolors.ENDC}')
    ResultName = CurrentTileName + '_transparent'
    print('    result   : ' + ResultName)
    Args = sliceargs(
      File,       # image name
      int(DimX),  # width
      int(DimY),  # height
      ResultName, # resulting filenames
      OutPath     # out path
    )
    JsonCheck = OutPath + ResultName + '.json'
    if (os.path.exists(JsonCheck)) :
      print(f'{bcolors.WARNING}    ignoring : ' + ResultName + '.json' + f'{bcolors.ENDC}')
      Args.no_json = True
    mt_slicer(Args)
CheckAffectedFiles( FullPath+'\\..\\', StartTime )

# Detect source files for seasonal multitiles
StartTime = time.time()
Patterns = [ CurrentTileName + '*_winter.png',
             CurrentTileName + '*_spring.png',
             CurrentTileName + '*_summer.png',
             CurrentTileName + '*_autumn.png' ]
print('4) Searching for simple multitiles :')
for Pattern in Patterns:
  print(f'  {bcolors.OKBLUE}' + Pattern + f'{bcolors.ENDC}')
  for File in Path(FullPath).glob(Pattern):
    PathHead, PathTail = os.path.split(File)
    Season = str(PathTail).split('.')[0].split('_')[-1]
    print('    '+Season+f'   : {bcolors.OKGREEN}' + PathTail + f'{bcolors.ENDC}')
    ResultName = CurrentTileName + '_season_' + Season
    print('    result   : ' + ResultName)
    Args = sliceargs(
      File,       # image name
      int(DimX),  # width
      int(DimY),  # height
      ResultName, # resulting filenames
      OutPath     # out path
    )
    JsonCheck = OutPath + ResultName + '.json'
    if (os.path.exists(JsonCheck)) :
      print(f'{bcolors.WARNING}    ignoring : ' + ResultName + '.json' + f'{bcolors.ENDC}')
      Args.no_json = True
    mt_slicer(Args)
CheckAffectedFiles( FullPath+'\\..\\', StartTime )

# Detect source files for seasonal transparent multitiles
StartTime = time.time()
Patterns = [ CurrentTileName + '*_winter_t*.png',
             CurrentTileName + '*_spring_t*.png',
             CurrentTileName + '*_summer_t*.png',
             CurrentTileName + '*_autumn_t*.png' ]
print('5) Searching for seasonal transparent multitiles :')
for Pattern in Patterns:
  print(f'  {bcolors.OKBLUE}' + Pattern + f'{bcolors.ENDC}')
  for File in Path(FullPath).glob(Pattern):
    PathHead, PathTail = os.path.split(File)
    Season = str(PathTail).split('.')[0].split('_')[-2]
    print('    '+Season+f'   : {bcolors.OKGREEN}' + PathTail + f'{bcolors.ENDC}')
    ResultName = CurrentTileName + '_season_' + Season + '_transparent'
    print('    result   : ' + ResultName)
    Args = sliceargs(
      File,        # image name
      int(DimX),   # width
      int(DimY),   # height
      ResultName,  # resulting filenames
      OutPath      # out path
    )
    JsonCheck = OutPath + ResultName + '.json'
    if (os.path.exists(JsonCheck)) :
      print(f'{bcolors.WARNING}    ignoring : ' + ResultName + '.json' + f'{bcolors.ENDC}')
      Args.no_json = True
    mt_slicer(Args)
CheckAffectedFiles( FullPath+'\\..\\', StartTime )

input('Press Enter to update tileset...')

subprocess.Popen(UpdateCmd, shell = True, cwd = UpdatePath)
