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


def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback

    traceback.print_exception(exc_type, exc_value, tb)
    input("Press Enter to exit...")
    sys.exit(-1)


def check_file_exsit(str_path, str_file):
    """Check if file exist at the provided path

    Args:
        str_path (str): Absolute or relative path
        str_file (str): FileName

    Returns:
        bool: True if file exist
    """
    TestFile = os.path.join(str_path, str_file)
    return os.path.isfile(TestFile)


def check_cdda_dir(str_path):
    if check_file_exsit(str_path, "VERSION.txt"):
        return os.path.normpath(str_path)
    else:
        return None


def find_cdda_dir(cli_arg):
    print(f"Determining CDDA executable directory:")
    cdda_cl_argument = False
    cdda_env_variable = False
    cdda_kitty_data = False

    cdda_dir = False

    # Check command line argument
    if cli_arg:
        cdda_cl_argument = check_cdda_dir(cli_arg)
        if cdda_cl_argument:
            print(
                f"- CLI argument : {cdda_cl_argument} {bcolors.OKGREEN}found!{bcolors.ENDC}"
            )
            cdda_dir = cdda_cl_argument
        else:
            print(
                f"- CLI argument : {cli_arg} {bcolors.WARNING}not found!{bcolors.ENDC}"
            )
    else:
        print(f"- CLI argument : {bcolors.WARNING}not provided!{bcolors.ENDC}")

    # Check environment variable
    try:
        env_arg = check_cdda_dir(os.getenv("CDDA_PATH"))
    except:
        env_arg = False

    if env_arg:
        cdda_env_variable = check_cdda_dir(env_arg)
        if cdda_env_variable:
            if cdda_cl_argument:
                if cdda_env_variable == cdda_cl_argument:
                    print(f"- ENV variable : exist and same as CLI argument.")
                else:
                    print(
                        f"- ENV variable : {cdda_env_variable} {bcolors.WARNING}different from CLI!{bcolors.ENDC}"
                    )
            else:
                cdda_dir = cdda_env_variable
                print(
                    f"- ENV variable : {cdda_env_variable} {bcolors.OKGREEN}found!{bcolors.ENDC}"
                )
        else:
            print(
                f"- ENV variable : {cli_arg} {bcolors.WARNING}not found!{bcolors.ENDC}"
            )
    else:
        print(f"- ENV variable : {bcolors.WARNING}not provided!{bcolors.ENDC}")

    # Check Kitty CDDA Launcher settings
    lad_env_variable = os.path.join(os.getenv("LOCALAPPDATA"), "CDDA Game Launcher")
    launcher_file = "configs.db"
    if check_file_exsit(lad_env_variable, launcher_file):
        try:
            dbfile = os.path.join(lad_env_variable, launcher_file)
            con = sqlite3.connect(dbfile)
            cur = con.cursor()
            sql_arg = cur.execute(
                'SELECT value FROM config_value WHERE name = "game_directory" '
            ).fetchone()[0]
            con.close()
        except:
            sql_arg = False

        if sql_arg:
            cdda_kitty_data = check_cdda_dir(sql_arg)
            if cdda_kitty_data:
                if cdda_env_variable:
                    if cdda_cl_argument:
                        if cdda_kitty_data == cdda_cl_argument:
                            print(
                                f"- Launcher  DB : setting exist and same as CLI argument."
                            )
                        elif cdda_kitty_data == cdda_env_variable:
                            print(
                                f"- Launcher  DB : setting exist and same as environment variable, but differs from CLI argument."
                            )
                        else:
                            print(
                                f"- Launcher  DB : {cdda_kitty_data} {bcolors.WARNING}different from everything above!{bcolors.ENDC}"
                            )
                    elif cdda_kitty_data == cdda_env_variable:
                        print(
                            f"- Launcher  DB : setting exist and same as environment variable."
                        )
                    else:
                        print(
                            f"- Launcher  DB : {cdda_kitty_data} {bcolors.WARNING}different from environment variable!{bcolors.ENDC}"
                        )
                elif cdda_cl_argument:
                    if cdda_kitty_data == cdda_cl_argument:
                        print(
                            f"- Launcher  DB : setting exist and same as CLI argument."
                        )
                    else:
                        print(
                            f"- Launcher  DB : {cdda_kitty_data} setting exist, but differs from CLI argument."
                        )
                else:
                    cdda_dir = cdda_kitty_data
                    print(
                        f"- Launcher  DB : {cdda_kitty_data} {bcolors.OKGREEN}found!{bcolors.ENDC}"
                    )
            else:
                print(
                    f"- Launcher  DB : {sql_arg} {bcolors.WARNING}setting exist, but no CDDA executable found{bcolors.ENDC}"
                )
        else:
            print(
                f"- Launcher  DB : {bcolors.WARNING}Launcher is here, but no game_directory found!{bcolors.ENDC}"
            )
    else:
        print(f"- Launcher  DB : no Kitten CDDA Launcher found.")

    # print('\n')
    if cdda_dir:
        print(f"+ game is here : {bcolors.OKCYAN}{cdda_dir}{bcolors.ENDC}")
        return cdda_dir
    else:
        print(
            f"{bcolors.FAIL}! Please provide path to the game as first argument to the script.{bcolors.ENDC}"
        )
        raise ValueError("CDDA game directory not found!")


