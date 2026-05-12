from __future__ import annotations

import argparse
import json
import sys

from .simulator import build_demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Print an offline EvoMap agent-memory behavior demo."
    )
    parser.add_argument(
        "--format",
        choices=("text", "markdown", "json"),
        default="text",
        help="Output format.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    demo = build_demo()

    if args.format == "json":
        print(json.dumps(demo.to_dict(), ensure_ascii=False, indent=2))
        return 0

    if args.format == "markdown":
        print(demo.to_markdown())
        return 0

    print(demo.to_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
