from core.models import Report, Entity
from sqlalchemy import select


async def search(db, tenant_id: str, q: str):
    out = []
    r = await db.execute(select(Report).where(Report.tenant_id == tenant_id, Report.subject.ilike(f'%{q}%')))
    out += [{'kind':'report','id':x.report_id,'title':x.subject,'score':0.8} for x in r.scalars().all()]
    e = await db.execute(select(Entity).where(Entity.tenant_id == tenant_id, Entity.name.ilike(f'%{q}%')))
    out += [{'kind':'entity','id':x.entity_id,'title':x.name,'score':0.7} for x in e.scalars().all()]
    return out
