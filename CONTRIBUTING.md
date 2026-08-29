# Contributing

Contributions should keep CSV analysis deterministic, validated, and easy to verify.

1. Create a focused branch from `main`.
2. Add tests for parsing, validation, statistics, or reporting behavior changes.
3. Run `ruff check .`, the coverage-gated unit tests, and the sample CSV smoke test.
4. Never commit credentials, confidential datasets, or personal data.
5. Reject malformed data explicitly instead of inventing or silently coercing missing values.
6. In the pull request, explain what changed, why it changed, and how it was tested.
