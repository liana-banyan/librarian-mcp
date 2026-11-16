'''CLI entry point for `librarian-mcp` console script.

Thin wrapper — delegates to the FastMCP server, but now also supports a bulk
JSONL import mode via the ``--import`` flag.
'''  # noqa: D401

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from librarian_mcp.metrics import record_measurement


def _validate_record(record: Dict[str, Any]) -> None:
    """Validate a measurement record.

    The expected schema (derived from the existing ``record_measurement``
    implementation) includes the following required fields:

    * ``model`` – ``str``
    * ``prompt_tokens`` – non‑negative ``int``
    * ``completion_tokens`` – non‑negative ``int``
    * ``total_tokens`` – non‑negative ``int``
    * ``cost`` – non‑negative ``float`` (or ``int``)
    * ``latency`` – non‑negative ``float`` (or ``int``)
    * ``correct`` – ``bool``

    An optional ``timestamp`` field may be present; if it is, we accept any
    JSON‑serialisable value (the downstream storage layer will handle it).

    Raises:
        ValueError: If any required field is missing or has an invalid type/value.
    """
    required_str_fields = ["model"]
    required_int_fields = ["prompt_tokens", "completion_tokens", "total_tokens"]
    required_float_fields = ["cost", "latency"]
    required_bool_fields = ["correct"]

    for field in required_str_fields:
        if field not in record:
            raise ValueError(f"missing required field '{field}'")
        if not isinstance(record[field], str):
            raise ValueError(f"field '{field}' must be a string")

    for field in required_int_fields:
        if field not in record:
            raise ValueError(f"missing required field '{field}'")
        if not isinstance(record[field], int) or record[field] < 0:
            raise ValueError(f"field '{field}' must be a non‑negative integer")

    for field in required_float_fields:
        if field not in record:
            raise ValueError(f"missing required field '{field}'")
        if not isinstance(record[field], (int, float)) or record[field] < 0:
            raise ValueError(f"field '{field}' must be a non‑negative number")

    for field in required_bool_fields:
        if field not in record:
            raise ValueError(f"missing required field '{field}'")
        if not isinstance(record[field], bool):
            raise ValueError(f"field '{field}' must be a boolean")

    # ``timestamp`` is optional – no strict validation needed here.


def import_jsonl(file_path: str) -> None:
    """Import measurements from a JSONL file.

    Args:
        file_path: Path to the JSONL file to import.
    """
    imported = 0
    skipped = 0
    path = Path(file_path)
    if not path.is_file():
        print(f"Error: file '{file_path}' does not exist or is not a regular file", file=sys.stderr)
        sys.exit(1)

    with path.open("r", encoding="utf-8") as f:
        for lineno, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue  # ignore blank lines
            try:
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("record is not a JSON object")
                _validate_record(record)
                # Preserve an existing timestamp if present; otherwise let
                # ``record_measurement`` generate one.
                record_measurement(**record)
                imported += 1
            except (json.JSONDecodeError, ValueError) as exc:
                print(f"Line {lineno}: malformed record – {exc}", file=sys.stderr)
                skipped += 1

    print(f"Imported {imported} records, skipped {skipped} malformed records.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="librarian-mcp", description="Librarian MCP server and utilities")
    parser.add_argument(
        "--import",
        dest="import_path",
        metavar="FILE",
        help="Import measurements from a UTF‑8 JSONL file and exit",
    )
    return parser


def main() -> None:
    """Entry point for the ``librarian-mcp`` console script.

    * Without arguments – starts the FastMCP server (original behaviour).
    * With ``--import FILE`` – processes the file and exits.
    """
    parser = _build_parser()
    args, unknown = parser.parse_known_args()

    if args.import_path:
        # Import mode – ignore any unknown arguments (they belong to the server).
        import_jsonl(args.import_path)
        return

    # Default behaviour – start the server.
    from librarian_mcp.server import main as serve
    serve()


if __name__ == "__main__":
    main()
