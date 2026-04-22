#!/usr/bin/env python3
"""
pull_launch_metrics.py — Citation-traffic instrumentation for K428 launch.

Queries four referrer surfaces and prints a summary table:
  1. Direct visits to librarian.the2ndsecond.com  (Cloud Run structured logs)
  2. PyPI downloads                               (pypistats API)
  3. GitHub stars/clones delta                    (GitHub REST API)
  4. Smithery install count                       (Smithery registry)

Requires:
  - GITHUB_TOKEN env var for GitHub API (public repo, but rate limits apply)
  - gcloud CLI authenticated for Cloud Run logs (surface 1)

Usage:
  python scripts/pull_launch_metrics.py
  python scripts/pull_launch_metrics.py --since 2026-04-22
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone


def fetch_json(url: str, headers: dict[str, str] | None = None) -> dict | list | None:
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  [WARN] Failed to fetch {url}: {e}", file=sys.stderr)
        return None


# ─── Surface 1: Cloud Run direct visits ──────────────────────────────────────

def get_cloud_run_visits(since: str) -> int | str:
    """Query Cloud Run structured logs for direct visit count."""
    filter_str = (
        f'resource.type="cloud_run_revision" '
        f'resource.labels.service_name="librarian-mcp" '
        f'httpRequest.requestUrl:"/"\n'
        f'timestamp>="{since}T00:00:00Z"'
    )
    try:
        result = subprocess.run(
            [
                "gcloud", "logging", "read", filter_str,
                "--format=json", "--limit=10000",
                "--project=lianabanyan-403dc",
            ],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            entries = json.loads(result.stdout) if result.stdout.strip() else []
            return len(entries)
        return f"error: {result.stderr[:100]}"
    except FileNotFoundError:
        return "gcloud CLI not found"
    except subprocess.TimeoutExpired:
        return "timeout"


# ─── Surface 2: PyPI downloads ────────────────────────────────────────────────

def get_pypi_downloads() -> dict[str, int | str]:
    """Fetch recent download stats from pypistats API."""
    url = "https://pypistats.org/api/packages/librarian-mcp/recent"
    data = fetch_json(url)
    if data and "data" in data:
        return {
            "last_day": data["data"].get("last_day", 0),
            "last_week": data["data"].get("last_week", 0),
            "last_month": data["data"].get("last_month", 0),
        }
    return {"error": "Could not fetch PyPI stats"}


# ─── Surface 3: GitHub stars/clones ──────────────────────────────────────────

def get_github_stats() -> dict[str, int | str]:
    """Fetch star count and clone traffic from GitHub API."""
    import os
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repo_url = "https://api.github.com/repos/liana-banyan/librarian-mcp"
    repo_data = fetch_json(repo_url, headers)
    stars = repo_data.get("stargazers_count", "?") if repo_data else "error"
    forks = repo_data.get("forks_count", "?") if repo_data else "error"

    clones_url = f"{repo_url}/traffic/clones"
    clones_data = fetch_json(clones_url, headers)
    clones_14d = clones_data.get("count", "?") if clones_data else "needs push access"

    return {"stars": stars, "forks": forks, "clones_14d": clones_14d}


# ─── Surface 4: Smithery install count ───────────────────────────────────────

def get_smithery_installs() -> int | str:
    """Check Smithery registry for install count."""
    url = "https://registry.smithery.ai/servers/librarian-mcp"
    data = fetch_json(url)
    if data and isinstance(data, dict):
        return data.get("installCount", data.get("install_count", "listed (count not exposed)"))
    return "not listed or API unavailable"


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Pull launch metrics for K428")
    parser.add_argument(
        "--since",
        default=(datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d"),
        help="Start date for metrics window (YYYY-MM-DD, default: yesterday)",
    )
    args = parser.parse_args()

    print(f"╔══════════════════════════════════════════════════════════╗")
    print(f"║  Librarian MCP — Launch Metrics (since {args.since})    ║")
    print(f"╠══════════════════════════════════════════════════════════╣")

    # Surface 1
    print(f"║                                                          ║")
    print(f"║  1. Cloud Run direct visits                              ║")
    visits = get_cloud_run_visits(args.since)
    print(f"║     Visits: {str(visits):<44} ║")

    # Surface 2
    print(f"║                                                          ║")
    print(f"║  2. PyPI downloads                                       ║")
    pypi = get_pypi_downloads()
    if "error" in pypi:
        print(f"║     {pypi['error']:<52} ║")
    else:
        print(f"║     Last day:   {str(pypi['last_day']):<40} ║")
        print(f"║     Last week:  {str(pypi['last_week']):<40} ║")
        print(f"║     Last month: {str(pypi['last_month']):<40} ║")

    # Surface 3
    print(f"║                                                          ║")
    print(f"║  3. GitHub stats                                         ║")
    gh = get_github_stats()
    print(f"║     Stars:       {str(gh['stars']):<39} ║")
    print(f"║     Forks:       {str(gh['forks']):<39} ║")
    print(f"║     Clones (14d): {str(gh['clones_14d']):<38} ║")

    # Surface 4
    print(f"║                                                          ║")
    print(f"║  4. Smithery registry                                    ║")
    smithery = get_smithery_installs()
    print(f"║     Installs: {str(smithery):<42} ║")

    print(f"║                                                          ║")
    print(f"╚══════════════════════════════════════════════════════════╝")


if __name__ == "__main__":
    main()
