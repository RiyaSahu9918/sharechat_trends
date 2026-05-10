from http.server import BaseHTTPRequestHandler, HTTPServer

from trend_app.api.router import handle_get, handle_post
from trend_app.config import HOST, PORT
from trend_app.db.schema import init_db
from trend_app.services.trends_service import ensure_seed_data


class TrendsHandler(BaseHTTPRequestHandler):
    def _send(self, status_code: int, content_type: str, body: bytes):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        status_code, content_type, body = handle_get(self.path)
        self._send(status_code, content_type, body)

    def do_POST(self):
        status_code, content_type, body = handle_post(self.path)
        self._send(status_code, content_type, body)


def run_server() -> None:
    init_db()
    ensure_seed_data()
    server = HTTPServer((HOST, PORT), TrendsHandler)
    print(f"Server running on http://{HOST}:{PORT}")
    server.serve_forever()
