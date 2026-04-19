# SOLACE — FAQ & Troubleshooting

---

## General Questions

### How long does a full collection take?

Typically 5–15 minutes depending on:
- Number of API keys configured (more keys = more sources)
- Target type (organizations have more corporate data, IPs have more network data)
- Network speed to external APIs
- Whether Tor is enabled (SPIDER-4 is slower)
- NLP model loading time on first run (~2 minutes on cold start)

The panel session adds another 5–20 minutes depending on `MAX_PANEL_ROUNDS`.

### How much does each collection cost in API fees?

Rough estimate per full pipeline run:
- **Claude Opus** (report summary + panel): ~$0.15–$0.30
- **GPT-4o** (panel): ~$0.10–$0.20
- **Gemini 1.5 Pro** (panel direction + synthesis): ~$0.03–$0.06
- **Total per collection**: ~$0.30–$0.60

Varies significantly by report size and panel rounds.

### Can I run without all three AI API keys?

The **collection, NLP, and report generation** will work with only the `ANTHROPIC_API_KEY`. The report executive summary and key findings require Claude. The panel engine requires all three.

If you only have one key, you can skip the panel step by running collection only:
```bash
# Collection + report only (no panel)
curl -X POST http://localhost:8000/api/collections \
  -d '{"target":"X","target_type":"organization"}'
```

### Is my data stored anywhere outside my server?

No. The only data that leaves your server is:
- API calls to Anthropic, OpenAI, and Google AI (your input + report content)
- API calls to OSINT services you've configured (Shodan, VirusTotal, etc.)
- Reports uploaded to Google Drive (if configured)

No analytics, telemetry, or data is sent to any SOLACE service.

### What's the difference between SOLACE and existing OSINT tools like Maltego?

Maltego is a manual, GUI-based tool for building entity graphs. SOLACE automates the entire workflow: collection → enrichment → reporting → AI analysis. The 3-AI panel is unique — no other tool has automated structured debate between multiple AI systems as an analysis step.

---

## Installation Issues

### Docker containers won't start

```bash
# Check Docker daemon
systemctl status docker

# Check compose syntax
docker compose config

# Check resource availability
df -h          # Disk space
free -h        # RAM
```

### "Secret key must be at least 32 characters"

Generate a proper key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
# Copy output to SECRET_KEY= in .env
```

### Postgres container not healthy

```bash
docker compose logs postgres
# Common: wrong password, previous data directory with different password

# Nuclear reset (destroys all data)
docker compose down -v
docker compose up -d postgres
```

### "No module named trafilatura" or similar

This is expected in test environments. The spiders have optional dependencies that are only needed when actually collecting. In the Docker environment, all dependencies are installed.

If running outside Docker:
```bash
pip install -r requirements.txt
```

### NLP models downloading slowly

The HuggingFace models (~4GB total) download on first use. This is expected. Set your HuggingFace token for faster downloads:
```bash
HUGGINGFACE_TOKEN=hf_...
```

---

## Panel Engine Issues

### Panel session fails immediately

Check API keys:
```bash
# Test each key
python3 -c "
import anthropic
c = anthropic.Anthropic(api_key='your_key')
r = c.messages.create(model='claude-opus-4-5', max_tokens=10, messages=[{'role':'user','content':'hi'}])
print('Claude OK:', r.content[0].text)
"
```

### "httpx" version error

If you see `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`:
```bash
pip install httpx==0.27.2
```

This is a known incompatibility between openai SDK 1.51.x and httpx 0.28+. The `requirements.txt` pins the correct version.

### Panel loops detected on every turn

The loop detection threshold may be too low. Increase it:
```bash
LOOP_DETECTION_THRESHOLD=0.80  # More lenient (0.0–1.0)
```

Or the `sentence-transformers` model isn't available and it's falling back to keyword overlap. Check:
```bash
python3 -c "from sentence_transformers import SentenceTransformer; print('OK')"
```

### Panel takes too long

Reduce rounds:
```bash
MAX_PANEL_ROUNDS=3
```

Or reduce tokens per turn:
```bash
PANEL_MAX_TOKENS=800
```

---

## Google Drive Issues

### Reports not appearing in Drive

1. Check credentials file exists: `ls credentials/google_service_account.json`
2. Check service account email has Editor access to the folder
3. Check folder ID in `.env` is correct
4. Check worker logs: `docker compose logs solace-worker | grep drive`

### "Service account has insufficient permissions"

The service account needs **Editor** (not Viewer) access to the Drive folder. Re-share the folder with the service account email.

---

## Telegram Issues

### Bot doesn't respond to commands

1. Start a chat with your bot — bots can only receive messages after you initiate
2. Check bot token: `https://api.telegram.org/bot{TOKEN}/getMe`
3. Check container is running: `docker compose ps telegram-collector`

