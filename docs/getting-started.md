# Getting Started with Librarian MCP

## Prerequisites

- Python 3.10 or later
- An MCP-capable AI client (Claude Code, Cursor, Continue, Zed, etc.)

## Installation

### From source (recommended during alpha)

```bash
git clone https://github.com/liana-banyan/librarian-mcp.git
cd librarian-mcp
pip install -e .
```

### From PyPI (coming soon)

```bash
pip install librarian-mcp
```

## Quick Start

### 1. Create a canonical source file

At the root of your project, create one of these files:

**`CANONICAL.md`** (simplest):

```markdown
# Project Canonical Values

- API base URL: https://api.example.com/v2
- Default timeout: 30 seconds
- Max retries: 3
- Auth method: Bearer token (JWT)
- Database: PostgreSQL 16
- Deploy target: AWS us-east-1
```

**`canonical_values.yaml`** (structured):

```yaml
project_name: My App
api:
  base_url: https://api.example.com/v2
  timeout_seconds: 30
  max_retries: 3
auth:
  method: bearer_jwt
  token_expiry_minutes: 60
database:
  engine: postgresql
  version: "16"
deploy:
  provider: aws
  region: us-east-1
```

### 2. Connect to your AI client

#### Claude Code

```bash
claude mcp add librarian -- python -m librarian_mcp
```

#### Cursor

Add to your MCP configuration (`~/.cursor/mcp.json`):

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

#### Continue (VSCode / JetBrains)

Add to your Continue configuration:

```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "stdio",
          "command": "python",
          "args": ["-m", "librarian_mcp"]
        }
      }
    ]
  }
}
```

### 3. Use the tools

Once connected, the AI client will have access to two tools:

- **`librarian_context`** — Call with your project root to load canonical values into the session.
- **`prose_provenance`** — Call with two file paths (canonical and candidate) to detect drift.

## Optional Dependencies

```bash
# For Opus-grader semantic review (v0.2.0)
pip install "librarian-mcp[opus]"

# For YAML canonical files
pip install "librarian-mcp[yaml]"

# Everything
pip install "librarian-mcp[all]"
```

## What's Next

- **v0.2.0**: Full R9 memory-packet architecture with priority-ordered, per-query re-ranked canonical context. YAML parsing for structured canonical files. Opus-grader semantic drift analysis.
- **v0.3.0**: Code refactor provenance (not just prose). Multi-repo context for teams.

See [the roadmap](https://github.com/liana-banyan/librarian-mcp/issues) for the full plan.

## Troubleshooting

**"No canonical source files found"**: Make sure you have a `CANONICAL.md`, `canonical_values.yaml`, or `.cursor/rules/*.mdc` file at the root of the project you're passing as `project_root`.

**MCP connection errors**: Ensure `python -m librarian_mcp` runs without errors from the command line first. The MCP SDK must be installed (`pip install mcp`).

## License

AGPL-3.0. Free forever for nonprofits under the Pledged Commons tier. Commercial licensing available at enterprise@liana-banyan.com.
