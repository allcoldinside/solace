from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.middleware.errors import unhandled_exception_handler
from api.middleware.observability import ObservabilityMiddleware
from api.middleware.security_audit import SecurityAuditMiddleware
from config.logging import configure_logging
from config.settings import get_settings
from core.database import shutdown_db
from security.rate_limit import RateLimitMiddleware
from api.routes import alerts, auth, audit, cases, claims, dashboard, entities, graph, health, maintenance, memory, metrics, panel, panel_runs, pipeline, reports, search, sources, system, tasks, timeline, watches

settings = get_settings()
configure_logging()

@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await shutdown_db()

app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=['*'], allow_headers=['*'])
app.add_middleware(RateLimitMiddleware)
app.add_middleware(ObservabilityMiddleware)
app.add_middleware(SecurityAuditMiddleware)

@app.middleware('http')
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

for r in [health.router, metrics.router, auth.router, pipeline.router, reports.router, panel.router, panel_runs.router, dashboard.router, cases.router, claims.router, timeline.router, sources.router, alerts.router, tasks.router, watches.router, entities.router, memory.router, graph.router, search.router, audit.router, system.router, maintenance.router]:
    app.include_router(r, prefix='/api')
