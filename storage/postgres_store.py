from sqlalchemy import select


class PostgresStore:
    def __init__(self, db):
        self.db = db

    async def list_all(self, model, tenant_id: str):
        res = await self.db.execute(select(model).where(model.tenant_id == tenant_id))
        return list(res.scalars().all())
