"""Dependency-free data-quality diagnostics for CSV-like row dictionaries."""
from __future__ import annotations

from collections import Counter
from statistics import mean, pstdev
from typing import Any


def infer_type(values: list[str]) -> str:
    cleaned = [value.strip() for value in values if value is not None and str(value).strip()]
    if not cleaned:
        return "empty"
    numeric = 0
    for value in cleaned:
        try:
            float(value.replace(",", ""))
            numeric += 1
        except (ValueError, AttributeError):
            pass
    if numeric == len(cleaned):
        return "number"
    lowered = {value.lower() for value in cleaned}
    if lowered <= {"true", "false", "yes", "no", "0", "1"}:
        return "boolean"
    return "text"


def missingness(rows: list[dict[str, Any]]) -> dict[str, float]:
    if not rows:
        return {}
    columns = sorted({key for row in rows for key in row})
    result: dict[str, float] = {}
    for column in columns:
        missing = sum(1 for row in rows if row.get(column) is None or str(row.get(column)).strip() == "")
        result[column] = missing / len(rows)
    return result


def duplicate_count(rows: list[dict[str, Any]]) -> int:
    canonical = [tuple(sorted((key, str(value)) for key, value in row.items())) for row in rows]
    counts = Counter(canonical)
    return sum(count - 1 for count in counts.values() if count > 1)


def numeric_outliers(values: list[float], z_threshold: float = 3.0) -> list[float]:
    if z_threshold <= 0:
        raise ValueError("z_threshold must be positive.")
    if len(values) < 2:
        return []
    sigma = pstdev(values)
    if sigma == 0:
        return []
    center = mean(values)
    return [value for value in values if abs((value - center) / sigma) > z_threshold]


def profile(rows: list[dict[str, Any]]) -> dict[str, object]:
    columns = sorted({key for row in rows for key in row})
    inferred: dict[str, str] = {}
    for column in columns:
        inferred[column] = infer_type([str(row.get(column, "")) for row in rows])
    return {
        "row_count": len(rows),
        "column_count": len(columns),
        "columns": columns,
        "inferred_types": inferred,
        "missingness": missingness(rows),
        "duplicate_rows": duplicate_count(rows),
    }