def get_repository_root(p):
    """Return None if p is not in a git repo, or the root of the repo if it is"""
    if call(["git", "branch"], stderr=STDOUT, stdout=open(os.devnull, "w"), cwd=p) != 0:
        return None
    else:
        root = check_output(["git", "rev-parse", "--show-toplevel"], cwd=p)
        return root.strip().decode("utf-8")


def select_tileset_dir(repo_root):
    gfx_dir = os.path.join(repo_root, "gfx")

    all_sub_dirs = [
        d for d in os.listdir(gfx_dir) if os.path.isdir(os.path.join(gfx_dir, d))
    ]

    print("    Available tilesets:")
    for i, sub_dir in enumerate(all_sub_dirs):
        print(f"    {i + 1}. {sub_dir}")

    try:
        user_choice = (
            int(input("Enter the number corresponding to the desired tileset: ")) - 1
        )
        selected_dir = all_sub_dirs[user_choice]
        return os.path.join(gfx_dir, selected_dir)
    except (ValueError, IndexError):
        print("Invalid input.")
        return None


def find_tset_dir(cli_arg2):
    print("Determining tileset and its location")
    repository_dir = False
    tileset_dir = False
    tileset_file = "tile_info.json"

    script_dir = os.path.abspath(os.path.dirname(__file__))
    cwd = os.path.normpath(os.getcwd())

    if cli_arg2:
        print("- Tileset argument provided. Lets try to find tileset location.")
        print(f"  - {bcolors.OKBLUE}{cli_arg2}{bcolors.ENDC}")
        if check_file_exsit(cli_arg2, tileset_file):
            print(f"- {bcolors.OKGREEN}Tileset found!{bcolors.ENDC}")
            tileset_dir = os.path.normpath(cli_arg2)
        else:
            print(f"- CLI argument is not a valid path to the tileset.")

        if check_file_exsit(os.path.join(cwd, cli_arg2), tileset_file):
            print(
                f"- CLI argument is a relative path. {bcolors.OKGREEN}Tileset found!{bcolors.ENDC}"
            )
            tileset_dir = os.path.normpath(os.path.join(cwd, cli_arg2))
        else:
            print(f"- CLI argument is not a relative path.")

        if script_dir:
            print(f"- Assuming that script is running from tileset repository")
            repository_dir = get_repository_root(script_dir)
            if repository_dir:
                print(f"  - Repository found!")
                if check_file_exsit(
                    os.path.normpath(os.path.join(repository_dir, "gfx", cli_arg2)),
                    tileset_file,
                ):
                    print(f"  - {bcolors.OKGREEN}Tileset found!{bcolors.ENDC}")
                    tileset_dir = os.path.normpath(
                        os.path.join(repository_dir, "gfx", cli_arg2)
                    )
                else:
                    print(f"  - Tileset not found")
            else:
                print(f"  - Repository not found")

    else:
        print(
            "- No tileset argument provided. Should try to find repository and offer a choice."
        )
        print(f"  - Check if current directory is in the repo.")
        repository_dir = get_repository_root(cwd)
        if repository_dir:
            print(f"  - Repository found!")
            tileset_dir = os.path.normpath(select_tileset_dir(repository_dir))
        else:
            print(f"  - Check if script directory is in the repo")
            repository_dir = get_repository_root(script_dir)
            if repository_dir:
                print(f"  - Repository found!")
                tileset_dir = os.path.normpath(select_tileset_dir(repository_dir))

    if tileset_dir:
        print(f"+ Tileset is here : {bcolors.OKCYAN}{tileset_dir}{bcolors.ENDC}")
        return tileset_dir
    else:
        print(
            f"! {bcolors.FAIL}Please provide a path to the tileset as the second script argument{bcolors.ENDC}"
        )
        raise ValueError("Tileset not found!")


