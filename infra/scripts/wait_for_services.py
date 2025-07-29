import os
import time
import socket
import requests

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "0.0.0.0")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_HEALTHCHECK = f"http://{API_HOST}:{API_PORT}/docs"

def wait_for_port(host, port, service_name):
    print(f"🔴 Waiting for {service_name} at {host}:{port}")
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"🟢 {service_name} is ready!\n")
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

if __name__ == "__main__":
    wait_for_port(POSTGRES_HOST, POSTGRES_PORT, "PostgreSQL")
    wait_for_port(API_HOST, API_PORT, "API TCP port")
    wait_for_api(API_HEALTHCHECK)