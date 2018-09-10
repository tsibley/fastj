"""
fastj: a command-line utility for reading and writing FASTJ files.
"""

import argparse
import fastj
from pathlib import Path
from typing import List

def run(args: List[str]) -> int:
    for r in fastj.read(Path(args[0]).open(encoding = "utf-8")):
        print(fastj.format(*r))
    return 0
