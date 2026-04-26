"""Metrics route."""

from fastapi import APIRouter, Response

from observability.metrics import metrics_response

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("")
async def metrics() -> Response:
    return Response(content=metrics_response(), media_type="text/plain; version=0.0.4")
