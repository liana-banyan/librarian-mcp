# CI for external PRs

The existing workflow (`.github/workflows/ci.yml`) already triggers on `pull_request` events targeting `main`:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

GitHub's default behavior runs `pull_request` workflows for PRs from forks in a read-only token context with no access to secrets (using the `pull_request` event, not `pull_request_target`). This satisfies the requirements:
- External PRs from forks trigger the workflow automatically
- Tests run in a sandboxed environment with no repository secret access
- Status checks are reported on the PR
- Existing push-to-main behavior is unchanged

No changes to the workflow are required. This is working as designed.
