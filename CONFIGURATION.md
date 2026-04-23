# SOLACE — Configuration Reference

All configuration is done via the `.env` file. Copy `.env.example` to `.env` and fill in your values.

---

## Core Application

```bash
# ── Required ──────────────────────────────────────────────────────────────
SECRET_KEY=                    # Min 32 chars. Generate: python3 -c "import secrets; print(secrets.token_hex(32))"
ENVIRONMENT=production         # production | development | testing
DEBUG=false                    # true enables SQL echo and verbose logging
LOG_LEVEL=INFO                 # DEBUG | INFO | WARNING | ERROR

# ── Panel Engine ─────────────────────────────────────────────────────────
MAX_PANEL_ROUNDS=6             # Rounds per panel session (2–12 recommended)
LOOP_DETECTION_THRESHOLD=0.65  # Cosine similarity threshold (0.0–1.0). Lower = more aggressive loop detection
DEFAULT_CLASSIFICATION=TLP:WHITE  # Default report classification
PANEL_MAX_TOKENS=1500          # Max tokens per analyst turn
```

---

## Databases

All databases are required. Passwords should be strong (20+ chars).

```bash
# ── PostgreSQL (Primary store + semantic search) ──────────────────────────
POSTGRES_URL=postgresql+asyncpg://solace:PASSWORD@postgres:5432/solace
POSTGRES_USER=solace
POSTGRES_PASSWORD=             # Strong password required
POSTGRES_DB=solace

# ── MongoDB (Raw document store) ──────────────────────────────────────────
MONGODB_URL=mongodb://solace:PASSWORD@mongodb:27017/solace
MONGODB_USER=solace
MONGODB_PASSWORD=              # Strong password required

# ── Neo4j (Entity relationship graph) ─────────────────────────────────────
NEO4J_URL=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=                # Strong password required

# ── Redis (Cache + Celery broker + pub/sub) ───────────────────────────────
REDIS_URL=redis://:PASSWORD@redis:6379/0
REDIS_PASSWORD=                # Strong password required

# ── ClickHouse (Time-series analytics) ────────────────────────────────────
CLICKHOUSE_HOST=clickhouse
CLICKHOUSE_PORT=9000
CLICKHOUSE_DB=solace
CLICKHOUSE_USER=solace
CLICKHOUSE_PASSWORD=           # Strong password required

# ── MinIO (Object/artifact storage) ───────────────────────────────────────
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=              # Username for MinIO (any value)
MINIO_SECRET_KEY=              # Password for MinIO (strong, 20+ chars)
MINIO_BUCKET=solace-artifacts  # Default bucket name
```

---

## AI API Keys

All three are required for the panel engine. Without all three, panel sessions will fail.

```bash
# ── Claude (ANALYST-ALPHA) ────────────────────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-...
# Used for: panel analysis + report executive summary + key findings generation
# Model: claude-opus-4-5

# ── OpenAI GPT-4o (ANALYST-BRAVO) ────────────────────────────────────────
OPENAI_API_KEY=sk-...
# Used for: panel analysis
# Model: gpt-4o

# ── Google Gemini (SESSION DIRECTOR) ─────────────────────────────────────
GOOGLE_AI_API_KEY=AIza...
# Used for: session direction, loop detection direction, final synthesis
# Model: gemini-1.5-pro

# ── HuggingFace (NLP models) ──────────────────────────────────────────────
HUGGINGFACE_TOKEN=hf_...
# Optional — needed for private/gated models. Public models work without it.

# ── Ollama (Local LLM) ────────────────────────────────────────────────────
OLLAMA_HOST=http://ollama:11434
OLLAMA_DEFAULT_MODEL=mistral   # mistral | llama3.2 | phi4 | etc.
```

---

## Google Drive

Required for automatic report storage as searchable Google Docs.

```bash
GOOGLE_DRIVE_CREDENTIALS_JSON=/app/credentials/google_service_account.json
# Path to service account JSON inside the container

GOOGLE_DRIVE_ROOT_FOLDER_ID=
# The ID of your top-level "SOLACE Intelligence Agency" folder
# Get from URL: drive.google.com/drive/folders/THIS_PART

GOOGLE_DRIVE_REPORTS_FOLDER_ID=
# Optional: pre-created subfolder for reports (auto-created if empty)

GOOGLE_DRIVE_ASSESSMENTS_FOLDER_ID=
# Optional: pre-created subfolder for panel assessments (auto-created if empty)
```

---

## Messaging

All messaging integrations are optional. The platform works without them.

### Telegram

```bash
# ── Bot API (for sending alerts and commands) ─────────────────────────────
TELEGRAM_BOT_TOKEN=            # From @BotFather
TELEGRAM_ALERT_CHAT_ID=        # Chat/channel ID to send alerts to

# ── MTProto API (for monitoring public channels) ──────────────────────────
TELEGRAM_API_ID=               # From my.telegram.org
TELEGRAM_API_HASH=             # From my.telegram.org
TELEGRAM_SESSION_STRING=       # Telethon session string (generated on first run)
```

