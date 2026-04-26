.PHONY: dev worker worker-high migration migrate prod-up prod-logs test compile

dev:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

worker:
	celery -A tasks.celery_app.celery_app worker -Q default,low --loglevel=INFO

worker-high:
	celery -A tasks.celery_app.celery_app worker -Q high,critical --loglevel=INFO

migration:
	alembic revision --autogenerate -m "schema update"

migrate:
	alembic upgrade head

prod-up:
	docker compose -f docker-compose.prod.yml up -d --build

prod-logs:
	docker compose -f docker-compose.prod.yml logs -f

test:
	pytest -q

compile:
	python -m compileall .
