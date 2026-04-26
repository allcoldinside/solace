"""Application settings for SOLACE."""

from __future__ import annotations

import secrets
from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False, populate_by_name=True)

    app_name: str = "SOLACE"
    environment: Literal["local", "test", "dev", "staging", "production"] = "local"
    debug: bool = False
    version: str = "1.0.0"
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(48), min_length=32, alias="SECRET_KEY")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14
    postgres_url: str = Field(default="postgresql+asyncpg://solace:solace@localhost:5432/solace", alias="POSTGRES_URL")
    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    celery_broker_url: str | None = Field(default=None, alias="CELERY_BROKER_URL")
    celery_result_backend: str | None = Field(default=None, alias="CELERY_RESULT_BACKEND")
    default_tenant_id: str = "default"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000", "http://localhost:5173"])
    rate_limit_requests: int = 120
    rate_limit_window_seconds: int = 60
    log_level: str = "INFO"
    json_logs: bool = True
    default_classification: str = "TLP:WHITE"
    max_panel_rounds: int = 3
    pipeline_queue: str = "default"

    @field_validator("database_url", mode="after")
    @classmethod
    def normalize_database_url(cls, value: str | None) -> str | None:
        if value and value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+asyncpg://", 1)
        return value

    @property
    def sqlalchemy_database_url(self) -> str:
        value = self.database_url or self.postgres_url
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+asyncpg://", 1)
        return value

    @property
    def resolved_celery_broker_url(self) -> str:
        return self.celery_broker_url or self.redis_url

    @property
    def resolved_celery_result_backend(self) -> str:
        return self.celery_result_backend or self.redis_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
