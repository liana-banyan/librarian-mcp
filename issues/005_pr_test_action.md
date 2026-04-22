# Issue: Add a GitHub Action that runs `pytest` on PRs from non-org contributors

**Labels:** `good-first-bounty`, `ci`, `help wanted`
**Bounty:** $25

## Description

The current CI workflow (`.github/workflows/ci.yml`) runs on pushes and PRs to `main`, but doesn't distinguish between org members and external contributors. For the bounty program to work, we need external PRs to automatically run the test suite so reviewers can see green checks before looking at the code.

## Deliverable

- Update or add a GitHub Actions workflow that:
  - Triggers on `pull_request` from forks (external contributors)
  - Runs `pytest -v` on Python 3.10, 3.11, 3.12
  - Does NOT have access to repository secrets (uses `pull_request` not `pull_request_target`)
  - Reports status check on the PR

## Acceptance criteria

- [ ] External PRs show a CI status check
- [ ] Tests run in a sandboxed environment (no secret access)
- [ ] Workflow file passes `actionlint` validation
- [ ] Existing CI for pushes to `main` is not disrupted

## Notes

The existing `ci.yml` may already cover this — check whether `pull_request` events from forks trigger the workflow. If they do, this issue becomes a documentation task (confirm + document). If not, add the missing trigger.
