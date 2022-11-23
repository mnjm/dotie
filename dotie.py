import os
import toml
import logging
from argparse import ArgumentParser

def load_map_file(map_fp):
    dmap = None
    try:
        dmap = toml.load(map_fp)
        logging.debug("------------------------ Map File --------------------------------\n" + toml.dumps(dmap))
    except (toml.TomlDecodeError, IOError, FileNotFoundError) as e:
        logging.error("ERROR", f"Reading {map_fp} failed!")
        print(e)
    return dmap

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
    # print(args)

    logging.basicConfig(format = '%(levelname)s: %(message)s',
                        level = logging.DEBUG if args.debug else logging.INFO)
    logging.info(f"Dry run? {args.dry_run}")

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

def install(args):
    logging.info("Install")
    if not args: return
    dmap = load_map_file(args.map_file)
    if not dmap: return
    links = {}

    for app in dmap:
        logging.info("-"*50)
        logging.info(f"App = {app}")

        for tgt in dmap[app]:
            src = os.path.expanduser(dmap[app][tgt])
            logging.info(f"Checking {tgt} --> {src}")
            tgt = os.path.join(args.dotfiles_dir, tgt)
            if os.path.isfile(tgt):
                if os.path.isfile(src) and os.path.realpath(src) != tgt:
                    logging.error(f"Source file {src} exists! Linking cannot be performed")
                    src = None
            else:
                logging.error(f"Target file {tgt} not found")
                tgt = None
            if src and tgt and src not in links:
                links[src] = tgt

    if not args.dry_run:
        for src in links:
            tgt = links[src]
            bdir = os.path.split(src)[0]
            if not os.path.isdir(bdir):
                logging.debug(f"{bdir} doesnt exists! mkdir'ing")
                os.makedirs(bdir)
            logging.info(f"Linking {src} --> {tgt}")
            if os.path.realpath(src) != tgt:
                os.symlink(tgt, src)
            else:
                logging.info("Links exists!")

def main():
    # dmap = dotie_map_loader("dotie_map.toml")
    # print(dmap)
    args = arguments()
    if not args: return

    if args.action == "install":
        install(args)

if __name__ == "__main__":
    main()
