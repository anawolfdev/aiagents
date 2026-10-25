"""
meshharmes.cli — punto de entrada del arnés: `python -m meshharmes status`.

Lee el backlog y dice en qué estado está. No escribe nada ni ejecuta la
fábrica: `harness` es el único dueño de `featureslist.json`.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from meshharmes import __version__
from meshharmes.backlog import BacklogError, read_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="meshharmes",
        description="MeshHarmes — estado del arnés y del backlog.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)
    status = sub.add_parser("status", help="Resume el backlog y dice qué toca.")
    status.add_argument(
        "--backlog",
        type=Path,
        default=None,
        help="Ruta al featureslist.json (por defecto, el del repositorio).",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "status":
        try:
            print(read_summary(args.backlog).render())
        except BacklogError as exc:
            print(f"meshharmes: {exc}", file=sys.stderr)
            return 1
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
