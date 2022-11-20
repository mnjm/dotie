import os
import toml
import sys
from argparse import ArgumentParser

def dotie_map_loader(map_fp):
    try:
        dmap = toml.load(map_fp)
    except (toml.TomlDecodeError, IOError, FileNotFoundError) as e:
        print("ERROR", f"Reading {map_fp} failed!")
        print(e)
        sys.exit(1)
    return dmap

def arguments():
    parser = ArgumentParser("Dotie - dotfiles linker")
    parser.add_argument("--dry-run", help = "dont make any changes to disk, just pretend",
                        action = 'store_true')
    parser.add_argument("--dotfiles_dir", help = "Dotfiles directory location. Will use DOTFILES env variable if not mentioned",
                        type = str)
    parser.add_argument("--map_file", help = "Map file location. Will use {DOTFILES}/dotie_map.toml if not mentioned",
                        type = str)
    parser.add_argument("--debug", action='store_true', help="Print debug info")
    subparsers = parser.add_subparsers(dest='action', required = True)
    install = subparsers.add_parser('install', help='install dotfiles')
    install.add_argument('apps', help="[app1] [app2] .. (apps to install)", nargs='*')
    uninstall = subparsers.add_parser('uninstall', help='uninstall dotifiles')
    uninstall.add_argument('apps', help="[app1] [app2] .. (apps to uninstall)", nargs='*')
    generate = subparsers.add_parser('generate', help="Generates map.toml template")
    generate.add_argument("src", help="app path in dotfiles dir {dotfiles}/{app}")
    generate.add_argument("dest", help="link target location")
    generate.add_argument("--fold", help="Generate templates with folds (*)", action='store_true')
    args = parser.parse_args()
    return args

def main():
    # dmap = dotie_map_loader("dotie_map.toml")
    # print(dmap)
    print(arguments())

if __name__ == "__main__":
    main()