def read_objects_from_file(json_file):
    objects = []
    with open(
        json_file, "r", encoding="utf-8"
    ) as file_with_objects:
        json_data = json.load(file_with_objects)
        objects.extend(json_data)
    file_with_objects.close
    return objects


def read_objects_from_dir(json_dir):
    objects_all = []
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            objects_all.extend(read_objects_from_file(os.path.join(json_dir, filename)))
    return objects_all


def get_unique_names(objects_list):
    unique_names = set()
    for obj in objects_list:
        object_name = obj.get("name")
        if isinstance(object_name, dict) and "str" in object_name:
            unique_names.add(object_name["str"])
        elif isinstance(object_name, str):
            unique_names.add(object_name)
    return list(unique_names)


def get_object_by_id(object_id, objects_list):
    for obj in objects_list:
        if isinstance(obj.get("id"), list):
            if object_id in obj["id"]:
                return obj
        elif obj.get("id") == object_id:
            return obj
        elif isinstance(obj.get("abstract"), list):
            if object_id in obj["abstract"]:
                return obj
        elif obj.get("abstract") == object_id:
            return obj
    return None


def get_object_name(object_id, objects_list):
    obj = get_object_by_id(object_id, objects_list)
    if "name" in obj:
        object_extracted_name = obj.get("name")
        if isinstance(object_extracted_name, dict) and "str" in object_extracted_name:
            object_name = object_extracted_name["str"]
        elif isinstance(object_extracted_name, str):
            object_name = object_extracted_name
        else:
            raise ValueError("Cant extract object name from data!")
    elif "copy-from" in obj:
        object_name = get_object_name(obj["copy-from"], objects_list)
    else:
        object_name = None
    return object_name


def get_all_names_and_ids(objects_list):
    names_and_ids = {}
    for name in get_unique_names(objects_list):
        names_and_ids[name] = set()

    for obj in objects_list:
        if obj.get("id"):
            extracted_ids = obj["id"] if isinstance(obj["id"], list) else [obj["id"]]
            for object_id in extracted_ids:
                name = get_object_name(object_id, objects_list)
                if name:
                    names_and_ids[name].add(object_id)

    sorted_results = sorted(
        names_and_ids.items(),
        # key=lambda x: ( len(x[1]), sorted(x[0]) ) # sorted by number of ids in name, then by names within similar number
        key=lambda x: x[0].lower(),  # sorted by names
    )

    return dict(sorted_results)


def get_json_filenames(folder_path):
    json_filenames = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".json") and file != "tile_info.json":
                json_filenames.append(os.path.join(root, file))
    return json_filenames


def get_ids_from_file(filename):
    with open(filename, "r") as json_file:
        json_data = json.load(json_file)
    json_file.close
    ids = []
    objects = []
    if isinstance(json_data, dict):
        objects.append(json_data.copy())
    else: objects = json_data
    for obj in objects:
        list_of_ids = obj.get("id", [])
        if isinstance(list_of_ids, str):
            list_of_ids = [list_of_ids]
        for main_id in list_of_ids:
            ids.append(main_id)
        additional_tiles = obj.get("additional_tiles", [])
        for tile in additional_tiles:
            tile_id = tile.get("id")
            if tile_id:
                additional_ids = [f"{main_id}_{tile_id}" for main_id in list_of_ids]
                ids.extend(additional_ids)
    return ids


