"""Tests for librarian_mcp.metrics — recording, summary, opt-in share."""

from __future__ import annotations

import json
from pathlib import Path

from librarian_mcp.metrics import (
    import_measurements,
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


class TestImportMeasurements:
    def test_imports_valid_lines_and_reports_malformed_lines(self, tmp_path, tmp_metrics_dir, capsys):
        source = tmp_path / "results.jsonl"
        valid_hot = {
            "session_id": "import-session",
            "vendor": "anthropic",
            "model": "claude-haiku-4-5",
            "condition": "HOT",
            "question_id": "Q1",
            "correct": True,
            "input_tokens": 1000,
            "output_tokens": 200,
            "cost_usd": 0.001,
            "latency_s": 1.2,
        }
        valid_cold = {**valid_hot, "condition": "COLD", "correct": False, "question_id": "Q2"}
        invalid_boolean = {**valid_hot, "correct": "yes"}

        source.write_text(
            "\n".join([
                json.dumps(valid_hot),
                "{oops",
                json.dumps(invalid_boolean),
                json.dumps(valid_cold),
            ]) + "\n",
            encoding="utf-8",
        )

        imported, skipped = import_measurements(source)
        assert (imported, skipped) == (2, 2)

        captured = capsys.readouterr()
        assert "Skipping malformed line 2" in captured.err
        assert "Skipping malformed line 3" in captured.err
        assert "Expecting property name enclosed in double quotes" in captured.err
        assert "correct must be a boolean" in captured.err

        stored = [
            json.loads(row)
            for row in (tmp_metrics_dir / "metrics.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        assert len(stored) == 2
        assert {row["condition"] for row in stored} == {"HOT", "COLD"}
        assert all(row["session_id"] == "import-session" for row in stored)

        aggregate = summary()
        assert aggregate["total_calls"] == 2
        assert aggregate["per_vendor"]["anthropic"]["calls"] == 2

    def test_rejects_invalid_values_and_missing_fields(self, tmp_path, tmp_metrics_dir, capsys):
        source = tmp_path / "results.jsonl"
        valid = {
            "session_id": "import-session",
            "vendor": "google",
            "model": "gemini-flash",
            "condition": "HOT",
            "question_id": "Q1",
            "correct": True,
            "input_tokens": 1000,
            "output_tokens": 200,
            "cost_usd": 0.001,
            "latency_s": 1.2,
        }
        negative_tokens = {**valid, "input_tokens": -1}
        missing_cost = {key: value for key, value in valid.items() if key != "cost_usd"}
        nonfinite_latency = {**valid, "latency_s": float("inf")}

        source.write_text(
            "\n".join([
                json.dumps(negative_tokens),
                json.dumps(missing_cost),
                json.dumps(nonfinite_latency),
            ]) + "\n",
            encoding="utf-8",
        )

        imported, skipped = import_measurements(source)
        assert (imported, skipped) == (0, 3)
        assert not (tmp_metrics_dir / "metrics.jsonl").exists()

        captured = capsys.readouterr()
        assert "input_tokens must be a nonnegative integer" in captured.err
        assert "missing fields: cost_usd" in captured.err
        assert "latency_s must be a finite nonnegative number" in captured.err

    def test_cli_import_prints_summary(self, tmp_path, tmp_metrics_dir, capsys, monkeypatch):
        source = tmp_path / "results.jsonl"
        valid = {
            "session_id": "cli-session",
            "vendor": "anthropic",
            "model": "claude-haiku-4-5",
            "condition": "HOT",
            "question_id": "Q1",
            "correct": True,
            "input_tokens": 1000,
            "output_tokens": 200,
            "cost_usd": 0.001,
            "latency_s": 1.2,
        }
        invalid = {**valid, "correct": "yes"}
        source.write_text(
            json.dumps(valid) + "\n" + json.dumps(invalid) + "\n",
            encoding="utf-8",
        )

        monkeypatch.setattr("sys.argv", ["librarian-mcp", "--import", str(source)])
        from librarian_mcp import cli

        cli.main()
        captured = capsys.readouterr()
        assert "Imported 1 records, skipped 1 malformed lines" in captured.out
        assert "Skipping malformed line 2" in captured.err
        assert summary()["total_calls"] == 1

    def test_default_entry_point_still_runs_the_server(self, monkeypatch):
        calls = []
        from librarian_mcp import server
        monkeypatch.setattr(server, "main", lambda: calls.append("started"))
        monkeypatch.setattr("sys.argv", ["librarian-mcp"])

        from librarian_mcp import cli
        cli.main()
        assert calls == ["started"]
