import http.server
import socketserver
import config

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("localhost",config.TCP_PORT), Handler) as httpd:
    httpd.serve_forever()
