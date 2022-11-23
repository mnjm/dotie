import os
import toml
import logging
from argparse import ArgumentParser

def dotie_map_loader(map_fp):
    try:
        dmap = toml.load(map_fp)
        return dmap
    except (toml.TomlDecodeError, IOError, FileNotFoundError) as e:
        print("ERROR", f"Reading {map_fp} failed!")
        print(e)
        return None

def arguments():
    # command line parser
    parser = ArgumentParser("Dotie - dotfiles linker")
    parser.add_argument("--dry-run", help = "dont make any changes to disk, just pretend",
                        action = 'store_true')
    parser.add_argument("--dotfiles-dir", help = "Dotfiles directory location. Will use DOTFILES env variable if not mentioned",
                        type = str)
    parser.add_argument("--map-file", help = "Map file location. Will use {DOTFILES}/dotie_map.toml if not mentioned",
                        type = str)
    parser.add_argument("--debug", action = 'store_true', help = "Print debug info")
    subparsers = parser.add_subparsers(dest = 'action', required = True)
    install = subparsers.add_parser('install', help = 'install dotfiles')
    install.add_argument('apps', help = "[app1] [app2] .. (apps to install)", nargs = '*')
    uninstall = subparsers.add_parser('uninstall', help = 'uninstall dotifiles')
    uninstall.add_argument('apps', help = "[app1] [app2] .. (apps to uninstall)", nargs = '*')
    generate = subparsers.add_parser('generate', help = "Generates map.toml template")
    generate.add_argument("src", help = "app path in dotfiles dir")
    generate.add_argument("dest", help = "link target location")
    generate.add_argument("--fold", help = "Generate templates with folds(*)", action = 'store_true')
    args = parser.parse_args()

    logging.basicConfig(format = '%(levelname)s: %(message)s',
                        level = logging.DEBUG if args.dry_run else logging.INFO)

    # find dotfiles_dir
    if not args.dotfiles_dir:
        if "DOTFILES" in os.environ:
            args.dotfiles_dir = os.environ["DOTFILES"]
        else:
            logging.error("Dotfiles dir not found! Either pass --dotfiles_dir {dotfiles_dir} or set env variable $DOTFILES")
            return None
        if not os.path.isdir(args.dotfiles_dir):
            logging.error(f"{args.dotfiles_dir} is not a dir")
            return None
    logging.info(f"Dotfiles_dir = {args.dotfiles_dir}")

    # find map toml file
    if not args.map_file:
        args.map_file = os.path.join(args.dotfiles_dir, "dotie_map.toml")
        if not os.path.isfile(args.map_file):
            logging.error("Map file not found! Either pass --map_file <map_file> or place the map file in to {}/dotie_map.toml".format(args.dotfiles_dir))
            return None
    logging.info(f"Map file = {args.map_file}")

    return args

def main():
    # dmap = dotie_map_loader("dotie_map.toml")
    # print(dmap)
    args = arguments()

if __name__ == "__main__":
    main()
