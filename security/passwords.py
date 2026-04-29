"""Password hashing helpers."""

from __future__ import annotations

import hashlib
import hmac
import os

try:
    import bcrypt as _bcrypt_lib
    _BCRYPT_AVAILABLE = True
except Exception:
    _BCRYPT_AVAILABLE = False


def hash_password(password: str) -> str:
    if _BCRYPT_AVAILABLE:
        salt = _bcrypt_lib.gensalt()
        return _bcrypt_lib.hashpw(password.encode(), salt).decode()
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()
    return f"pbkdf2_sha256${salt}${digest}"


def verify_password(password: str, password_hash: str) -> bool:
    if password_hash.startswith("pbkdf2_sha256$"):
        try:
            _, salt, digest = password_hash.split("$", 2)
            test = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()
            return hmac.compare_digest(test, digest)
        except Exception:
            return False
    if _BCRYPT_AVAILABLE:
        try:
            return _bcrypt_lib.checkpw(password.encode(), password_hash.encode())
        except Exception:
            return False
    return False
