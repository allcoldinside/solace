from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from storage.audit_store import AuditStore


async def write_audit(
    db: AsyncSession,
    tenant_id: str,
    actor_user_id: str,
    action: str,
    resource_type: str,
    resource_id: str,
    metadata_json: dict | None = None,
    request: Request | None = None,
):
    request_id = getattr(request.state, 'request_id', 'system') if request else 'system'
    ip_address = request.client.host if request and request.client else 'unknown'
    user_agent = request.headers.get('user-agent', 'unknown') if request else 'unknown'
    await AuditStore(db).create(
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        metadata_json=metadata_json or {},
        request_id=request_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
