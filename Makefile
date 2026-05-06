.PHONY: dev worker beat test lint migrate migration compose-up compose-down

dev:
	uvicorn api.main:app --reload

worker:
	celery -A tasks.celery_app.celery_app worker -Q default,low,high,critical -l info

beat:
	celery -A tasks.celery_app.celery_app beat -l info

test:
	pytest -q

lint:
	ruff check .

migration:
	alembic revision --autogenerate -m "init"

migrate:
	alembic upgrade head

compose-up:
	docker compose up --build

compose-down:
	docker compose down
