# CSV Insight Analyzer

[![CI](https://github.com/mirrazaabbas/csv-insight-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/mirrazaabbas/csv-insight-analyzer/actions/workflows/ci.yml)

A dependency-free Python data-analysis and data-quality toolkit for validating CSV sales data, calculating business metrics, and profiling generic row-based datasets.

## Sales analytics

The original `analyzer.py` workflow includes:

- Required-column validation
- Revenue parsing with row-level errors
- Total revenue
- Average revenue
- Median revenue
- Top-performing region
- Top-performing product
- Revenue breakdown by region
- UTF-8 CSV handling
- CLI reporting

Required sales columns:

`region`, `product`, `revenue`

Additional columns such as `date` are allowed.

## Data-quality diagnostics

`data_quality.py` expands the project beyond sales aggregation with reusable profiling helpers:

- Automatic column collection
- Numeric type inference
- Boolean type inference
- Text type inference
- Empty-column detection
- Per-column missingness ratios
- Duplicate-row counting
- Population-standard-deviation-based numeric outlier detection
- Generic dataset profile containing row/column counts, inferred types, missingness and duplicates

The profiling layer works on ordinary `list[dict]` row structures and has no third-party runtime dependency.

## Run the sales analyzer

```bash
python analyzer.py sample_sales.csv
```

## Example data-quality profile

```python
import csv
import data_quality

with open("sample_sales.csv", newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

print(data_quality.profile(rows))
```

Numeric outlier checks are available independently:

```python
outliers = data_quality.numeric_outliers([10, 11, 12, 100], z_threshold=1.5)
```

## Quality checks

```bash
python -m pip install -r requirements-dev.txt
ruff check .
coverage run -m unittest discover -s tests -v
coverage report --fail-under=80
python analyzer.py sample_sales.csv
```

CI runs on Python 3.10–3.12 and covers both the business-metric analyzer and reusable data-quality diagnostics.

## Dependency maintenance

Dependabot is configured for weekly Python and GitHub Actions dependency updates.

## Current scope

The project intentionally keeps a dependency-free core. It does not claim a full pandas-style analytics platform, machine-learning anomaly detector, or time-series forecasting engine. Visualization, large-file streaming, advanced date/time inference, correlation analysis, and richer HTML reporting remain optional extensions.

## Skills demonstrated

Python · CSV Processing · Data Validation · Data Quality · Type Inference · Missing-data Analysis · Duplicate Detection · Outlier Detection · Statistics · Business Metrics · CLI Design · Testing · CI/CD
