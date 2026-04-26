"""Revoked token storage."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import RevokedToken


class TokenStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def revoke(self, jti: str, tenant_id: str, expires_at: datetime | None = None) -> RevokedToken:
        token = RevokedToken(jti=jti, tenant_id=tenant_id, expires_at=expires_at)
        self.db.add(token)
        await self.db.commit()
        return token

    async def is_revoked(self, jti: str) -> bool:
        result = await self.db.execute(select(RevokedToken).where(RevokedToken.jti == jti))
        return result.scalar_one_or_none() is not None
