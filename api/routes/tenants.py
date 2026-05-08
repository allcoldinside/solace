from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.schemas import MessageResponse, TenantCreateRequest
from security.deps import current_user, require_role
from storage.tenant_store import TenantStore

router = APIRouter(prefix='/tenants', tags=['tenants'])


@router.get('')
async def list_tenants(db: AsyncSession = Depends(get_db), _=Depends(require_role('admin'))):
    return await TenantStore(db).list_all()


@router.post('', response_model=MessageResponse)
async def create_tenant(
    payload: TenantCreateRequest,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role('admin')),
):
    await TenantStore(db).ensure_default(payload.tenant_id)
    return MessageResponse(message='tenant created')


@router.get('/{tenant_id}')
async def get_tenant(
    tenant_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(current_user),
):
    if user.role != 'admin' and user.tenant_id != tenant_id:
        raise HTTPException(status_code=403, detail='forbidden')
    t = await TenantStore(db).get(tenant_id)
    if not t:
        raise HTTPException(status_code=404, detail='not found')
    return t
