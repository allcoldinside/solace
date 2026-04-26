# SOLACE Architecture

## Topology
- **API layer:** `api/` FastAPI app with route modules under `/api`.
- **Security layer:** JWT auth, bearer dependencies, revocation checks, rate limit middleware.
- **Data layer:** async SQLAlchemy models/stores in `core/` + `storage/`.
- **Intelligence pipeline:** `tasks/pipeline.py` orchestration.
- **Scale/runtime:** Celery + Redis queueing (`low/default/high/critical`).
- **Observability:** Prometheus counters/histograms and trace ID middleware.

## Canonical Pipeline Order
1. collect (24 collector bots)
2. aggregate
3. raw store (in-memory handoff in scaffold)
4. enrich
5. entity resolution
6. graph ingest
7. report generation
8. report invariant validation
9. save report
10. save entities
11. save memory
12. generate autonomous tasks
13. panel analysis (8 analyst bots)
14. save panel session
15. alert evaluation
16. metrics emission
17. return result

## Multi-bot Systems
### Collector system (24)
`collectors.COLLECTOR_BOT_IDS = SPIDER-1..SPIDER-24`

### Panel system (8)
`panel.models.PANEL_BOT_IDS = ANALYST-ALPHA..ANALYST-HOTEL`

## Data Model Summary
Core SQLAlchemy entities:
- Tenant, User
- Report, PanelSessionRecord
- Case, WatchRecord
- Entity, MemoryEntry
- AutonomousTask, CollectionJob
- AuditLog, RevokedToken

## Deployment Shapes
- **Local dev:** API + Redis (compose)
- **Prod-like:** API + worker(default/low) + worker(high/critical) + Redis
