# Librarian MCP

**A real, measured alternative to "bigger context windows."**
Pre-curated canonical memory + prose/code provenance checking, delivered as a [Model Context Protocol](https://modelcontextprotocol.io) server that works across Claude Code, Cursor, VSCode (via Continue), and any MCP-capable client.

## What it does

Two tools, both exposed via MCP:

1. **`librarian_context`** — loads a tightly-curated "memory packet" of your project's canonical truth (pricing, people, decisions, rules, API contracts, patent numbers — whatever you declare canonical) at the start of every AI-assisted session. Eliminates the "forgets by prompt #21" failure mode documented across Gemini 3.1 Pro, long-context Claude, and Copilot.

2. **`prose_provenance`** — deterministic + Opus-assisted drift detection between two versions of any document. Catches silently-removed voice anchors ("Keystones"), stale canonical numbers reintroduced, section structure changes, register shifts, softened stakes, and disclaimer insertion. Works on letters, specs, contracts, and (next release) code refactors.

## Why we built this

Independently measured result (Painter Benchmark, April 18, 2026, three models × 75 platform-specific questions, each twice):

- **Without the Librarian:** ~8 out of 100 correct
- **With the Librarian:** 93–97 out of 100 correct, across every AI tested (Haiku 4.5, Sonnet 4.6, Opus 4.7)
- **4.3× more right answers per dollar of compute**

Applied inside Microsoft Copilot's inference path, the same architecture recovers an estimated **$750M/year** in waste. Inside Anthropic's developer tools, **~$130M/year**. Both numbers sourced from [R9 Empirical Test Companion Paper, B108](https://liana-banyan.com/papers/r9-empirical) (to be published; contact for preprint).

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

### Quick start (local, Python)

```bash
git clone https://github.com/liana-banyan/librarian-mcp.git
cd librarian-mcp
pip install -e .
librarian-mcp serve  # starts on stdio for MCP clients
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

## Status

**April 20, 2026 — v0.1.0 (early access).** Prose Provenance tool is live and measured. Librarian Context tool ships next release. Roadmap in [docs/roadmap.md](docs/roadmap.md).

## License

[AGPL-3.0](LICENSE). Commercial licensing for the paid tiers is a separate agreement; the Pledged Commons tier is covered by AGPL + the [Cooperative Defensive Patent Pledge](https://liana-banyan.com/pledge).

## Contact

- General: hello@liana-banyan.com
- Enterprise: enterprise@liana-banyan.com
- Press / AI policy / datacenter-alternative questions: press@liana-banyan.com
- Founder: Jonathan Jones, Founder & General Manager, Liana Banyan Corporation (Wyoming C-Corp)

---

*"You build the Features — We're building the Board."*

**Pledged into the commons. For the Keep.**
