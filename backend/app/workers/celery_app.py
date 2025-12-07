"""Celery application configuration."""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "housemusic",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.task_routes = {"app.workers.tasks_*": {"queue": "default"}}
celery_app.autodiscover_tasks(packages=["app.workers"])
