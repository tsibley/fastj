"""
CLI and executable-module entrypoint.
"""

import os
from sys import argv, exit, stdout
from . import cli

# Entry point for setuptools-installed script.
def main():
    try:
        return cli.run( argv[1:] )

    except BrokenPipeError:
        # From https://docs.python.org/3/library/signal.html#note-on-sigpipe:
        #
        #    Python flushes standard streams on exit.  Redirect remaining output
        #    to /dev/null to avoid another BrokenPipeError at shutdown.
        #
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, stdout.fileno())

    except KeyboardInterrupt:
        # Ignore this, but print a newline to leave cleaner console output.
        print()

# Run when called as `python -m fastj`.
if __name__ == "__main__":
    exit( main() )
