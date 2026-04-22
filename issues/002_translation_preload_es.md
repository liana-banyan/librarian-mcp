# Issue: Add a translation preload (Spanish) of `r9v2_base.md`

**Labels:** `good-first-bounty`, `translation`, `chapter-2-prep`, `help wanted`
**Bounty:** $75

## Description

Chapter 2 (Mellon — multilingual retrieval) needs native-speaker canonical files. This issue requests a Spanish translation of the base preload document `preload/r9v2_base.md`.

## Deliverable

- New file: `preload/r9v2_base_es.md`
- Faithful translation preserving all canonical numbers, section headers, and rhetorical keystones
- Translator's note as a comment block at the top of the file

## Acceptance criteria

- [ ] Run `prose_provenance` between `r9v2_base.md` and `r9v2_base_es.md` — structural sections preserved
- [ ] All canonical numbers (83.3%, 2,267 innovations, 13 provisionals, etc.) appear verbatim in the translation
- [ ] Translator is a native Spanish speaker (self-attested in PR description)
- [ ] Existing tests pass

## Notes

FR/PT/ZH translations are also welcome as separate PRs — each earns the same bounty. See [BOUNTIES.md](../BOUNTIES.md).
