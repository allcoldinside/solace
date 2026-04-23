# SOLACE — Usage Guide

Complete reference for operating SOLACE day-to-day.

---

## Starting a Collection

The full OSINT pipeline — 8 spiders → NLP → report → panel → alerts — can be triggered from several interfaces.

### Dashboard (Recommended)

1. Open http://localhost:3000
2. HQ Overview → **Dispatch Collection** panel
3. Enter target name (e.g., `Acme Corporation`)
4. Select target type: `Organization | Person | Infrastructure | Event | Threat Actor`
5. Click **Deploy Bot Team**

The dashboard shows the queued task ID. When complete, the report appears in the Intel Reports page.

### CLI

```bash
# Basic collection
python scripts/run_panel.py --target "Acme Corporation" --type organization

# Person
python scripts/run_panel.py --target "John Smith" --type person

# IP address / domain
python scripts/run_panel.py --target "198.51.100.42" --type infrastructure

# Threat actor
python scripts/run_panel.py --target "APT-29" --type threat_actor --rounds 8

# Save panel transcript
python scripts/run_panel.py --target "Acme Corp" --output /tmp/acme_analysis.md
```

### Makefile

```bash
make collect TARGET="Acme Corporation" TYPE=organization
make collect TARGET="198.51.100.42" TYPE=infrastructure
```

### API

```bash
curl -X POST http://localhost:8000/api/collections \
  -H "Content-Type: application/json" \
  -d '{
    "target": "Acme Corporation",
    "target_type": "organization",
    "requestor": "api",
    "priority": "normal"
  }'

# Response:
# {
#   "task_id": "abc123",
#   "celery_task_id": "def456",
#   "target": "Acme Corporation",
#   "status": "queued"
# }
```

Check task status:
```bash
curl http://localhost:8000/api/collections/abc123
```

### Telegram

```
/run Acme Corporation organization
/run 198.51.100.42 infrastructure
/run APT-29 threat_actor
```

### Discord

```
/osint Acme Corporation organization
/osint John Smith person
```

---

## Working With Reports

### Viewing Reports

**Dashboard:**
1. Intel Reports → browse by date, filter by classification or confidence
2. Semantic search: type a natural language query → ranked results by embedding similarity
3. Click any report → Structured View (entity map, findings, threat) or Full Markdown

**API:**
```bash
# List recent reports
curl "http://localhost:8000/api/reports?page=1&page_size=20"

# Get specific report
curl "http://localhost:8000/api/reports/REPORT-20250412-ACME-CORP-A3F9B2C1"

# Semantic search
curl "http://localhost:8000/api/reports/search?q=offshore+financial+connections"
```

**Telegram:**
```
/report REPORT-20250412-ACME-CORP-A3F9B2C1
/search offshore financial sanctions
```

### Report ID Format

```
REPORT-{YYYYMMDD}-{SUBJECT-SLUG}-{UID8}

Examples:
  REPORT-20250412-ACME-CORP-A3F9B2C1
  REPORT-20250412-APT29-B7D2E4F1
  REPORT-20250412-198-51-100-42-C9A1D3E5
```

### Report Confidence Levels

| Level | Score | Meaning |
|-------|-------|---------|
| **HIGH** | ≥ 0.75 | Multiple authoritative sources, high reliability average |
| **MEDIUM** | 0.45–0.74 | Mix of sources, reasonable coverage |
| **LOW** | < 0.45 | Limited sources, low reliability |

---

## Running Panel Sessions

The 3-AI panel can run as part of a full pipeline (automatic) or standalone on an existing report.

### Standalone on Existing Report

```bash
# From CLI
python scripts/run_panel.py --report-id REPORT-20250412-ACME-CORP-A3F9B2C1

# With custom rounds
python scripts/run_panel.py --report-id REPORT-20250412-ACME-CORP-A3F9B2C1 --rounds 4

# Save output
python scripts/run_panel.py --report-id REPORT-20250412-ACME-CORP-A3F9B2C1 \
  --output /tmp/acme_assessment.md
```

### From Dashboard

