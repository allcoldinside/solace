from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.schemas import CaseCreateRequest
from security.deps import current_user
from storage.case_store import CaseStore
router = APIRouter(prefix='/cases', tags=['cases'])
@router.get('')
async def list_cases(db: AsyncSession = Depends(get_db), user=Depends(current_user)): return await CaseStore(db).list(user.tenant_id)
@router.post('')
async def create_case(payload: CaseCreateRequest, db: AsyncSession = Depends(get_db), user=Depends(current_user)): return await CaseStore(db).create(user.tenant_id, payload.title, payload.description)
@router.get('/{case_id}')
async def get_case(case_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    x = await CaseStore(db).get(user.tenant_id, case_id)
    if not x: raise HTTPException(status_code=404, detail='not found')
    return x
