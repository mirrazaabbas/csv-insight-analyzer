# AI platform compatibility

The CSV analyzer computes all metrics locally and works with no model provider. An optional AI explanation layer uses the shared `AIClient` interface with OpenAI/OpenAI-compatible APIs, Anthropic Claude, or Google Gemini.

## Offline verification

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python analyzer.py sample_sales.csv
```

No API key is required for these checks.

## Provider selection

```bash
# OpenAI or OpenAI-compatible
export AI_PROVIDER=openai
export AI_API_KEY="YOUR_KEY"
export AI_MODEL="YOUR_CHAT_MODEL"
# Optional: export AI_BASE_URL="https://provider.example/v1"
```

```bash
# Anthropic Claude
export AI_PROVIDER=anthropic
export AI_API_KEY="YOUR_KEY"
export AI_MODEL="YOUR_CLAUDE_MODEL"
```

```bash
# Google Gemini
export AI_PROVIDER=gemini
export AI_API_KEY="YOUR_KEY"
export AI_MODEL="YOUR_GEMINI_MODEL"
```

## Run the optional AI explanation

```bash
python - <<'PY'
from pathlib import Path
from ai_features import explain_report
from ai_platform import create_ai_client
from analyzer import analyze_sales, load_rows

report = analyze_sales(load_rows(Path("sample_sales.csv")))
print(explain_report(report, create_ai_client()))
PY
```

The model receives only already-computed report metrics and is instructed not to invent unsupported trends or causal claims.
