"""
Hosted HTTP entrypoint for librarian-mcp on Cloud Run.

Exposes two read-only tools (librarian_context, prose_provenance) via
streamable-http MCP transport.  Record/metrics/opt-in tools are intentionally
excluded from the hosted surface (local-only via pip).

Rate limiting: 60 req/min/IP via sliding-window middleware.
Logging: structured JSON (referrer, user-agent, tool, latency).

Usage:
    python -m librarian_mcp.hosted          # local dev
    gunicorn librarian_mcp.hosted:app       # production (Cloud Run)

Environment:
    PORT            — listen port (default 8080, Cloud Run sets this)
    RATE_LIMIT      — requests/min/IP (default 60)
"""

from __future__ import annotations

import json
import logging
import os
import time
from collections import defaultdict
from pathlib import Path
from typing import Annotated, Any, Optional

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, HTMLResponse, JSONResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from librarian_mcp.context import build_packet, log_context_query

logger = logging.getLogger("librarian-hosted")
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}',
)

PORT = int(os.environ.get("PORT", "8080"))
RATE_LIMIT = int(os.environ.get("RATE_LIMIT", "60"))

# ─── Rate limiter (sliding window per IP) ────────────────────────────────────

_request_log: dict[str, list[float]] = defaultdict(list)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Any) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = _request_log[client_ip]
        cutoff = now - 60.0
        _request_log[client_ip] = [t for t in window if t > cutoff]

        if len(_request_log[client_ip]) >= RATE_LIMIT:
            return JSONResponse(
                {"error": "rate_limited", "retry_after_seconds": 60},
                status_code=429,
                headers={"Retry-After": "60"},
            )
        _request_log[client_ip].append(now)
        return await call_next(request)


# ─── Referrer/UA logging middleware ───────────────────────────────────────────

class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Any) -> Response:
        start = time.time()
        response = await call_next(request)
        elapsed = time.time() - start
        logger.info(json.dumps({
            "path": str(request.url.path),
            "method": request.method,
            "referrer": request.headers.get("referer", ""),
            "user_agent": request.headers.get("user-agent", ""),
            "client_ip": request.client.host if request.client else "unknown",
            "status": response.status_code,
            "latency_ms": round(elapsed * 1000, 1),
        }))
        return response


# ─── Hosted MCP server (read-only subset) ────────────────────────────────────

hosted_mcp = FastMCP(
    "librarian-mcp-hosted",
    instructions=(
        "Hosted read-only Librarian MCP endpoint. "
        "Two tools: librarian_context (intent-aware canonical memory) and "
        "prose_provenance (drift detection). "
        "Romulator 9000 — Chapter 1: The Librarian — v0.2.0"
    ),
)


@hosted_mcp.tool()
def librarian_context(
    intent: Annotated[
        str,
        'Intent string or JSON list. Options: "" (base only), "canonical", '
        '"outreach", "architecture", "founder_voice", "benchmark", "operational". '
        'Pass a JSON array for union: \'["benchmark", "founder_voice"]\'',
    ] = "",
    max_tokens: Annotated[int, "Maximum token budget for the memory packet (default 16000)"] = 16_000,
) -> dict[str, Any]:
    """Load the canonical memory packet for a specific intent."""
    parsed_intent: str | list[str] = intent
    if intent.startswith("["):
        try:
            parsed_intent = json.loads(intent)
        except json.JSONDecodeError:
            pass
    result = build_packet(intent=parsed_intent, max_tokens=max_tokens)
    log_context_query(parsed_intent, result["token_count"])
    return result


def _load_text(path: str) -> str | None:
    p = Path(path)
    if not p.exists():
        return None
    try:
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _extract_sections(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip().startswith("#")]


def _find_missing_phrases(canonical: str, candidate: str, phrases: list[str]) -> tuple[list[str], list[str]]:
    missing, preserved = [], []
    canonical_lower, candidate_lower = canonical.lower(), candidate.lower()
    for phrase in phrases:
        pl = phrase.lower()
        if pl in canonical_lower and pl not in candidate_lower:
            missing.append(phrase)
        elif pl in canonical_lower:
            preserved.append(phrase)
    return missing, preserved


def _count_paragraphs(text: str) -> int:
    return len([p.strip() for p in text.split("\n\n") if p.strip()])


def _verdict_from_score(score: int) -> str:
    if score == 0:
        return "clean"
    if score < 5:
        return "minor"
    if score < 15:
        return "significant"
    return "severe"


