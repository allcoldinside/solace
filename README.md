<div align="center">

```
  ███████╗ ██████╗ ██╗      █████╗  ██████╗███████╗
  ██╔════╝██╔═══██╗██║     ██╔══██╗██╔════╝██╔════╝
  ███████╗██║   ██║██║     ███████║██║     █████╗
  ╚════██║██║   ██║██║     ██╔══██║██║     ██╔══╝
  ███████║╚██████╔╝███████╗██║  ██║╚██████╗███████╗
  ╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝
```

**Solo OSINT & Layered Analysis with Collaborative Experts**

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)](https://react.dev)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)](https://docker.com)
[![Tests](https://img.shields.io/badge/Tests-129%20passing-00ff88?style=flat-square)](tests/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

*A complete, self-hosted AI intelligence platform. Collect → Enrich → Report → Analyze → Alert.*

[**Quick Start**](#quick-start) · [**Architecture**](#architecture) · [**The Panel Engine**](#the-3-ai-analyst-panel) · [**Configuration**](docs/CONFIGURATION.md) · [**Usage**](docs/USAGE.md) · [**FAQ**](docs/FAQ.md)

</div>

---

## What is SOLACE?

SOLACE is a solo-operated, self-hosted open-source intelligence platform that automates the full intelligence cycle from collection through analysis and reporting. Everything runs on your own infrastructure — no data leaves your perimeter.

**The core idea:** You give it a target (a person, organization, IP address, or event). Eight autonomous spider bots fan out across the open web, dark web, corporate registries, threat feeds, and satellite data simultaneously. The collected intelligence is enriched by a local NLP pipeline, assembled into a structured report, stored in Google Drive, and then handed to a **three-AI analyst panel** — Claude, ChatGPT, and Gemini — who debate the findings like a real intelligence team. Results are routed to your Telegram, Discord, or Signal.

**No cloud dependencies.** No SaaS subscriptions. No data leaving your server.

---

## Key Features

### 8-Bot Scraper Team
Eight specialized spider bots run concurrently, each owning a distinct intelligence domain:

| Bot | Domain | Sources |
|-----|--------|---------|
| SPIDER-1 | Web & News | Google News RSS, DuckDuckGo, Article extraction via trafilatura |
| SPIDER-2 | Social & Forums | Reddit (PRAW), HackerNews, Nitter/Twitter mirrors |
| SPIDER-3 | Network & DNS | WHOIS, DNS records (A/MX/NS/TXT), Shodan, Censys |
| SPIDER-4 | Dark Web | Tor via Ahmia index + DarkSearch (isolated network) |
| SPIDER-5 | Corporate & Financial | OpenCorporates, SEC EDGAR, OpenSanctions |
| SPIDER-6 | Geospatial | OpenStreetMap Overpass, Nominatim geocoding, IP geolocation |
| SPIDER-7 | Documents | CISA advisories, Semantic Scholar academic papers |
| SPIDER-8 | Threat Feeds | OTX AlienVault, VirusTotal, GreyNoise, AbuseIPDB |

### NLP Enrichment Pipeline
Every collected item passes through HuggingFace models before storage:
- **Named Entity Recognition** — `dslim/bert-base-NER` extracts people, orgs, locations
- **Sentiment Analysis** — `cardiffnlp/twitter-roberta` scores each item −1.0 to +1.0
- **Multilingual Translation** — `Helsinki-NLP/opus-mt-mul-en` handles 100+ languages
- **Embedding Generation** — `BAAI/bge-m3` creates 1024-dim vectors for semantic search
- **Keyword Extraction** — topic tagging for report categorization

### Structured Intelligence Reports
Reports follow a strict schema (`REPORT-YYYYMMDD-SUBJECT-UID8`) with:
- AI-written executive summary (Claude Opus)
- Structured key findings with confidence ratings
- Entity map (people, organizations, locations, infrastructure)
- Chronological timeline
- Behavioral indicators from sentiment/pattern analysis
- Threat assessment with sanctions screening
- Full source provenance log
- Identified gaps and follow-on collection recommendations

Reports upload automatically to Google Drive as native Google Docs — fully searchable and compatible with NotebookLM.

### The 3-AI Analyst Panel
The crown jewel. Three AI systems with distinct roles debate every report:

| Analyst | Model | Role |
|---------|-------|------|
| **ANALYST-ALPHA** | Claude Opus | OSINT methodology + behavioral analysis |
| **ANALYST-BRAVO** | GPT-4o | Human patterns + influence mapping |
| **SESSION DIRECTOR** | Gemini 1.5 Pro | Manager, anti-loop enforcer, synthesizer |

Gemini tracks every point made, detects when analysts repeat themselves (via embedding similarity), redirects with new questions, and produces a final structured assessment preserving analyst disagreements.

### Full Communications Stack
- **Telegram** — command bot (`/run`, `/panel`, `/search`) + alert delivery
- **Discord** — slash commands, topic-channel-per-tag, live panel transcript streaming
- **Signal** — encrypted delivery for TLP:RED critical alerts only
- **Routing** — TLP:RED → Signal + Telegram priority + Discord | TLP:AMBER → Telegram + Discord | TLP:WHITE/GREEN → Discord topic channel

### React SCIF Dashboard
Dark phosphor-green aesthetic. Live WebSocket panel streaming. Pages:
- **HQ Overview** — stat tiles, recent reports, one-click collection dispatch, bot team status
- **Intel Reports** — semantic search, confidence/classification filters, full report viewer
- **Panel Engine** — live transcript view with analyst color coding, session config
- **Entity Graph** — entity registry browser with type/confidence filtering
- **Collector Status** — real-time bot health, reliability scores, source listings

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        COLLECTION LAYER                          │
│  SPIDER-1 │ SPIDER-2 │ SPIDER-3 │ SPIDER-4 (Tor, isolated)    │
│  SPIDER-5 │ SPIDER-6 │ SPIDER-7 │ SPIDER-8                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │  Celery async task queue
┌──────────────────────────▼──────────────────────────────────────┐
│                      AGGREGATOR BOT                              │
│  SHA-256 dedup │ reliability normalization │ sort by confidence  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    NLP ENRICHMENT PIPELINE                       │
│  NER (bert-base) │ Sentiment (roberta) │ Translation (Helsinki) │
│  Embeddings (bge-m3) │ Keywords │ Language detection            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    REPORT GENERATOR BOT                          │
│  Claude Opus writes summary + findings │ rest assembled from NLP │
│  Upload to Google Drive (native GDoc) │ embed in pgvector        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│               3-AI ANALYST PANEL (Crown Jewel)                   │
│                                                                   │
│  ANALYST-ALPHA (Claude) ◄──────► ANALYST-BRAVO (GPT-4o)        │
│          ↑                               ↑                       │
│          └───────── SESSION DIRECTOR (Gemini) ──────────────────┘│
│                    Anti-loop │ Questions │ Synthesis              │
└──────────────────────────┬──────────────────────────────────────┘
                           │  Final assessment → Google Drive
┌──────────────────────────▼──────────────────────────────────────┐
│                     DELIVERY LAYER                               │
│  Telegram Bot │ Discord Bot │ Signal CLI │ React Dashboard       │
└─────────────────────────────────────────────────────────────────┘
```

### Storage Stack

| Store | Role |
|-------|------|
| **PostgreSQL + pgvector** | Primary store + semantic search over report embeddings |
| **Neo4j** | Entity relationship graph — who knows who, org structures |
| **MongoDB** | Raw document store for bulk collected items |
| **Redis** | Cache, Celery broker, pub/sub for live alerts |
| **ClickHouse** | Time-series analytics — collection events, panel metrics |
| **MinIO** | S3-compatible artifact storage (documents, captures) |
| **Google Drive** | Final report archive as native searchable Google Docs |

---

## Quick Start

### Prerequisites

- Docker + Docker Compose
- Python 3.12+ (for CLI tools)
- API keys: **Anthropic**, **OpenAI**, **Google AI** (required for panel)
- Recommended: 16GB+ RAM, 50GB+ disk

### 1. Clone & Bootstrap

```bash
git clone https://github.com/YOUR_USERNAME/solace.git
cd solace
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

The bootstrap script will:
- Check all dependencies
- Create `.env` from template (prompting for API keys)
- Auto-generate a secure `SECRET_KEY`
- Pull and build all Docker images
- Initialize databases with schema and pgvector extension
- Start the full stack

### 2. Configure API Keys

Edit `.env` with your API keys — at minimum, you need:

```bash
ANTHROPIC_API_KEY=sk-ant-...      # Required: Claude panel analyst
OPENAI_API_KEY=sk-...             # Required: GPT-4o panel analyst
GOOGLE_AI_API_KEY=AIza...         # Required: Gemini director
```

For Google Drive integration (report storage):
```bash
GOOGLE_DRIVE_CREDENTIALS_JSON=/app/credentials/google_service_account.json
```
Place your service account JSON at `credentials/google_service_account.json`.

See [Configuration Guide](docs/CONFIGURATION.md) for the complete reference.

### 3. Start

```bash
# Full stack
make up

# Or with Docker Compose directly
docker compose up -d

# Development mode (hot-reload, Flower task monitor, exposed DB ports)
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### 4. Access Services

| Service | URL | Notes |
|---------|-----|-------|
| **SOLACE Dashboard** | http://localhost:3000 | Main UI |
| **API Documentation** | http://localhost:8000/api/docs | Interactive Swagger UI |
| **Grafana** | http://localhost:3001 | Metrics & dashboards |
| **n8n** | http://localhost:5678 | Workflow automation |
| **Neo4j Browser** | http://localhost:7474 | Entity graph explorer |
| **MinIO Console** | http://localhost:9001 | Artifact browser |
| **Celery Flower** | http://localhost:5555 | Task queue monitor (dev only) |

### 5. Run Your First Collection

```bash
# Via Makefile
make collect TARGET="Acme Corporation" TYPE=organization

# Via CLI
python scripts/run_panel.py --target "Acme Corporation" --type organization

# Via API
curl -X POST http://localhost:8000/api/collections \
  -H "Content-Type: application/json" \
  -d '{"target":"Acme Corporation","target_type":"organization","requestor":"cli"}'

# Via Dashboard
# Open http://localhost:3000 → HQ Overview → Dispatch Collection
```

### 6. Seed Development Data

```bash
# Create sample reports, entities, and panel sessions
make seed

# More data for load testing
python scripts/seed_data.py --reports 50 --entities 100
```

---

## Usage Guide

See **[docs/USAGE.md](docs/USAGE.md)** for the complete usage guide. Quick reference:

### Telegram Commands
```
/run <target> [type]    Trigger OSINT collection
/status                 Show bot team and system status
/report <id>            Get report summary by ID
/panel <report_id>      Start AI panel analysis on a report
/search <query>         Semantic search across reports
/help                   Show all commands
```

### Discord Slash Commands
```
/osint <target> [type]  Trigger collection
/panel <report_id>      Start panel session (streams to #panel-sessions)
/search <query>         Semantic search
```

### CLI Tools
```bash
# Trigger collection
python scripts/run_panel.py --target "APT-29" --type threat_actor --rounds 4

# Run panel on existing report
python scripts/run_panel.py --report-id REPORT-20250412-APT29-AB123456

# Save panel transcript to file
python scripts/run_panel.py --target "Acme Corp" --output reports/acme_panel.md

# Seed dev data
python scripts/seed_data.py --reports 10 --entities 30
```

### Makefile Targets
```bash
make up           # Start all services
make down         # Stop all services
make logs         # Follow all logs
make logs-api     # Follow API logs
make logs-worker  # Follow Celery worker logs
make shell        # Python shell in API container
make db-shell     # PostgreSQL shell
make test         # Run full test suite (129 tests)
make seed         # Seed dev database
make panel TARGET="Acme Corp"  # Run panel from CLI
make collect TARGET="Acme Corp" TYPE=organization
make health       # Check API health
```

---

## The 3-AI Analyst Panel

This is SOLACE's most distinctive capability. See **[docs/PANEL.md](docs/PANEL.md)** for deep documentation. Here's the overview:

### How It Works

1. **Gemini opens the session** — reviews the report, sets the analytical agenda, issues the first targeted question
2. **Claude (ANALYST-ALPHA) analyzes first** — applies OSINT + behavioral analysis methodology, rates confidence on every point
3. **GPT-4o (ANALYST-BRAVO) responds** — sees Claude's analysis, must build on or challenge it with new angles
4. **Gemini reviews the round** — tracks covered ground, detects loops, issues next question or redirects
5. **Repeat for 2–12 rounds**
6. **Gemini synthesizes** — produces structured final assessment preserving all analyst disagreements

### Loop Detection

Gemini tracks every analytical point made. If an analyst tries to repeat covered ground (detected via BAAI/bge-m3 cosine similarity, threshold 0.65), Gemini interrupts:

> *"LOOP DETECTED — ANALYST-ALPHA: that ground was covered in Round 2. Redirect your analysis to the source reliability section."*

The analyst regenerates with an explicit redirect instruction. This keeps sessions productive and prevents the AI-specific failure mode of circular reasoning.

### What You Get

The final synthesis includes:
- Numbered key findings with confidence ratings
- Behavioral and pattern analysis synthesis
- Points where both analysts agreed (higher confidence)
- **Preserved analyst disagreements** — where Claude and GPT diverged, both positions are kept, not resolved
- Identified gaps and recommended follow-on collection
- Director's overall assessment

---

## Report Format

Every report follows the SOLACE schema:

```
REPORT-{YYYYMMDD}-{SUBJECT-SLUG}-{UID8}

Example: REPORT-20250412-ACME-CORP-A3F9B2C1
```

### Sections

| Section | Content |
|---------|---------|
| Executive Summary | AI-written 2–4 paragraph overview (who, what, where, when, significance) |
| Key Findings | Numbered, confidence-rated, sourced findings |
| Entity Map | People, organizations, locations, infrastructure — extracted via NER |
| Timeline | Chronological events with sources |
| Behavioral Indicators | NLP-derived patterns, sentiment trends, anomalies |
| Threat Assessment | CRITICAL/HIGH/MEDIUM/LOW rating, IOC count, sanctions check |
| Source Log | Full provenance — every URL, collector, reliability score, content hash |
| Gaps | What wasn't collected, what's unknown |
| Analyst Notes | Auto-generated flags for the panel |

### Classifications

Reports follow TLP (Traffic Light Protocol):

| Classification | Meaning | Alert Routing |
|----------------|---------|---------------|
| `TLP:WHITE` | Public — unrestricted | Discord topic channel |
| `TLP:GREEN` | Community — limited sharing | Discord topic channel |
| `TLP:AMBER` | Organization — restricted | Telegram + Discord alerts |
| `TLP:RED` | Need-to-know — strict | Signal + Telegram priority + Discord |

---

## Configuration

See **[docs/CONFIGURATION.md](docs/CONFIGURATION.md)** for the full reference. Critical values:

```bash
# Required for panel engine
ANTHROPIC_API_KEY=         # Claude Opus - ANALYST-ALPHA
OPENAI_API_KEY=            # GPT-4o - ANALYST-BRAVO
GOOGLE_AI_API_KEY=         # Gemini 1.5 Pro - SESSION DIRECTOR

# Required for report storage
GOOGLE_DRIVE_CREDENTIALS_JSON=credentials/google_service_account.json

# Panel behavior
MAX_PANEL_ROUNDS=6                 # 2–12 recommended
LOOP_DETECTION_THRESHOLD=0.65     # 0.0–1.0 (lower = more aggressive)
DEFAULT_CLASSIFICATION=TLP:WHITE
```

---

## Project Structure

```
solace/
├── agents/          LangGraph autonomous agent layer
├── api/             FastAPI REST + WebSocket API
├── caddy/           Reverse proxy configuration
├── collectors/      8 spider bots + aggregator
├── comms/           Telegram, Discord, Signal integration
├── config/          Settings, logging, Prometheus config
├── core/            Database models, schemas, Redis client
├── dashboard/       React SCIF-aesthetic frontend
├── grafana/         Pre-configured dashboards + datasources
├── nlp/             HuggingFace NLP enrichment pipeline
├── panel/           3-AI analyst panel engine
├── reports/         Report schema + AI report generator
├── scripts/         Bootstrap, seed data, CLI panel runner
├── storage/         Google Drive, pgvector, Neo4j, MongoDB, MinIO, ClickHouse
├── tasks/           Celery pipeline and panel tasks
└── tests/           129 tests across 11 test classes
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [INSTALL.md](docs/INSTALL.md) | Full installation guide — prerequisites, Docker, first run, troubleshooting |
| [CONFIGURATION.md](docs/CONFIGURATION.md) | Complete `.env` reference for all 50+ settings |
| [USAGE.md](docs/USAGE.md) | Step-by-step usage — dashboard, CLI, Telegram, Discord, API |
| [PANEL.md](docs/PANEL.md) | Deep dive into the 3-AI panel — prompts, loop detection, session lifecycle |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design — data flow, component interactions, database schema |
| [COLLECTORS.md](docs/COLLECTORS.md) | Spider bot reference — all 8 bots, sources, reliability scores |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Development setup, test suite, PR guidelines |
| [FAQ.md](docs/FAQ.md) | Common questions and troubleshooting |

---

## Legal & Ethical Notice

SOLACE collects **passive, open-source intelligence only** — publicly available information. Users are responsible for:

- Complying with applicable laws and platform Terms of Service
- Respecting rate limits on all data sources
- Adhering to TLP classification guidelines
- Not storing personal data beyond operational necessity

SPIDER-4 (dark web collection) runs in an isolated Docker network (`tor_net`) with no access to `solace_net`. It must be explicitly enabled and requires the Tor service to be reachable.

---

## License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">

*Built with Claude Opus · GPT-4o · Gemini 1.5 Pro*

</div>