1. Open Intel Reports → click a report
2. Click **Panel Analysis** button (top right)
3. OR: Panel Engine page → enter topic + target + optional report ID → Convene Panel
4. Watch live transcript stream in the interface

### From Telegram

```
/panel REPORT-20250412-ACME-CORP-A3F9B2C1
```

### From API

```bash
# Start panel
curl -X POST http://localhost:8000/api/panel \
  -H "Content-Type: application/json" \
  -d '{
    "report_id": "REPORT-20250412-ACME-CORP-A3F9B2C1",
    "topic": "Full intelligence assessment of Acme Corporation",
    "target": "Acme Corporation",
    "max_rounds": 6
  }'

# Response includes session_id and websocket_url for live streaming

# Get completed session
curl http://localhost:8000/api/panel/SESSION-A3F9B2C1

# WebSocket for live streaming
ws://localhost:8000/api/panel/SESSION-A3F9B2C1/stream
```

### Understanding Panel Output

A completed panel session produces:

```markdown
# SOLACE PANEL INTELLIGENCE ASSESSMENT
session_id: SESSION-A3F9B2C1
report_id:  REPORT-20250412-ACME-CORP-A3F9B2C1
analysts:   ANALYST-ALPHA (Claude), ANALYST-BRAVO (ChatGPT)
director:   SESSION DIRECTOR (Gemini)
rounds:     6 of 6
duration:   14m 23s

## 1. KEY INTELLIGENCE FINDINGS
1. [HIGH] Subject has offshore financial connections via shell entities...
2. [HIGH] Linguistic deception indicators in Q3 public statements...
3. [MEDIUM] Network infrastructure historically linked to known threat clusters...

## 2. BEHAVIORAL & PATTERN ANALYSIS
...

## 3. ANALYST AGREEMENTS
Both analysts independently confirmed the behavioral pattern anomalies...

## 4. ANALYST DISAGREEMENTS — PRESERVED
ALPHA: HIGH threat attribution confidence based on IOC correlation
BRAVO: MEDIUM — attribution requires stronger evidence, correlation alone insufficient

## 5. GAPS & UNCERTAINTIES
- No dark web presence captured
- Financial history pre-2022 incomplete...

## 6. RECOMMENDED FOLLOW-ON COLLECTION
- Re-run with SPIDER-4 enabled for dark web coverage
- Manual review of SEC EDGAR filings 2018–2022

## 7. OVERALL ASSESSMENT
Subject warrants continued monitoring. Threat level MEDIUM with escalation triggers...
```

---

## Alert Routing

Alerts are routed based on TLP classification:

| Classification | Channels | When |
|----------------|----------|------|
| `TLP:RED` | Signal + Telegram (priority) + Discord #alerts | CRITICAL threat, sanctions match |
| `TLP:AMBER` | Telegram + Discord #alerts | HIGH threat, concerning findings |
| `TLP:GREEN` | Discord topic channel | Standard collection complete |
| `TLP:WHITE` | Discord topic channel | Routine intelligence |

### Setting Classification

The system auto-assigns classification based on threat assessment:
- **CRITICAL threat level** → TLP:RED
- **HIGH threat level** → TLP:AMBER  
- **MEDIUM/LOW** → TLP:WHITE/GREEN

---

## Searching Reports

### Semantic Search

Searches use BAAI/bge-m3 embeddings for meaning-aware results (not just keyword matching).

```bash
# Via dashboard search bar
# Via Telegram: /search offshore financial connections cayman islands
# Via API:
curl "http://localhost:8000/api/reports/search?q=sanctions+evasion+shell+company"
```

### Filtering

```bash
# By classification
curl "http://localhost:8000/api/reports?classification=TLP:AMBER"

# By confidence
curl "http://localhost:8000/api/reports?confidence=HIGH"

# By tag
curl "http://localhost:8000/api/reports?tag=financial"

# Combined
curl "http://localhost:8000/api/reports?classification=TLP:AMBER&confidence=HIGH"
```

---

## Managing Collections

### Scheduled Collections

