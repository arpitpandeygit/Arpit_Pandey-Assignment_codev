import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from app.observability.metrics import (
    TOTAL_REQUESTS,
    SUCCESS_COUNT,
    FAILURE_COUNT,
    REQUEST_LATENCY
)
from app.observability.logging import logger

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        start = time.time()
        TOTAL_REQUESTS.inc()

        try:
            response = await call_next(request)
            latency = (time.time() - start) * 1000
            REQUEST_LATENCY.observe(latency)

            SUCCESS_COUNT.inc()
            logger.info(
                "request_completed",
                request_id=request_id,
                path=request.url.path,
                latency_ms=latency,
                status_code=response.status_code
            )
            return response

        except Exception as e:
            latency = (time.time() - start) * 1000
            FAILURE_COUNT.inc()

            logger.error(
                "request_failed",
                request_id=request_id,
                path=request.url.path,
                latency_ms=latency,
                error=str(e)
            )
            raise

