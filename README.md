# FASTJ

Structured metadata for your FASTA sequences.


## Format

The FASTJ format is a convention for including structured sequence metadata
inside a FASTA file while remaining interchangeable with most software that
consumes FASTA.

In FASTJ, metadata is stored as a single-line JSON object in the _description_
field of the typical FASTA `>id description` definition line.  FASTA parsers
treat everything after the first whitespace in the definition line as the
_description_.  (Everything before, minus the `>` prefix, is the _id_.)

A simple example of FASTJ:

    >specimenA {"date":"2017-05-04", "virus":"flu"}
    ATCG…
    >specimenB {"date":"2017-05-13", "virus":"flu"}
    CGAT…

Missing descriptions should be treated as an empty JSON empty.  That is, the
following two FASTJ sequence records are equivalent:

    >seqA
    ATCG
    >seqA {}
    ATCG

That's all!


## Command

The command-line program `fastj` provides tools to __read__ and __write__ FASTJ
files and to otherwise work with them.


### fastj write

Writes FASTJ sequences to stdout from FASTA + metadata.

Input is from named files, if given with the input flag, otherwise stdin.

Output is always FASTJ written to stdout.

Examples:

#### `fastj write --fasta file.fasta --delimiter="|" --fields virus date id`

_file.fasta_

    >flu|2017-05-04|specimenA
    ATCG…
    >flu|2017-05-13|specimenB
    CGAT…

_output_

    >specimenA {"date":"2017-05-04", "virus":"flu"}
    ATCG…
    >specimenB {"date":"2017-05-13", "virus":"flu"}
    CGAT…


#### `fastj write --fasta file.fasta --metadata file.tsv`

_file.fasta_

    >specimenA
    ATCG…
    >specimenB
    CGAT…

_file.tsv_

    id,virus,date
    specimenA,flu,2017-05-04
    specimenB,flu,2017-05-13

_output_

    >specimenA {"date":"2017-05-04", "virus":"flu"}
    ATCG…
    >specimenB {"date":"2017-05-13", "virus":"flu"}
    CGAT…


#### `fastj write --json file.json`

_file.json_ (output from `fastj read`)

```json
[{ "id": "specimenA", "sequence": "ATCG…", "date": "2017-05-04", "virus": "flu" }
,{ "id": "specimenB", "sequence": "CGAT…", "date": "2017-05-13", "virus": "flu" }
]
```

_output_

    >specimenA {"date":"2017-05-04", "virus":"flu"}
    ATCG…
    >specimenB {"date":"2017-05-13", "virus":"flu"}
    CGAT…


### fastj read

Converts FASTJ sequences to another format.

Input is from the listed files, if any, otherwise stdin.

Output defaults to JSON.  Supported output formats are:

* `json`: The top-level value will always be an array, even if there is only
  one sequence record.

* `fasta`: Plain FASTA with delimited sequence ids constructed from the FASTJ
  fields.

Examples:

_file.fastj_ for all examples

    >specimenA {"date":"2017-05-04", "virus":"flu"}
    ATCG…
    >specimenB {"date":"2017-05-13", "virus":"flu"}
    CGAT…

#### `fastj read [file.fastj [file2.fastj […]]]`

```json
[{ "id": "specimenA", "sequence": "ATCG…", "date": "2017-05-04", "virus": "flu" }
,{ "id": "specimenB", "sequence": "CGAT…", "date": "2017-05-13", "virus": "flu" }
]
```

#### `fastj read --output=fasta --fields virus date id -- [file.fastj [file2.fastj […]]]`

    >flu|2017-05-04|specimenA
    ATCG…
    >flu|2017-05-13|specimenB
    CGAT…

#### `fastj read --output=fasta --delimiter=/ --fields virus date id -- [file.fastj [file2.fastj […]]]`

    >flu/2017-05-04/specimenA
    ATCG…
    >flu/2017-05-13/specimenB
    CGAT…


### fastj index

_Tentative._


### fastj search

_Tentative._
