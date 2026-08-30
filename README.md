# CSV Insight Analyzer

[![CI](https://github.com/mirrazaabbas/csv-insight-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/mirrazaabbas/csv-insight-analyzer/actions/workflows/ci.yml)
[![Security](https://github.com/mirrazaabbas/csv-insight-analyzer/actions/workflows/security.yml/badge.svg)](https://github.com/mirrazaabbas/csv-insight-analyzer/actions/workflows/security.yml)

A dependency-free Python analytics project that combines a validated sales-report workflow with reusable CSV data-quality profiling, numeric summaries, correlations, time-series aggregation, and safe JSON/HTML reports.

## Implemented capabilities

### Sales analysis

- Validates the required `region`, `product`, and `revenue` schema.
- Rejects malformed rows and invalid numeric values.
- Computes total, mean and median revenue.
- Ranks top region and top product.
- Produces revenue breakdowns by region and product.

### Generic dataset profiling

- Row and column counts.
- Inferred numeric, boolean, text and empty column types.
- Per-column missingness.
- Duplicate-row counts.
- Numeric min/max/mean/median/population-standard-deviation summaries.
- Pearson correlations for usable numeric column pairs.
- Optional time-series aggregation for a selected date and numeric value column.
- Absolute and percentage change across the time series.

### Reporting and engineering quality

- Deterministic JSON output.
- Escaped standalone HTML output.
- Installable `csv-insights` command.
- Python 3.10-3.12 CI.
- Ruff linting and branch coverage gate.
- Package build and installed-wheel smoke tests.
- CodeQL, dependency auditing and CycloneDX SBOM generation.
- Provenance-backed tagged GitHub releases.

## Quick start

```bash
python -m pip install -e .
csv-insights sample_sales.csv
```

To write reports for the sales workflow:

```bash
csv-insights sample_sales.csv --json sales.json --html sales.html
```

For generic profiling:

```bash
csv-insights sample_sales.csv --profile --json profile.json --html profile.html
```

For a dataset with date and numeric value columns:

```bash
csv-insights data.csv --profile --date-column date --value-column revenue
```

The generic profiler does not require the sales-specific columns.

## Python API

```python
from pathlib import Path

from analyzer import load_rows
from insights import analyze_dataset

rows = load_rows(Path("data.csv"), required_columns=set())
report = analyze_dataset(rows)
print(report["profile"])
print(report["numeric_summary"])
print(report["correlations"])
```

## Data-quality behavior

The profiler is intentionally transparent and dependency-free. A column is classified as numeric only when every non-empty value can be parsed as a number. Correlations are reported only when at least two paired observations exist and both variables have non-zero variance.

Time-series parsing accepts ISO-style dates plus a small documented set of common date formats. Invalid dates or numeric values fail with a row-level validation message instead of being silently coerced.

## Quality gates

```bash
python -m pip install --upgrade pip -r requirements-dev.txt build
ruff check .
coverage run -m unittest discover -s tests -v
coverage report --fail-under=80
python analyzer.py sample_sales.csv
python analyzer.py sample_sales.csv --profile
python -m build
```

## Scope

This repository is a compact analytics engineering portfolio project, not a replacement for a full dataframe/statistics platform. Correlations are descriptive and do not imply causation. The project avoids invented business conclusions: it computes and reports only values supported by the supplied CSV.

## Skills demonstrated

Python · CSV Processing · Data Quality · Descriptive Statistics · Correlation Analysis · Time Series · Validation · JSON · HTML Reporting · Testing · CI/CD · CodeQL · SBOM · Packaging
