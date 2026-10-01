# CI for contributions from forks

The existing [CI workflow](../.github/workflows/ci.yml) handles pull requests
targeting `main`, including pull requests from forks. It also runs on pushes to
`main`. No separate external-contributor workflow is needed.

Each run has three `test` jobs on `ubuntu-latest`, using Python 3.10, 3.11 and
3.12. Each job installs `.[dev,all]`, runs Ruff, runs strict mypy, then runs
`pytest -v --tb=short`. A failure in one Python job does not cancel the others
because the matrix sets `fail-fast: false`. A failed step still prevents later
steps in that job from running: a lint failure is not evidence that pytest ran.

## Finding and interpreting your checks

1. Open a pull request from your fork with `main` as its base branch.
2. Open its **Checks** tab, or find the corresponding `pull_request` run under
   the upstream repository's **Actions** tab. Match the run to your latest commit.
3. Inspect all three Python jobs and the **Run tests** step in each job. Include
   run links and actual results in your PR; distinguish passed, failed, skipped,
   and approval-pending checks.

GitHub may require a maintainer to approve a first-time or external contributor's
workflow run. An `action_required` run or an approval banner means the workflow
was triggered but needs maintainer action; it does not mean the trigger is
missing or tests passed. Ask a maintainer to inspect and approve the run. Do not
add another workflow or change the event to bypass that review.

The separate `license/cla` check concerns the contribution agreement. It is not a
pytest result and does not establish that any Python job executed.

See GitHub's [fork-run approval guide](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/approve-runs-from-forks).

## Fork security boundary

CI uses `pull_request`, not `pull_request_target`. Under GitHub's normal public
fork-PR policy, repository secrets are withheld and `GITHUB_TOKEN` is read-only.
This workflow does not reference repository secrets or request elevated token
permissions, and it runs on GitHub-hosted runners. It still installs and executes
PR-controlled code, which is why maintainers should review a run before approval.
Do not provide personal credentials to make a test pass.

See GitHub's [pull-request event documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request)
for the platform's fork restrictions and approval behavior.

## Running the same checks locally

From the repository root, create and activate a virtual environment using one of
the matrix's Python versions. Then run these commands separately so you can
record each result:

```sh
python -m pip install --upgrade pip
python -m pip install -e ".[dev,all]"
ruff check src/ tests/
mypy --strict src/librarian_mcp/
pytest -v --tb=short
```

Repeat with Python 3.10, 3.11 and 3.12 to reproduce the full matrix. Passing on
one version does not establish that the other two pass. If installation or
collection fails, record the Python/package versions and the error; do not
describe that as a successful test run. Dependencies are not locked, so include
resolved versions when reporting differences between local and CI results.

For workflow edits, install [actionlint](https://github.com/rhysd/actionlint)
and validate the workflow from the repository root:

```sh
actionlint .github/workflows/ci.yml
```

Actionlint validates the workflow definition. Only an actual upstream run can
show that repository approval settings allowed the jobs to execute.
