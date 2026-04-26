"""Audit writer."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AuditLog, User


async def write_audit(db: AsyncSession, user: User | None, action: str, resource_type: str, resource_id: str | None = None, details: dict[str, Any] | None = None) -> AuditLog:
    log = AuditLog(
        tenant_id=user.tenant_id if user else "default",
        actor_user_id=user.user_id if user else None,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details or {},
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log
