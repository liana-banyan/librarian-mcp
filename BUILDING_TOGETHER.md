# Building Together

*Every town its own fab shop — and its own librarian.*

## Who this is for

You want to use the Librarian in your own project AND contribute back upstream. You're not here to reverse-engineer; you're here to build. This guide shows you how to run it, extend it, and give back.

<!-- FOUNDER HOOK: Pine Books anchor — the first library he built was a cardboard box in a barracks. The point was never the box; it was knowing where to find what you needed when the lights went out. -->

## Running it yourself

```bash
# Install from PyPI
pip install librarian-mcp

# Start the MCP server (stdio transport, works with Claude Code / Cursor / Continue)
python -m librarian_mcp

# Or with the console script
librarian-mcp
```

The Librarian ships with a curated preload directory — canonical values, architectural docs, benchmark methodology, founder voice anchors. On first run, it loads these files and serves them through the `librarian_context` tool based on intent routing.

### Connecting to your MCP client

**Claude Code:**
```bash
claude mcp add librarian python -m librarian_mcp
```

**Cursor** — add to `~/.cursor/mcp.json`:
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

**Continue (VSCode / JetBrains):** See [docs/continue-integration.md](docs/continue-integration.md).

## Adding your own preload

The preload directory (`preload/`) is organized by intent:

```
preload/
├── r9v2_base.md              ← always loaded (priority 0)
├── canonical/                 ← loaded for "canonical" intent
├── architecture/              ← loaded for "architecture" intent
├── benchmark/                 ← loaded for "benchmark" intent
├── founder_voice/             ← loaded for "founder_voice" intent
└── outreach/                  ← loaded for "outreach" intent
```

To add your own preload file:

1. Create a `.md` file in the appropriate intent subdirectory
2. First line should be a `# Heading` identifying the document
3. Content should be factual, referenceable, and canonical — the Librarian treats preload files as ground truth
4. Keep individual files under 5,000 tokens for clean budget management
5. PR with a clear description of what the file adds and why it belongs in that intent category

## Running the benchmark on your own corpus

The Eyewitness Benchmark proved the mechanism on the Liana Banyan corpus. Running it on yours proves it's not corpus-specific.

```bash
# Install with benchmark dependencies
pip install librarian-mcp[all]

# Record measurements using the MCP tool
# (your benchmark harness calls record_measurement per question)

# View aggregated results
# (call metrics_summary via MCP, or inspect ~/.librarian-mcp/metrics.jsonl directly)
```

Your benchmark should test the same structure: HOT (with preload) vs COLD (without), same question bank, single-blind grading. If you reproduce the R10 methodology and submit your JSONL, you earn a benchmark replication bounty and co-citation in the next Paper. See [BOUNTIES.md](BOUNTIES.md).

## Contributing a translation

Chapter 2 (Mellon — *Speak Friend and Enter*) will add multilingual retrieval across 110 languages. That needs native-speaker canonical files, not machine translations.

To contribute a translation preload:

1. Start with `preload/r9v2_base.md` — it's the base document loaded for every intent
2. Translate faithfully. Preserve all canonical numbers, all section headers, all rhetorical keystones
3. Name the file `r9v2_base_{lang_code}.md` (e.g., `r9v2_base_es.md` for Spanish)
4. Run `prose_provenance` against the English original to verify your translation preserves structural fidelity
5. PR with the translation and a brief translator's note

Translation preloads are bounty-eligible. See [BOUNTIES.md](BOUNTIES.md).

## Reporting a drift finding

`prose_provenance` detects when a revised document drifts from its canonical original. If you find a drift in any published Liana Banyan document:

1. Run `prose_provenance` with the canonical and candidate paths
2. Note the drift score, verdict, and which keystones or canonical numbers were affected
3. Open a GitHub issue with the drift report and the `prose_provenance` output
4. Tag it `drift-report`

Drift reports help us maintain canonical integrity across 2,267 innovations and 13 provisional patent applications. They're taken seriously.

## Becoming a Member Keystone contributor

Chapter 3 — Paired Provenance — will allow members to register their own canonical documents with the Librarian and track drift across their corpus. This ships in v0.4.0 and is not yet available.

When it ships, Member Keystone contributors will be able to:

- Register canonical files into the commons index
- Receive provenance alerts when downstream copies drift
- Contribute to the aggregate Eyewitness dataset (opt-in)
- Earn contributor credit visible in the commons dashboard

Watch this space. Or better yet, [watch the repo](https://github.com/liana-banyan/librarian-mcp).

## The à-la-carte ecosystem pledge

The Librarian is one tool in a larger platform, but it stands alone. You don't need a Liana Banyan account to install it. You don't need to subscribe to use it. You don't need to agree to anything beyond AGPL-3.0 to fork it.

The commercial tiers exist to pay for the commons — not to gate-keep the tool. Cost+20% on operating expense. That's the whole margin.

If you need more than what the open-source edition provides — hosted multi-repo context, team sharing, audit logs, SAML — those tiers exist and they fund everyone else's $0 tier.

---

*"Help each other help ourselves."*

*Pledged into the commons. For the Keep.*
