# Issue: Add a new preload file under `preload/founder_voice/` from published Pudding texts

**Labels:** `good-first-bounty`, `corpus`, `help wanted`
**Bounty:** $25

## Description

The `preload/founder_voice/` directory currently contains five files (anachronism_principle, cloyd_pattern, pine_books_anchor, rhetorical_keystones, three_clock_timeline). Published Pudding texts from the Liana Banyan corpus contain additional founder voice anchors that should be available to the `founder_voice` intent.

## Deliverable

- One new `.md` file in `preload/founder_voice/` derived from published Pudding texts
- File follows existing format: `# Heading` first line, factual/referenceable content, under 5,000 tokens
- PR includes a brief note on which source text was used

## Acceptance criteria

- [ ] File loads correctly via `librarian_context(intent="founder_voice")`
- [ ] `prose_provenance` can diff the new file against the source without errors
- [ ] Existing tests pass (`pytest -v`)

## Notes

Pledged Commons Grant signature required before merge. See [BOUNTIES.md](../BOUNTIES.md).
