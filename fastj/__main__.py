"""
CLI and executable-module entrypoint.
"""

from sys import argv, exit
from . import cli

# Entry point for setuptools-installed script.
def main():
    return cli.run( argv[1:] )

# Run when called as `python -m fastj`.
if __name__ == "__main__":
    exit( main() )
