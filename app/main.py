import json
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from worker.task import bar, baz, error_handler, foo

load_dotenv()

app = FastAPI()


class Item(BaseModel):
    amount: int
    x: int
    y: int


@app.post("/task-foo")
def task_foo(item: Item):
    foo.apply_async((item.amount, item.x, item.y), link_error=error_handler.s(), priority=0)
    return JSONResponse({"Result": "OK"})


@app.post("/task-bar")
def task_bar(item: Item):
    bar.apply_async((item.amount, item.x, item.y), link_error=error_handler.s(), priority=10)
    return JSONResponse({"Result": "OK"})


@app.post("/task-baz")
def task_baz(item: Item):
    baz.apply_async((item.amount, item.x, item.y), link_error=error_handler.s())
    return JSONResponse({"Result": "OK"})


@app.post("/run-task-flower")
async def run_task(item: Item):
    flower_host = "http://flower:5555"
    task_name = "foo"
    task_args = [item.amount, item.x, item.y]
    status_success = 200

    flower_user = os.getenv("FLOWER_USER")
    flower_password = os.getenv("FLOWER_PASSWORD")

    auth = (flower_user, flower_password)

    headers = {
        "Content-Type": "application/json",
    }

    payload = json.dumps({"args": task_args})

    response = httpx.post(
        f"{flower_host}/api/task/async-apply/{task_name}",
        headers=headers,
        data=payload,
        auth=auth,
    )

    if response.status_code == status_success:
        print("Task executed successfully:", response.json())
    else:
        print("Failed to execute task:", response.status_code, response.text)

    return JSONResponse({"Result": "OK"})
