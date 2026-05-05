"""Tenant CRUD routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import TenantCreateRequest, TenantSchema
from security.deps import current_user, require_role
from storage.tenant_store import TenantStore

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.get("", response_model=list[TenantSchema])
async def list_tenants(db: AsyncSession = Depends(get_db), user=Depends(require_role("admin"))) -> list:
    from sqlalchemy import select
    from core.models import Tenant
    result = await db.execute(select(Tenant).order_by(Tenant.created_at.desc()))
    return list(result.scalars().all())


@router.post("", response_model=TenantSchema, status_code=201)
async def create_tenant(
    payload: TenantCreateRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role("admin")),
) -> TenantSchema:
    store = TenantStore(db)
    from sqlalchemy import select
    from core.models import Tenant
    existing = await db.execute(select(Tenant).where(Tenant.tenant_id == payload.tenant_id))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="tenant already exists")
    row = await store.create(payload.tenant_id, payload.name)
    return row


@router.get("/{tenant_id}", response_model=TenantSchema)
async def get_tenant(
    tenant_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role("admin")),
) -> TenantSchema:
    from sqlalchemy import select
    from core.models import Tenant
    result = await db.execute(select(Tenant).where(Tenant.tenant_id == tenant_id))
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="tenant not found")
    return row
