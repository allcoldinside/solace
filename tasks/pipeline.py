import time
from sqlalchemy.ext.asyncio import AsyncSession
from collectors.seed_collector import SeedCollector
from collectors.aggregator import aggregate
from nlp.pipeline import enrich_items
from intelligence.entity_resolution import resolve_entities
from reports.generator import generate_report
from core.invariants import validate_report
from graph.builder import ingest_graph
from memory.service import save_memory
from agents.autonomy import generate_autonomous_tasks
from panel.engine import analyze_panel
from alerts.engine import evaluate_alerts
from observability.metrics import pipeline_duration, pipeline_success, pipeline_failure, panel_turn_counter
from core.models import Report, AutonomousTask
from storage.entity_store import EntityStore
from storage.panel_store import PanelStore


async def run_pipeline(db: AsyncSession, tenant_id: str, target: str, target_type: str) -> dict:
    start = time.perf_counter()
    try:
        collected = await SeedCollector().collect(target, target_type)
        aggregated = aggregate(collected)
        raw_store = aggregated
        enriched = enrich_items(raw_store)
        entities = resolve_entities(enriched)
        report = generate_report(target, target_type, enriched, entities)
        graph_info = ingest_graph(entities, report.report_id)
        validate_report(report)

        db_report = Report(
            report_id=report.report_id, tenant_id=tenant_id, subject=report.subject,
            subject_type=report.subject_type, classification=report.classification,
            confidence=report.confidence, confidence_score=report.confidence_score,
            full_markdown=report.full_markdown, payload=report.__dict__,
        )
        db.add(db_report); await db.commit()

        entity_store = EntityStore(db)
        for e in entities:
            await entity_store.upsert(tenant_id=tenant_id, name=e['name'], kind=e['kind'], confidence=e['confidence'])

        await save_memory(db, tenant_id, report.report_id, report.executive_summary, {'graph': graph_info})

        tasks = generate_autonomous_tasks(report.report_id)
        for t in tasks:
            db.add(AutonomousTask(tenant_id=tenant_id, task_id=t['task_id'], report_id=report.report_id, kind=t['kind'], payload=t))
        await db.commit()

        panel = analyze_panel(report)
        panel_turn_counter.inc(len(panel['transcript']))
        session = await PanelStore(db).create(tenant_id, report.report_id, panel['summary'], panel['transcript'])
        alerts = evaluate_alerts(report)

        pipeline_success.inc()
        pipeline_duration.observe(time.perf_counter() - start)
        return {'report_id': report.report_id, 'session_id': session.session_id, 'entities_saved': len(entities), 'alerts': alerts}
    except Exception:
        pipeline_failure.inc()
        pipeline_duration.observe(time.perf_counter() - start)
        raise
