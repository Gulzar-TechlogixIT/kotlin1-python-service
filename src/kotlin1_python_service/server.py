"""Small standard-library HTTP service for local development."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os

from py_lib1 import normalize_text
from py_lib_2 import get_logger

PORT = int(os.environ.get("PORT", "8087"))
SERVICE_NAME = "kotlin1-python-service"
logger = get_logger(SERVICE_NAME)


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]

        if path == "/health":
            self._send_json(
                200, {"status": "ok", "service": SERVICE_NAME}
            )
        elif path == "/api/message":
            message = normalize_text("  Hello from   Kotlin1 Python service  ")
            logger.info("Message endpoint requested")
            self._send_json(200, {
                "service": SERVICE_NAME,
                "message": message,
                "sharedLibraries": ["py-lib1", "py-lib-2"],
            })
        elif path == "/api/summary":
            self._send_json(200, {
                "application": "Kotlin1",
                "service": SERVICE_NAME,
                "status": "ok",
                "message": "Independent Python service for Kotlin1",
                "sharedLibraries": ["py-lib1", "py-lib-2"],
            })
        else:
            self._send_json(
                404, {"error": "not found", "service": SERVICE_NAME}
            )

    def log_message(self, fmt: str, *args) -> None:
        logger.info(fmt % args)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    logger.info("%s listening on http://127.0.0.1:%s", SERVICE_NAME, PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Stopping %s", SERVICE_NAME)
    finally:
        server.server_close()
