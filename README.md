# SOLACE v1

SOLACE is a multi-bot intelligence platform scaffold with:
- **24 collector bots** (`SPIDER-1..SPIDER-24`) for seed-capable collection.
- **8 panel analyst bots** (`ANALYST-ALPHA..ANALYST-HOTEL`) for structured review.
- FastAPI backend, async SQLAlchemy models, JWT auth, tenant-aware data access, Celery workers, and Prometheus metrics.

## Documentation Map
- [Architecture](ARCHITECTURE.md)
- [Installation](INSTALL.md)
- [Configuration](CONFIGURATION.md)
- [Usage](USAGE.md)
- [Collectors](COLLECTORS.md)
- [Panel System](PANEL.md)
- [Security](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [FAQ](FAQ.md)

## Quick Start
```bash
cp .env.example .env
pip install -r requirements.txt
python -m compileall .
pytest -q
uvicorn api.main:app --reload
```

OpenAPI docs: `http://localhost:8000/docs`

## Core Runtime Commands
```bash
# API
uvicorn api.main:app --reload

# Worker (default/low)
celery -A tasks.celery_app.celery_app worker -Q default,low -l info

# Worker (high/critical)
celery -A tasks.celery_app.celery_app worker -Q high,critical -l info

# DB migration flow (manual, explicit)
make migration && make migrate
```
Boot:
- `uvicorn api.main:app --reload`
- `celery -A tasks.celery_app.celery_app worker -Q default,low -l info`

Migrations:
- `make migration && make migrate`

Endpoints are under `/api` including auth, pipeline, reports, panel, cases, watches, entities, memory, graph, search, audit, system, maintenance.
