# Issue: Add a test case demonstrating `prose_provenance` catching a removed Rhetorical Keystone

**Labels:** `good-first-bounty`, `testing`, `help wanted`
**Bounty:** $25

## Description

`prose_provenance` detects when keystone phrases are silently dropped from a revised document. We need an explicit test case that demonstrates this with a known Rhetorical Keystone from the preload.

## Deliverable

- New test in `tests/test_provenance.py`
- Test creates two temp files: a canonical version containing a keystone phrase, and a candidate version with that phrase removed
- Calls `prose_provenance` and asserts:
  - `keystones_missing` includes the removed phrase
  - `drift_score > 0`
  - `verdict` is not `"clean"`

## Acceptance criteria

- [ ] Test passes with `pytest -v tests/test_provenance.py`
- [ ] Test uses a real Rhetorical Keystone from `preload/founder_voice/rhetorical_keystones.md`
- [ ] Test is self-contained (creates and cleans up temp files)
- [ ] All existing tests still pass

## Notes

This is a great first issue if you want to understand how prose provenance works. Read `server.py` lines 79–209 for the implementation.
