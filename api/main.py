"""FastAPI application entrypoint."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from api.middleware.errors import install_error_handlers
from api.middleware.observability import ObservabilityMiddleware
from api.routes import audit, auth, cases, entities, graph, health, maintenance, memory, metrics, panel, pipeline, reports, search, system, watches
from config.logging import configure_logging
from config.settings import get_settings
from core.database import close_db
from security.rate_limit import RateLimitMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers.setdefault("x-content-type-options", "nosniff")
        response.headers.setdefault("x-frame-options", "DENY")
        response.headers.setdefault("referrer-policy", "no-referrer")
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield
    await close_db()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.version, docs_url="/api/docs", redoc_url="/api/redoc", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(ObservabilityMiddleware)
    install_error_handlers(app)
    for router in (health.router, metrics.router, auth.router, pipeline.router, reports.router, panel.router, cases.router, watches.router, entities.router, memory.router, graph.router, search.router, audit.router, system.router, maintenance.router):
        app.include_router(router, prefix="/api")
    return app


app = create_app()
