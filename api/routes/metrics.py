from fastapi import APIRouter, Response
from observability.metrics import render_metrics
router = APIRouter(tags=['metrics'])
@router.get('/metrics')
async def metrics(): return Response(render_metrics(), media_type='text/plain; version=0.0.4')
