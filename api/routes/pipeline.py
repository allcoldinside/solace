from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.schemas import PipelineRequest, PipelineResponse
from security.deps import current_user
from tasks.pipeline import run_pipeline

router = APIRouter(prefix='/pipeline', tags=['pipeline'])

@router.post('/run', response_model=PipelineResponse)
async def pipeline_run(payload: PipelineRequest, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    result = await run_pipeline(db, user.tenant_id, payload.target, payload.target_type.value)
    return PipelineResponse(report_id=result['report_id'], session_id=result['session_id'], entities_saved=result['entities_saved'])
