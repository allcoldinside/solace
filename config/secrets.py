"""Secrets helper — reads from environment / .env via Settings."""
from config.settings import get_settings


def get_secret_key() -> str:
    return get_settings().secret_key


def get_database_url() -> str:
    return get_settings().database_url


def get_redis_url() -> str:
    return get_settings().redis_url
