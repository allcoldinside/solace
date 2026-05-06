from starlette.middleware.base import BaseHTTPMiddleware

from observability.tracing import new_trace_id


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get('X-Request-ID') or new_trace_id()
        request.state.trace_id = request_id
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers['X-Trace-ID'] = request_id
        response.headers['X-Request-ID'] = request_id
        return response
