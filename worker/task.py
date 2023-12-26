import logging
import random
import time

from celery.exceptions import MaxRetriesExceededError

from worker.celery import app

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# engine = create_engine(os.environ.get("DATABASE_URL"))
# Session = sessionmaker(bind=engine)


@app.task
def error_handler(request, exc, traceback):
    print("Task {0} raised exception: {1!r}\n{2!r}".format(request.id, exc, traceback))


@app.task(name="foo", bind=True, max_retries=3, default_retry_delay=60, queue="default")
def foo(self, a, b, c):
    try:
        # session = Session()
        time.sleep(a)
        # session.close()
        return b + c
    except Exception as exc:
        try:
            logging.error("Retrying task")
            self.retry(exc=exc)
        except MaxRetriesExceededError:
            logging.error("Max retries exceeded")


@app.task(name="bar", queue="default")
def bar(a, b, c):
    time.sleep(a)
    return b + c


@app.task(name="baz", queue="baz")
def baz(a, b, c):
    time.sleep(a)
    return b + c


@app.task(name="emoji", queue="schedule")
def emoji():
    emojis = ["🎉", "🌟", "🚀", "👍", "🐍"]
    return random.choice(emojis)
