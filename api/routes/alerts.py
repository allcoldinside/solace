from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import AlertRuleCreateRequest, AlertRuleUpdateRequest, WatchlistCreateRequest
from security.audit import write_audit
from security.deps import current_user
from storage.alert_store import AlertStore

router = APIRouter(prefix='/alerts', tags=['alerts'])


@router.post('/watchlists')
async def create_watchlist(payload: WatchlistCreateRequest, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    return await AlertStore(db).create_watchlist(user.tenant_id, payload.case_id, payload.name, payload.terms, payload.entity_ids, user.user_id)


@router.get('/watchlists')
async def list_watchlists(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    return await AlertStore(db).list_watchlists(user.tenant_id)


@router.post('/rules')
async def create_rule(payload: AlertRuleCreateRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    rule = await AlertStore(db).create_rule(user.tenant_id, payload.name, payload.scope, payload.rule_type, payload.threshold, payload.enabled, payload.metadata_json)
    await write_audit(db, user.tenant_id, user.user_id, 'alert_rule.create', 'alert_rule', rule.rule_id, {'rule_type': payload.rule_type}, request=request)
    return rule


@router.patch('/rules/{rule_id}')
async def update_rule(rule_id: str, payload: AlertRuleUpdateRequest, request: Request, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    rule = await AlertStore(db).get_rule(user.tenant_id, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail='rule not found')
    updates = payload.model_dump(exclude_none=True)
    for k, v in updates.items():
        setattr(rule, k, v)
    await db.commit(); await db.refresh(rule)
    await write_audit(db, user.tenant_id, user.user_id, 'alert_rule.update', 'alert_rule', rule_id, {'updates': updates}, request=request)
    return rule


@router.get('/rules')
async def list_rules(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    return await AlertStore(db).list_rules(user.tenant_id)


@router.get('')
async def list_alerts(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    return await AlertStore(db).list_alerts(user.tenant_id)
