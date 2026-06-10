import asyncio

from tasks.celery_app import celery_app
from core.database import SessionLocal
from alerts.rules import evaluate_alert_rules


@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def evaluate_alerts_task(self, tenant_id: str, case_id: str, source_id: str, claim_texts: list[str], entity_names: list[str], risk_score: float = 0.0):
    async def _run():
        async with SessionLocal() as db:
            created = await evaluate_alert_rules(db, tenant_id, case_id, source_id, claim_texts, entity_names, risk_score)
            return len(created)
    try:
        return asyncio.run(_run())
    except Exception as exc:
        raise self.retry(exc=exc)
