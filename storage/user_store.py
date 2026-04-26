"""User persistence."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from security.passwords import hash_password, verify_password


class UserStore:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, email: str, password: str, tenant_id: str = "default", role: str = "analyst") -> User:
        user = User(email=email.lower(), password_hash=hash_password(password), tenant_id=tenant_id, role=role)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email.lower()))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: str) -> User | None:
        result = await self.db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self.get_by_email(email)
        if user and user.is_active and verify_password(password, user.password_hash):
            return user
        return None
