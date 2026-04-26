"""Pipeline routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import PipelineRequest, PipelineResponse
from security.deps import current_user
from tasks.pipeline import run_pipeline

router = APIRouter(prefix="/pipeline", tags=["pipeline"])

@router.post("/run", response_model=PipelineResponse)
async def run(payload: PipelineRequest, db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> PipelineResponse:
    return await run_pipeline(db, payload, user)
