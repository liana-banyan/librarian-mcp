"""
Librarian MCP Server — v0.2.0 (April 21, 2026)

Five tools exposed via MCP to any capable client:

  1. librarian_context    — intent-aware canonical memory packet (v0.2.0)
  2. prose_provenance     — deterministic drift detection between document versions
  3. record_measurement   — log benchmark measurement to local JSONL
  4. metrics_summary      — per-vendor / per-model aggregation of recorded measurements
  5. opt_in_share         — toggle anonymous sharing flag for metrics

Runtime:
  Uses the FastMCP high-level API from the MCP Python SDK (v1.6+).
  Run: `python -m librarian_mcp` or `librarian-mcp`
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Annotated, Any, Optional

from mcp.server.fastmcp import FastMCP

from librarian_mcp.context import build_packet, log_context_query
from librarian_mcp.metrics import opt_in_share as _opt_in_share
from librarian_mcp.metrics import record_measurement as _record_measurement
from librarian_mcp.metrics import summary as _metrics_summary

mcp = FastMCP(
    "librarian-mcp",
    instructions=(
        "Pre-curated canonical memory + prose/code provenance checking + benchmark metrics. "
        "Five tools: librarian_context (intent-aware memory), prose_provenance (drift detection), "
        "record_measurement / metrics_summary / opt_in_share (benchmark tracking). "
        "v0.2.0"
    ),
)


# ─── TOOL 1: LIBRARIAN CONTEXT (v0.2.0) ─────────────────────────────────────


@mcp.tool()
def librarian_context(
    intent: Annotated[
        str,
        'Intent string or JSON list. Options: "" (base only), "canonical", '
        '"outreach", "architecture", "founder_voice", "benchmark", "operational". '
        'Pass a JSON array for union: \'["benchmark", "founder_voice"]\'',
    ] = "",
    max_tokens: Annotated[int, "Maximum token budget for the memory packet (default 16000)"] = 16_000,
) -> dict[str, Any]:
    """Load the canonical memory packet for a specific intent.

    Returns a curated markdown packet assembled from the preload directory,
    scoped to the requested intent. Supports single intent strings and
    JSON-encoded lists for union queries. Enforces token budget with
    priority-based truncation.

    Returns: packet (markdown), sections_included (file paths), token_count,
    source_version (git SHA), truncation_note (if any files were removed).
    """
    parsed_intent: str | list[str] = intent
    if intent.startswith("["):
        try:
            parsed_intent = json.loads(intent)
        except json.JSONDecodeError:
            pass

    result = build_packet(intent=parsed_intent, max_tokens=max_tokens)
    log_context_query(parsed_intent, result["token_count"])
    return result


# ─── TOOL 2: PROSE PROVENANCE ────────────────────────────────────────────────


def _load_text(path: str) -> str | None:
    """Safely load text from a file path."""
    p = Path(path)
    if not p.exists():
        return None
    try:
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _extract_sections(text: str) -> list[str]:
    """Extract section headers, excluding top-level Markdown fenced code blocks."""
    sections: list[str] = []
    fence = ""
    for line in text.splitlines():
        if fence:
            # A closer uses the same character, at least the opening length,
            # at most three leading spaces, and no trailing non-whitespace.
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}[ \t]*", line):
                fence = ""
            continue

        opening = re.match(r" {0,3}(`{3,}|~{3,})(.*)$", line)
        if opening:
            marker, info = opening.groups()
            # Backtick fence info strings cannot themselves contain backticks.
            if marker[0] == "~" or "`" not in info:
                fence = marker
                continue

        if line.strip().startswith("#"):
            sections.append(line.strip())
    return sections


def _find_missing_phrases(canonical: str, candidate: str, phrases: list[str]) -> tuple[list[str], list[str]]:
    """Check which phrases from a list are present/missing in the candidate."""
    missing = []
    preserved = []
    canonical_lower = canonical.lower()
    candidate_lower = candidate.lower()
    for phrase in phrases:
        pl = phrase.lower()
        if pl in canonical_lower and pl not in candidate_lower:
            missing.append(phrase)
        elif pl in canonical_lower:
            preserved.append(phrase)
    return missing, preserved


def _count_paragraphs(text: str) -> int:
    """Count non-empty paragraphs (separated by blank lines)."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return len(paragraphs)


def _verdict_from_score(score: int) -> str:
    if score == 0:
        return "clean"
    if score < 5:
        return "minor"
    if score < 15:
        return "significant"
    return "severe"


