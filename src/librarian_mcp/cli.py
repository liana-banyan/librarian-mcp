"""CLI entry point for `librarian-mcp` console script."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    """Import JSONL measurements or run the MCP server on stdio."""
    parser = argparse.ArgumentParser(prog="librarian-mcp")
    parser.add_argument(
        "--import",
        dest="import_path",
        metavar="FILE",
        help="Bulk-import benchmark measurements from a UTF-8 JSONL file",
    )
    args = parser.parse_args(argv)
    if args.import_path:
        path = Path(args.import_path)
        if not path.is_file():
            print(f"error: import file not found: {path}", file=sys.stderr)
            return 2
        from librarian_mcp.metrics import import_jsonl

        imported, skipped = import_jsonl(path)
        print(f"Imported {imported} records, skipped {skipped} malformed lines")
        return 0

    from librarian_mcp.server import main as serve

    serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
