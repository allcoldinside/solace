"""JWT token helpers (pure-Python HS256, no cryptography dependency)."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from config.settings import get_settings


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_decode(data: str) -> bytes:
    pad = 4 - len(data) % 4
    if pad != 4:
        data += "=" * pad
    return base64.urlsafe_b64decode(data)


def _sign(header_b64: str, payload_b64: str, secret: str) -> str:
    msg = f"{header_b64}.{payload_b64}".encode()
    sig = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
    return _b64url_encode(sig)


def _encode(payload: dict[str, Any], secret: str) -> str:
    header = _b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    body = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    sig = _sign(header, body, secret)
    return f"{header}.{body}.{sig}"


def _decode(token: str, secret: str) -> dict[str, Any]:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("malformed token")
        header_b64, body_b64, sig = parts
        expected = _sign(header_b64, body_b64, secret)
        if not hmac.compare_digest(expected, sig):
            raise ValueError("invalid signature")
        payload: dict[str, Any] = json.loads(_b64url_decode(body_b64))
        now = int(datetime.now(timezone.utc).timestamp())
        if "exp" in payload and now > payload["exp"]:
            raise ValueError("token expired")
        return payload
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid token: {exc}") from exc


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
    token = _encode(payload, settings.secret_key)
    return token, jti, expires_at


def create_access_token(subject: str, tenant_id: str, role: str) -> tuple[str, str, datetime]:
    return create_token(subject=subject, tenant_id=tenant_id, role=role, token_type="access", expires_delta=timedelta(minutes=get_settings().access_token_expire_minutes))


def create_refresh_token(subject: str, tenant_id: str, role: str) -> tuple[str, str, datetime]:
    return create_token(subject=subject, tenant_id=tenant_id, role=role, token_type="refresh", expires_delta=timedelta(days=get_settings().refresh_token_expire_days))


def decode_token(token: str) -> dict[str, Any]:
    return _decode(token, get_settings().secret_key)
