import uuid
from sqlalchemy import select
from core.models import User


class UserStore:
    def __init__(self, db): self.db = db

    async def create(self, email: str, hashed_password: str, role: str, tenant_id: str):
        obj = User(user_id=f'USER-{uuid.uuid4().hex[:10]}', email=email, hashed_password=hashed_password, role=role, tenant_id=tenant_id)
        self.db.add(obj)
        await self.db.commit(); await self.db.refresh(obj)
        return obj

    async def get_by_email(self, email: str):
        res = await self.db.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()
