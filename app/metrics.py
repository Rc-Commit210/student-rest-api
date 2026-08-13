import time

from flask import Response, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)


REQUEST_COUNT = Counter(
    "student_api_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "student_api_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5),
)


def register_metrics(app):

    @app.before_request
    def start_timer():
        request._prometheus_start_time = time.time()

    @app.after_request
    def record_metrics(response):
        if request.path == "/metrics":
            return response

        endpoint = request.endpoint or "unknown"

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=str(response.status_code),
        ).inc()

        start_time = getattr(
            request,
            "_prometheus_start_time",
            time.time(),
        )

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(time.time() - start_time)

        return response

    @app.route("/metrics")
    def metrics():
        return Response(
            generate_latest(),
            mimetype=CONTENT_TYPE_LATEST,
        )
