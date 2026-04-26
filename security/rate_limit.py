import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from config.settings import get_settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.limit = get_settings().rate_limit_per_minute
        self.bucket: dict[str, list[float]] = {}

    async def dispatch(self, request, call_next):
        ip = request.client.host if request.client else 'unknown'
        now = time.time()
        vals = [t for t in self.bucket.get(ip, []) if now - t < 60]
        if len(vals) >= self.limit:
            return JSONResponse({'detail': 'rate limit exceeded'}, status_code=429)
        vals.append(now)
        self.bucket[ip] = vals
        return await call_next(request)
