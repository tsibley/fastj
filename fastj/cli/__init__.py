"""
usage: fastj from fasta [--fields <field> ...] [--] [<file.fasta> ...]
       fastj from fasta [--metadata <file.tsv>] [<file.fasta> ...]
       fastj from json [<file.json> ...]
       fastj from ndjson [<file.json> ...]

       fastj to fasta [--fields <field> ...] [--] [<file.fastj> ...]
       fastj to json [<file.fastj> ...]
       fastj to ndjson [<file.fastj> ...]

       fastj --help
       fastj --version

A utility for reading and writing FASTJ files to and from FASTA and JSON.
See <https://github.com/tsibley/fastj#readme> for more information.

Written by Thomas Sibley <https://tsibley.net>.
"""

import argparse
import fastj
import json
import re
from pathlib import Path
from textwrap import dedent
from typing import List

def run(args: List[str]) -> int:
    doc_paragraphs = __doc__.strip("\n").split("\n\n")

    help_parser = argparse.ArgumentParser(
        "fastj",
        usage           = re.sub(r"^usage: ", "", doc_paragraphs[0]),
        description     = "\n\n".join(doc_paragraphs[1:-1]),
        epilog          = doc_paragraphs[-1],
        formatter_class = argparse.RawDescriptionHelpFormatter,
        add_help        = False)

    # Manual argument handling mixed with automatic, because argparse's
    # subparser behaviour makes the top-level behaviour I want very hard to
    # accomplish without bending over backwards.  What's below is much simpler.
    command = " ".join(args[:2])
    args    = args[2:]

    if command in {"to fasta", "to json"}:
        # XXX TODO: use stdin if no args
        # XXX TODO: parse args for --fields, etc
        paths = args

        first = True
        for path in map(Path, paths):
            with path.open(encoding = "utf-8") as file:
                for record in fastj.read(file):
                    if first:
                        print("[", end = "")
                        first = False
                    else:
                        print("\n,", end = "")

                    print(
                        json.dumps(
                            record._asdict(),
                            sort_keys  = True,
                            separators = (',', ':')), end = "")
        print("]")

    elif command in {"from fasta", "from json"}:
        # XXX TODO
        ...

    elif command in {"--help", "-h"}:
        help_parser.print_help()

    elif command in {"--version", "-v"}:
        print("fastj", fastj.__version__)

    else:
        help_parser.print_help()
        return 1

    return 0
