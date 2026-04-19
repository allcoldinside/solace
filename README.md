# SOLACE (Scaffold)

This repository now contains an initial SOLACE scaffold implementing:

- Environment settings (`config/settings.py`)
- Structured logging helpers (`config/logging.py`)
- Core enums + schemas (`core/schemas.py`)
- Aggregation logic (`collectors/aggregator.py`)
- Report ID and markdown schema helpers (`reports/schema.py`)
- Baseline tests (`tests/test_solace.py`)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```
