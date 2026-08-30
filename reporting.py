"""Safe machine-readable and standalone HTML reporting helpers."""
from __future__ import annotations

import html
import json
from typing import Any


def to_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True)


def to_html(report: dict[str, Any], *, title: str = "CSV Insight Report") -> str:
    payload = html.escape(to_json(report))
    safe_title = html.escape(title)
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        f"<title>{safe_title}</title>"
        "<style>body{font-family:system-ui,sans-serif;max-width:1100px;margin:40px auto;padding:0 20px;}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:8px;overflow:auto;}</style>"
        f"</head><body><h1>{safe_title}</h1><pre>{payload}</pre></body></html>"
    )
