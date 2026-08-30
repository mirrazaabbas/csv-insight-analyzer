import tempfile
import unittest
from pathlib import Path

import analyzer


class CsvAnalyzerTests(unittest.TestCase):
    def test_analyze_sales(self):
        rows = [
            {"region": "North", "product": "AI", "revenue": "100"},
            {"region": "South", "product": "AI", "revenue": "200"},
        ]
        report = analyzer.analyze_sales(rows)
        self.assertEqual(report["rows"], 2)
        self.assertEqual(report["total_revenue"], 300.0)
        self.assertEqual(report["top_region"][0], "South")
        self.assertEqual(report["top_product"][0], "AI")
        self.assertEqual(report["by_product"]["AI"], 300.0)

    def test_validation_errors(self):
        with self.assertRaises(ValueError):
            analyzer.analyze_sales([])
        with self.assertRaises(ValueError):
            analyzer.to_float("not-a-number", 2)
        with self.assertRaises(ValueError):
            analyzer.analyze_sales([{"region": "", "product": "AI", "revenue": "10"}])
        with self.assertRaises(ValueError):
            analyzer.analyze_sales([{"region": "North", "product": "", "revenue": "10"}])

    def test_load_rows_schema_and_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            bad = folder / "bad.csv"
            bad.write_text("region,revenue\nNorth,10\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                analyzer.load_rows(bad)

            empty = folder / "empty.csv"
            empty.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                analyzer.load_rows(empty)

            valid = folder / "valid.csv"
            valid.write_text(
                "region,product,revenue\nNorth,AI,1200\n",
                encoding="utf-8",
            )
            rows = analyzer.load_rows(valid)
            self.assertEqual(rows[0]["region"], "North")

            generic = folder / "generic.csv"
            generic.write_text("date,value\n2026-01-01,10\n", encoding="utf-8")
            self.assertEqual(len(analyzer.load_rows(generic, required_columns=set())), 1)

            malformed = folder / "malformed.csv"
            malformed.write_text("region,product,revenue\nNorth,AI,1,200\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                analyzer.load_rows(malformed)

            with self.assertRaises(ValueError):
                analyzer.load_rows(folder / "missing.csv")

    def test_comma_separated_revenue(self):
        self.assertEqual(analyzer.to_float("1,250.50", 2), 1250.5)


if __name__ == "__main__":
    unittest.main()
