# SOLACE — Installation Guide

Complete installation from zero to running platform.

---

## System Requirements

### Minimum
- **OS:** Linux (Ubuntu 22.04+), macOS 13+, or Windows 11 with WSL2
- **CPU:** 4 cores
- **RAM:** 8GB (16GB recommended for running HuggingFace NLP models locally)
- **Disk:** 20GB free (50GB recommended — Docker images + databases)
- **Docker:** 24.0+ with Docker Compose v2

### Recommended (full stack with local NLP)
- **RAM:** 32GB+ (NLP models load into memory: ~4GB combined)
- **GPU:** NVIDIA RTX 3090+ for running Ollama local LLM (optional)
- **Disk:** 100GB+ SSD

---

## Prerequisites

### 1. Install Docker

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

**macOS:**
```bash
brew install --cask docker
# Then open Docker Desktop
```

**Verify:**
```bash
docker --version          # Docker version 24.0+
docker compose version    # Docker Compose version v2+
```

### 2. Install Python 3.12+ (for CLI tools only)

```bash
# Ubuntu
sudo apt install python3.12 python3.12-pip

# macOS
brew install python@3.12

# Verify
python3 --version
```

### 3. Get API Keys

You need at minimum three API keys for the panel engine:

| Service | Where to get it | Required? |
|---------|----------------|-----------|
| **Anthropic** (Claude) | https://console.anthropic.com | ✅ Yes |
| **OpenAI** (GPT-4o) | https://platform.openai.com | ✅ Yes |
| **Google AI** (Gemini) | https://aistudio.google.com | ✅ Yes |
| Shodan | https://account.shodan.io | Optional (SPIDER-3) |
| VirusTotal | https://www.virustotal.com/gui/my-apikey | Optional (SPIDER-8) |
| OTX AlienVault | https://otx.alienvault.com/api | Optional (SPIDER-8) |
| GreyNoise | https://www.greynoise.io | Optional (SPIDER-8) |
| Censys | https://search.censys.io/account/api | Optional (SPIDER-3) |
| OpenCorporates | https://opencorporates.com/api_accounts | Optional (SPIDER-5) |

---

## Installation

### Option A: Automated Bootstrap (Recommended)

```bash
git clone https://github.com/YOUR_USERNAME/solace.git
cd solace
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

The script will guide you through everything interactively.

### Option B: Manual Step-by-Step

#### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/solace.git
cd solace
```

#### Step 2: Configure environment

```bash
cp .env.example .env
```

Edit `.env` — at minimum set:
```bash
# Generate a secure key first:
python3 -c "import secrets; print(secrets.token_hex(32))"

SECRET_KEY=<output from above>
POSTGRES_PASSWORD=choose_a_strong_password
REDIS_PASSWORD=choose_a_strong_password
NEO4J_PASSWORD=choose_a_strong_password
CLICKHOUSE_PASSWORD=choose_a_strong_password
MINIO_SECRET_KEY=choose_a_strong_password

ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_AI_API_KEY=AIza...
```

#### Step 3: Create credentials directory

```bash
mkdir -p credentials
```

If you want Google Drive integration, place your service account JSON here:
```bash
credentials/google_service_account.json
```

