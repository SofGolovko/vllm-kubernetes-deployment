
import logging
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


def setup_logging(level: str = "INFO") -> None:

    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logging.getLogger("vllm.audit").setLevel(log_level)



setup_logging()
logger = logging.getLogger("vllm.audit")

class SafeAccessLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.info(
                "request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
                request_id, request.method, request.url.path,
                  status_code, duration_ms,
            )