@mcp.tool()
def prose_provenance(
    canonical_path: Annotated[str, "Path to the canonical (original/golden) version of the document"],
    candidate_path: Annotated[str, "Path to the candidate (new/revised) version to check against canonical"],
    doc_type: Annotated[str, "Document type: letter | scaffold | proposal | tribute | generic"] = "generic",
    keystones: Annotated[
        Optional[str], "JSON array of keystone phrases to check (voice anchors that must be preserved)"
    ] = None,
    canonical_numbers: Annotated[Optional[str], "JSON array of canonical numbers/values to verify"] = None,
) -> dict[str, Any]:
    """Deterministic drift detection between two versions of any document.

    Checks for:
    - Keystone phrases (voice anchors) silently dropped from the candidate
    - Canonical numbers/values changed or removed
    - Section structure changes (headers added/removed)
    - Paragraph count delta (significant expansion or contraction)

    Returns a structured drift report with a severity verdict (clean/minor/significant/severe).
    """
    canonical_text = _load_text(canonical_path)
    if canonical_text is None:
        return {"error": f"Cannot read canonical file: {canonical_path}"}

    candidate_text = _load_text(candidate_path)
    if candidate_text is None:
        return {"error": f"Cannot read candidate file: {candidate_path}"}

    drift_score = 0

    ks_phrases: list[str] = []
    if keystones:
        try:
            ks_phrases = json.loads(keystones)
        except json.JSONDecodeError:
            ks_phrases = [k.strip() for k in keystones.split(",") if k.strip()]

    cn_values: list[str] = []
    if canonical_numbers:
        try:
            cn_values = json.loads(canonical_numbers)
        except json.JSONDecodeError:
            cn_values = [n.strip() for n in canonical_numbers.split(",") if n.strip()]

    ks_missing, ks_preserved = _find_missing_phrases(canonical_text, candidate_text, ks_phrases)
    drift_score += len(ks_missing) * 3

    cn_missing, cn_preserved = _find_missing_phrases(canonical_text, candidate_text, cn_values)
    drift_score += len(cn_missing) * 2

    canon_sections = _extract_sections(canonical_text)
    cand_sections = _extract_sections(candidate_text)
    sections_added = [s for s in cand_sections if s not in canon_sections]
    sections_removed = [s for s in canon_sections if s not in cand_sections]
    drift_score += len(sections_removed) * 2 + len(sections_added)

    canon_paras = _count_paragraphs(canonical_text)
    cand_paras = _count_paragraphs(candidate_text)
    para_delta = cand_paras - canon_paras
    if abs(para_delta) > 5:
        drift_score += abs(para_delta) // 3

    len_ratio = len(candidate_text) / max(len(canonical_text), 1)
    if len_ratio < 0.5 or len_ratio > 2.0:
        drift_score += 5

    return {
        "canonical_path": canonical_path,
        "candidate_path": candidate_path,
        "doc_type": doc_type,
        "drift_score": drift_score,
        "verdict": _verdict_from_score(drift_score),
        "keystones_missing": ks_missing,
        "keystones_preserved": ks_preserved,
        "canonical_numbers_missing": cn_missing,
        "canonical_numbers_preserved": cn_preserved,
        "sections_added": sections_added,
        "sections_removed": sections_removed,
        "paragraph_count_canonical": canon_paras,
        "paragraph_count_candidate": cand_paras,
        "paragraph_delta": para_delta,
        "length_ratio": round(len_ratio, 3),
        "version": "v0.2.0",
    }


# ─── TOOL 3: RECORD MEASUREMENT ─────────────────────────────────────────────


@mcp.tool()
def record_measurement(
    session_id: Annotated[str, "Session identifier for this benchmark run"],
    vendor: Annotated[str, "Vendor name: anthropic, google, openai, perplexity, etc."],
    model: Annotated[str, "Model identifier, e.g. claude-haiku-4-5-20251001"],
    condition: Annotated[str, "Test condition: HOT (with librarian) or COLD (without)"],
    question_id: Annotated[str, "Question identifier from the benchmark bank"],
    correct: Annotated[bool, "Whether the answer was graded correct"],
    input_tokens: Annotated[int, "Input tokens consumed"],
    output_tokens: Annotated[int, "Output tokens generated"],
    cost_usd: Annotated[float, "Cost in USD for this call"],
    latency_s: Annotated[float, "Latency in seconds for this call"],
) -> dict[str, Any]:
    """Record a single benchmark measurement to the local JSONL metrics file.

    Appends one line to ~/.librarian-mcp/metrics.jsonl. Used by benchmark
    harnesses (R10 cross-vendor, Eyewitness) to track accuracy and cost.
    """
    _record_measurement(
        session_id=session_id,
        vendor=vendor,
        model=model,
        condition=condition,
        question_id=question_id,
        correct=correct,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=cost_usd,
        latency_s=latency_s,
    )
    return {"status": "recorded", "session_id": session_id, "question_id": question_id}


# ─── TOOL 4: METRICS SUMMARY ────────────────────────────────────────────────


@mcp.tool()
def metrics_summary(
    since_timestamp: Annotated[
        Optional[str],
        "ISO timestamp to filter from (inclusive). Omit for all-time summary.",
    ] = None,
) -> dict[str, Any]:
    """Return per-vendor and per-model aggregation of all recorded measurements.

    Reads ~/.librarian-mcp/metrics.jsonl and computes accuracy, cost savings,
    and cache hit rate broken down by vendor and model.
    """
    return _metrics_summary(since_timestamp=since_timestamp)


# ─── TOOL 5: OPT-IN SHARE ───────────────────────────────────────────────────


@mcp.tool()
def opt_in_share(
    enabled: Annotated[bool, "True to enable anonymous sharing, False to disable"] = True,
) -> dict[str, Any]:
    """Toggle anonymous metrics sharing. Default is OFF.

    When enabled, summary data may be shared to a commons dashboard in a
    future release. The POST endpoint is not yet implemented (deferred to K425).
    """
    return _opt_in_share(enabled=enabled)


# ─── CLI ENTRY POINT ─────────────────────────────────────────────────────────


def main() -> None:
    """Run the Librarian MCP server on stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
