from datetime import datetime, timedelta, timezone
import uuid
import jwt
from config.settings import get_settings


settings = get_settings()


def _encode(sub: str, tenant_id: str, role: str, expires_min: int, token_type: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'sub': sub,
        'tenant_id': tenant_id or settings.default_tenant_id,
        'role': role,
        'type': token_type,
        'jti': str(uuid.uuid4()),
        'iat': int(now.timestamp()),
        'exp': int((now + timedelta(minutes=expires_min)).timestamp()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(sub: str, tenant_id: str, role: str) -> str:
    return _encode(sub, tenant_id, role, settings.access_token_exp_minutes, 'access')


def create_refresh_token(sub: str, tenant_id: str, role: str) -> str:
    return _encode(sub, tenant_id, role, settings.refresh_token_exp_minutes, 'refresh')


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
