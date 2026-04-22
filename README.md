# Librarian MCP

```bash
pip install librarian-mcp
```

[![PyPI version](https://img.shields.io/pypi/v/librarian-mcp.svg)](https://pypi.org/project/librarian-mcp/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Pledged Commons](https://img.shields.io/badge/Pledged-Commons-green.svg)](https://liana-banyan.com/pledge)
[![CI](https://github.com/liana-banyan/librarian-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/liana-banyan/librarian-mcp/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/liana-banyan/librarian-mcp.svg?style=social)](https://github.com/liana-banyan/librarian-mcp)

**A real, measured alternative to "bigger context windows."**
Pre-curated canonical memory + prose/code provenance checking + benchmark metrics, delivered as a [Model Context Protocol](https://modelcontextprotocol.io) server that works across Claude Code, Cursor, VSCode (via Continue), and any MCP-capable client.

**[Try it without installing →](https://librarian.the2ndsecond.com)**

## What it does

Five tools, all exposed via MCP:

| Tool | What it does | Added |
|---|---|---|
| **`librarian_context`** | Intent-aware canonical memory packet. Loads curated preload content scoped to your query intent (outreach, architecture, benchmark, founder voice, etc.). Eliminates the "forgets by prompt #21" failure mode. | v0.1.0 (stub), **v0.2.0** (intent-aware) |
| **`prose_provenance`** | Deterministic drift detection between two document versions. Catches silently-removed voice anchors, stale canonical numbers, section changes, register shifts. | v0.1.0 |
| **`record_measurement`** | Log a single benchmark measurement (vendor, model, condition, accuracy, cost, latency) to local JSONL. | **v0.2.0** |
| **`metrics_summary`** | Per-vendor and per-model aggregation of recorded measurements. Shows accuracy lift, cost savings, cache hit rate. | **v0.2.0** |
| **`opt_in_share`** | Toggle anonymous metrics sharing flag. Default OFF. Commons dashboard POST endpoint ships in a future release. | **v0.2.0** |

## Why we built this

Independently measured result (Eyewitness Benchmark R10, April 2026, eight models across four vendors, 1,200 graded calls, inter-rater kappa 0.883/0.850):

- **Without the Librarian (COLD):** mean 8.7% correct
- **With the Librarian (HOT):** mean 94.8% correct — **86.1 percentage-point lift**
- **Haiku 4.5 (cheapest) ties Opus 4.7 (most expensive)** at 19x cost difference
- **4.3x more right answers per dollar of compute**

Applied inside Microsoft Copilot's inference path, the same architecture recovers an estimated **$750M/year** in waste. Inside Anthropic's developer tools, **~$130M/year**. Full methodology in the R9 Empirical Test Companion Paper.

## `librarian_context` — Intent API

```python
librarian_context(intent="outreach", max_tokens=16000)
```

| Intent | What it loads | Approx. tokens |
|---|---|---|
| `""` (default) | Base R9-v2 preload only | ~4,500 |
| `"canonical"` | Base + canonical values + canonical laws | ~15,000 |
| `"outreach"` | Base + canonical + Opening Gambit + letter queue + Cephas + Glass Door + Witness | ~30,000 |
| `"architecture"` | Base + canonical + Pledge + IP split + Medallion + Pedestal Stake | ~20,000 |
| `"founder_voice"` | Base + Rhetorical Keystones + Pine Books + Anachronism + Cloyd + Three-clock | ~10,000 |
| `"benchmark"` | Base + R10 results + R9 brief + 75-Q bank + rubric + posture disclosure | ~10,000 |
| `"operational"` | Union of `outreach` + `canonical` | ~30,000 |

**List inputs** for union queries: `intent='["benchmark", "founder_voice"]'`

Returns:
```json
{
  "packet": "...markdown...",
  "sections_included": ["r9v2_base.md", "canonical/canonical_values.yaml", ...],
  "token_count": 14832,
  "source_version": "a1b2c3d4e5f6",
  "truncation_note": null
}
```

## `metrics_summary` — Schema

```json
{
  "total_calls": 1200,
  "per_vendor": {
    "anthropic": {
      "calls": 600,
      "hot_accuracy": 95.3,
      "cold_baseline_est": 8.2,
      "dollars_saved_est": 42.17,
      "cache_hit_rate": 50.0
    }
  },
  "per_model": {
    "claude-haiku-4-5-20251001": { "..." : "..." }
  },
  "cumulative_hot_accuracy": 94.8,
  "cumulative_cold_baseline_est": 8.7,
  "cumulative_dollars_saved_est": 127.50,
  "opt_in_share": false,
  "since": "all_time"
}
```

## Pricing

| Tier | Who it's for | Price |
|---|---|---|
| **Pledged Commons** | Any nonprofit, cooperative, academic institution, or public-service organization with IRS-verified EIN (or international equivalent) | **$0 forever.** Full feature set. Under the Cooperative Defensive Patent Pledge. |
| **Individual** | Single developer | $0 (community edition, this repo) for local use; $15/mo for hosted multi-repo context + team sharing |
| **Team** | 2–50 seats | $10/seat/mo (min $50) |
| **Enterprise** | 50+ seats, custom canonical schemas, audit logs, SAML, support | Contact. Typically $50–100/seat/mo. |

**The commercial tiers pay for the commons.** No grant funding, no VC, no extractive margin. Cost+20% on operating expense. That's it.

## Why MCP (not a Cursor extension)

Because you shouldn't have to pick between your AI assistants. MCP servers work across Claude Code, Cursor (v0.45+), Continue (VSCode / JetBrains), Zed, and every MCP-capable client in the roadmap. One server, all your tools.

## Install

### Quick start (local, Python 3.10+)

```bash
git clone https://github.com/liana-banyan/librarian-mcp.git
cd librarian-mcp
pip install -e .
librarian-mcp  # starts on stdio for MCP clients
```

### With optional dependencies

```bash
pip install -e ".[all]"   # tiktoken (accurate token counts) + anthropic + pyyaml
pip install -e ".[dev]"   # + pytest, ruff, mypy for development
```

### Claude Code

```bash
claude mcp add librarian python -m librarian_mcp
```

### Cursor

Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "librarian": {
      "command": "python",
      "args": ["-m", "librarian_mcp"]
    }
  }
}
```

### Continue (VSCode / JetBrains)

See [docs/continue-integration.md](docs/continue-integration.md).

## Development

```bash
pip install -e ".[dev,all]"
ruff check src/ tests/          # lint
mypy --strict src/librarian_mcp/  # type check
pytest -v                        # test (34 tests)
```

## Status

**April 21, 2026 — v0.2.0.** Intent-aware `librarian_context` live with bundled preload (R10-validated). Benchmark metrics recording live. Prose Provenance tool upgraded to v0.2.0. PyPI name `librarian-mcp` reserved. CI/CD staged.

## License

[AGPL-3.0](LICENSE). Commercial licensing for the paid tiers is a separate agreement; the Pledged Commons tier is covered by AGPL + the [Cooperative Defensive Patent Pledge](https://liana-banyan.com/pledge).

## Contact

- General: hello@liana-banyan.com
- Enterprise: enterprise@liana-banyan.com
- Press / AI policy / datacenter-alternative questions: press@liana-banyan.com
- Founder: Jonathan Jones, Founder & General Manager, Liana Banyan Corporation (Wyoming C-Corp)

## Contributing

We welcome contributions — code, corpus preloads, benchmark replications, and research extensions.

- **[BOUNTIES.md](BOUNTIES.md)** — paid bounties for specific contributions, from $25 `good-first-bounty` issues to $500 deep bounties
- **[BUILDING_TOGETHER.md](BUILDING_TOGETHER.md)** — guide to running, extending, and contributing back upstream

---

*"You build the Features — We're building the Board."*

**Pledged into the commons. For the Keep.**
