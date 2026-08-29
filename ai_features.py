"""Optional cross-platform AI explanation for deterministic CSV analysis results."""
from __future__ import annotations

import json

from ai_platform import AIClient


def explain_report(report: dict[str, object], client: AIClient) -> str:
    if not isinstance(report, dict) or not report:
        raise ValueError("Report must be a non-empty dictionary.")
    system = (
        "You are a business-data analyst. Explain only the supplied computed metrics, distinguish "
        "observations from recommendations, and do not invent trends or causal claims not supported by data."
    )
    return client.generate(system, json.dumps(report, ensure_ascii=False, default=list))
