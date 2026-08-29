# Security Policy

## Supported branch

The `main` branch is the actively maintained version of this portfolio project.

## Reporting a vulnerability

Do not publish credentials, private datasets, personal data, or actionable exploit details in a public issue. Use GitHub private vulnerability reporting when available. Otherwise, open a minimal issue without sensitive reproduction details until a private channel is established.

## Security principles

- Never commit API keys, tokens, passwords, or confidential datasets.
- Treat CSV files as untrusted input.
- Validate required columns and numeric fields before analysis.
- Reject malformed or incomplete data with clear errors instead of silently fabricating values.
- Keep sample data synthetic or intentionally public.
