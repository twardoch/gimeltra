#!/usr/bin/env python3
""" """

import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

import gimeltra

PROG = "gimeltrapy"


def cli():
    parser = ArgumentParser(prog=f"{PROG}")
    parser.add_argument("-t", "--text", metavar="TEXT", dest="text")
    parser.add_argument("-i", "--input", metavar="FILE", dest="in_file")
    parser.add_argument(
        "-s",
        "--script",
        metavar="SCRIPT",
        dest="in_script",
        default=None,
        help="Input script as ISO 15924 code",
    )
    parser.add_argument(
        "-o",
        "--to-script",
        metavar="SCRIPT",
        dest="out_script",
        default="Latn",
        help="Output script as ISO 15924 code",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        dest="stats",
        help="""List supported scripts""",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=1,
        help="-v show progress, -vv show debug",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"{PROG} {gimeltra.__version__}",
        help="show version and exit",
    )
    return parser


def main(*args, **kwargs):
    parser = cli(*args, **kwargs)
    args = parser.parse_args()
    args.verbose = 40 - (10 * args.verbose) if args.verbose > 0 else 0
    logging.basicConfig(
        level=args.verbose,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    opts = vars(args)
    logging.debug("Running with options:\n%s" % repr(opts))
    del opts["verbose"]
    if opts["in_file"]:
        with open(Path(opts["in_file"]), encoding="utf8") as f:
            text = f.read()
    elif opts["text"]:
        text = opts["text"]
    else:
        text = sys.stdin.read().rstrip()
    tr = gimeltra.gimeltra.Transliterator()
    if opts.get("stats", False):
        print(f"{len(tr.db.keys()) - 1} scripts: {' '.join(tr.db.keys())}")
    else:
        res = tr.tr(
            text,
            sc=opts["in_script"],
            to_sc=opts["out_script"],
        )
        print(res)


if __name__ == "__main__":
    main()
