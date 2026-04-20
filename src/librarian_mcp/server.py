"""
Librarian MCP Server — v0.1.0 (April 20, 2026)

Exposes two tools to any MCP-capable client (Claude Code, Cursor, Continue, Zed, ...):

  1. librarian_context    — loads canonical memory packet for the current project
  2. prose_provenance     — drift detection between two versions of any document

Status:
  * librarian_context is live with basic file-discovery mode. Full R9 memory-packet
    architecture (priority-ordered, per-query re-ranked) ships in v0.2.0.
  * prose_provenance is live with deterministic checks (Keystones, canonical numbers,
    structure delta). Opus-grader semantic layer requires an Anthropic API key.

Runtime:
  Uses the FastMCP high-level API from the MCP Python SDK (v1.6+).
  Run: `python -m librarian_mcp` or `librarian-mcp serve`
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Annotated, Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "librarian-mcp",
    instructions=(
        "Pre-curated canonical memory + prose/code provenance checking. "
        "Two tools: librarian_context (memory packet) and prose_provenance (drift detection). "
        "v0.1.0"
    ),
)


# ─── TOOL 1: LIBRARIAN CONTEXT ────────────────────────────────────────────────


@mcp.tool()
def librarian_context(
    project_root: Annotated[str, "Absolute path to the project root directory"],
    query: Annotated[Optional[str], "Optional query for per-query re-ranking (v0.2.0)"] = None,
    max_tokens: Annotated[int, "Maximum token budget for the memory packet"] = 8000,
) -> dict:
    """Load the canonical memory packet for a project.

    Scans the project root for canonical source files (canonical_values.yaml,
    CANONICAL.md, .cursor/rules/*.mdc, .canonical/values.yaml) and assembles
    them into a single curated markdown packet sized to the client's token budget.

    Returns a dict with: packet (markdown), sources (file paths), tokens_estimated,
    version, and status notes.
    """
    root = Path(project_root)
    if not root.is_dir():
        return {"error": f"Project root not found: {project_root}"}

    sources: list[str] = []
    chunks: list[str] = []

    candidates = [
        "canonical_values.yaml",
        "CANONICAL.md",
        "canonical_values.json",
        ".canonical/values.yaml",
        ".canonical/values.json",
    ]

    # Also scan .cursor/rules/ for any .mdc files
    rules_dir = root / ".cursor" / "rules"
    if rules_dir.is_dir():
        for mdc in sorted(rules_dir.glob("*.mdc")):
            candidates.append(str(mdc.relative_to(root)))

    for candidate in candidates:
        p = root / candidate
        if p.exists() and p.is_file():
            try:
                text = p.read_text(encoding="utf-8")
                sources.append(str(p))
                chunks.append(f"## {p.name}\n\n{text}")
            except (OSError, UnicodeDecodeError):
                continue

    packet = "\n\n---\n\n".join(chunks) if chunks else (
        "_No canonical source files found. "
        "Create `CANONICAL.md` or `canonical_values.yaml` at your project root._"
    )

    # Rough token estimate: ~4 chars per token
    truncated = packet[: max_tokens * 4]
    tokens_est = min(len(packet) // 4, max_tokens)

    return {
        "packet": truncated,
        "sources": sources,
        "tokens_estimated": tokens_est,
        "version": "v0.1.0",
        "note": "Full R9 memory-packet architecture (priority-ordered, per-query re-ranked) ships in v0.2.0.",
    }


# ─── TOOL 2: PROSE PROVENANCE ─────────────────────────────────────────────────

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
    """Extract markdown section headers from text."""
    return [line.strip() for line in text.splitlines() if line.strip().startswith("#")]


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
    keystones: Annotated[Optional[str], "JSON array of keystone phrases to check (voice anchors that must be preserved)"] = None,
    canonical_numbers: Annotated[Optional[str], "JSON array of canonical numbers/values to verify"] = None,
) -> dict:
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

    # Parse optional JSON args
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

    # Check keystones
    ks_missing, ks_preserved = _find_missing_phrases(canonical_text, candidate_text, ks_phrases)
    drift_score += len(ks_missing) * 3

    # Check canonical numbers
    cn_missing, cn_preserved = _find_missing_phrases(canonical_text, candidate_text, cn_values)
    drift_score += len(cn_missing) * 2

    # Section header delta
    canon_sections = _extract_sections(canonical_text)
    cand_sections = _extract_sections(candidate_text)
    sections_added = [s for s in cand_sections if s not in canon_sections]
    sections_removed = [s for s in canon_sections if s not in cand_sections]
    drift_score += len(sections_removed) * 2 + len(sections_added)

    # Paragraph count delta
    canon_paras = _count_paragraphs(canonical_text)
    cand_paras = _count_paragraphs(candidate_text)
    para_delta = cand_paras - canon_paras
    if abs(para_delta) > 5:
        drift_score += abs(para_delta) // 3

    # Character-length ratio (catch major expansions/contractions)
    len_ratio = len(candidate_text) / max(len(canonical_text), 1)
    if len_ratio < 0.5 or len_ratio > 2.0:
        drift_score += 5

    report = {
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
        "version": "v0.1.0",
        "note": "Opus-grader semantic layer available in v0.2.0 with Anthropic API key.",
    }

    return report


# ─── CLI ENTRY POINT ──────────────────────────────────────────────────────────

def main():
    """Run the Librarian MCP server on stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
