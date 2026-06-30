#!/usr/bin/env python3
"""
Simple verification runner for the KPI Bluebook generator.
It executes the pipeline against the sample_project and prints progress lines.
Usage:
  python run_generation.py [<source_dir>]
Defaults to ./sample_project if no source_dir is provided.
"""

import sys
import pathlib

from bluebook_generator.main import generate_bluebook


def main(argv: list[str]) -> int:
    root = pathlib.Path(__file__).parent.resolve()
    source = (
        pathlib.Path(argv[1]).resolve()
        if len(argv) > 1
        else (root / "sample_project").resolve()
    )
    for msg in generate_bluebook(str(source)):
        print(msg)
    # success exit - errors are printed by the generator and pipeline continues
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