### Discord

```bash
DISCORD_BOT_TOKEN=             # From Discord Developer Portal
DISCORD_GUILD_ID=              # Your server's ID (Enable Developer Mode to see)
DISCORD_ALERTS_CHANNEL_ID=     # Channel for TLP:AMBER/RED alerts
DISCORD_PANEL_CHANNEL_ID=      # Channel for live panel transcript streaming
```

### Signal

```bash
SIGNAL_CLI_CONFIG_PATH=/app/signal-cli-config  # Path to signal-cli config dir
SIGNAL_SENDER_NUMBER=+1234567890               # Phone number registered with Signal
# Note: Signal is outbound-only for TLP:RED alerts
```

---

## OSINT API Keys

All optional. Each enables additional spider bot capabilities.

```bash
# ── Network Intelligence (SPIDER-3) ──────────────────────────────────────
SHODAN_API_KEY=                # shodan.io — exposed service scanning
CENSYS_API_ID=                 # censys.io — certificate + device intel
CENSYS_API_SECRET=             # censys.io secret
SECURITYTRAILS_API_KEY=        # securitytrails.com — DNS history

# ── Threat Intelligence (SPIDER-8) ───────────────────────────────────────
VIRUSTOTAL_API_KEY=            # virustotal.com — file/URL/IP threat data
ALIENVAULT_OTX_API_KEY=        # otx.alienvault.com — threat pulse feeds
GREYNOISE_API_KEY=             # greynoise.io — internet noise vs targeted traffic
BINARYEDGE_API_KEY=            # binaryedge.io — internet scan data

# ── Corporate Intelligence (SPIDER-5) ─────────────────────────────────────
OPENCORPORATES_API_KEY=        # opencorporates.com — 180+ country company registry

# ── Identity Intelligence ─────────────────────────────────────────────────
HUNTER_API_KEY=                # hunter.io — email discovery
```

---

## Intel Platforms

Optional integrations with self-hosted threat intelligence platforms.

```bash
# ── MISP (Malware Information Sharing Platform) ───────────────────────────
MISP_URL=http://misp
MISP_API_KEY=                  # From MISP administration panel

# ── TheHive (Case Management) ─────────────────────────────────────────────
THEHIVE_URL=http://thehive:9000
THEHIVE_API_KEY=               # From TheHive user settings
```

---

## Tor (Dark Web Collection)

```bash
TOR_SOCKS_PROXY=socks5://tor:9050  # Tor SOCKS5 proxy
TOR_CONTROL_PORT=9051
TOR_CONTROL_PASSWORD=              # Tor control password
```

Note: SPIDER-4 runs in an isolated `tor_net` Docker network. It cannot communicate with `solace_net` by design.

---

## Reverse Proxy & Auth

```bash
# ── Caddy ─────────────────────────────────────────────────────────────────
SOLACE_DOMAIN=solace.local     # Your domain or local hostname
CADDY_ADMIN_EMAIL=admin@solace.local  # For TLS certificate issuance

# ── Authentik (SSO) ───────────────────────────────────────────────────────
AUTHENTIK_SECRET_KEY=          # 50+ char random string
AUTHENTIK_BOOTSTRAP_EMAIL=admin@solace.local
AUTHENTIK_BOOTSTRAP_PASSWORD=  # Initial admin password
```

---

## Environment Variable Summary

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `SECRET_KEY` | ✅ | — | Min 32 chars |
| `POSTGRES_PASSWORD` | ✅ | — | |
| `REDIS_PASSWORD` | ✅ | — | |
| `NEO4J_PASSWORD` | ✅ | — | |
| `CLICKHOUSE_PASSWORD` | ✅ | — | |
| `MINIO_SECRET_KEY` | ✅ | — | |
| `ANTHROPIC_API_KEY` | ✅ (panel) | — | |
| `OPENAI_API_KEY` | ✅ (panel) | — | |
| `GOOGLE_AI_API_KEY` | ✅ (panel) | — | |
| `MONGODB_PASSWORD` | ✅ | — | |
| `GOOGLE_DRIVE_CREDENTIALS_JSON` | ⚠️ | — | Required for Drive storage |
| `TELEGRAM_BOT_TOKEN` | ⚠️ | — | Required for Telegram alerts |
| `DISCORD_BOT_TOKEN` | ⚠️ | — | Required for Discord |
| `MAX_PANEL_ROUNDS` | ✅ | `6` | |
| `LOOP_DETECTION_THRESHOLD` | ✅ | `0.65` | |
| `DEFAULT_CLASSIFICATION` | ✅ | `TLP:WHITE` | |
| All OSINT API keys | ❌ | `""` | Optional, enable more sources |

✅ = Required   ⚠️ = Required for that feature   ❌ = Optional
