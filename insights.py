"""Dependency-free numeric, correlation, and time-series insights for CSV rows."""
from __future__ import annotations

import math
import statistics
from collections import defaultdict
from datetime import date, datetime
from itertools import combinations
from typing import Any

import data_quality

DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%m/%d/%Y")


def _number(value: Any) -> float:
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(f"not a numeric value: {value!r}") from exc


def _date(value: Any) -> date:
    text = str(value).strip()
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        pass
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"unsupported date value: {value!r}")


def numeric_columns(rows: list[dict[str, Any]]) -> list[str]:
    profile = data_quality.profile(rows)
    inferred = profile["inferred_types"]
    return sorted(column for column, kind in inferred.items() if kind == "number")


def numeric_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    result: dict[str, dict[str, float | int]] = {}
    for column in numeric_columns(rows):
        values = [
            _number(row[column])
            for row in rows
            if row.get(column) is not None and str(row.get(column)).strip()
        ]
        if not values:
            continue
        result[column] = {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "stddev": statistics.pstdev(values) if len(values) > 1 else 0.0,
        }
    return result


def _pearson(left: list[float], right: list[float]) -> float | None:
    if len(left) != len(right) or len(left) < 2:
        return None
    left_mean = statistics.mean(left)
    right_mean = statistics.mean(right)
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right, strict=True))
    left_sq = sum((a - left_mean) ** 2 for a in left)
    right_sq = sum((b - right_mean) ** 2 for b in right)
    denominator = math.sqrt(left_sq * right_sq)
    if denominator == 0:
        return None
    return numerator / denominator


def correlations(rows: list[dict[str, Any]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for left_name, right_name in combinations(numeric_columns(rows), 2):
        pairs = [
            (_number(row[left_name]), _number(row[right_name]))
            for row in rows
            if row.get(left_name) is not None
            and str(row.get(left_name)).strip()
            and row.get(right_name) is not None
            and str(row.get(right_name)).strip()
        ]
        coefficient = _pearson([pair[0] for pair in pairs], [pair[1] for pair in pairs])
        if coefficient is not None:
            output.append(
                {
                    "left": left_name,
                    "right": right_name,
                    "correlation": round(coefficient, 6),
                    "observations": len(pairs),
                }
            )
    return sorted(output, key=lambda row: abs(float(row["correlation"])), reverse=True)


def time_series_summary(
    rows: list[dict[str, Any]],
    date_column: str,
    value_column: str,
) -> dict[str, object]:
    if not rows:
        raise ValueError("time-series analysis requires rows")
    if date_column not in rows[0] or value_column not in rows[0]:
        raise ValueError("time-series columns must exist in the dataset")
    totals: dict[date, float] = defaultdict(float)
    for row_number, row in enumerate(rows, 2):
        try:
            when = _date(row.get(date_column, ""))
            value = _number(row.get(value_column, ""))
        except ValueError as exc:
            raise ValueError(f"invalid time-series value on CSV row {row_number}: {exc}") from exc
        totals[when] += value
    points = [{"date": key.isoformat(), "value": totals[key]} for key in sorted(totals)]
    first = float(points[0]["value"])
    last = float(points[-1]["value"])
    absolute_change = last - first
    pct_change = None if first == 0 else (absolute_change / first) * 100
    return {
        "date_column": date_column,
        "value_column": value_column,
        "points": points,
        "periods": len(points),
        "first_value": first,
        "last_value": last,
        "absolute_change": absolute_change,
        "percent_change": None if pct_change is None else round(pct_change, 4),
    }


def analyze_dataset(
    rows: list[dict[str, Any]],
    *,
    date_column: str | None = None,
    value_column: str | None = None,
) -> dict[str, object]:
    if not rows:
        raise ValueError("dataset contains no rows")
    if (date_column is None) != (value_column is None):
        raise ValueError("date_column and value_column must be provided together")
    result: dict[str, object] = {
        "profile": data_quality.profile(rows),
        "numeric_summary": numeric_summary(rows),
        "correlations": correlations(rows),
    }
    if date_column and value_column:
        result["time_series"] = time_series_summary(rows, date_column, value_column)
    return result
