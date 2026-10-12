"""Non-finite measurements must never change the JSONL store."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from librarian_mcp import metrics


def _record(*, cost_usd: float = 0.01, latency_s: float = 0.5, question_id: str = "q1") -> None:
    metrics.record_measurement(
        session_id="finite-test",
        vendor="test-vendor",
        model="test-model",
        condition="HOT",
        question_id=question_id,
        correct=True,
        input_tokens=10,
        output_tokens=5,
        cost_usd=cost_usd,
        latency_s=latency_s,
    )


@pytest.mark.parametrize("value", [0.0, 0.01, 1e-8])
def test_finite_values_remain_readable(tmp_metrics_dir: Path, value: float) -> None:
    _record(cost_usd=value, latency_s=value)
    row = json.loads((tmp_metrics_dir / "metrics.jsonl").read_text(encoding="utf-8"))
    assert row["cost_usd"] == value
    assert row["latency_s"] == value


@pytest.mark.parametrize("field", ["cost_usd", "latency_s"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_rejection_does_not_create_store(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str, value: float
) -> None:
    store = tmp_path / "not-created"
    monkeypatch.setattr(metrics, "DATA_DIR", store)
    monkeypatch.setattr(metrics, "METRICS_PATH", store / "metrics.jsonl")
    with pytest.raises(ValueError):
        _record(**{field: value})
    assert not store.exists()


@pytest.mark.parametrize("field", ["cost_usd", "latency_s"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_rejection_preserves_existing_rows_and_next_valid_append(
    tmp_metrics_dir: Path, field: str, value: float
) -> None:
    _record()
    path = tmp_metrics_dir / "metrics.jsonl"
    before = path.read_bytes()
    with pytest.raises(ValueError):
        _record(**{field: value})
    assert path.read_bytes() == before
    _record(question_id="q2")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert [row["question_id"] for row in rows] == ["q1", "q2"]
