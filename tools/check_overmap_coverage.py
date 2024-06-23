"""
this script will try to find out what overmap tiles have sprites
"""

import sys
import os
from subprocess import STDOUT, call, check_output
import argparse
import sqlite3
import json


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def ShowExceptionAndExit(exc_type, exc_value, tb):
    import traceback

    traceback.print_exception(exc_type, exc_value, tb)
    input("Press Enter to exit.")
    sys.exit(-1)


def CheckFile(str_path, str_file):
    """Check if file exist at the provided path

    Args:
        str_path (str): Absolute or relative path
        str_file (str): FileName

    Returns:
        bool: True if file exist
    """
    TestFile = os.path.join(str_path, str_file)
    return os.path.isfile(TestFile)


def CheckCDDAdir(str_path):
    if CheckFile(str_path, "VERSION.txt"):
        return os.path.normpath(str_path)
    else:
        return False


def FindCDDAdir(cli_arg):
    print(f"Determining CDDA executable directory:")
    CDDAcli = False
    CDDAenv = False
    CDDAsql = False

    Result = False

    # Check command line argument
    if cli_arg:
        CDDAcli = CheckCDDAdir(cli_arg)
        if CDDAcli:
            print(
                f"- CLI argument : "
                + CDDAcli
                + f"{bcolors.OKGREEN} found!{bcolors.ENDC}"
            )
            Result = CDDAcli
        else:
            print(
                f"- CLI argument : "
                + cli_arg
                + f"{bcolors.WARNING} not found!{bcolors.ENDC}"
            )
    else:
        print(f"- CLI argument : " + f"{bcolors.WARNING}not provided!{bcolors.ENDC}")

    # Check environment variable
    try:
        env_arg = CheckCDDAdir(os.getenv("CDDA_PATH"))
    except:
        env_arg = False

    if env_arg:
        CDDAenv = CheckCDDAdir(env_arg)
        if CDDAenv:
            if CDDAcli:
                if CDDAenv == CDDAcli:
                    print(f"- ENV variable : exist and same as CLI argument.")
                else:
                    print(
                        f"- ENV variable : "
                        + CDDAenv
                        + f"{bcolors.WARNING} different from CLI!{bcolors.ENDC}"
                    )
            else:
                Result = CDDAenv
                print(
                    f"- ENV variable : "
                    + CDDAenv
                    + f"{bcolors.OKGREEN} found!{bcolors.ENDC}"
                )
        else:
            print(
                f"- ENV variable : "
                + cli_arg
                + f"{bcolors.WARNING} not found!{bcolors.ENDC}"
            )
    else:
        print(f"- ENV variable : " + f"{bcolors.WARNING}not provided!{bcolors.ENDC}")

    # Check Kitty CDDA Launcher settings
    AppsLocalDir = os.path.join(os.getenv("LOCALAPPDATA"), "CDDA Game Launcher")
    KittenSettings = "configs.db"
    if CheckFile(AppsLocalDir, KittenSettings):
        try:
            dbfile = os.path.join(AppsLocalDir, KittenSettings)
            con = sqlite3.connect(dbfile)
            cur = con.cursor()
            sql_arg = cur.execute(
                'SELECT value FROM config_value WHERE name = "game_directory" '
            ).fetchone()[0]
            con.close()
        except:
            sql_arg = False

        if sql_arg:
            CDDAsql = CheckCDDAdir(sql_arg)
            if CDDAsql:
                if CDDAenv:
                    if CDDAcli:
                        if CDDAsql == CDDAcli:
                            print(
                                f"- Launcher  DB : setting exist and same as CLI argument."
                            )
                        elif CDDAsql == CDDAenv:
                            print(
                                f"- Launcher  DB : setting exist and same as environment variable, but differs from CLI argument."
                            )
                        else:
                            print(
                                f"- Launcher  DB : "
                                + CDDAsql
                                + f"{bcolors.WARNING} different from everything above!{bcolors.ENDC}"
                            )
                    elif CDDAsql == CDDAenv:
                        print(
                            f"- Launcher  DB : setting exist and same as environment variable."
                        )
                    else:
                        print(
                            f"- Launcher  DB : "
                            + CDDAsql
                            + f"{bcolors.WARNING} different from environment variable!{bcolors.ENDC}"
                        )
                elif CDDAcli:
                    if CDDAsql == CDDAcli:
                        print(
                            f"- Launcher  DB : setting exist and same as CLI argument."
                        )
                    else:
                        print(
                            f"- Launcher  DB : "
                            + CDDAsql
                            + f" setting exist, but differs from CLI argument."
                        )
                else:
                    Result = CDDAsql
                    print(
                        f"- Launcher  DB : "
                        + CDDAsql
                        + f"{bcolors.OKGREEN} found!{bcolors.ENDC}"
                    )
            else:
                print(
                    f"- Launcher  DB : "
                    + sql_arg
                    + f"{bcolors.WARNING} setting exist, but no CDDA executable found{bcolors.ENDC}"
                )
        else:
            print(
                f"- Launcher  DB : {bcolors.WARNING}Launcher is here, but no game_directory found!{bcolors.ENDC}"
            )
    else:
        print(f"- Launcher  DB : no Kitten CDDA Launcher found.")

    # print('\n')
    if Result:
        print(f"+ game is here : {bcolors.OKCYAN}" + Result + f"{bcolors.ENDC}")
        return Result
    else:
        print(f"{bcolors.FAIL}! CDDA game directory not found!{bcolors.ENDC}")
        exit(1)


