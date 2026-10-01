# Contributor CI

Pull requests to `main` already run the repository's CI workflow, including pull requests opened from forks. External contributors do not need a separate workflow file.

## What runs on a pull request

The workflow in `.github/workflows/ci.yml` uses the `pull_request` event and runs the same test job on Python 3.10, 3.11, and 3.12. Each matrix job runs:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev,all]"
ruff check src/ tests/
mypy --strict src/librarian_mcp/
pytest -v --tb=short
```

A pull request should therefore show CI status checks for all three Python versions. You can open the pull request's **Checks** tab, or use the checks shown near the merge box, to inspect failures and logs.

## Fork pull requests and secrets

The workflow intentionally uses `pull_request`, not `pull_request_target`. GitHub does not pass repository Actions secrets to workflows triggered by pull requests from forks. This keeps unreviewed external code from gaining the repository's secret values while still allowing the normal lint, type-check, and test suite to run.

Do not change this workflow to `pull_request_target` just to make a forked pull request run automatically. That event has a different security model and is unnecessary for this repository's test suite.

## First-time contributor approval

GitHub can require a maintainer to approve a workflow run from a first-time or otherwise restricted external contributor, depending on the repository or organization Actions settings. If a pull request says that a workflow is waiting for approval, the `pull_request` trigger is still configured correctly. A maintainer needs to approve that run in GitHub Actions; the contributor does not need to add or modify a workflow.

After approval, the existing Python 3.10, 3.11, and 3.12 matrix runs normally and reports its status on the pull request.

## Run the same checks locally

From the repository root:

```bash
python -m pip install -e ".[dev,all]"
ruff check src/ tests/
mypy --strict src/librarian_mcp/
pytest -v --tb=short
```

If you have `actionlint` installed, you can also validate the workflow syntax before opening a pull request:

```bash
actionlint .github/workflows/ci.yml
```

A local pass is not a substitute for the pull-request checks, but it catches most failures before CI starts.

## If CI does not appear

Check these in order:

1. The pull request targets the repository's `main` branch.
2. The **Actions** or **Checks** UI is not waiting for maintainer approval.
3. The workflow file still contains a `pull_request` trigger for `main`.
4. The pull request has not changed workflow permissions or attempted to depend on repository secrets.

If the workflow still does not appear after those checks, report the pull request URL and what GitHub shows in the Actions UI so the repository configuration can be investigated without weakening the fork security model.
