# SOLACE v1

Boot:
- `uvicorn api.main:app --reload`
- `celery -A tasks.celery_app.celery_app worker -Q default,low -l info`

Migrations:
- `make migration && make migrate`

Endpoints are under `/api` including auth, pipeline, reports, panel, cases, watches, entities, memory, graph, search, audit, system, maintenance.
