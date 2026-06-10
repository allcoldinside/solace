from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from security.audit import write_audit
from security.deps import current_user
from storage.case_store import CaseStore
from storage.entity_store import EntityStore, RelationshipStore

router = APIRouter(prefix='/cases', tags=['entities'])


@router.get('/{case_id}/entities')
async def list_entities(case_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')
    return await EntityStore(db).list_by_case(user.tenant_id, case_id)


@router.get('/{case_id}/relationships')
async def list_relationships(case_id: str, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')
    return await RelationshipStore(db).list_by_case(user.tenant_id, case_id)


@router.post('/entities/{primary_entity_id}/merge/{duplicate_entity_id}')
async def merge_entities(primary_entity_id: str, duplicate_entity_id: str, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    merged = await EntityStore(db).merge(user.tenant_id, primary_entity_id, duplicate_entity_id)
    if not merged:
        raise HTTPException(status_code=404, detail='entity not found')
    await write_audit(db, user.tenant_id, user.user_id, 'entity.merge', 'entity', primary_entity_id, {'duplicate_entity_id': duplicate_entity_id}, request=request)
    return merged
