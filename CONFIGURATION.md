# Configuration

SOLACE uses environment-driven configuration from `.env` (via `pydantic-settings`).

## Required (minimum)
```bash
SECRET_KEY=change-this-secret-in-prod-32-chars-min
DATABASE_URL=sqlite+aiosqlite:///./solace.db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Common Options
```bash
APP_NAME=SOLACE
ENV=dev
API_PREFIX=/api
ACCESS_TOKEN_EXP_MINUTES=30
REFRESH_TOKEN_EXP_MINUTES=10080
RATE_LIMIT_PER_MINUTE=120
DEFAULT_TENANT_ID=default
```

## Production Notes
- Replace SQLite with Postgres via `DATABASE_URL`.
- Rotate `SECRET_KEY` securely.
- Restrict CORS origins to explicit trusted domains.
- Run migrations manually (`make migration && make migrate`), not at app startup.
