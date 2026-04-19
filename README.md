# SOLACE (Foundation)

This repository now contains a stronger SOLACE foundation with:

- environment + secret loading (`config/settings.py`)
- structured JSON logging (`config/logging.py`)
- core enums/schemas (`core/schemas.py`)
- base async collector primitives (`collectors/base_collector.py`)
- collector aggregation logic (`collectors/aggregator.py`)
- report ID + markdown schema helpers (`reports/schema.py`)
- panel prompts, loop detection, and session state (`panel/`)
- expanded baseline tests (`tests/test_solace.py`)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```
