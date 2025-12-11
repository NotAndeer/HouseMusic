"""Celery application configuration."""

from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "housemusic",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks_webhooks", "app.workers.tasks_campaigns"],
)

# Security and serialization
celery_app.conf.accept_content = ["json"]
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.result_expires = 3600  # 1 hour

# Task routing
celery_app.conf.task_routes = {
    "app.workers.tasks_webhooks.*": {"queue": "webhooks"},
    "app.workers.tasks_campaigns.*": {"queue": "campaigns"},
}

# Worker behavior
celery_app.conf.task_acks_late = True
celery_app.conf.worker_prefetch_multiplier = 1