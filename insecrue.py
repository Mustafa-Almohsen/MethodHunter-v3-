#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class InsecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_PUT(self):
        length = int(self.headers['Content-Length'])
        path = self.translate_path(self.path)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'wb') as f:
            f.write(self.rfile.read(length))

        self.send_response(200, "OK (File Created)")
        self.end_headers()
        self.wfile.write(b"File uploaded via PUT!\n")

if __name__ == "__main__":
    server_address = ("0.0.0.0", 80)  # listen on port 80
    httpd = HTTPServer(server_address, InsecureHTTPRequestHandler)
    print("🚨 Insecure HTTP server running on http://127.0.0.1:80")
    print("   Allows PUT file upload with no restrictions!")
    httpd.serve_forever()
