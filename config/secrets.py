"""Secrets access helpers.

Reads values from environment / settings. Extend this module to support
external vaults (AWS Secrets Manager, HashiCorp Vault, etc.) without
changing call sites.
"""

from __future__ import annotations

from config.settings import get_settings


def get_secret_key() -> str:
    return get_settings().secret_key


def get_database_url() -> str:
    return get_settings().sqlalchemy_database_url


def get_redis_url() -> str:
    return get_settings().redis_url
