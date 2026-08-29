# CSV Insight Analyzer

A dependency-free Python command-line tool for validating and summarizing sales CSV data into practical business metrics.

## Features

- Required-column validation
- Revenue parsing with clear row-level errors
- Total, average, and median revenue
- Top-performing region and product
- Revenue breakdown by region
- UTF-8 CSV handling
- Automated tests and CI

## Required columns

`region`, `product`, `revenue`

Additional columns such as `date` are allowed.

## Run

```bash
python analyzer.py sample_sales.csv
```

## Skills demonstrated

Python · CSV Processing · Data Validation · Statistics · Business Metrics · CLI Design
