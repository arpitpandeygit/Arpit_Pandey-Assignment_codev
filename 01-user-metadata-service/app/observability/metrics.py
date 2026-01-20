from prometheus_client import Counter, Histogram

TOTAL_REQUESTS = Counter(
    "total_requests",
    "Total HTTP requests"
)

SUCCESS_COUNT = Counter(
    "success_count",
    "Total successful requests"
)

FAILURE_COUNT = Counter(
    "failure_count",
    "Total failed requests"
)

REQUEST_LATENCY = Histogram(
    "request_latency_ms",
    "Request latency in ms"
)

