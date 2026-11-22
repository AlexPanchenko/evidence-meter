"""The `evidence-meter` command (`python -m evidence_meter`).

Commands arrive with the first features; for now it only shows help.
"""

import argparse

from evidence_meter import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evidence-meter",
        description="Collect, compute, guard and report team-level engineering metrics.",
    )
    parser.add_argument("--version", action="version", version=f"evidence-meter {__version__}")
    parser.add_subparsers(dest="command", title="commands")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
    return 0
