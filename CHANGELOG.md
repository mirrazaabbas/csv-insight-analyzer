# Changelog

All notable changes to this project are documented here.

## 1.0.0 - 2026-08-30

### Added
- Generic CSV profiling with inferred column types, missingness and duplicate-row diagnostics.
- Numeric summaries for all fully numeric columns.
- Pearson correlation ranking across numeric column pairs.
- Optional date/value time-series aggregation with absolute and percentage change.
- Safe JSON and escaped standalone HTML reports.
- Installable `csv-insights` CLI.
- Python 3.10-3.12 CI with coverage, generic-profile smoke tests, package build and installed-wheel verification.
- CodeQL, dependency auditing, CycloneDX SBOM generation and provenance-backed tagged releases.

### Changed
- CSV loading now rejects malformed rows that contain more values than header columns.
- Sales analysis now reports both regional and product revenue breakdowns.
