from fastapi import Request
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter("api_requests_total", "Total number of requests")
RESPONSE_TIME = Histogram("api_response_time_seconds", "Response time in seconds")

async def track_metrics(request: Request, call_next):
    REQUEST_COUNT.inc()
    with RESPONSE_TIME.time():
        response = await call_next(request)
    return response
