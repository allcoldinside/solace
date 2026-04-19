# SOLACE — Architecture

System design, data flow, component interactions, and database schema.

---

## High-Level Data Flow

```
User Input (target + type)
        │
        ▼
┌───────────────────┐
│  Celery Task Queue│  ← Redis broker
│  (async pipeline) │
└────────┬──────────┘
         │
         ▼  ── concurrent via asyncio.gather() ──
┌────────────────────────────────────────────────┐
│           SPIDER BOT TEAM (8 bots)              │
│  SPIDER-1  SPIDER-2  SPIDER-3  SPIDER-4(Tor)   │
│  SPIDER-5  SPIDER-6  SPIDER-7  SPIDER-8        │
└────────────────────┬───────────────────────────┘
                     │ CollectionResult × 8
                     ▼
            ┌─────────────────┐
            │  AGGREGATOR BOT │
            │  SHA-256 dedup  │
            │  reliability ↑  │
            │  sort by score  │
            └────────┬────────┘
                     │ list[RawIntelItemSchema]
                     ▼
            ┌─────────────────┐
            │  NLP PIPELINE   │
            │  NER · sentiment│
            │  embeddings     │
            │  translation    │
            │  keywords       │
            └────────┬────────┘
                     │ list[EnrichedIntelItem]
                     ▼
            ┌─────────────────┐
            │  REPORT WRITER  │
            │  Claude: summary│
            │  Claude: findings│
            │  deterministic: │
            │  entity map,    │
            │  timeline,      │
            │  threat scoring │
            └────────┬────────┘
                     │ ReportData
         ┌───────────┼───────────────┐
         ▼           ▼               ▼
     PostgreSQL   MongoDB         Google Drive
     + pgvector   (raw items)    (native GDoc)
         │
         ▼  embed in pgvector
    ┌─────────────────┐
    │  PANEL ENGINE   │
    │  Claude/GPT/    │
    │  Gemini debate  │
    │  Loop detection │
    │  Synthesis      │
    └────────┬────────┘
             │ final_synthesis
         ┌───┴──────────────────┐
         ▼                      ▼
     PostgreSQL           Google Drive
     (session data)       (assessment)
         │
         ▼
    NOTIFICATION ROUTER
    TLP:RED  → Signal + Telegram + Discord
    TLP:AMBER → Telegram + Discord
    TLP:WHITE/GREEN → Discord topic channel
```

---

## Component Details

### Celery Pipeline

The full 11-step pipeline runs as a single Celery task:

```python
@celery_app.task(bind=True, max_retries=3)
def run_full_osint_pipeline(target, target_type, requestor, priority):
    # 1.  Deploy 8 spiders concurrently (asyncio.gather, return_exceptions=True)
    # 2.  Aggregate + deduplicate
    # 3.  NLP enrichment
    # 4.  Generate report (Claude for summary/findings)
    # 5.  Store in PostgreSQL
    # 6.  Upload to Google Drive
    # 7.  Embed into pgvector
    # 8.  Run 3-AI panel session
    # 9.  Store panel session
    # 10. Upload panel assessment to Google Drive
    # 11. Route notifications
```

Each step is wrapped in try/except — a failed step logs the error but doesn't abort the pipeline. The report always gets stored even if Drive upload or panel fails.

### Spider Bot Architecture

All 8 spiders implement `BaseCollector`:

```python
class BaseCollector(ABC):
    bot_id: str            # SPIDER-N
    domain: str            # collection domain label
    rate_limit: float      # seconds between requests
    source_reliability: float  # baseline reliability score

    @abstractmethod
    async def collect(target, target_type) -> CollectionResult

    @abstractmethod
    async def validate_target(target) -> bool

    async def _fetch(url, params, headers, method, json_body) -> dict|str|None
    # 3 retries, exponential backoff, 429 handling, per-request rate limiting

    def _content_hash(content) -> str   # SHA-256
    def _build_item(...) -> RawIntelItemSchema
    def _build_result(...) -> CollectionResult
```

Each spider runs in its own `aiohttp.ClientSession` context (`async with spider`).

### NLP Pipeline (No Blocking)

All model inference runs in `asyncio.get_event_loop().run_in_executor(None, sync_fn)` to avoid blocking the async event loop. Models are lazy-loaded with `@lru_cache` — they download on first call and stay in memory:

```
dslim/bert-base-NER          — ~400MB — Named entity recognition
cardiffnlp/twitter-roberta   — ~500MB — Sentiment analysis  
yanekyuk/bert-keyword        — ~400MB — Keyword extraction
BAAI/bge-m3                  — ~2.3GB — Embedding generation (1024-dim)
Helsinki-NLP/opus-mt-mul-en  — ~300MB — Translation (multilingual → English)
langdetect                   — ~8MB   — Language detection
```

