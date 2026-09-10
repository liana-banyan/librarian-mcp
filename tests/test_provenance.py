"""Tests for prose_provenance — drift detection (regression tests from v0.1.0)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from librarian_mcp.server import _extract_sections, prose_provenance


@pytest.mark.parametrize("fence", ["```", "~~~", "````", "   ```"])
def test_code_comment_change_is_not_section_drift(tmp_path: Path, fence: str) -> None:
    canonical = f"# Guide\n\n{fence}python\n# Old comment\nprint(1)\n{fence}\n\n## Usage\n"
    candidate = canonical.replace("# Old comment", "# New comment")
    canonical_path = tmp_path / "canonical.md"
    candidate_path = tmp_path / "candidate.md"
    canonical_path.write_text(canonical, encoding="utf-8")
    candidate_path.write_text(candidate, encoding="utf-8")

    result = prose_provenance(str(canonical_path), str(candidate_path))

    assert result["sections_removed"] == []
    assert result["sections_added"] == []
    assert result["drift_score"] == 0
    assert result["verdict"] == "clean"


@pytest.mark.parametrize(
    ("code_block", "expected"),
    [
        ("````md\n```\n# In code\n`````\n## After", ["## After"]),
        ("~~~\n```\n# In code\n~~~\n## After", ["## After"]),
        ("```\n``` not a closing fence\n# In code\n```\n## After", ["## After"]),
        ("```\n    ```\n# In code\n```\n## After", ["## After"]),
        ("```\n# In unclosed code", []),
        ("``` invalid`info\n## Not in code", ["## Not in code"]),
    ],
)
def test_section_extraction_respects_fence_boundaries(code_block: str, expected: list[str]) -> None:
    assert _extract_sections(code_block) == expected


class TestProseProvenance:
    def test_identical_files_clean(self, tmp_path: Path) -> None:
        content = "# Title\n\nSome canonical text with 83.3% creator keep.\n"
        (tmp_path / "canonical.md").write_text(content, encoding="utf-8")
        (tmp_path / "candidate.md").write_text(content, encoding="utf-8")

        result = prose_provenance(
            canonical_path=str(tmp_path / "canonical.md"),
            candidate_path=str(tmp_path / "candidate.md"),
        )
        assert result["verdict"] == "clean"
        assert result["drift_score"] == 0

    def test_missing_canonical_returns_error(self, tmp_path: Path) -> None:
        (tmp_path / "candidate.md").write_text("text", encoding="utf-8")
        result = prose_provenance(
            canonical_path=str(tmp_path / "nonexistent.md"),
            candidate_path=str(tmp_path / "candidate.md"),
        )
        assert "error" in result

    def test_missing_candidate_returns_error(self, tmp_path: Path) -> None:
        (tmp_path / "canonical.md").write_text("text", encoding="utf-8")
        result = prose_provenance(
            canonical_path=str(tmp_path / "canonical.md"),
            candidate_path=str(tmp_path / "nonexistent.md"),
        )
        assert "error" in result

    def test_keystones_missing_detected(self, tmp_path: Path) -> None:
        canonical = "# Letter\n\nHelp each other help ourselves.\n\nCardboard boots.\n"
        candidate = "# Letter\n\nGeneric placeholder text.\n\nDifferent text.\n"
        (tmp_path / "canonical.md").write_text(canonical, encoding="utf-8")
        (tmp_path / "candidate.md").write_text(candidate, encoding="utf-8")

        result = prose_provenance(
            canonical_path=str(tmp_path / "canonical.md"),
            candidate_path=str(tmp_path / "candidate.md"),
            keystones=json.dumps(["Help each other help ourselves", "Cardboard boots"]),
        )
        assert "Help each other help ourselves" in result["keystones_missing"]
        assert "Cardboard boots" in result["keystones_missing"]
        assert result["drift_score"] > 0

    def test_canonical_numbers_missing_detected(self, tmp_path: Path) -> None:
        canonical = "# Stats\n\nWe have 2,267 innovations and 83.3% creator keep.\n"
        candidate = "# Stats\n\nWe have many innovations and fair creator keep.\n"
        (tmp_path / "canonical.md").write_text(canonical, encoding="utf-8")
        (tmp_path / "candidate.md").write_text(candidate, encoding="utf-8")

        result = prose_provenance(
            canonical_path=str(tmp_path / "canonical.md"),
            candidate_path=str(tmp_path / "candidate.md"),
            canonical_numbers=json.dumps(["2,267", "83.3%"]),
        )
        assert "2,267" in result["canonical_numbers_missing"]
        assert "83.3%" in result["canonical_numbers_missing"]

    def test_section_changes_detected(self, tmp_path: Path) -> None:
        canonical = "# Title\n\n## Section A\n\nText\n\n## Section B\n\nText\n"
        candidate = "# Title\n\n## Section A\n\nText\n\n## Section C\n\nText\n"
        (tmp_path / "canonical.md").write_text(canonical, encoding="utf-8")
        (tmp_path / "candidate.md").write_text(candidate, encoding="utf-8")

        result = prose_provenance(
            canonical_path=str(tmp_path / "canonical.md"),
            candidate_path=str(tmp_path / "candidate.md"),
        )
        assert "## Section B" in result["sections_removed"]
        assert "## Section C" in result["sections_added"]

    def test_severe_length_change(self, tmp_path: Path) -> None:
        canonical = "# Short\n\nBrief.\n"
        candidate = "# Long\n\n" + ("Extended content paragraph.\n\n" * 50)
        (tmp_path / "canonical.md").write_text(canonical, encoding="utf-8")
        (tmp_path / "candidate.md").write_text(candidate, encoding="utf-8")

        result = prose_provenance(
            canonical_path=str(tmp_path / "canonical.md"),
            candidate_path=str(tmp_path / "candidate.md"),
        )
        assert result["length_ratio"] > 2.0
        assert result["drift_score"] >= 5

    def test_version_is_v020(self, tmp_path: Path) -> None:
        content = "text"
        (tmp_path / "a.md").write_text(content, encoding="utf-8")
        (tmp_path / "b.md").write_text(content, encoding="utf-8")
        result = prose_provenance(
            canonical_path=str(tmp_path / "a.md"),
            candidate_path=str(tmp_path / "b.md"),
        )
        assert result["version"] == "v0.2.0"
