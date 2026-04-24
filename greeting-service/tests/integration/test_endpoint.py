import json
import threading
import unittest
from contextlib import contextmanager
from urllib.request import urlopen

from src.main import create_server


@contextmanager
def running_server():
    server = create_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


class EndpointTests(unittest.TestCase):
    def test_hello_endpoint_returns_json(self):
        with running_server() as server:
            url = (
                f"http://127.0.0.1:{server.server_port}"
                "/hello?name=Workshop&lang=fr"
            )
            with urlopen(url) as response:
                payload = json.loads(response.read().decode("utf-8"))

        self.assertEqual(200, response.status)
        self.assertEqual(
            {"greeting": "Bonjour, Workshop!", "language": "fr"},
            payload,
        )

    def test_unknown_route_returns_404(self):
        with running_server() as server:
            url = f"http://127.0.0.1:{server.server_port}/missing"
            try:
                urlopen(url)
            except Exception as error:
                payload = json.loads(error.read().decode("utf-8"))
                status_code = error.code

        self.assertEqual(404, status_code)
        self.assertEqual({"error": "Not found"}, payload)


if __name__ == "__main__":
    unittest.main()
