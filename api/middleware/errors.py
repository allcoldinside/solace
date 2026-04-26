"""API error handling."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.errors import SolaceError


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(SolaceError)
    async def solace_error_handler(request: Request, exc: SolaceError):
        return JSONResponse(status_code=400, content={"detail": str(exc), "trace_id": getattr(request.state, "trace_id", None)})
