# Issue: Add a CLI flag to `record_measurement` for bulk JSONL import

**Labels:** `good-first-bounty`, `enhancement`, `help wanted`
**Bounty:** $50

## Description

Currently, `record_measurement` accepts one measurement at a time via MCP tool call. For users who have existing benchmark results in JSONL format, there's no way to bulk-import them into the `~/.librarian-mcp/metrics.jsonl` store.

## Deliverable

- Add a `--import` flag to the `librarian-mcp` CLI entry point
- `librarian-mcp --import path/to/results.jsonl` reads the file line-by-line and appends validated records to the metrics store
- Validate each line against the expected schema (session_id, vendor, model, condition, question_id, correct, input_tokens, output_tokens, cost_usd, latency_s)
- Skip malformed lines with a warning to stderr
- Print summary: `Imported N records, skipped M malformed lines`

## Acceptance criteria

- [ ] `librarian-mcp --import test_data.jsonl` works from the command line
- [ ] Malformed lines are skipped with warnings (not silent, not fatal)
- [ ] `metrics_summary` correctly aggregates imported records
- [ ] New test in `tests/test_metrics.py` covering the import path
- [ ] Existing tests pass

## Notes

See [BUILDING_TOGETHER.md](../BUILDING_TOGETHER.md) for development setup.
