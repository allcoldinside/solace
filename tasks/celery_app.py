from celery import Celery
from kombu import Queue
from config.settings import get_settings

s = get_settings()
celery_app = Celery('solace', broker=s.celery_broker_url, backend=s.celery_result_backend)
celery_app.conf.task_queues = [Queue('low'), Queue('default'), Queue('high'), Queue('critical')]
celery_app.conf.task_default_queue = 'default'
