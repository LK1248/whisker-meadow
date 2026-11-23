"""Tiny local receiver: the sim page POSTs run results here; they're saved under tools/sim/out/<name>.json."""
import http.server, json, pathlib, re
OUT = pathlib.Path(__file__).resolve().parent / 'out'
OUT.mkdir(exist_ok=True)

class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:8766')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        name = re.sub(r'[^a-zA-Z0-9_-]', '', self.path.strip('/')) or 'run'
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        json.loads(body)  # must be valid JSON
        (OUT / f'{name}.json').write_bytes(body)
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self, *a): pass

http.server.HTTPServer(('127.0.0.1', 8767), H).serve_forever()