def get_all_sprited_ids(folder_path):
    ids = []
    filenames_and_ids = []
    for json_file in get_json_filenames(folder_path):
        ids_from_file = get_ids_from_file(json_file)
        ids += ids_from_file
        filenames_and_ids.append((json_file, ids_from_file))
    return ids, filenames_and_ids


def get_filename_for_id(id_to_find, filenames_and_ids):
    for filename, ids in filenames_and_ids:
        if id_to_find in ids:
            return filename
    return None


def sort_and_mark_objects(names_and_ids, sprited_ids, sorting_option):
    result = []
    total_marked_ids = 0
    total_unmarked_ids = 0

    for name, ids in names_and_ids.items():
        marked_ids = sorted([id for id in ids if id in sprited_ids])
        unmarked_ids = sorted([id for id in ids if id not in sprited_ids])
        if len(marked_ids) + len(unmarked_ids) > 0:
            result.append((name, marked_ids, unmarked_ids))
            total_marked_ids += len(marked_ids)
            total_unmarked_ids += len(unmarked_ids)

    if sorting_option == "name":
        result.sort(key=lambda x: x[0].lower())
    elif sorting_option == "size":
        result.sort(key=lambda x: (len(x[1]) + len(x[2]), x[0].lower(), x[1], x[2]))
    elif sorting_option == "percent":
        result.sort(
            key=lambda x: (
                1 - (len(x[1]) / (len(x[1]) + len(x[2]))),
                x[0].lower(),
                x[1],
                x[2],
            )
        )
    else:
        result.sort(key=lambda x: x[0])

    return result, total_marked_ids, total_unmarked_ids


def check_substring_in_list(substring, string_list):
    for s in string_list:
        if substring in s:
            return True
    return False


## MARK: main function

def main(args):
    if not args.yes:
        sys.excepthook = show_exception_and_exit

    game_dir = find_cdda_dir(args.game_dir)
    game_overmap_dir = os.path.join(game_dir, "data\json\overmap\overmap_terrain")
    game_overmap_mx = os.path.join(game_dir, "data\json\overmap\map_extras.json")
    game_overmap_weather = os.path.join(game_dir, "data\json\weather_type.json")
    tileset_dir = find_tset_dir(args.tileset_dir)
    game_overmap_hardcoded = os.path.join(tileset_dir,"..\\..\\tools\\special_overmap_symbols.json")

    if args.part == 'm':
        overmap_objects = read_objects_from_dir(game_overmap_dir)
        print(f"{bcolors.BOLD}Main part of overmap objects is seleced{bcolors.ENDC}")
    elif args.part == 'w':
        overmap_objects = read_objects_from_file(game_overmap_weather)
        print(f"{bcolors.BOLD}Overmap weather is selected{bcolors.ENDC}")
    elif args.part == 'x':
        overmap_objects = read_objects_from_file(game_overmap_mx)
        print(f"{bcolors.BOLD}Overmap extras is selected{bcolors.ENDC}")
    else:
        overmap_objects = read_objects_from_file(game_overmap_hardcoded)
        print(f"{bcolors.BOLD}Hardcoded overmap objects are selected{bcolors.ENDC}")


    id_with_sprites, filenames_and_ids = get_all_sprited_ids(tileset_dir)

    names_and_ids = get_all_names_and_ids(overmap_objects)

    print(f"Total overmap objects in game: " + str(len(names_and_ids)))
    if args.name:
        print(f"  - Filtering objects names by substring : {bcolors.BOLD}{args.name}{bcolors.ENDC}")
    if args.id:
        print(f"  - Filtering ids by substring : {bcolors.BOLD}{args.id}{bcolors.ENDC}")
    if args.todo:
        print(f"  - Filtering IDs that have sprites. Only upsrited IDs will be shown.")
    print()

    sorted_result, total_marked_ids, total_unmarked_ids = sort_and_mark_objects(
        names_and_ids, id_with_sprites, args.sort
    )

    csv_result = []
    csv_result.append('"name";"mark";"id"')
    for name, marked_ids, unmarked_ids in sorted_result:
        if args.part == 'w':
            name = "Weather"
        if (
            not args.name and not args.id
        ) or (
            not args.id and args.name in name
        ) or (
            not args.name and (check_substring_in_list(args.id, marked_ids) or check_substring_in_list(args.id, unmarked_ids))
        ) or (
            args.name in name and (check_substring_in_list(args.id, marked_ids) or check_substring_in_list(args.id, unmarked_ids))
        ):
            if args.part != 'w':
                print(
                    f"{bcolors.BOLD}{bcolors.UNDERLINE}{name} ({len(marked_ids)} / {len(unmarked_ids)+len(marked_ids)}):{bcolors.ENDC}"
                )
            for id1 in marked_ids:
                longest_id = len(max(marked_ids, key=len))
                if ((not args.id) or (args.id in id1)) and not args.todo:
                    print(
                        f"{bcolors.OKBLUE}{args.mark} - {str(id1).ljust(longest_id)}{bcolors.ENDC}" +
                        (f" : {bcolors.UNDERLINE}{get_filename_for_id(id1, filenames_and_ids)}{bcolors.ENDC}" if args.json else "")
                    )
                    csv_result.append('"' + name + '";"' + args.mark + '";"' + id1 + '"')
            for id2 in unmarked_ids:
                if (not args.id) or (args.id in id2):
                    print(f"  - {id2}")
                    csv_result.append('"' + name + '";" ";"' + id2 + '"')

    print()
    print(f"Total sprited/unsprited IDs: {total_marked_ids}/{total_unmarked_ids} [total: {total_marked_ids+total_unmarked_ids}] ({round(total_marked_ids/(total_marked_ids+total_unmarked_ids)*100,1)}%)"
    )

    if args.file:
        try:
            output_file = open(args.file, "w")
            for line in csv_result:
                print(line, file=output_file)
            output_file.close()
            print(f"Result saved to: {bcolors.OKCYAN}{os.path.normpath(args.file)}{bcolors.ENDC}")
        except:
            raise ValueError("Cant write to output file!")

