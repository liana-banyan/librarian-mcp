"""
Librarian Metrics — local JSONL measurement recorder for benchmark tracking.

Records per-call measurements (vendor, model, condition, cost, accuracy) and
provides per-vendor / per-model summary aggregation. Opt-in anonymous sharing
flag is stored locally; the POST endpoint ships in a future release.

Storage: ~/.librarian-mcp/metrics.jsonl (measurements)
         ~/.librarian-mcp/config.json   (opt-in flag)
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any

DATA_DIR = Path.home() / ".librarian-mcp"
METRICS_PATH = DATA_DIR / "metrics.jsonl"
CONFIG_PATH = DATA_DIR / "config.json"


def _ensure_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_config() -> dict[str, Any]:
    if CONFIG_PATH.exists():
        try:
            data: dict[str, Any] = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_config(config: dict[str, Any]) -> None:
    _ensure_dir()
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


# ─── Record ───────────────────────────────────────────────────────────────────

def record_measurement(
    session_id: str,
    vendor: str,
    model: str,
    condition: str,
    question_id: str,
    correct: bool,
    input_tokens: int,
    output_tokens: int,
    cost_usd: float,
    latency_s: float,
) -> None:
    """Append one measurement to the local JSONL file."""
    record = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "session_id": session_id,
        "vendor": vendor,
        "model": model,
        "condition": condition,
        "question_id": question_id,
        "correct": correct,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost_usd,
        "latency_s": latency_s,
    }
    # Reject NaN and infinities before creating or changing the metrics store.
    payload = json.dumps(record, allow_nan=False) + "\n"
    _ensure_dir()
    with open(METRICS_PATH, "a", encoding="utf-8") as f:
        f.write(payload)


# ─── Summary ──────────────────────────────────────────────────────────────────

def _bucket_stats(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute accuracy and cost stats for a list of measurement records."""
    if not records:
        return {
            "calls": 0,
            "hot_accuracy": 0.0,
            "cold_baseline_est": 0.0,
            "dollars_saved_est": 0.0,
            "cache_hit_rate": 0.0,
        }

    total = len(records)
    hot_records = [r for r in records if r.get("condition") == "HOT"]
    cold_records = [r for r in records if r.get("condition") == "COLD"]

    hot_correct = sum(1 for r in hot_records if r.get("correct"))
    cold_correct = sum(1 for r in cold_records if r.get("correct"))

    hot_accuracy = (hot_correct / len(hot_records) * 100) if hot_records else 0.0
    cold_baseline = (cold_correct / len(cold_records) * 100) if cold_records else 0.0

    hot_cost = sum(r.get("cost_usd", 0) for r in hot_records)
    cold_cost = sum(r.get("cost_usd", 0) for r in cold_records)

    # Savings estimate: what would it cost to get HOT-level accuracy without the
    # librarian? Assumes you'd need ~(hot_accuracy/cold_baseline) more COLD calls
    # at COLD cost to match HOT accuracy. If no COLD data, savings = 0.
    if cold_baseline > 0 and cold_records:
        avg_cold_cost = cold_cost / len(cold_records)
        equivalent_cold_calls = (hot_correct / (cold_baseline / 100)) if cold_baseline > 0 else 0
        dollars_saved = (equivalent_cold_calls * avg_cold_cost) - hot_cost
    else:
        dollars_saved = 0.0

    cache_hit_rate = (len(hot_records) / total * 100) if total else 0.0

    return {
        "calls": total,
        "hot_accuracy": round(hot_accuracy, 2),
        "cold_baseline_est": round(cold_baseline, 2),
        "dollars_saved_est": round(max(0, dollars_saved), 4),
        "cache_hit_rate": round(cache_hit_rate, 2),
    }


def summary(since_timestamp: str | None = None) -> dict[str, Any]:
    """Read JSONL and return per-vendor / per-model aggregation.

    Returns the B112-specified schema: total_calls, per_vendor, per_model,
    cumulative stats, opt_in_share flag, since timestamp.
    """
    records: list[dict[str, Any]] = []
    if METRICS_PATH.exists():
        try:
            for raw_line in METRICS_PATH.read_text(encoding="utf-8").splitlines():
                stripped = raw_line.strip()
                if stripped:
                    records.append(json.loads(stripped))
        except (json.JSONDecodeError, OSError):
            pass

    if since_timestamp:
        records = [r for r in records if r.get("timestamp", "") >= since_timestamp]

    # Per-vendor aggregation
    by_vendor: dict[str, list[dict[str, Any]]] = {}
    for r in records:
        vendor: str = r.get("vendor", "unknown")
        by_vendor.setdefault(vendor, []).append(r)

    per_vendor = {v: _bucket_stats(recs) for v, recs in by_vendor.items()}

    # Per-model aggregation
    by_model: dict[str, list[dict[str, Any]]] = {}
    for r in records:
        model: str = r.get("model", "unknown")
        by_model.setdefault(model, []).append(r)

    per_model = {m: _bucket_stats(recs) for m, recs in by_model.items()}

    # Cumulative
    cumulative = _bucket_stats(records)

    config = _load_config()

    return {
        "total_calls": len(records),
        "per_vendor": per_vendor,
        "per_model": per_model,
        "cumulative_hot_accuracy": cumulative["hot_accuracy"],
        "cumulative_cold_baseline_est": cumulative["cold_baseline_est"],
        "cumulative_dollars_saved_est": cumulative["dollars_saved_est"],
        "opt_in_share": config.get("opt_in_share", False),
        "since": since_timestamp or "all_time",
    }


# ─── Opt-in share ─────────────────────────────────────────────────────────────

def opt_in_share(enabled: bool = True) -> dict[str, str]:
    """Toggle the anonymous sharing flag. POST endpoint deferred to K425."""
    config = _load_config()
    config["opt_in_share"] = enabled
    _save_config(config)
    return {"status": "enabled" if enabled else "disabled"}
