from __future__ import annotations

import unittest
from unittest.mock import patch

import ai_features
import ai_platform


class FakeClient:
    def generate(self, system: str, user: str) -> str:
        self.system = system
        self.user = user
        return "Revenue is concentrated in the top reported region."


class AiFeatureTests(unittest.TestCase):
    def test_ai_report_explanation(self) -> None:
        client = FakeClient()
        report = {
            "rows": 2,
            "total_revenue": 300.0,
            "top_region": ("South", 200.0),
            "by_region": {"South": 200.0, "North": 100.0},
        }
        result = ai_features.explain_report(report, client)
        self.assertIn("Revenue", result)
        self.assertIn("total_revenue", client.user)
        with self.assertRaises(ValueError):
            ai_features.explain_report({}, client)

    def test_provider_response_shapes(self) -> None:
        cases = [
            ("openai", {"choices": [{"message": {"content": "openai ok"}}]}, "openai ok"),
            ("anthropic", {"content": [{"text": "claude ok"}]}, "claude ok"),
            (
                "gemini",
                {"candidates": [{"content": {"parts": [{"text": "gemini ok"}]}}]},
                "gemini ok",
            ),
        ]
        for provider, payload, expected in cases:
            client = ai_platform.HTTPAIClient(
                ai_platform.AIConfig(provider, "key", "model", "https://example.test")
            )
            with patch.object(client, "_post", return_value=payload):
                self.assertEqual(client.generate("system", "user"), expected)


if __name__ == "__main__":
    unittest.main()
