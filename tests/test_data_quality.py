import unittest

import data_quality


class DataQualityTests(unittest.TestCase):
    def test_type_inference(self):
        self.assertEqual(data_quality.infer_type(["1", "2.5"]), "number")
        self.assertEqual(data_quality.infer_type(["yes", "no"]), "boolean")
        self.assertEqual(data_quality.infer_type(["north", "south"]), "text")
        self.assertEqual(data_quality.infer_type(["", " "]), "empty")

    def test_missingness_and_duplicates(self):
        rows = [
            {"region": "North", "revenue": "10"},
            {"region": "North", "revenue": "10"},
            {"region": "", "revenue": "20"},
        ]
        self.assertAlmostEqual(data_quality.missingness(rows)["region"], 1 / 3)
        self.assertEqual(data_quality.duplicate_count(rows), 1)

    def test_outliers_and_validation(self):
        self.assertEqual(data_quality.numeric_outliers([1, 1, 1]), [])
        outliers = data_quality.numeric_outliers([0, 0, 0, 100], z_threshold=1.5)
        self.assertEqual(outliers, [100])
        with self.assertRaises(ValueError):
            data_quality.numeric_outliers([1, 2], z_threshold=0)

    def test_profile(self):
        report = data_quality.profile([{"a": "1", "b": "x"}, {"a": "2", "b": ""}])
        self.assertEqual(report["row_count"], 2)
        self.assertEqual(report["inferred_types"]["a"], "number")
        self.assertEqual(report["duplicate_rows"], 0)


if __name__ == "__main__":
    unittest.main()
