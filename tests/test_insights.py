import unittest

import insights


class InsightTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"date": "2026-01-01", "revenue": "100", "units": "10", "region": "North"},
            {"date": "2026-01-02", "revenue": "200", "units": "20", "region": "South"},
            {"date": "2026-01-03", "revenue": "300", "units": "30", "region": "North"},
        ]

    def test_numeric_summary_and_correlations(self):
        self.assertEqual(insights.numeric_columns(self.rows), ["revenue", "units"])
        summary = insights.numeric_summary(self.rows)
        self.assertEqual(summary["revenue"]["mean"], 200.0)
        self.assertEqual(summary["units"]["median"], 20.0)
        correlations = insights.correlations(self.rows)
        self.assertEqual(len(correlations), 1)
        self.assertEqual(correlations[0]["correlation"], 1.0)
        self.assertEqual(correlations[0]["observations"], 3)

    def test_constant_or_short_series_has_no_correlation(self):
        constant = [
            {"a": "1", "b": "2"},
            {"a": "1", "b": "3"},
        ]
        self.assertEqual(insights.correlations(constant), [])
        self.assertIsNone(insights._pearson([1.0], [1.0]))
        self.assertIsNone(insights._pearson([1.0, 2.0], [1.0]))

    def test_time_series_summary(self):
        result = insights.time_series_summary(self.rows, "date", "revenue")
        self.assertEqual(result["periods"], 3)
        self.assertEqual(result["first_value"], 100.0)
        self.assertEqual(result["last_value"], 300.0)
        self.assertEqual(result["absolute_change"], 200.0)
        self.assertEqual(result["percent_change"], 200.0)

        duplicate_dates = [
            {"date": "01/01/2026", "value": "10"},
            {"date": "01/01/2026", "value": "5"},
            {"date": "02/01/2026", "value": "30"},
        ]
        aggregated = insights.time_series_summary(duplicate_dates, "date", "value")
        self.assertEqual(aggregated["points"][0]["value"], 15.0)

    def test_time_series_zero_base_and_validation(self):
        zero = [
            {"date": "2026/01/01", "value": "0"},
            {"date": "2026/01/02", "value": "10"},
        ]
        self.assertIsNone(insights.time_series_summary(zero, "date", "value")["percent_change"])
        with self.assertRaises(ValueError):
            insights.time_series_summary([], "date", "value")
        with self.assertRaises(ValueError):
            insights.time_series_summary(self.rows, "missing", "revenue")
        with self.assertRaises(ValueError):
            insights.time_series_summary(
                [{"date": "not-a-date", "value": "10"}], "date", "value"
            )
        with self.assertRaises(ValueError):
            insights._number("not-a-number")
        with self.assertRaises(ValueError):
            insights._date("not-a-date")

    def test_analyze_dataset(self):
        result = insights.analyze_dataset(
            self.rows,
            date_column="date",
            value_column="revenue",
        )
        self.assertEqual(result["profile"]["row_count"], 3)
        self.assertIn("numeric_summary", result)
        self.assertIn("correlations", result)
        self.assertIn("time_series", result)
        plain = insights.analyze_dataset(self.rows)
        self.assertNotIn("time_series", plain)
        with self.assertRaises(ValueError):
            insights.analyze_dataset([])
        with self.assertRaises(ValueError):
            insights.analyze_dataset(self.rows, date_column="date")


if __name__ == "__main__":
    unittest.main()
