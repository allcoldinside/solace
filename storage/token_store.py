from sqlalchemy import select
from core.models import RevokedToken


class TokenStore:
    def __init__(self, db): self.db = db

    async def revoke(self, jti: str, tenant_id: str):
        self.db.add(RevokedToken(jti=jti, tenant_id=tenant_id))
        await self.db.commit()

    async def is_revoked(self, jti: str) -> bool:
        res = await self.db.execute(select(RevokedToken).where(RevokedToken.jti == jti))
        return res.scalar_one_or_none() is not None
