# SOLACE v1 consolidation status

Branch: `solace-v1-consolidation`

The GitHub branch now contains the v1 backend consolidation directly, including:

- FastAPI backend at `api.main:app`
- canonical SQLAlchemy 2.0 ORM models
- canonical Pydantic v2 schemas
- async SQLAlchemy database setup
- JWT access and refresh token helpers
- bcrypt/PBKDF2 password hashing helper
- bearer auth dependencies and role guard
- token revocation store
- tenant-aware stores for reports, users, entities, cases, watches, panel sessions, tenants, audit, and tokens
- seed collector and aggregator
- lightweight NLP enrichment
- entity resolution
- report schema/generator and report invariants
- graph ingest stub
- memory service
- autonomy task generator
- deterministic panel engine
- alert engine stub
- Prometheus metrics and trace IDs
- Celery app with low/default/high/critical queues
- Dockerfile, Docker Compose, production Compose, Makefile, Alembic config/env/revision marker, CI workflow, tests, requirements, pyproject, env example, and VERSION

Connector limitation still observed:

- `dashboard/src/api/client.ts` was blocked by the GitHub connector safety guard even with harmless one-line content. The backend branch otherwise contains the v1 consolidation.

Validation performed in the execution workspace before GitHub writeout:

```bash
python -m compileall .
pytest -q
```

The branch should be validated again in GitHub CI after dependency installation.
