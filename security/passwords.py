"""Password hashing helpers."""

from __future__ import annotations

import hashlib
import hmac
import os

try:
    from passlib.context import CryptContext
except Exception:  # pragma: no cover
    CryptContext = None

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") if CryptContext else None


def hash_password(password: str) -> str:
    if _pwd_context is not None:
        return _pwd_context.hash(password)
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()
    return f"pbkdf2_sha256${salt}${digest}"


def verify_password(password: str, password_hash: str) -> bool:
    if _pwd_context is not None and not password_hash.startswith("pbkdf2_sha256$"):
        return _pwd_context.verify(password, password_hash)
    try:
        _, salt, digest = password_hash.split("$", 2)
        test = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()
        return hmac.compare_digest(test, digest)
    except Exception:
        return False