See [Google Drive Setup](#google-drive-setup) below.

#### Step 4: Pull Docker images

```bash
docker compose pull
```

#### Step 5: Build application images

```bash
docker compose build --parallel
```

This builds the SOLACE API, worker, and dashboard containers.

#### Step 6: Start core databases

```bash
docker compose up -d postgres redis mongodb neo4j minio
```

Wait for them to be healthy (about 30–60 seconds):
```bash
docker compose ps
# All should show "healthy"
```

#### Step 7: Initialize database schema

```bash
docker compose run --rm solace-api python -c "
import asyncio
from core.database import init_db
asyncio.run(init_db())
print('Database initialized')
"
```

#### Step 8: Start the full stack

```bash
docker compose up -d
```

#### Step 9: Verify everything is running

```bash
make health
# Expected: {"status":"operational","version":"1.0.0",...}

docker compose ps
# All services should show "Up" or "healthy"
```

---

## Google Drive Setup

To store reports as searchable native Google Docs:

### 1. Create a Google Cloud Project

1. Go to https://console.cloud.google.com
2. Create a new project (e.g., "SOLACE")
3. Enable the **Google Drive API**:
   - APIs & Services → Enable APIs → Search "Drive" → Enable

### 2. Create a Service Account

1. APIs & Services → Credentials → Create Credentials → Service Account
2. Name: `solace-drive` — click Create
3. Skip optional steps — click Done
4. Click the service account → Keys → Add Key → JSON
5. Download the JSON file
6. Copy to `credentials/google_service_account.json`

### 3. Create and Share the Drive Folder

1. Open Google Drive in your browser
2. Create a folder named `SOLACE Intelligence Agency`
3. Right-click → Share → Add the service account email (from the JSON file) → Editor
4. Copy the folder ID from the URL: `https://drive.google.com/drive/folders/`**`THIS_PART`**

### 4. Configure `.env`

```bash
GOOGLE_DRIVE_CREDENTIALS_JSON=/app/credentials/google_service_account.json
GOOGLE_DRIVE_ROOT_FOLDER_ID=<folder ID from step 3>
```

SOLACE will automatically create subfolders (Raw Reports, Panel Assessments, etc.) on first run.

---

## Telegram Bot Setup

### 1. Create a Bot

1. Message `@BotFather` on Telegram
2. Send `/newbot` — follow prompts
3. Copy the bot token

### 2. Get API Credentials (for monitoring public channels)

1. Go to https://my.telegram.org
2. Log in → API Development Tools
3. Create an application
4. Note your `api_id` and `api_hash`

### 3. Configure `.env`

```bash
TELEGRAM_BOT_TOKEN=1234567890:AAABBB...
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abc123def456...
TELEGRAM_ALERT_CHAT_ID=your_chat_id_or_channel_id
```

To get your chat ID, message `@userinfobot` on Telegram.

---

## Discord Bot Setup

### 1. Create Application

1. Go to https://discord.com/developers/applications
2. New Application → Name it `SOLACE`
3. Bot → Add Bot → Copy token
4. Enable: `Message Content Intent`, `Server Members Intent`

### 2. Invite to Server

1. OAuth2 → URL Generator
2. Scopes: `bot`, `applications.commands`
3. Permissions: `Send Messages`, `Embed Links`, `Manage Channels`, `Read Message History`
4. Open the generated URL and invite to your server

### 3. Get IDs

Enable Developer Mode in Discord (Settings → Advanced → Developer Mode).
Right-click your server → Copy ID = Guild ID.
Right-click #alerts channel → Copy ID = Alerts Channel ID.

### 4. Configure `.env`

```bash
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_GUILD_ID=your_server_id
DISCORD_ALERTS_CHANNEL_ID=your_alerts_channel_id
DISCORD_PANEL_CHANNEL_ID=your_panel_channel_id
```

---

## Ollama (Local LLM — Optional)

For offline/local LLM support in addition to the cloud panel:

```bash
# Pull models after stack is running
docker exec solace-ollama ollama pull mistral
docker exec solace-ollama ollama pull llama3.2

# Configure in .env
OLLAMA_DEFAULT_MODEL=mistral
```

---

## GPU Support (Optional)

To enable GPU acceleration for Ollama and HuggingFace models:

```bash
# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

Then uncomment the GPU section in `docker-compose.yml` under the `ollama` service.

---

## Development Mode

For local development with hot-reload:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Dev mode adds:
- Hot-reload for API (Uvicorn `--reload`) and worker (watchmedo)
- Celery Flower at http://localhost:5555
- All database ports exposed for local tools
- Vite HMR for the dashboard
- Lighter resource limits

### Running tests

```bash
# Inside container
make test

# Or locally if Python deps installed
cd solace
PYTHONPATH=. python3 -m pytest tests/test_solace.py -v
# Expected: 129 passed
```

---

## Updating

```bash
git pull origin main
docker compose build --parallel
docker compose up -d
```

Run any new migrations:
```bash
docker compose exec solace-api alembic upgrade head
```

---

## Uninstalling

```bash
# Stop and remove everything (keeps data)
docker compose down

# Remove all data too (DESTRUCTIVE)
make clean
# or
docker compose down -v --remove-orphans
docker system prune -f
```

---

## Troubleshooting

### API won't start
```bash
docker compose logs solace-api
# Common causes:
# - Database not ready → wait 30s and retry
# - Missing env var → check SECRET_KEY is set and >= 32 chars
```

### Database connection refused
```bash
docker compose ps postgres
# If not healthy: docker compose restart postgres
# Check logs: docker compose logs postgres
```

### NLP models failing to load
```bash
docker compose logs solace-worker
# Models download on first use (~4GB total)
# Ensure enough disk space and worker has 4GB+ RAM allocated
```

### Panel engine returns errors
```bash
# Verify API keys work:
python3 -c "import anthropic; c = anthropic.Anthropic(api_key='your_key'); print('OK')"
python3 -c "import openai; c = openai.OpenAI(api_key='your_key'); print('OK')"
```

### Google Drive upload fails
```bash
docker compose logs solace-worker | grep drive
# Check credentials JSON is at the right path
# Check service account has Editor access to the folder
```

See [FAQ.md](FAQ.md) for more.
