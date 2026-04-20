# Why Librarian MCP Exists

**Short version:** every AI company is currently paying a tax they don't know they're paying. We measured the tax. We built the architecture that recovers it. We're open-sourcing it so the commons doesn't have to wait for the incumbents to notice.

---

## The invisible tax

Every AI session starts from zero. Every million-token context window has to be repacked with the same ground truth the last session already had. The bill comes in disguised as "inference cost," but what the model is actually billing you for is its own forgetting.

Measured consequences:

| Platform | Reported symptom | Industry answer |
|---|---|---|
| Gemini 3.1 Pro (Google) | "Forgets" Prompt #1 by prompt #21–25 (AI Pro subscriber public complaint, March 2026) | Infini-Attention + TurboQuant — compress more paint into the same can |
| Microsoft Copilot | Pulls from files/inbox on demand; no canonical index — gets "whatever it grabbed" | Bigger brush, dipping into whatever can is closest |
| Anthropic (Claude) | Session memory + prompt caching — smart brush, not a smart system | Same architecture, better fabric |

All three push on **paint and brush**. Same shape, bigger scale. None decide, because no one owns the decision, *which facts are canonical.*

## What we measured

**Painter Benchmark, April 18, 2026:** 75 platform-specific questions × 3 models × 2 conditions (with Librarian / without).

| Model | Without Librarian | With Librarian |
|---|---|---|
| Claude Haiku 4.5 (3-rep, n=225) | 8.4% | **93.3% ± 1.7%** |
| Claude Sonnet 4.6 (1-rep, n=75) | 9.3% | **92.0%** |
| Claude Opus 4.7 (1-rep, n=75) | 8.2% | **97.3%** |

**4.3× more correct answers per dollar of compute.** Architecture works on models never trained against it. Cheap enough to use every session.

## What it's worth

At steady-state commercial deployment:

- Inside Microsoft Copilot's inference path: **~$750M/yr** recovered
- Inside Anthropic's own developer tools: **~$130M/yr** recovered
- Across MacKenzie Scott's 2,300+ Yield Giving grantees if they adopt under the Pledge: **$115M–$280M/yr recurring** (conservative)
- Across the broader US nonprofit sector at the same adoption rate: **$1–$5B/yr**

These aren't marketing projections. They're conservative extrapolations from the measured per-session delta applied to published deployment-scale estimates. Full derivation: [R9 Empirical Test Companion Paper (B108)](https://liana-banyan.com/papers/r9-empirical).

## What we're offering

This repo ships two MCP tools:

1. **`librarian_context`** — pre-curated canonical memory packet. Loads at session start. Replaces "let the model find the needle in a bigger haystack" with "hand the model the needle before it asks." Measured 4.3× cost-per-correct advantage.

2. **`prose_provenance`** — drift detection on document refactors. Catches Keystones (voice anchors) silently dropped, stale canonical numbers reintroduced, register shifts, softened stakes. Works on letters, specs, contracts, and — next release — code refactors.

## Why we're giving it away (to the commons)

We own 13 patent provisionals on this architecture. We have until November 26, 2026 to convert them to utility patents. **We're pledging 80% of the portfolio into the [Cooperative Defensive Patent Pledge](https://liana-banyan.com/pledge)**, which makes the architecture free forever for any nonprofit, cooperative, academic institution, or public-service entity with an IRS-verified EIN (or international equivalent). No grant application. No gatekeeping. EIN on day one of awareness.

The commercial tiers pay for the commons. Cost+20% on operating expense. No VC. No extractive margin. No "freemium-until-acquired."

The 80% is the only number where cooperation costs less than defection.

## For AI-policy readers

If you're writing legislation about new datacenter construction (the April 2026 proposals from Senator Sanders and Representative Ocasio-Cortez, among others): we are the concrete counter-example to the claim that further scale is the only path to AI utility.

- **Measured:** 4.3× cost-per-correct advantage without a single new GPU.
- **Deployed:** working tool, this repo, today.
- **Free for nonprofits:** structurally, in perpetuity.
- **Patent-protected for the commons:** no corporate actor can lock it out of the civic sector.

You don't need to trust us. The benchmark is reproducible. The code is AGPL. The Pledge is legally binding. Run it, read it, check it, use it.

## For developers

Install. Run. Keep your preferred editor. Bring your own canonical file. Keep your preferred model. Nothing is locked in. Nothing is bundled. If you add one piece (just context), you save what you save. If you add the next (provenance checking), you layer the synergy. Your choice, every time.

## Contact

Jonathan Jones, Founder & General Manager, Liana Banyan Corporation
- hello@liana-banyan.com
- press@liana-banyan.com

*"You build the Features — We're building the Board."*

**For the Keep.**