Total: ~4GB RAM for all models loaded simultaneously.

### Panel Engine Concurrency

Panel turns are sequential (Alpha → Bravo → Director) because each analyst's turn depends on the previous. However, all API calls use `run_in_executor` to avoid blocking:

```python
async def _get_alpha_turn(session, question) -> str:
    response = await loop.run_in_executor(None, claude_sync_call)
    # Loop detection (sync, fast)
    if is_loop:
        response = await loop.run_in_executor(None, claude_sync_call_with_redirect)
    session.record_position(analyst_id, response)
    return response
```

### WebSocket Live Streaming

The `stream()` method on `PanelEngine` yields event dicts:

```python
async def stream(report_content, topic, target, ...) -> AsyncGenerator[dict, None]:
    yield {"type": "session_started", "session_id": ..., ...}
    
    while not concluded:
        session.round += 1
        yield {"type": "round_started", "round": session.round}
        
        alpha = await self._get_alpha_turn(...)
        yield {"type": "analyst_turn", "analyst": "ANALYST-ALPHA", "content": alpha}
        
        bravo = await self._get_bravo_turn(...)
        yield {"type": "analyst_turn", "analyst": "ANALYST-BRAVO", "content": bravo}
        
        direction = await self.gemini.direct(...)
        yield {"type": "director_turn", "content": direction, "status": status}
    
    synthesis = await self.gemini.synthesize(session)
    yield {"type": "session_complete", "final_synthesis": synthesis}
```

The FastAPI WebSocket endpoint (`/api/panel/{session_id}/stream`) connects clients to this stream. The Celery task calls `/api/panel/{session_id}/event` (internal) to push events to connected WebSocket clients.

---

## Database Schema

### PostgreSQL (Primary Store + Semantic Search)

```sql
-- Core intelligence tables
entities (
  id UUID PK,
  entity_type VARCHAR(50),       -- person|org|infrastructure|event|threat_actor
  name VARCHAR(500),
  aliases TEXT[],
  confidence FLOAT,
  tags TEXT[],
  metadata_ JSONB,
  first_seen TIMESTAMP,
  last_seen TIMESTAMP
)

entity_relationships (
  id UUID PK,
  source_id UUID FK → entities,
  target_id UUID FK → entities,
  rel_type VARCHAR(100),         -- CO_OCCURS_WITH, EMPLOYS, CONTROLS, etc.
  strength FLOAT,
  evidence_ids TEXT[]
)

raw_intel_items (
  id UUID PK,
  content_hash VARCHAR(64) UNIQUE,  -- SHA-256, dedup key
  collector_id VARCHAR(20),
  source_url TEXT,
  source_type VARCHAR(50),
  content TEXT,
  content_en TEXT,               -- translated content (null if English)
  language VARCHAR(10),
  target VARCHAR(500),
  target_type VARCHAR(50),
  collected_at TIMESTAMP,
  reliability_score FLOAT,
  processed BOOLEAN,
  metadata_ JSONB
)

reports (
  id UUID PK,
  report_id VARCHAR(100) UNIQUE, -- REPORT-YYYYMMDD-SLUG-UID8
  subject VARCHAR(500),
  subject_type VARCHAR(50),
  classification VARCHAR(20),    -- TLP:WHITE|GREEN|AMBER|RED
  confidence VARCHAR(10),        -- HIGH|MEDIUM|LOW
  confidence_score FLOAT,
  analyst_bots TEXT[],
  tags TEXT[],
  executive_summary TEXT,
  key_findings JSONB,
  entity_map JSONB,
  timeline JSONB,
  behavioral_indicators JSONB,
  threat_assessment JSONB,
  source_log JSONB,
  gaps TEXT[],
  analyst_notes TEXT[],
  full_markdown TEXT,
  embedding VECTOR(1024),        -- pgvector for semantic search
  google_drive_file_id VARCHAR(100),
  collection_started TIMESTAMP,
  collection_completed TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

panel_sessions (
  id UUID PK,
  session_id VARCHAR(50) UNIQUE, -- SESSION-UID8
  report_id UUID FK → reports (nullable),
  topic VARCHAR(1000),
  target VARCHAR(500),
  transcript JSONB,              -- [{turn_id, round, analyst, content, is_loop_flagged}]
  positions JSONB,               -- {analyst_id: [position_summaries]}
  covered_topics TEXT[],
  disagreements JSONB,           -- [{round, topic, alpha_pos, bravo_pos}]
  rounds_completed INTEGER,
  final_synthesis TEXT,
  concluded BOOLEAN,
  google_drive_file_id VARCHAR(100),
  start_time TIMESTAMP,
  end_time TIMESTAMP
)

iocs (
  id UUID PK,
  ioc_type VARCHAR(50),          -- ip|domain|hash|url|email
  value VARCHAR(1000),
  malicious_score FLOAT,
  tags TEXT[],
  source VARCHAR(100),
  expires TIMESTAMP
)

collection_tasks (
  id UUID PK,
  target VARCHAR(500),
  target_type VARCHAR(50),
  requestor VARCHAR(100),
  priority VARCHAR(20),
  status VARCHAR(20),            -- pending|queued|running|complete|failed
  celery_task_id VARCHAR(100),
  result_report_id VARCHAR(100),
  error TEXT,
  created_at TIMESTAMP,
  started_at TIMESTAMP,
  completed_at TIMESTAMP
)
```

