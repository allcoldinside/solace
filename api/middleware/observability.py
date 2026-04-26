from starlette.middleware.base import BaseHTTPMiddleware
from observability.tracing import new_trace_id


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        trace_id = new_trace_id()
        request.state.trace_id = trace_id
        response = await call_next(request)
        response.headers['X-Trace-ID'] = trace_id
        return response
