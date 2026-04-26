from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.models import Report
from security.deps import current_user
router = APIRouter(prefix='/reports', tags=['reports'])
@router.get('')
async def list_reports(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    r = await db.execute(select(Report).where(Report.tenant_id == user.tenant_id)); return list(r.scalars().all())
@router.get('/{report_id}')
async def get_report(report_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    r = await db.execute(select(Report).where(Report.tenant_id == user.tenant_id, Report.report_id == report_id)); x = r.scalar_one_or_none()
    if not x: raise HTTPException(status_code=404, detail='not found')
    return x
