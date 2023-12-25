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
    result_backend=os.environ.get(
        "CELERY_RESULT_BACKEND"
    ),
)
