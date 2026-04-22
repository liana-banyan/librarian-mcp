# Bounties

## Why bounties exist

Open source without a participation path is just a white paper.

We published `librarian-mcp` under AGPL-3.0 and signed the Cooperative Defensive Patent Pledge because the architecture works better when more people run it on more corpora. The Eyewitness Benchmark proved the mechanism across eight models and four vendors; what it hasn't yet proved is that the mechanism survives contact with someone else's library. That's the next proof, and we can't collect it alone.

Bounties convert would-be reverse-engineers into contributors. If you're going to take the thing apart, we'd rather pay you to tell us what you found than watch you build a closed fork. AGPL + Pledged Commons + bounty = participation, not piracy. Positive-sum pull.

<!-- FOUNDER HOOK: Cloyd layaway story — the kid who couldn't afford the thing learned to build the thing. Participation > piracy, then and now. -->

## Bounty classes

### 1. Code bounties

Specific open issues tagged [`good-first-bounty`](https://github.com/liana-banyan/librarian-mcp/labels/good-first-bounty) or [`deep-bounty`](https://github.com/liana-banyan/librarian-mcp/labels/deep-bounty). Each issue states the deliverable and the dollar amount. Start with a `good-first-bounty` to learn the codebase; graduate to `deep-bounty` when you're comfortable with the preload schema and the intent-routing logic.

### 2. Corpus contributions

Translation preloads, domain-specific preloads, provenance-grading rubrics. If you teach the Librarian something it didn't know and the contribution passes review, that's a bounty. Corpus contributions are especially valuable for Chapter 2 (Mellon) — multilingual retrieval across 110 languages needs native-speaker canonical files, not machine translations.

### 3. Benchmark replications

Reproduce the Eyewitness Benchmark (R10) on a new model or a new vendor. Use `record_measurement` to log results; submit the JSONL file with your PR. Valid replications earn co-citation in the next Paper and a cash bounty.

### 4. Research extensions

Novel analyses on published metrics — cost curves, latency distributions, accuracy-by-question-type breakdowns, cross-vendor anomaly detection. Accepted research extensions earn co-authorship on future Papers.

<!-- FOUNDER HOOK: The aviation/saxophone/shape-note example — every field the Founder entered, the people who got good were the ones who shared their practice notes. -->

## Pledged Commons grant requirement

All bounty winners sign the [Pledged Commons Grant](https://liana-banyan.com/pledge) before payment. This ensures your contribution stays in the commons and can't be patent-trapped by a downstream actor. The grant is non-exclusive — you keep all rights to your own work; you're granting the commons a permanent license, not transferring ownership.

## Payment rails

| Method | Details |
|---|---|
| **USD** | Stripe, Wise, or PayPal transfer. Net-30 from acceptance. |
| **Credits** | Platform credits (redeemable when the member portal opens). 1.2× face value. |
| **Swag** | Liana Banyan contributor kit for bounties under $50 where you'd prefer the shirt over the check. |

Founder approves rate per bounty. Amounts are listed on each issue. Standard `good-first-bounty` issues start at $25–$75; `deep-bounty` issues at $150–$500. Benchmark replications and research extensions are negotiated per scope.

## What we do NOT bounty

- Anything that compromises safety or user privacy
- Work that bypasses attribution (stripping AGPL notices, removing provenance metadata)
- Contributions that break the canonical ratification path (you can propose changes to canonical values, but they're ratified by the Founder, not by merge)
- Forks marketed as independent products without AGPL compliance
- Social engineering, phishing, or credential-harvesting attempts disguised as security research

## Getting started

1. Browse the [open bounty issues](https://github.com/liana-banyan/librarian-mcp/issues?q=is%3Aopen+label%3Agood-first-bounty,deep-bounty)
2. Comment on the issue to claim it (first-come, first-served; 7-day inactivity timeout)
3. Fork, branch, implement, PR
4. Sign the Pledged Commons Grant (linked in the PR template)
5. Review + merge → payment initiated

---

*"Help each other help ourselves."*

*Pledged into the commons. For the Keep.*
