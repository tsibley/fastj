"""
FASTJ: Structured metadata for your FASTA sequences.
"""

import json
import re
from typing import Generator, NamedTuple, TextIO, Tuple
from .__version__ import __version__


FastjRecord = NamedTuple(
    "FastjRecord", [
        ("id",       str),
        ("metadata", dict),
        ("sequence", str)])


def parse(title: str, sequence: str) -> FastjRecord:
    """
    Parse a *title* and *sequence* string into a :class:`.FastjRecord`.

    The leading ``>`` of a FASTA definition line should not be included in
    *title*.
    """
    try:
        id, description = re.split(r"\s+", title, maxsplit = 1)
    except ValueError:
        id, description = title, ""

    # Special-case ">{" input which elides the empty id.  We don't produce this
    # variant, but subscribe to the maxim of being "liberal in what you accept
    # and strict in what you emit."
    if id.startswith("{"):
        id, description = "", id + description

    description = description.strip()

    if description:
        metadata = json.loads(description)
    else:
        metadata = None

    return FastjRecord(id, metadata, sequence)


def format(record: Tuple[str, dict, str]) -> str:
    """
    Format a :class:`.FastjRecord`, or any (id: str, metadata: dict, sequence:
    str) tuple into a FASTJ record string suitable for interchange.

    At least one field of the tuple must have a value.
    """
    id, metadata, sequence = record

    if id:
        id = id.strip()
        assert " "  not in id
        assert "\t" not in id

    if sequence:
        sequence = sequence.strip()

    if metadata:
        metadata = \
            json.dumps(
                metadata,
                sort_keys  = True,
                separators = (',', ':'))

    assert id or sequence or metadata

    # There are other ways to do this of course, perhaps more traditional ones
    # like string concatentation, but I like this enumeration of cases because
    # it concisely and clearly shows what the function can return.
    field_presence = tuple(map(bool, (id, metadata, sequence)))

    case = {
        (True, True, True):   ">{id} {metadata}\n{sequence}",
        (True, True, False):  ">{id} {metadata}",
        (True, False, True):  ">{id}\n{sequence}",
        (True, False, False): ">{id}",
        (False, True, True):  "> {metadata}\n{sequence}",
        (False, True, False): "> {metadata}",
        (False, False, True): ">\n{sequence}",
    }

    return case[field_presence].format_map(locals())


def read(handle: TextIO) -> Generator[FastjRecord, None, None]:
    """
    Iterate over FASTJ records from a handle.

    Each record in the stream is returned as a :class:`.FastjRecord` tuple (id,
    metadata, sequence).  This is a named tuple, so you may also use the id,
    metadata, and sequence attributes to access data.  Metadata is a dict of
    the decoded JSON metadata from the record description.

    >>> with open("example.fastj") as handle:
    ...     for record in fastj.read(handle):
    ...         print(record)
    ...
    FastjRecord(id='sequenceA', metadata={'date': '2017-05-04', 'virus': 'flu'}, sequence='ATCG…')
    FastjRecord(id='sequenceB', metadata={'date': '2017-05-13', 'virus': 'flu'}, sequence='CGAT…')
    """

    for title, sequence in _read_fasta(handle):
        yield parse(title, sequence)


def _read_fasta(handle: TextIO) -> Generator[Tuple[str, str], None, None]:
    """
    A copy of Bio.SeqIO.FastaIO.SimpleFastaParser from BioPython.

    I wouldn't write it this way, but I assume the routine was long-ago
    optimized by BioPython devs.  I don't want to redo the work, but also
    don't want to dep on all of BioPython.  Hence, it is copied verbatim, as
    of 08ff145.
    """

    # Skip any text before the first record (e.g. blank lines, comments)
    while True:
        line = handle.readline()
        if line == "":
            return  # Premature end of file, or just empty?
        if line[0] == ">":
            break

    while True:
        if line[0] != ">":
            raise ValueError(
                "Records in Fasta files should start with '>' character")
        title = line[1:].rstrip()
        lines = []
        line = handle.readline()
        while True:
            if not line:
                break
            if line[0] == ">":
                break
            lines.append(line.rstrip())
            line = handle.readline()

        # Remove trailing whitespace, and any internal spaces
        # (and any embedded \r which are possible in mangled files
        # when not opened in universal read lines mode)
        yield title, "".join(lines).replace(" ", "").replace("\r", "")

        if not line:
            return  # StopIteration

    assert False, "Should not reach this line"
