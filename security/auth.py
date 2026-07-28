import base64
import hashlib
import hmac
import json
import time
import uuid
from datetime import datetime, timedelta, timezone

from config.settings import get_settings

settings = get_settings()


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_decode(s: str) -> bytes:
    pad = 4 - len(s) % 4
    return base64.urlsafe_b64decode(s + "=" * pad)


def _encode(sub: str, tenant_id: str, role: str, expires_min: int, token_type: str) -> str:
    now = int(time.time())
    header = _b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = _b64url_encode(
        json.dumps(
            {
                "sub": sub,
                "tenant_id": tenant_id or settings.default_tenant_id,
                "role": role,
                "type": token_type,
                "jti": str(uuid.uuid4()),
                "iat": now,
                "exp": now + expires_min * 60,
            },
            separators=(",", ":"),
        ).encode()
    )
    sig_input = f"{header}.{payload}".encode()
    sig = hmac.new(settings.secret_key.encode(), sig_input, hashlib.sha256).digest()
    return f"{header}.{payload}.{_b64url_encode(sig)}"


def create_access_token(sub: str, tenant_id: str, role: str) -> str:
    return _encode(sub, tenant_id, role, settings.access_token_exp_minutes, "access")


def create_refresh_token(sub: str, tenant_id: str, role: str) -> str:
    return _encode(sub, tenant_id, role, settings.refresh_token_exp_minutes, "refresh")


def decode_token(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("invalid token format")
    header_b64, payload_b64, sig_b64 = parts
    sig_input = f"{header_b64}.{payload_b64}".encode()
    expected = hmac.new(settings.secret_key.encode(), sig_input, hashlib.sha256).digest()
    actual = _b64url_decode(sig_b64)
    if not hmac.compare_digest(expected, actual):
        raise ValueError("invalid token signature")
    payload = json.loads(_b64url_decode(payload_b64))
    if payload.get("exp", 0) < int(time.time()):
        raise ValueError("token expired")
    return payload
