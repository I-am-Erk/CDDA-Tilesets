import glob
import argparse
import json
import subprocess
from tqdm import tqdm


def switch(to_be_switched: dict, a: int, b: int, modified: bool) -> bool:
    if 'fg' in to_be_switched:
        if isinstance(to_be_switched['fg'], list) and len(to_be_switched['fg']) >= 4:
            if isinstance(to_be_switched['fg'][0], dict):
                for obj in to_be_switched['fg']:
                    if 'sprite' in obj:
                        obj['sprite'][a], obj['sprite'][b] = obj['sprite'][b], obj['sprite'][a]
            else:
                to_be_switched['fg'][a], to_be_switched['fg'][b] = to_be_switched['fg'][b], to_be_switched['fg'][a]
            modified = True
    if 'bg' in to_be_switched:
        if isinstance(to_be_switched['bg'], list) and len(to_be_switched['bg']) >= 4:
            if isinstance(to_be_switched['bg'][0], dict):
                for obj in to_be_switched['bg']:
                    if 'sprite' in obj:
                        obj['sprite'][a], obj['sprite'][b] = obj['sprite'][b], obj['sprite'][a]
            else:
                to_be_switched['bg'][a], to_be_switched['bg'][b] = to_be_switched['bg'][b], to_be_switched['bg'][a]
            modified = True
    return modified


def decide_switch(to_be_switched: dict, modified: bool) -> bool:
    if 'additional_tiles' in to_be_switched:
        for item in to_be_switched['additional_tiles']:
            if item['id'] == 'corner' or item['id'] == 't_connection':
                modified = switch(item, 1, 3, modified)
            elif item['id'] == 'end_piece':
                modified = switch(item, 0, 2, modified)
    elif 'rotates' in to_be_switched:
        if to_be_switched['rotates']:
            modified = switch(to_be_switched, 1, 3, modified)
    return modified


def main(args: argparse.Namespace) -> None:
    for filename in tqdm(glob.glob(args.folder + '/**/*.json', recursive=True)):
        with open(filename, 'r+') as f:
            modified = False
            d = json.load(f)
            if isinstance(d, list):
                for obj in d:
                    modified = decide_switch(obj, modified)
            elif isinstance(d, dict):
                modified = decide_switch(d, modified)
            if modified:
                f.seek(0)
                json.dump(d, f, indent=4)
        if modified:
            subprocess.run([args.linter, filename])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fix rotation in multi-tile json")
    parser.add_argument(
        "folder",
        help="path to the folder of json to edit")
    parser.add_argument("linter", help="Path to linter")
    main(parser.parse_args())
