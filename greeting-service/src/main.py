"""HTTP entry point for the greeting service."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from src.greeter import build_response

CONTENT_TYPE = "application/json; charset=utf-8"


def _first(values):
    return values[0] if values else None


class GreetingRequestHandler(BaseHTTPRequestHandler):
    server_version = "GreetingService/0.1"

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/hello":
            self._handle_hello(parsed.query)
            return

        if parsed.path == "/health":
            self._write_json(200, {"status": "ok"})
            return

        self._write_json(404, {"error": "Not found"})

    def log_message(self, format_string, *args):
        # Disable access logs so user-provided query strings never hit stdout.
        return

    def _handle_hello(self, query):
        params = parse_qs(query, keep_blank_values=True)
        status_code, payload = build_response(
            name=_first(params.get("name")),
            lang=_first(params.get("lang")),
        )
        self._write_json(status_code, payload)

    def _write_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode(
            "utf-8"
        )
        self.send_response(status_code)
        self.send_header("Content-Type", CONTENT_TYPE)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def create_server(host="127.0.0.1", port=8000):
    return ThreadingHTTPServer((host, port), GreetingRequestHandler)


def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    server = create_server(host=host, port=port)
    print(f"Serving greeting-service on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
