import json
import unittest

from reporting import to_html, to_json


class ReportingTests(unittest.TestCase):
    def test_json_and_html_are_safe(self):
        report = {"title": "<script>alert(1)</script>", "value": 10}
        rendered_json = to_json(report)
        self.assertEqual(json.loads(rendered_json)["value"], 10)
        rendered_html = to_html(report, title="<Unsafe>")
        self.assertIn("&lt;Unsafe&gt;", rendered_html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", rendered_html)
        self.assertNotIn("<script>alert(1)</script>", rendered_html)


if __name__ == "__main__":
    unittest.main()
