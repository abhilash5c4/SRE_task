# Simple Flask metrics application using prometheus_client
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
from prometheus_client import multiprocess, make_wsgi_app
from prometheus_client.core import CollectorRegistry
import random
import time
from flask import Flask, Response

app = Flask(__name__)

# Create a dedicated registry for clarity
REGISTRY = CollectorRegistry()

# Custom application metrics
REQUESTS = Counter('example_app_requests_total', 'Total number of requests', ['path'], registry=REGISTRY)
IN_PROGRESS = Gauge('example_app_requests_inprogress', 'In-progress requests', registry=REGISTRY)
PROCESS_TIME = Histogram('example_app_process_seconds', 'Processing time in seconds', registry=REGISTRY, buckets=(0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5))

@app.route("/")
def root():
    return "Hello! visit /work to simulate work, /metrics for Prometheus metrics.\n"

@app.route("/work")
def work():
    REQUESTS.labels(path="/work").inc()
    IN_PROGRESS.inc()
    start = time.time()
    # Simulate variable work
    time.sleep(random.uniform(0.01, 0.4))
    PROCESS_TIME.observe(time.time() - start)
    IN_PROGRESS.dec()
    return "Work done\n"

@app.route("/metrics")
def metrics():
    # Return metrics in Prometheus text format
    data = generate_latest(REGISTRY)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    # Use built-in server for simplicity in container (could use Gunicorn)
    app.run(host="0.0.0.0", port=8000)