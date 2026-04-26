"""In-memory rate limiting middleware with Redis-ready boundaries."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from config.settings import get_settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._buckets: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        settings = get_settings()
        now = time.monotonic()
        window = settings.rate_limit_window_seconds
        limit = settings.rate_limit_requests
        key = request.client.host if request.client else "unknown"
        bucket = self._buckets[key]
        while bucket and now - bucket[0] > window:
            bucket.popleft()
        if len(bucket) >= limit:
            return JSONResponse(status_code=429, content={"detail": "rate limit exceeded"})
        bucket.append(now)
        return await call_next(request)
