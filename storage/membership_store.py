from sqlalchemy import select

from core.models import UserTenantMembership


class MembershipStore:
    def __init__(self, db):
        self.db = db

    async def add(self, user_id: str, tenant_id: str, role: str) -> UserTenantMembership:
        record = UserTenantMembership(user_id=user_id, tenant_id=tenant_id, role=role)
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def has_membership(self, user_id: str, tenant_id: str) -> bool:
        result = await self.db.execute(
            select(UserTenantMembership).where(
                UserTenantMembership.user_id == user_id,
                UserTenantMembership.tenant_id == tenant_id,
            )
        )
        return result.scalar_one_or_none() is not None
