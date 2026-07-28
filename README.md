# SOLACE

**SOLACE** is a production-oriented open-source intelligence platform. It collects, enriches, and analyses data about organisations, persons, and infrastructure, then produces structured threat intelligence reports with panel analysis and autonomous follow-up tasks.

## Quick start

```bash
cp .env.example .env
# Edit .env – set SECRET_KEY to a 32+ character random string

pip install -r requirements.txt
make migrate        # create/upgrade database schema via Alembic
make dev            # uvicorn api.main:app --reload on :8000
```

## Architecture

```
solace/
├── api/            FastAPI app + routes + middleware
├── config/         Settings, logging, secrets helpers
├── core/           DB engine, ORM models, Pydantic schemas, invariants
├── security/       JWT auth, deps, passwords, rate limiting, audit
├── storage/        Async SQLAlchemy stores (one per domain)
├── collectors/     BaseCollector + SeedCollector + spider stubs
├── nlp/            Enrichment pipeline
├── intelligence/   Entity resolution
├── reports/        ReportData schema + generator
├── graph/          Graph ingest stub
├── memory/         Memory persistence service
├── agents/         Autonomous task generator
├── panel/          Panel engine + session state + models
├── alerts/         Alert evaluation engine
├── tasks/          Celery app + pipeline task + priority queues
├── observability/  Prometheus metrics + trace ID
├── search/         Cross-model search engine
├── dashboard/      TypeScript API client
└── tests/          pytest test suite
```

## API endpoints

| Method | Path | Auth |
|--------|------|------|
| POST | /api/auth/register | public |
| POST | /api/auth/login | public |
| POST | /api/auth/refresh | public |
| GET | /api/auth/me | bearer |
| POST | /api/auth/logout | bearer |
| POST | /api/pipeline/run | bearer |
| GET | /api/reports | bearer |
| GET | /api/reports/{report_id} | bearer |
| GET | /api/panel | bearer |
| GET | /api/panel/{session_id} | bearer |
| GET/POST | /api/cases | bearer |
| GET | /api/cases/{case_id} | bearer |
| GET/POST | /api/watches | bearer |
| GET | /api/watches/{watch_id} | bearer |
| GET | /api/entities | bearer |
| GET | /api/memory | bearer |
| GET | /api/graph | bearer |
| GET | /api/search | bearer |
| GET | /api/audit | admin bearer |
| GET | /api/system/info | public |
| GET | /api/health | public |
| GET | /api/metrics | public (Prometheus) |
| GET | /api/maintenance | public |

## Workers

```bash
make worker        # default + low priority queues
make worker-high   # high + critical priority queues
```

## Migrations

```bash
make migration msg="describe change"   # generate revision
make migrate                           # apply to DB
```

## Tests

```bash
make test          # pytest -v
```

## Docker

```bash
# Development
docker compose up

# Production
cp .env.example .env  # set SECRET_KEY, DATABASE_URL
make prod-up
make prod-logs
```

## Security

- Passwords: bcrypt (pure C, no cffi/cryptography dependency)
- Tokens: HMAC-SHA256 JWT (HS256, pure Python stdlib – no cryptography package needed)
- Claims: `sub`, `tenant_id`, `role`, `type`, `jti`, `iat`, `exp`
- Token revocation: persisted `jti` blacklist in the database
- Rate limiting: in-process sliding window middleware (swap for Redis in production)
- Audit log: auth events written to `audit_logs` table

## Enterprise / multi-tenant

Each resource is scoped by `tenant_id`. Register users with a `tenant_id` claim; all reads/writes are automatically filtered. Defaults to `"default"` for single-tenant local mode.

## Limitations / known gaps

- JWT uses in-process HMAC with no cross-node revocation; upgrade `storage/token_store.py` for Redis-backed revocation on multi-worker deployments
- Rate limiter is in-process; replace `RateLimitMiddleware` with a Redis-backed implementation for multi-worker
- NLP enrichment and entity resolution are rule-based stubs; swap `nlp/pipeline.py` and `intelligence/entity_resolution.py` for real models
- Graph ingest is a stub in `graph/builder.py`; wire to Neo4j / NetworkX as needed
- Panel analysis returns a two-turn stub; wire `panel/engine.py` to real LLM agents
- Spider collectors beyond `SeedCollector` require external API credentials
