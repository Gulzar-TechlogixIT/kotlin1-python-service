import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"


def test_health_message_and_summary_routes():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    env = os.environ.copy()
    env["PORT"] = str(port)
    process = subprocess.Popen(
        [sys.executable, str(SRC / "kotlin1_python_service" / "server.py")],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        base = f"http://127.0.0.1:{port}"
        last_error = None
        for _ in range(40):
            try:
                with urllib.request.urlopen(base + "/health", timeout=1) as response:
                    health = json.loads(response.read())
                break
            except Exception as exc:  # server may still be starting
                last_error = exc
                time.sleep(0.1)
        else:
            raise AssertionError(f"service did not start: {last_error}")

        assert health == {"status": "ok", "service": "kotlin1-python-service"}
        with urllib.request.urlopen(base + "/api/message", timeout=2) as response:
            message = json.loads(response.read())
        assert message["service"] == "kotlin1-python-service"
        assert message["message"] == "Hello from Kotlin1 Python service"
        with urllib.request.urlopen(base + "/api/summary", timeout=2) as response:
            summary = json.loads(response.read())
        assert summary["application"] == "Kotlin1"
        assert summary["status"] == "ok"
    finally:
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)