Use n8n (http://localhost:5678) to create scheduled workflows:

1. Open n8n → New Workflow
2. Add HTTP Request node → POST to `http://solace-api:8000/api/collections`
3. Body: `{"target": "your_target", "target_type": "organization"}`
4. Add Schedule Trigger → set frequency (daily, weekly, etc.)

### Monitoring Active Tasks

```bash
# Via Celery Flower (dev mode)
open http://localhost:5555

# Via Makefile
make logs-worker

# Via API
curl http://localhost:8000/api/collections/{task_id}
```

---

## Entity Graph

The Neo4j entity graph is populated automatically from report entity maps.

**Access:**
- Dashboard → Entity Graph page
- Neo4j Browser → http://localhost:7474 (dev: neo4j / your_password)

**Query examples in Neo4j Browser:**
```cypher
# All people linked to a specific organization
MATCH (p:Person)-[:CO_OCCURS_WITH]-(o:Organization {name: "Acme Corp"})
RETURN p, o

# Most connected entities
MATCH (e)-[r]-()
RETURN e.name, count(r) as connections
ORDER BY connections DESC
LIMIT 20

# Network within 2 hops of a target
MATCH path = (e {name: "John Smith"})-[*1..2]-(connected)
RETURN path
```

---

## Grafana Dashboards

Pre-configured dashboards at http://localhost:3001:

- **SOLACE Platform Overview** — API health, collection rates, panel metrics, report counts
- **Collection Analytics** — Per-spider performance, items collected over time, error rates
- **Panel Engine Metrics** — Session duration, rounds per session, loop detection rate

Default credentials: admin / (your `AUTHENTIK_BOOTSTRAP_PASSWORD`)

---

## n8n Workflows

Pre-built workflow templates for common automations:

**Daily Target Monitoring:**
```
Schedule (daily 0600) → POST /api/collections → check status → send Telegram notification
```

**Batch Collection:**
```
Read targets from spreadsheet → loop → POST /api/collections → aggregate results
```

**Alert Escalation:**
```
Watch Discord → if TLP:RED → forward to Signal → log to Google Sheet
```

Import templates from `n8n_workflows/` (if provided) or build custom ones.

---

## Seed Data for Development

Populate the database with realistic sample data:

```bash
# Standard seed (10 reports, 30 entities, 5 panel sessions)
make seed

# Custom amounts
python scripts/seed_data.py --reports 50 --entities 100

# Output:
# ══════════════════════════════════════════
#   SOLACE — Seeding Development Data
# ══════════════════════════════════════════
# Seeding reports...
#   ✓ Created 10 sample reports
# Seeding entities...
#   ✓ Created 30 sample entities
# Seeding panel sessions...
#   ✓ Created 5 sample panel sessions
```

---

## Common Workflows

### Daily Intelligence Review

1. Check Telegram/Discord for overnight alerts
2. Dashboard → HQ Overview → review new reports
3. For HIGH confidence or TLP:AMBER/RED reports → run panel analysis
4. Review panel assessments in Google Drive

### Target Research

1. Run collection: `make collect TARGET="Acme Corp" TYPE=organization`
2. Wait for completion (5–15 minutes depending on sources)
3. Open report → review key findings and entity map
4. Run panel: `/panel REPORT-20250412-ACME-CORP-XXXXXXXX`
5. Review panel assessment → download from Google Drive

### Building an Entity Network

1. Run collections on several related targets
2. Open Dashboard → Entity Graph
3. Look for shared entities (people/orgs appearing in multiple reports)
4. Query Neo4j for relationship paths:
   ```cypher
   MATCH path = (a {name: "Target A"})-[*1..3]-(b {name: "Target B"})
   RETURN path
   ```

### Exporting Reports

Reports are automatically in Google Drive as native Google Docs. Additionally:

```bash
# Download report markdown via API
curl http://localhost:8000/api/reports/REPORT-ID | jq -r '.full_markdown' > report.md

# Or from MinIO (artifacts)
# Open http://localhost:9001 → solace-artifacts bucket → reports/
```
