import httpx
import json

flower_host = "http://localhost:5556"
task_name = "foo"
task_args = [1, 1, 1]
status_success = 200

auth = ("admin", "admin")

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
    print(
        "Failed to execute task:",
        response.status_code,
        response.text,
    )
