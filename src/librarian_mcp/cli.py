"""CLI entry point for the ``librarian-mcp`` console script."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from librarian_mcp import metrics

_REQUIRED_FIELDS = {
    "session_id", "vendor", "model", "condition", "question_id",
    "correct", "input_tokens", "output_tokens", "cost_usd", "latency_s",
}


def _is_nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _is_nonnegative_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def _validate_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("record must be a JSON object")
    if set(record) != _REQUIRED_FIELDS:
        missing = sorted(_REQUIRED_FIELDS - set(record))
        extra = sorted(set(record) - _REQUIRED_FIELDS)
        details = []
        if missing:
            details.append(f"missing fields: {', '.join(missing)}")
        if extra:
            details.append(f"unknown fields: {', '.join(extra)}")
        raise ValueError("; ".join(details))
    for field in ("session_id", "vendor", "model", "condition", "question_id"):
        if not isinstance(record[field], str) or not record[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    if not isinstance(record["correct"], bool):
        raise ValueError("correct must be a boolean")
    for field in ("input_tokens", "output_tokens"):
        if not _is_nonnegative_int(record[field]):
            raise ValueError(f"{field} must be a non-negative integer")
    for field in ("cost_usd", "latency_s"):
        if not _is_nonnegative_number(record[field]):
            raise ValueError(f"{field} must be a finite non-negative number")
    return record


def _import_jsonl(path: Path) -> tuple[int, int]:
    """Import validated measurements and return ``(imported, skipped)``."""
    imported = 0
    skipped = 0
    try:
        lines = path.open(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Unable to read {path}: {exc}") from exc
    with lines:
        for line_number, raw_line in enumerate(lines, start=1):
            if not raw_line.strip():
                skipped += 1
                print(f"line {line_number}: skipped blank line", file=sys.stderr)
                continue
            try:
                record = _validate_record(json.loads(raw_line))
                metrics.record_measurement(**record)
            except (json.JSONDecodeError, ValueError, TypeError) as exc:
                skipped += 1
                print(f"line {line_number}: skipped malformed record ({exc})", file=sys.stderr)
                continue
            imported += 1
    return imported, skipped


def main(argv: Sequence[str] | None = None) -> None:
    """Import JSONL measurements or run the MCP server on stdio."""
    parser = argparse.ArgumentParser(prog="librarian-mcp")
    parser.add_argument("--import", dest="import_path", type=Path, help="import measurement records from a JSONL file")
    args = parser.parse_args(argv)
    if args.import_path is not None:
        imported, skipped = _import_jsonl(args.import_path)
        print(f"Imported {imported} records, skipped {skipped} malformed lines")
        return
    from librarian_mcp.server import main as serve
    serve()


if __name__ == "__main__":
    main()
