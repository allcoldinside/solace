"""Case routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import CaseCreateRequest
from security.deps import current_user
from storage.case_store import CaseStore

router = APIRouter(prefix="/cases", tags=["cases"])

@router.get("")
async def list_cases(db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> list[dict]:
    rows = await CaseStore(db).list(user.tenant_id)
    return [{"case_id": r.case_id, "title": r.title, "status": r.status, "created_at": r.created_at} for r in rows]

@router.post("")
async def create_case(payload: CaseCreateRequest, db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> dict:
    row = await CaseStore(db).create(user.tenant_id, payload.title, payload.description)
    return {"case_id": row.case_id, "title": row.title, "status": row.status}

@router.get("/{case_id}")
async def get_case(case_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)) -> dict:
    row = await CaseStore(db).get(user.tenant_id, case_id)
    if row is None:
        raise HTTPException(status_code=404, detail="case not found")
    return {"case_id": row.case_id, "title": row.title, "description": row.description, "status": row.status}
