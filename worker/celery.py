import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

app = Celery(__name__)


app.conf.update(
    result_expires=3600,
    broker_connection_retry_on_startup=True,
    result_accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    include=["worker.task"],
    broker_url=os.environ.get("CELERY_BROKER_URL"),
    result_backend=os.environ.get("CELERY_RESULT_BACKEND"),
    task_queue_max_priority=10,
)

app.conf.broker_transport_options = {
    "queue_order_strategy": "priority",
}

app.conf.beat_schedule = {
    "emoji every 5s": {"task": "worker.task.emoji", "schedule": 5.0},
}

app.conf.timezone = "UTC"
