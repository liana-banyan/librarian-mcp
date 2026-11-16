'''librarian_mcp.server

Provides the public API for the MCP server utilities, including the
`prose_provenance` function used by the CLI and the hosted endpoint.
'''  # noqa: D401

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List


def _load_file(path: str) -> str:
    """Read a text file and return its content.

    Returns an empty string on I/O error and lets the caller decide how to
    handle the situation.
    """
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return ""


def _exact_number_regex(num: str) -> re.Pattern:
    """Return a compiled regex that matches *exactly* ``num``.

    The pattern ensures the match is not part of a larger numeric token. It
    disallows digits, commas, periods, or sign characters immediately before
    or after the number.
    """
    escaped = re.escape(num)
    # Negative look‑behind / look‑ahead for characters that could make the
    # match part of a larger number.
    pattern = rf"(?<![\d.,]){escaped}(?![\d.,])"
    return re.compile(pattern)


def _find_missing_phrases(
    canonical: str, candidate: str, phrases: List[str]
) -> List[str]:
    """Return the subset of ``phrases`` that are *not* present in ``candidate``.

    The original implementation performed a simple ``phrase in candidate``
    check. This helper retains that behaviour for generic keystone phrases.
    """
    missing: List[str] = []
    for phrase in phrases:
        if phrase not in candidate:
            missing.append(phrase)
    return missing


def _find_missing_numbers(
    canonical: str, candidate: str, numbers: List[str]
) -> List[str]:
    """Return numbers from ``numbers`` that are not found as *exact* matches.

    ``numbers`` are expected to be the literal strings extracted from the
    canonical document (e.g. ``"2,267"`` or ``"83.3%"``).  A number is considered
    present only when it matches the compiled exact‑value regex.
    """
    missing: List[str] = []
    for num in numbers:
        regex = _exact_number_regex(num)
        if not regex.search(candidate):
            missing.append(num)
    return missing


def prose_provenance(
    *,
    canonical_path: str,
    candidate_path: str,
    keystones: str | None = None,
    canonical_numbers: str | None = None,
) -> Dict[str, Any]:
    """Detect drift between a *canonical* markdown file and a *candidate* file.

    The function returns a dictionary with the following keys:

    * ``verdict`` – ``"clean"`` if no drift is detected, otherwise ``"drift"``.
    * ``drift_score`` – a simple integer count of missing keystones and numbers.
    * ``keystones_missing`` – list of missing keystone phrases (if any).
    * ``numbers_missing`` – list of missing canonical numbers (if any).
    * ``error`` – present when either input file cannot be read.
    """
    # ---------------------------------------------------------------------
    # Load files
    # ---------------------------------------------------------------------
    canonical_text = _load_file(canonical_path)
    candidate_text = _load_file(candidate_path)

    if not canonical_text:
        return {"error": f"canonical file not found or unreadable: {canonical_path}"}
    if not candidate_text:
        return {"error": f"candidate file not found or unreadable: {candidate_path}"}

    # ---------------------------------------------------------------------
    # Parse optional JSON arguments
    # ---------------------------------------------------------------------
    keystone_list: List[str] = []
    if keystones:
        try:
            keystone_list = json.loads(keystones)
        except json.JSONDecodeError:
            return {"error": "keystones argument is not valid JSON"}

    number_list: List[str] = []
    if canonical_numbers:
        try:
            number_list = json.loads(canonical_numbers)
        except json.JSONDecodeError:
            return {"error": "canonical_numbers argument is not valid JSON"}

    # ---------------------------------------------------------------------
    # Detect missing keystones and numbers
    # ---------------------------------------------------------------------
    keystones_missing = _find_missing_phrases(canonical_text, candidate_text, keystone_list)
    numbers_missing = _find_missing_numbers(canonical_text, candidate_text, number_list)

    drift_score = len(keystones_missing) + len(numbers_missing)
    verdict = "clean" if drift_score == 0 else "drift"

    return {
        "verdict": verdict,
        "drift_score": drift_score,
        "keystones_missing": keystones_missing,
        "numbers_missing": numbers_missing,
    }
