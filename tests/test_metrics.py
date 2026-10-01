"""Tests for librarian_mcp.metrics — recording, summary, opt-in share."""

from __future__ import annotations

import json
from pathlib import Path

from librarian_mcp.cli import main as cli_main
from librarian_mcp.metrics import (
    opt_in_share,
    record_measurement,
    summary,
)


def _record_sample(vendor: str, model: str, condition: str, correct: bool, cost: float) -> None:
    """Helper to record a measurement with sensible defaults."""
    record_measurement(
        session_id="test-session",
        vendor=vendor,
        model=model,
        condition=condition,
        question_id=f"Q-{vendor}-{condition}",
        correct=correct,
        input_tokens=1000,
        output_tokens=200,
        cost_usd=cost,
        latency_s=1.5,
    )


class TestRecordMeasurement:
    def test_writes_jsonl_line(self, tmp_metrics_dir: Path) -> None:
        record_measurement(
            session_id="s1",
            vendor="anthropic",
            model="claude-haiku-4-5",
            condition="HOT",
            question_id="Q1",
            correct=True,
            input_tokens=1000,
            output_tokens=200,
            cost_usd=0.001,
            latency_s=1.2,
        )
        metrics_path = tmp_metrics_dir / "metrics.jsonl"
        assert metrics_path.exists()
        lines = metrics_path.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["vendor"] == "anthropic"
        assert record["correct"] is True
        assert record["session_id"] == "s1"

    def test_appends_multiple_records(self, tmp_metrics_dir: Path) -> None:
        _record_sample("anthropic", "haiku", "HOT", True, 0.001)
        _record_sample("google", "gemini-flash", "COLD", False, 0.0001)

        metrics_path = tmp_metrics_dir / "metrics.jsonl"
        lines = metrics_path.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2


class TestSummary:
    def test_empty_metrics(self, tmp_metrics_dir: Path) -> None:
        result = summary()
        assert result["total_calls"] == 0
        assert result["per_vendor"] == {}
        assert result["per_model"] == {}

    def test_per_vendor_breakdown(self, tmp_metrics_dir: Path) -> None:
        _record_sample("anthropic", "haiku", "HOT", True, 0.001)
        _record_sample("anthropic", "haiku", "HOT", True, 0.001)
        _record_sample("google", "gemini-flash", "HOT", False, 0.0001)

        result = summary()
        assert result["total_calls"] == 3
        assert "anthropic" in result["per_vendor"]
        assert "google" in result["per_vendor"]
        assert result["per_vendor"]["anthropic"]["calls"] == 2
        assert result["per_vendor"]["google"]["calls"] == 1

    def test_per_model_breakdown(self, tmp_metrics_dir: Path) -> None:
        _record_sample("anthropic", "haiku-4-5", "HOT", True, 0.001)
        _record_sample("anthropic", "opus-4-7", "HOT", True, 0.05)

        result = summary()
        assert "haiku-4-5" in result["per_model"]
        assert "opus-4-7" in result["per_model"]

    def test_hot_cold_accuracy(self, tmp_metrics_dir: Path) -> None:
        _record_sample("anthropic", "haiku", "HOT", True, 0.001)
        _record_sample("anthropic", "haiku", "HOT", True, 0.001)
        _record_sample("anthropic", "haiku", "HOT", False, 0.001)
        _record_sample("anthropic", "haiku", "COLD", False, 0.001)
        _record_sample("anthropic", "haiku", "COLD", False, 0.001)

        result = summary()
        vendor_stats = result["per_vendor"]["anthropic"]
        assert vendor_stats["hot_accuracy"] > 60  # 2/3 = 66.7%
        assert vendor_stats["cold_baseline_est"] == 0.0  # 0/2

    def test_since_timestamp_filter(self, tmp_metrics_dir: Path) -> None:
        _record_sample("anthropic", "haiku", "HOT", True, 0.001)

        result = summary(since_timestamp="2099-01-01T00:00:00Z")
        assert result["total_calls"] == 0

        result = summary(since_timestamp="2020-01-01T00:00:00Z")
        assert result["total_calls"] == 1


class TestOptInShare:
    def test_enable_disable_roundtrip(self, tmp_metrics_dir: Path) -> None:
        result = opt_in_share(enabled=True)
        assert result["status"] == "enabled"

        s = summary()
        assert s["opt_in_share"] is True

        result = opt_in_share(enabled=False)
        assert result["status"] == "disabled"

        s = summary()
        assert s["opt_in_share"] is False

    def test_default_is_off(self, tmp_metrics_dir: Path) -> None:
        s = summary()
        assert s["opt_in_share"] is False


class TestImportJsonlCli:
    def test_cli_import_skips_malformed_and_aggregates(self, tmp_metrics_dir: Path, tmp_path: Path, capsys) -> None:
        valid = {
            "session_id": "s-import",
            "vendor": "anthropic",
            "model": "haiku",
            "condition": "HOT",
            "question_id": "Q-import",
            "correct": True,
            "input_tokens": 10,
            "output_tokens": 2,
            "cost_usd": 0.01,
            "latency_s": 1.25,
        }
        source = tmp_path / "test_data.jsonl"
        source.write_text(
            json.dumps(valid)
            + "\nnot-json\n"
            + json.dumps({**valid, "input_tokens": True})
            + "\n"
            + json.dumps({**valid, "question_id": "Q-import-2", "correct": False})
            + "\n",
            encoding="utf-8",
        )
        rc = cli_main(["--import", str(source)])
        assert rc == 0
        out = capsys.readouterr()
        assert "Imported 2 records, skipped 2 malformed lines" in out.out
        assert "line 2" in out.err
        result = summary()
        assert result["total_calls"] == 2
        assert result["per_vendor"]["anthropic"]["calls"] == 2

    def test_cli_import_missing_file(self, tmp_metrics_dir: Path, tmp_path: Path) -> None:
        missing = tmp_path / "absent.jsonl"
        assert cli_main(["--import", str(missing)]) == 2
