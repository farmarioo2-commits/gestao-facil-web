import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class FlutterWebHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self' data: blob: https:; "
            "script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval' https:; "
            "style-src 'self' 'unsafe-inline' https:; "
            "img-src 'self' data: blob: https:; "
            "font-src 'self' data: https:; "
            "connect-src 'self' https: wss:; "
            "worker-src 'self' blob:; "
            "object-src 'none';"
        )
        super().end_headers()

    def do_GET(self):
        requested = Path(self.translate_path(self.path))
        if not requested.exists() and "." not in Path(self.path).name:
            self.path = "/index.html"
        super().do_GET()


port = int(os.environ.get("PORT", "8080"))
server = ThreadingHTTPServer(("0.0.0.0", port), FlutterWebHandler)
print(f"Gestao Facil Web rodando na porta {port}", flush=True)
server.serve_forever()