############################################################################## end of main ################## MARK: start of the scritp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check overmap tileset coverage.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Can be used with environment variables.\n"
        "use the provided tools:\n"
        "  game_dir can be set up with `set_game_path.cmd`\n"
        "  tileset_dir can be set up with `set_tileset.cmd`\n"
        "\n"
        "Additionally, if using the Kitten CDDA launcher,\n"
        "this tool can retrieve game_dir from the launcher.\n",
    )
    parser.add_argument(
        "game_dir",
        type=str,
        nargs="?",
        help="Path to the game executable. If left empty, the tool will attempt to determine the path through other methods.",
    )
    parser.add_argument(
        "tileset_dir",
        type=str,
        nargs="?",
        help="Tileset directory name. If left empty, the tool will attempt to identify possible tilesets based on the current directory.",
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Specify a filename for output (only names and IDs)."
    )
    parser.add_argument(
        "-m",
        "--mark",
        choices=["v", "X", "#"],
        default="#",
        help="Choose a symbol ('v', 'X', or '#') for IDs that have a sprite.",
    )
    parser.add_argument(
        "-s",
        "--sort",
        type=str,
        choices=["name", "size", "percent"],
        default="name",
        help="Choose sorting: 'name' (by name in lowercase), 'size' (by the number of IDs under the name, then alphabetically), or 'percent' (by the number of IDs covered).",
    )
    parser.add_argument(
        "-n", "--name", type=str, help="Substring to look in a group name."
    )
    parser.add_argument("-i", "--id", type=str, help="Substring to look in an id name.")
    parser.add_argument(
        "-t", "--todo",
        action="store_true",
        help="Show only IDs that do not have a sprite."
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Print all json file names."
    )
    parser.add_argument(
        "-p",
        "--part",
        choices=["m", "x", "o", "w"],
        default="m",
        help="Choose a part of overmap objects to check: 'm' - main part, 'w' - weather, 'x' - map extras, 'o' - other om objects",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true", help="Don't wait for user input."
    )

    main(parser.parse_args())