def GetGitRoot(p):
    """Return None if p is not in a git repo, or the root of the repo if it is"""
    if call(["git", "branch"], stderr=STDOUT, stdout=open(os.devnull, "w"), cwd=p) != 0:
        return None
    else:
        root = check_output(["git", "rev-parse", "--show-toplevel"], cwd=p)
        return root.strip().decode("utf-8")


def SelectTileset(repo_root):
    GFXdir = os.path.join(repo_root, "gfx")

    AllSubDirs = [
        d for d in os.listdir(GFXdir) if os.path.isdir(os.path.join(GFXdir, d))
    ]

    print("    Available tilesets:")
    for i, SubDir in enumerate(AllSubDirs):
        print(f"    {i + 1}. {SubDir}")

    try:
        UserChoice = (
            int(input("Enter the number corresponding to the desired tileset: ")) - 1
        )
        SelectedDir = AllSubDirs[UserChoice]
        return (os.path.join(GFXdir, SelectedDir))
    except (ValueError, IndexError):
        print("Invalid input.")
        return None


def FindTilesetDir(cli_arg2):
    print("Determining tileset and its location")
    RepoDir = False
    Result = False
    TSetFName = "tile_info.json"

    ScriptDir = os.path.abspath(os.path.dirname(__file__))
    CWDir = os.path.normpath(os.getcwd())

    if cli_arg2:
        print("- Tileset argument provided. Lets try to find tileset location.")
        print(f"  - {bcolors.OKBLUE}" + cli_arg2 + f"{bcolors.ENDC}")
        if CheckFile(cli_arg2, TSetFName):
            print(f"- {bcolors.OKGREEN}Tileset found!{bcolors.ENDC}")
            Result = os.path.normpath(cli_arg2)
        else:
            print(f"- CLI argument is not a valid path to the tileset.")

        if CheckFile(os.path.join(CWDir, cli_arg2), TSetFName):
            print(
                f"- CLI argument is a relative path. {bcolors.OKGREEN}Tileset found!{bcolors.ENDC}"
            )
            Result = os.path.normpath(os.path.join(CWDir, cli_arg2))
        else:
            print(f"- CLI argument is not a relative path.")

        if ScriptDir:
            print(f"- Assuming that script is running from tileset repository")
            RepoDir = GetGitRoot(ScriptDir)
            if RepoDir:
                print(f"  - Repository found!")
                if CheckFile(
                    os.path.normpath(os.path.join(RepoDir, "gfx", cli_arg2)), TSetFName
                ):
                    print(f"  - {bcolors.OKGREEN}Tileset found!{bcolors.ENDC}")
                    Result = os.path.normpath(os.path.join(RepoDir, "gfx", cli_arg2))
                else:
                    print(f"  - Tileset not found")
            else:
                print(f"  - Repository not found")

    else:
        print(
            "- No tileset argument provided. Should try to find repository and offer a choice."
        )
        print(f"  - Check if current directory is in the repo.")
        RepoDir = GetGitRoot(CWDir)
        if RepoDir:
            print(f"  - Repository found!")
            Result = os.path.normpath(SelectTileset(RepoDir))
        else:
            print(f"  - Check if script directory is in the repo")
            RepoDir = GetGitRoot(ScriptDir)
            if RepoDir:
                print(f"  - Repository found!")
                Result = os.path.normpath(SelectTileset(RepoDir))

    if Result:
        print(f"+ Tileset is here : {bcolors.OKCYAN}" + Result + f"{bcolors.ENDC}")
        return Result
    else:
        print(f"! {bcolors.FAIL}Tileset not found.{bcolors.ENDC}")
        exit(2)


def ReadJSONfromFiles(json_dir):
    ObjectsAll = []
    for FileName in os.listdir(json_dir):
        if FileName.endswith(".json"):
            with open(os.path.join(json_dir, FileName), "r", encoding="utf-8") as JSONFile:
                JSONData = json.load(JSONFile)
                ObjectsAll.extend(JSONData)
    return ObjectsAll


def GetUniqueNames(objects_list):
    UniqueNames = set()
    for Obj in objects_list:
        Name = Obj.get("name")
        if isinstance(Name, dict) and "str" in Name:
            UniqueNames.add(Name["str"])
        elif isinstance(Name, str):
            UniqueNames.add(Name)
    return list(UniqueNames)


