import uuid

from sqlalchemy import select

from core.models import Alert, AlertRule, Watchlist


class AlertStore:
    def __init__(self, db):
        self.db = db

    async def create_watchlist(self, tenant_id: str, case_id: str, name: str, terms: list[str], entity_ids: list[str], created_by: str):
        w = Watchlist(watchlist_id=f'WL-{uuid.uuid4().hex[:10]}', tenant_id=tenant_id, case_id=case_id, name=name, terms=terms, entity_ids=entity_ids, created_by=created_by)
        self.db.add(w); await self.db.commit(); await self.db.refresh(w); return w

    async def list_watchlists(self, tenant_id: str):
        r = await self.db.execute(select(Watchlist).where(Watchlist.tenant_id == tenant_id)); return list(r.scalars().all())

    async def create_rule(self, tenant_id: str, name: str, scope: str, rule_type: str, threshold: float, enabled: bool, metadata_json: dict):
        rule = AlertRule(rule_id=f'AR-{uuid.uuid4().hex[:10]}', tenant_id=tenant_id, name=name, scope=scope, rule_type=rule_type, threshold=threshold, enabled=enabled, metadata_json=metadata_json)
        self.db.add(rule); await self.db.commit(); await self.db.refresh(rule); return rule

    async def get_rule(self, tenant_id: str, rule_id: str):
        r = await self.db.execute(select(AlertRule).where(AlertRule.tenant_id == tenant_id, AlertRule.rule_id == rule_id)); return r.scalar_one_or_none()

    async def list_rules(self, tenant_id: str):
        r = await self.db.execute(select(AlertRule).where(AlertRule.tenant_id == tenant_id)); return list(r.scalars().all())

    async def list_alerts(self, tenant_id: str):
        r = await self.db.execute(select(Alert).where(Alert.tenant_id == tenant_id)); return list(r.scalars().all())

    async def create_alert(self, tenant_id: str, case_id: str, rule_id: str, title: str, severity: str, message: str, source_id: str, claim_id: str):
        a = Alert(alert_id=f'ALT-{uuid.uuid4().hex[:10]}', tenant_id=tenant_id, case_id=case_id, rule_id=rule_id, title=title, severity=severity, message=message, source_id=source_id, claim_id=claim_id)
        self.db.add(a); await self.db.commit(); await self.db.refresh(a); return a
