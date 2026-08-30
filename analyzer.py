import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

from insights import analyze_dataset
from reporting import to_html, to_json

REQUIRED_COLUMNS = {"region", "product", "revenue"}


def load_rows(path: Path, required_columns: set[str] | None = None) -> list[dict[str, str]]:
    required = REQUIRED_COLUMNS if required_columns is None else required_columns
    try:
        with path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                raise ValueError("CSV file has no header row.")
            missing = required - set(reader.fieldnames)
            if missing:
                raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
            rows = list(reader)
            if any(None in row for row in rows):
                raise ValueError("CSV contains rows with more values than header columns.")
            return rows
    except FileNotFoundError as exc:
        raise ValueError(f"CSV file not found: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"CSV file is not valid UTF-8: {path}") from exc


def to_float(value: str, row_number: int) -> float:
    try:
        return float(value.replace(",", "").strip())
    except (AttributeError, ValueError) as exc:
        raise ValueError(f"Invalid revenue value on data row {row_number}: {value!r}") from exc


def analyze_sales(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        raise ValueError("The CSV file contains no data rows.")

    revenues: list[float] = []
    by_region: dict[str, float] = defaultdict(float)
    by_product: dict[str, float] = defaultdict(float)

    for index, row in enumerate(rows, start=2):
        region = (row.get("region") or "").strip()
        product = (row.get("product") or "").strip()
        if not region or not product:
            raise ValueError(f"Missing region or product on CSV row {index}.")
        revenue = to_float(row.get("revenue", ""), index)
        revenues.append(revenue)
        by_region[region] += revenue
        by_product[product] += revenue

    top_region = max(by_region.items(), key=lambda item: item[1])
    top_product = max(by_product.items(), key=lambda item: item[1])
    return {
        "rows": len(rows),
        "total_revenue": sum(revenues),
        "average_revenue": statistics.mean(revenues),
        "median_revenue": statistics.median(revenues),
        "top_region": top_region,
        "top_product": top_product,
        "by_region": dict(sorted(by_region.items(), key=lambda item: item[1], reverse=True)),
        "by_product": dict(sorted(by_product.items(), key=lambda item: item[1], reverse=True)),
    }


def print_report(report: dict[str, object]) -> None:
    print("\nCSV Insight Analyzer")
    print("--------------------")
    print(f"Rows analyzed: {report['rows']}")
    print(f"Total revenue: ${report['total_revenue']:,.2f}")
    print(f"Average revenue per row: ${report['average_revenue']:,.2f}")
    print(f"Median revenue per row: ${report['median_revenue']:,.2f}")
    top_region = report["top_region"]
    top_product = report["top_product"]
    print(f"Top region: {top_region[0]} (${top_region[1]:,.2f})")
    print(f"Top product: {top_product[0]} (${top_product[1]:,.2f})")
    print("\nRevenue by region:")
    for region, revenue in report["by_region"].items():
        print(f"- {region}: ${revenue:,.2f}")


def _write_reports(report: dict[str, object], json_path: Path | None, html_path: Path | None) -> None:
    if json_path:
        json_path.write_text(to_json(report) + "\n", encoding="utf-8")
    if html_path:
        html_path.write_text(to_html(report), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a sales CSV or profile a general CSV dataset.")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--profile", action="store_true", help="run generic dataset profiling instead of the sales report")
    parser.add_argument("--date-column", help="date column for optional time-series analysis")
    parser.add_argument("--value-column", help="numeric value column for optional time-series analysis")
    parser.add_argument("--json", dest="json_path", type=Path, help="write a JSON report")
    parser.add_argument("--html", dest="html_path", type=Path, help="write an HTML report")
    args = parser.parse_args()
    try:
        if args.profile:
            rows = load_rows(args.csv_file, required_columns=set())
            report = analyze_dataset(
                rows,
                date_column=args.date_column,
                value_column=args.value_column,
            )
            print(to_json(report))
        else:
            if args.date_column or args.value_column:
                parser.error("--date-column/--value-column require --profile")
            report = analyze_sales(load_rows(args.csv_file))
            print_report(report)
        _write_reports(report, args.json_path, args.html_path)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
