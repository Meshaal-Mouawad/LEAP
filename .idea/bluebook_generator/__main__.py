"""Enable running the CLI via:

    python -m bluebook_generator --help

Useful when the `bluebook` console script isn't on PATH yet.
"""

from .cli import main


if __name__ == "__main__":  # pragma: no cover
    main()
