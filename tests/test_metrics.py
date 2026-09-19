"""Tests for librarian_mcp.metrics — recording, summary, opt-in share."""

from __future__ import annotations

import json
from pathlib import Path

from librarian_mcp import cli
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


class TestJsonlImport:
    def test_imports_valid_records_and_skips_malformed_lines(self, tmp_path: Path, tmp_metrics_dir: Path, capsys) -> None:
        source = tmp_path / "measurements.jsonl"
        source.write_text(
            json.dumps({
                "session_id": "s1", "vendor": "anthropic", "model": "haiku",
                "condition": "HOT", "question_id": "Q1", "correct": True,
                "input_tokens": 100, "output_tokens": 20, "cost_usd": 0.001, "latency_s": 1.2,
            }) + "\n" + '{"session_id": "incomplete"}\n' + "not json\n",
            encoding="utf-8",
        )

        cli.main(["--import", str(source)])

        captured = capsys.readouterr()
        assert captured.out == "Imported 1 records, skipped 2 malformed lines\n"
        assert "line 2:" in captured.err
        assert "line 3:" in captured.err
        assert summary()["total_calls"] == 1

    def test_rejects_boolean_token_counts(self, tmp_path: Path, tmp_metrics_dir: Path, capsys) -> None:
        source = tmp_path / "measurements.jsonl"
        source.write_text(
            json.dumps({
                "session_id": "s1", "vendor": "anthropic", "model": "haiku",
                "condition": "HOT", "question_id": "Q1", "correct": True,
                "input_tokens": True, "output_tokens": 20, "cost_usd": 0.001, "latency_s": 1.2,
            }) + "\n",
            encoding="utf-8",
        )

        cli.main(["--import", str(source)])

        captured = capsys.readouterr()
        assert captured.out == "Imported 0 records, skipped 1 malformed lines\n"
        assert "input_tokens must be a non-negative integer" in captured.err
        assert summary()["total_calls"] == 0