@hosted_mcp.tool()
def prose_provenance(
    canonical_path: Annotated[str, "Path to the canonical (original/golden) version of the document"],
    candidate_path: Annotated[str, "Path to the candidate (new/revised) version to check against canonical"],
    doc_type: Annotated[str, "Document type: letter | scaffold | proposal | tribute | generic"] = "generic",
    keystones: Annotated[Optional[str], "JSON array of keystone phrases to check"] = None,
    canonical_numbers: Annotated[Optional[str], "JSON array of canonical numbers/values to verify"] = None,
) -> dict[str, Any]:
    """Deterministic drift detection between two versions of any document."""
    canonical_text = _load_text(canonical_path)
    if canonical_text is None:
        return {"error": f"Cannot read canonical file: {canonical_path}"}
    candidate_text = _load_text(candidate_path)
    if candidate_text is None:
        return {"error": f"Cannot read candidate file: {candidate_path}"}

    drift_score = 0
    ks_phrases: list[str] = []
    if keystones:
        try:
            ks_phrases = json.loads(keystones)
        except json.JSONDecodeError:
            ks_phrases = [k.strip() for k in keystones.split(",") if k.strip()]

    cn_values: list[str] = []
    if canonical_numbers:
        try:
            cn_values = json.loads(canonical_numbers)
        except json.JSONDecodeError:
            cn_values = [n.strip() for n in canonical_numbers.split(",") if n.strip()]

    ks_missing, ks_preserved = _find_missing_phrases(canonical_text, candidate_text, ks_phrases)
    drift_score += len(ks_missing) * 3
    cn_missing, cn_preserved = _find_missing_phrases(canonical_text, candidate_text, cn_values)
    drift_score += len(cn_missing) * 2

    canon_sections = _extract_sections(canonical_text)
    cand_sections = _extract_sections(candidate_text)
    sections_added = [s for s in cand_sections if s not in canon_sections]
    sections_removed = [s for s in canon_sections if s not in cand_sections]
    drift_score += len(sections_removed) * 2 + len(sections_added)

    canon_paras = _count_paragraphs(canonical_text)
    cand_paras = _count_paragraphs(candidate_text)
    para_delta = cand_paras - canon_paras
    if abs(para_delta) > 5:
        drift_score += abs(para_delta) // 3

    len_ratio = len(candidate_text) / max(len(canonical_text), 1)
    if len_ratio < 0.5 or len_ratio > 2.0:
        drift_score += 5

    return {
        "canonical_path": canonical_path,
        "candidate_path": candidate_path,
        "doc_type": doc_type,
        "drift_score": drift_score,
        "verdict": _verdict_from_score(drift_score),
        "keystones_missing": ks_missing,
        "keystones_preserved": ks_preserved,
        "canonical_numbers_missing": cn_missing,
        "canonical_numbers_preserved": cn_preserved,
        "sections_added": sections_added,
        "sections_removed": sections_removed,
        "paragraph_count_canonical": canon_paras,
        "paragraph_count_candidate": cand_paras,
        "paragraph_delta": para_delta,
        "length_ratio": round(len_ratio, 3),
        "version": "v0.2.0",
    }


# ─── REST API for the web playground ──────────────────────────────────────────

async def playground_api(request: Request) -> JSONResponse:
    """POST /api/playground — accepts pasted canonical content, returns a memory packet."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    intent = body.get("intent", "")
    max_tokens = body.get("max_tokens", 16000)
    result = build_packet(intent=intent, max_tokens=max_tokens)
    return JSONResponse(result)


async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "version": "v0.2.0", "chapter": "The Librarian"})


# ─── Static landing page ─────────────────────────────────────────────────────

HOSTED_DIR = Path(__file__).resolve().parent.parent.parent / "hosted"


async def landing_page(request: Request) -> Response:
    index_path = HOSTED_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    return HTMLResponse("<h1>Librarian MCP</h1><p>Landing page not built yet.</p>")


# ─── Starlette app assembly ──────────────────────────────────────────────────

routes = [
    Route("/", landing_page),
    Route("/health", health),
    Route("/api/playground", playground_api, methods=["POST"]),
]

if HOSTED_DIR.exists() and (HOSTED_DIR / "static").exists():
    routes.append(Mount("/static", StaticFiles(directory=str(HOSTED_DIR / "static")), name="static"))

app = Starlette(
    routes=routes,
    middleware=[
        Middleware(RequestLogMiddleware),
        Middleware(RateLimitMiddleware),
    ],
)

# Mount the MCP streamable-http transport at /mcp
mcp_app = hosted_mcp.streamable_http_app()
app.mount("/mcp", mcp_app)


def main() -> None:
    """Run the hosted server (dev mode)."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")


if __name__ == "__main__":
    main()
