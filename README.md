# SOLACE (Foundation)

This repository contains the resolved SOLACE foundation after reconciling branch differences for:

- `README.md`
- `config/settings.py`
- `core/schemas.py`
- `tests/test_solace.py`

## Included foundation modules

- environment + secret loading (`config/settings.py`)
- structured JSON logging (`config/logging.py`)
- core enums and schemas (`core/schemas.py`)
- base async collector primitives (`collectors/base_collector.py`)
- collection aggregation logic (`collectors/aggregator.py`)
- report ID and markdown schema helpers (`reports/schema.py`)
- panel prompts, loop detection, and session state (`panel/`)
- baseline test suite (`tests/test_solace.py`)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```