### Neo4j (Entity Graph)

Node labels: `Person`, `Organization`, `Infrastructure`, `Location`, `Entity`

Properties: `id` (UUID5 from name), `name`, `source_report`

Relationship types:
- `CO_OCCURS_WITH` — entities in the same report
- `EMPLOYS` — organization employs person
- `CONTROLS` — controls relationship
- `LINKED_TO` — generic link with evidence

### MongoDB (Raw Document Store)

Collections:
```
raw_intel      — {content, collector_id, report_id, stored_at, ...}
               — Text index on 'content' for full-text search
artifacts      — {artifact_type, data, stored_at}
```

### ClickHouse (Time-Series Analytics)

```sql
collection_events (
  event_time DateTime,
  collector_id String,
  target String, target_type String,
  items_count UInt32,
  duration_ms UInt32,
  errors_count UInt16,
  status String
) ENGINE = MergeTree() PARTITION BY toYYYYMM(event_time) ORDER BY (event_time, collector_id)

panel_events (
  event_time DateTime,
  session_id String, report_id String,
  round_number UInt8, analyst String,
  content_len UInt32, is_loop UInt8,
  event_type String
) ENGINE = MergeTree() PARTITION BY toYYYYMM(event_time) ORDER BY (event_time, session_id)

ioc_events (
  event_time DateTime,
  ioc_type String, ioc_value String,
  source String, malicious_score Float32,
  report_id String, tags Array(String)
) ENGINE = MergeTree() PARTITION BY toYYYYMM(event_time) ORDER BY (event_time, ioc_type, ioc_value)
```

---

## Network Architecture

```
Internet ──→ Caddy (80/443) ──→ solace_net
                                    │
                         ┌──────────┼──────────┐
                         ▼          ▼          ▼
                    solace-api  solace-     grafana
                    (8000)      dashboard   (3000)
                                (80)
                         │
                    ┌────┴────┐
                    ▼         ▼
               postgres    redis
               mongodb     neo4j
               clickhouse  minio

tor_net (ISOLATED — internal: true)
    └── tor (9050/9051 only)
         └── SPIDER-4 connects via SOCKS5 proxy
              (tor_net has NO access to solace_net)
```

The Tor network isolation is enforced by Docker — `tor_net` is defined as `internal: true`, meaning it has no internet gateway except through the Tor daemon.

---

## LangGraph Agent Layer

The autonomous agent layer provides an alternative to the pipeline task — agents can decide dynamically which spiders to run and how to analyze results.

```
AgentState {
  target, target_type, task,
  messages, findings, report_ids,
  entity_map, threat_indicators,
  geo_data, final_assessment,
  iteration, max_iterations, next_agent
}

Graph:
  conditional_entry → route_to_agent()
  
  monitor_agent → search existing reports → route_to_agent()
  profile_agent → build entity profile → route_to_agent()
  threat_agent  → check IOCs + sanctions → "synthesize"
  synthesize    → combine all findings → END
```

Agents use shared tools: `search_reports`, `get_entity_network`, `trigger_collection`, `check_sanctions`, `summarize_findings`.

---

## API Design

The REST API follows RESTful conventions with async FastAPI:

```
GET    /api/health                     Platform health check
GET    /api/reports                    List reports (paginated, filtered)
GET    /api/reports/{report_id}        Get full report
GET    /api/reports/search             Semantic search
POST   /api/collections                Trigger collection task
GET    /api/collections/{task_id}      Task status
POST   /api/panel                      Start panel session
GET    /api/panel/{session_id}         Get completed session
WS     /api/panel/{session_id}/stream  Live transcript streaming
POST   /api/panel/{session_id}/event   Internal: push WebSocket event
GET    /api/entities                   List entity registry
```

All responses use consistent JSON structure. Errors include `detail` string. Pagination uses `page` + `page_size` query params.
