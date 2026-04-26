# Installation

## Prerequisites
- Python 3.11+
- Redis (for Celery broker/backend)
- Optional: Docker + Docker Compose

## Local install
```bash
git clone <your-repo-url>
cd solace
cp .env.example .env
pip install -r requirements.txt
python -m compileall .
pytest -q
```

## Run locally
```bash
uvicorn api.main:app --reload
celery -A tasks.celery_app.celery_app worker -Q default,low -l info
```

## Docker
```bash
docker compose up --build
```

## Production-style compose
```bash
docker compose -f docker-compose.prod.yml up -d --build
```
