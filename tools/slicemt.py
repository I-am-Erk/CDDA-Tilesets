import sys
import os
import fnmatch
from pathlib import Path

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

if len(sys.argv) < 2:
  FullPath = os.getcwd()
else:
  FullPath = sys.argv[1]
print(f"Will work on : {bcolors.OKCYAN}" + FullPath + f"{bcolors.ENDC}")

PathDetails = FullPath.split("\\")
CurrentTileName = PathDetails[-2]
print(f"Tile name is : {bcolors.OKCYAN}" + CurrentTileName + f"{bcolors.ENDC}")

PathLevel = fnmatch.filter(PathDetails,"*pngs*x*")
if len(PathLevel) > 0:
  LevelParts = PathLevel[0].split("_")
  Dimensions = LevelParts[-1]
  DimX = Dimensions.split("x")[0]
  DimY = Dimensions.split("x")[1]
else:
  print(f"{bcolors.FAIL}Check folder. It has to be cloned repository.{bcolors.ENDC}")
  quit()
print(f"Dimentions   : {bcolors.OKCYAN}" + DimX + " x " + DimY + f"{bcolors.ENDC}")

Patterns = [ CurrentTileName + "_var*.png" ]
for Pattern in Patterns:
  print(Pattern)
  for File in Path(FullPath).glob(Pattern):
    head, tail = os.path.split(File)
    print(tail)

input("Press Enter to continue...")
