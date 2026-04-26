from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'SOLACE'
    env: str = 'dev'
    api_prefix: str = '/api'
    secret_key: str = Field('change-me-in-env-please-32-characters-minimum', min_length=32)
    access_token_exp_minutes: int = 30
    refresh_token_exp_minutes: int = 60 * 24 * 7
    algorithm: str = 'HS256'

    database_url: str = Field('sqlite+aiosqlite:///./solace.db', alias='DATABASE_URL')
    redis_url: str = Field('redis://localhost:6379/0', alias='REDIS_URL')
    celery_broker_url: str = Field('redis://localhost:6379/0', alias='CELERY_BROKER_URL')
    celery_result_backend: str = Field('redis://localhost:6379/0', alias='CELERY_RESULT_BACKEND')

    cors_origins: list[str] = ['*']
    default_tenant_id: str = 'default'
    rate_limit_per_minute: int = 120


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
