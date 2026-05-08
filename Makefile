dev:
	uvicorn api.main:app --reload

worker:
	celery -A tasks.celery_app.celery_app worker -Q default,low -l info

worker-high:
	celery -A tasks.celery_app.celery_app worker -Q high,critical -l info

migration:
	alembic revision --autogenerate -m "init"

migrate:
	alembic upgrade head

prod-up:
	docker compose -f docker-compose.prod.yml up -d --build

prod-logs:
	docker compose -f docker-compose.prod.yml logs -f

prod-down:
	docker compose -f docker-compose.prod.yml down

test:
	pytest -v

lint:
	python -m compileall . -q

install:
	pip install -r requirements.txt

.PHONY: dev worker worker-high migration migrate prod-up prod-logs prod-down test lint install
