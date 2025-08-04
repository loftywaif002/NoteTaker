import json
import logging
import requests
from typing import Optional, Dict  # add at top if not already there
from config import settings
log = logging.getLogger("mcp-client")
MCP_TIMEOUT = 12  # seconds

def _safe_post(path: str, payload: dict):
    if not settings.MCP_BASE_URL:
        log.info("MCP_BASE_URL not set; skipping MCP call.")
        return None
    try:
        url = settings.MCP_BASE_URL.rstrip("/") + path
        r = requests.post(url, json=payload, timeout=MCP_TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log.warning("MCP call failed: %s", e)
        return None

def summarize_and_tag_stream(text: str):
    """
    Calls MCP /summarize and streams the JSON line by line.
    """
    resp = _safe_post("/summarize", {"text": text})
    if isinstance(resp, dict):
        def stream():
            yield "{\n"
            yield f'  "summary": "{resp.get("summary", "").replace("\"", "\\\"")}",\n'
            yield f'  "tags": {json.dumps(resp.get("tags") or [])}\n'
            yield "}\n"
        return stream()
    def fallback_stream():
        yield '{"summary": null, "tags": []}'
    return fallback_stream()


def index_note(note_id: str, text: str, metadata: Optional[Dict] = None):
    """
    Expected MCP /index response: { "ok": true }
    """
    metadata = metadata or {}
    resp = _safe_post("/index", {"id": note_id, "text": text, "metadata": metadata})
    return bool(resp and resp.get("ok"))

def delete_note_index(note_id: str):
    """
    Expected MCP /delete response: { "ok": true }
    """
    resp = _safe_post("/delete", {"id": note_id})
    return bool(resp and resp.get("ok"))

def semantic_search(query: str, k: int = 10):
    """
    Expected MCP /search response: { "results": [ {"id": "...", "score": 0.0}, ... ] }
    """
    resp = _safe_post("/search", {"query": query, "k": k})
    if not isinstance(resp, dict):
        return []
    return resp.get("results") or []
