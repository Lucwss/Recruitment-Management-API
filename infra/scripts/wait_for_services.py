import asyncio
import os
import socket
import time

import requests
from tortoise import Tortoise

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", 8000))
API_HEALTHCHECK = f"http://{API_HOST}:{API_PORT}/docs"


def wait_for_port():
    print(f"🔴 Waiting for PostgreSQL at {POSTGRES_HOST}:{POSTGRES_PORT}")
    while True:
        try:
            with socket.create_connection((POSTGRES_HOST, POSTGRES_PORT), timeout=2):
                print("🟢 PostgreSQL is ready!\n")
                return
        except (socket.timeout, ConnectionRefusedError):
            print(".", end="", flush=True)
            time.sleep(1)


def wait_for_api(url):
    print(f"🔴 Waiting for API at {url}")
    while True:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code < 500:
                print("🟢 API is ready!\n")
                return
        except requests.exceptions.RequestException:
            print(".", end="", flush=True)
            time.sleep(1)


async def clear_database():
    print("🟢 Cleaning database ... \n")
    for model in Tortoise.apps.get("models", {}).values():
        await model.all().delete()


if __name__ == "__main__":
    wait_for_port()
    wait_for_api(API_HEALTHCHECK)
    asyncio.run(clear_database())
