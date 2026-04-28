"""Secrets helper – centralises secret retrieval.

In local/dev mode secrets come from environment variables via Settings.
In production, swap this module to pull from Vault, AWS Secrets Manager, etc.
"""
from config.settings import get_settings


def get_secret_key() -> str:
    return get_settings().secret_key


def get_database_url() -> str:
    return get_settings().database_url


def get_redis_url() -> str:
    return get_settings().redis_url
