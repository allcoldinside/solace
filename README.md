# SOLACE

SOLACE is a FastAPI-based intelligence workflow service with PostgreSQL, Redis, Celery, and MinIO.

## Repository bootstrap (Ticket 1)
This repository includes:
- FastAPI application entrypoint (`api/main.py`)
- SQLAlchemy 2.0 async database setup (`core/database.py`)
- Alembic migration setup (`alembic.ini`, `alembic/env.py`)
- Celery app/tasks (`tasks/celery_app.py`)
- Docker Compose stack for API, PostgreSQL, Redis, worker, beat, and MinIO (`docker-compose.yml`)
- Pytest setup (`tests/`)

## Local development

1. Create an environment file:

```bash
cp .env.example .env
```

2. Set required secrets in `.env` (especially `SECRET_KEY`).

3. Start services:

```bash
docker compose up --build
```

4. Run migrations:

```bash
make migrate
```

5. Verify health endpoint:

```bash
curl http://localhost:8000/api/health
```

Expected response:

```json
{"status":"ok"}
```

## Common commands

```bash
make dev       # run API locally with uvicorn
make worker    # run celery worker
make beat      # run celery beat
make test      # run pytest
make lint      # run ruff
make migrate   # alembic upgrade head
make migration # create new migration
```

## Notes
- No secrets are hard-coded; use environment variables.
- Default Docker Compose values are for local development only.


## Source/document upload note
- Upload endpoint: `POST /api/cases/{case_id}/sources/upload`.
- Text extraction is implemented for `txt`, `md`, and basic `html`.
- PDF extraction currently uses a safe stub placeholder (`[pdf text extraction stub: parser not configured]`) pending selection of an approved parser.

- Uploads enqueue a document processing task that normalizes text and creates chunks with source offsets.

- Claims endpoints: `POST /api/cases/{case_id}/claims`, `GET /api/cases/{case_id}/claims`, `GET /api/cases/claims/{claim_id}/evidence`.

- Entity endpoints: `GET /api/cases/{case_id}/entities`, `GET /api/cases/{case_id}/relationships`, merge via `POST /api/cases/entities/{primary_entity_id}/merge/{duplicate_entity_id}`.

- Timeline endpoints: `POST /api/cases/{case_id}/timeline`, `GET /api/cases/{case_id}/timeline`, `POST /api/cases/{case_id}/timeline/generate`.

- Report export currently supports markdown via `/api/reports/{report_id}/export/markdown`; PDF/DOCX export is a follow-up item.

- Alerts endpoints: `/api/alerts/watchlists`, `/api/alerts/rules`, `/api/alerts`.

- Panel analysis endpoints: `POST /api/cases/{case_id}/panel-runs`, `GET /api/cases/{case_id}/panel-runs`, `GET /api/cases/panel-runs/{panel_run_id}/responses`, approval + conversion endpoints under `/api/cases/panel-runs/*`.

- Task/approval endpoints: `/api/tasks`, `/api/tasks/{task_id}`, `/api/tasks/approvals`, `/api/tasks/approvals/{approval_request_id}/decision`.

- LLM gateway uses `LLM_PROVIDER` (defaults to `mock`) and does not require external credentials for local tests.

- Dashboard MVP is available at `/api/dashboard` and provides login, cases, upload, claims/entities/timeline, report, tasks, alerts, and admin audit views.

- Security auditing records failed authorization/authentication responses as `auth.failure` and `authz.denied` audit events.
