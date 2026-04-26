"""Celery application entrypoint."""

from __future__ import annotations

from celery import Celery
from kombu import Queue

from config.settings import get_settings
from tasks.queues import CRITICAL, DEFAULT, HIGH, LOW

settings = get_settings()

celery_app = Celery("solace", broker=settings.resolved_celery_broker_url, backend=settings.resolved_celery_result_backend)
celery_app.conf.task_queues = (Queue(LOW), Queue(DEFAULT), Queue(HIGH), Queue(CRITICAL))
celery_app.conf.task_default_queue = DEFAULT
celery_app.conf.task_routes = {"tasks.celery_app.run_pipeline_task": {"queue": DEFAULT}}


@celery_app.task(name="tasks.celery_app.run_pipeline_task")
def run_pipeline_task(payload: dict) -> dict:
    return {"accepted": True, "payload": payload}
