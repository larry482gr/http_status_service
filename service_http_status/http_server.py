from http.server import HTTPServer
from prometheus_client import start_http_server
from service_http_status.http_handler import HttpHandler

def run_service():
    # Start up the server to expose the metrics.
    start_http_server(8000)
    server = HTTPServer(('', 8001), HttpHandler)
    print("Prometheus metrics available on port 8000 /metrics")
    print("HTTP server available on port 8001")
    server.serve_forever()