def GetObjByID(id, objects_list):
    for Obj in objects_list:
        if isinstance(Obj.get("id"), list):
            if id in Obj["id"]:
                return Obj
        elif Obj.get("id") == id:
            return Obj
        elif isinstance(Obj.get("abstract"), list):
            if id in Obj["abstract"]:
                return Obj
        elif Obj.get("abstract") == id:
            return Obj
    return None


def GetObjName(id, objects_list):
    Obj = GetObjByID(id, objects_list)
    if "name" in Obj:
        FullName = Obj.get("name")
        if isinstance(FullName, dict) and "str" in FullName:
            RealName = FullName["str"]
        elif isinstance(FullName, str):
            RealName = FullName
        else:
            exit(3)
    elif "copy-from" in Obj:
        ParentID = Obj["copy-from"]
        RealName = GetObjName(ParentID, objects_list)
    else:
        exit(4)
    return RealName


def GetAllNamesAndIDs(objects_list):
    NamesAndIds = {}
    AllNames = GetUniqueNames(objects_list)
    for Name in AllNames:
        NamesAndIds[Name] = set()

    for Obj in objects_list:
        if Obj.get("id"):
            ObjIDs = Obj["id"] if isinstance(Obj["id"], list) else [Obj["id"]]
            for ID in ObjIDs:
                Name = GetObjName(ID, objects_list)
                NamesAndIds[Name].add(ID)

    SortedResults = sorted(
        NamesAndIds.items(),
        # key=lambda x: ( len(x[1]), sorted(x[1]) )
        key=lambda x: x[0].lower(),
    )

    return dict(SortedResults)


def GetAllJSONfiles(folder_path):
    JSONfiles = []
    for Root, Dirs, Files in os.walk(folder_path):
        for File in Files:
            if File.lower().endswith('.json') and File != "tile_info.json":
                JSONfiles.append(os.path.join(Root, File))
    return JSONfiles


def GetAllIDsFromFile(filename):
    with open(filename, "r") as JSONfile:
        JSONdata = json.load(JSONfile)
    IDs = []
    if isinstance(JSONdata, dict):
        return [JSONdata.get("id")]
    elif isinstance(JSONdata, list):
        IDs = []
        for Obj in JSONdata:
            if isinstance(Obj["id"], list):
                IDs.extend(Obj["id"])
            else:
                IDs.append(Obj["id"])
        return IDs
    else:
        raise ValueError("Input JSON data should be a single object or a list of objects.")


def GetAllSpritedIDs(folder_path):
    AllIDs = []
    AllJSONFiles = GetAllJSONfiles(folder_path)
    for JSONfile in AllJSONFiles:
        AllIDs += GetAllIDsFromFile(JSONfile)
    return AllIDs

def main(args):
    sys.excepthook = ShowExceptionAndExit

    CDDAdir = FindCDDAdir(args.CDDAdir)
    OverMapJSONdir = os.path.join(CDDAdir, "data\json\overmap\overmap_terrain")

    TsetDir = FindTilesetDir(args.tileset)
    AllOverMapObjects = ReadJSONfromFiles(OverMapJSONdir)

    SpritedIDs = GetAllSpritedIDs(TsetDir)


    print(f"Total overmap objects in game: " + str(len(AllOverMapObjects)))
    print()

    Result = GetAllNamesAndIDs(AllOverMapObjects)

    for Name, IDs in Result.items():
        if len(IDs) > 0:
            print(f"{Name} ({len(IDs)} IDs):")
        for ID in IDs:
            Mark = "*" if ID in SpritedIDs else " "
            print(f"{Mark} - {ID}")

    # om terrain names/ids can be found in:
    # cdda\data\json\overmap\overmap_terrain\
    # all files

    # if 'type' = 'overmap_terrain'
    # then 'name' is a group, name can be absent if 'copy-from' 'abstract'
    # and 'id' is a OMT


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check overmap tileset coverage.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Can be used with environment variables.\n"
        "use the provided tools:\n"
        "  CDDAdir can be set up with `set_game_path.cmd`\n"
        "  tileset can be set up with `set_tileset.cmd`\n"
        "\n"
        "Additionally, if using the Kitten CDDA launcher,\n"
        "this tool can retrieve CDDAdir from the launcher.\n",
    )
    parser.add_argument(
        "CDDAdir",
        type=str,
        nargs="?",
        help="Path to the game executable. If left empty, the tool will attempt to determine the path through other methods.",
    )
    parser.add_argument(
        "tileset",
        type=str,
        nargs="?",
        help="Tileset directory name. If left empty, the tool will attempt to identify possible tilesets based on the current directory.",
    )
    parser.add_argument("--tile", type=str, help="Specific overmap tile to check.")

    main(parser.parse_args())