### `/run` command doesn't trigger collection

The Celery worker must be running:
```bash
docker compose ps solace-worker
# Should show "Up"
docker compose logs solace-worker | tail -20
```

---

## Database Issues

### pgvector extension error

```bash
docker compose exec postgres psql -U solace -d solace -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

If this fails, ensure you're using `pgvector/pgvector:pg16` image (not plain postgres).

### Neo4j not connecting

```bash
docker compose logs neo4j | tail -20
# Check password matches NEO4J_PASSWORD in .env
# First start takes 1-2 minutes
```

### "Out of disk space" on collections

ClickHouse and MongoDB can grow large. Check:
```bash
docker system df
du -sh /var/lib/docker/volumes/
```

Prune old collection data:
```bash
# Delete raw intel items older than 90 days
docker compose exec postgres psql -U solace -d solace -c "
DELETE FROM raw_intel_items WHERE collected_at < NOW() - INTERVAL '90 days';
"
```

---

## Performance

### Collections are slow

Enable parallel collection (already default — verify Celery worker has concurrency):
```bash
docker compose logs solace-worker | grep concurrency
# Should show --concurrency=2 or higher
```

Increase concurrency in docker-compose.yml:
```yaml
command: celery -A tasks.celery_app worker --concurrency=4 -Q collection,panel,nlp
```

### Dashboard is slow to load reports

Ensure pgvector index exists:
```bash
docker compose exec postgres psql -U solace -d solace -c "
CREATE INDEX IF NOT EXISTS reports_embedding_idx ON reports USING ivfflat (embedding vector_cosine_ops);
"
```

### NLP enrichment taking > 10 minutes

Increase worker memory allocation in `docker-compose.yml`:
```yaml
solace-worker:
  deploy:
    resources:
      limits:
        memory: 8g
```

---

## Security

### Changing passwords after initial setup

```bash
# Stop everything
docker compose down

# Update passwords in .env
# Then update in databases:

# PostgreSQL
docker compose up -d postgres
docker compose exec postgres psql -U solace -c "ALTER USER solace PASSWORD 'new_password';"

# Redis
docker compose up -d redis
docker compose exec redis redis-cli CONFIG SET requirepass new_password

# Update all POSTGRES_PASSWORD, REDIS_PASSWORD etc. in .env
docker compose up -d
```

### Exposing SOLACE to the internet

By default, only port 80/443 (Caddy) and 3000/8000 (dashboard/API) are exposed. To expose publicly:

1. Set a real domain in `.env`: `SOLACE_DOMAIN=solace.yourdomain.com`
2. Ensure ports 80 and 443 are open on your firewall
3. Caddy will automatically obtain TLS certificates via Let's Encrypt
4. Consider enabling Authentik SSO for authentication

### TLP:RED alert delivery

TLP:RED alerts go to Signal (if configured). Signal requires:
1. A registered phone number
2. `signal-cli` daemon running in the container
3. `SIGNAL_SENDER_NUMBER` set to that number
4. Recipients configured in your Signal account

---

## Customization

### Adding a new spider bot

See [COLLECTORS.md](COLLECTORS.md) — Adding Custom Collectors.

### Changing panel analyst prompts

Edit `panel/prompts.py`. The prompts are clearly labeled and documented. Test changes:
```bash
PYTHONPATH=. python3 -m pytest tests/test_solace.py::TestPanelPrompts -v
```

### Changing report schema

Edit `reports/schema.py`. The `to_markdown()` method controls the final report format. After changes:
```bash
PYTHONPATH=. python3 -m pytest tests/test_solace.py::TestReportSchema -v
```

### Custom confidence thresholds

```python
# In reports/generator.py — _score_confidence()
# Current formula:
score = (avg_reliability * 0.5) + (source_diversity/8 * 0.3) + (volume/20 * 0.2)

# Adjust weights to match your requirements:
# e.g., weight volume more heavily:
score = (avg_reliability * 0.4) + (source_diversity/8 * 0.2) + (volume/20 * 0.4)
```
