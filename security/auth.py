"""JWT token helpers."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from config.settings import get_settings


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_token(*, subject: str, tenant_id: str, role: str, token_type: str, expires_delta: timedelta) -> tuple[str, str, datetime]:
    settings = get_settings()
    jti = uuid.uuid4().hex
    expires_at = _now() + expires_delta
    payload: dict[str, Any] = {
        "sub": subject,
        "tenant_id": tenant_id,
        "role": role,
        "jti": jti,
        "type": token_type,
        "iat": int(_now().timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)
    return token, jti, expires_at


def create_access_token(subject: str, tenant_id: str, role: str) -> tuple[str, str, datetime]:
    return create_token(subject=subject, tenant_id=tenant_id, role=role, token_type="access", expires_delta=timedelta(minutes=get_settings().access_token_expire_minutes))


def create_refresh_token(subject: str, tenant_id: str, role: str) -> tuple[str, str, datetime]:
    return create_token(subject=subject, tenant_id=tenant_id, role=role, token_type="refresh", expires_delta=timedelta(days=get_settings().refresh_token_expire_days))


def decode_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
