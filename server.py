#!/usr/bin/env python3
import http.server
import socketserver
import os

os.chdir('/Users/hr_chang/claud')

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"✅ 서버 시작: http://localhost:{PORT}")
    print(f"\n📁 접속 방법:")
    print(f"  - http://localhost:{PORT}/design1_ocean.html")
    print(f"  - http://localhost:{PORT}/design2_forest.html")
    print(f"  - http://localhost:{PORT}/design3_garden.html")
    print(f"  - http://localhost:{PORT}/design4_mandala.html")
    print(f"  - http://localhost:{PORT}/design5_dinosaur.html")
    httpd.serve_forever()
