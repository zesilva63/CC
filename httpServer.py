import http.server
import socketserver

TCP_PORT = 80

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("localhost",TCP_PORT), Handler) as httpd:
    httpd.serve_forever()
