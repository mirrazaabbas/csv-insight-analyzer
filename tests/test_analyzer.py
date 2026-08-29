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

    def test_validation_errors(self):
        with self.assertRaises(ValueError):
            analyzer.analyze_sales([])
        with self.assertRaises(ValueError):
            analyzer.to_float("not-a-number", 2)
        with self.assertRaises(ValueError):
            analyzer.analyze_sales([{"region": "", "product": "AI", "revenue": "10"}])

    def test_load_rows_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.csv"
            bad.write_text("region,revenue\nNorth,10\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                analyzer.load_rows(bad)


if __name__ == "__main__":
    unittest.main()
