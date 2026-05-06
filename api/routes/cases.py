from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import CaseCreateRequest, CaseUpdateRequest
from security.audit import write_audit
from security.deps import current_user
from storage.case_store import CaseStore

router = APIRouter(prefix='/cases', tags=['cases'])


@router.get('')
async def list_cases(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    return await CaseStore(db).list(user.tenant_id)


@router.post('')
async def create_case(payload: CaseCreateRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).create(
        user.tenant_id,
        payload.title,
        payload.description,
        user.user_id,
        payload.priority,
        payload.assigned_to,
    )
    await write_audit(db, user.tenant_id, user.user_id, 'case.create', 'case', case.case_id, {'title': payload.title}, request=request)
    return case


@router.get('/{case_id}')
async def get_case(case_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    x = await CaseStore(db).get(user.tenant_id, case_id)
    if not x:
        raise HTTPException(status_code=404, detail='not found')
    return x


@router.patch('/{case_id}')
async def update_case(case_id: str, payload: CaseUpdateRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='not found')
    updates = payload.model_dump(exclude_none=True)
    updated = await CaseStore(db).update(case, **updates)
    action = 'case.archive' if updates.get('status') == 'archived' else 'case.update'
    await write_audit(db, user.tenant_id, user.user_id, action, 'case', case.case_id, {'updates': updates}, request=request)
    return updated


@router.delete('/{case_id}')
async def delete_case(case_id: str, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='not found')
    await CaseStore(db).delete(case)
    await write_audit(db, user.tenant_id, user.user_id, 'case.delete', 'case', case_id, {}, request=request)
    return {'message': 'deleted'}
