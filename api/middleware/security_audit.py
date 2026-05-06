from starlette.middleware.base import BaseHTTPMiddleware

from core.database import SessionLocal
from security.auth import decode_token
from storage.audit_store import AuditStore


class SecurityAuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if response.status_code not in (401, 403):
            return response

        action = 'auth.failure' if response.status_code == 401 else 'authz.denied'
        actor_user_id = 'anonymous'
        tenant_id = 'default'

        auth_header = request.headers.get('authorization', '')
        if auth_header.lower().startswith('bearer '):
            token = auth_header.split(' ', 1)[1].strip()
            try:
                claims = decode_token(token)
                actor_user_id = claims.get('sub', 'anonymous')
                tenant_id = claims.get('tenant_id', 'unknown')
            except Exception:
                pass

        async with SessionLocal() as db:
            await AuditStore(db).create(
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                action=action,
                resource_type='http_endpoint',
                resource_id=request.url.path,
                metadata_json={'method': request.method, 'status_code': response.status_code},
                request_id=getattr(request.state, 'request_id', 'unknown'),
                ip_address=request.client.host if request.client else 'unknown',
                user_agent=request.headers.get('user-agent', 'unknown'),
            )

        return response
