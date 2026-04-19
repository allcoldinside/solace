"""Application settings for SOLACE."""

from pathlib import Path

from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "SOLACE"
    secret_key: str = Field(..., min_length=32)
    postgres_url: str = "postgresql+asyncpg://solace:solace@localhost:5432/solace"
    mongodb_url: str = "mongodb://localhost:27017"
    neo4j_url: str = "bolt://neo4j:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "neo4j"
    redis_url: str = "redis://localhost:6379/0"
    clickhouse_host: str = "clickhouse"
    clickhouse_port: int = 9000
    clickhouse_db: str = "solace"
    clickhouse_user: str = "solace"
    clickhouse_password: str = "solace"
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "solace-artifacts"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    google_ai_api_key: str = ""
    huggingface_token: str = ""
    ollama_host: str = "http://ollama:11434"
    google_drive_credentials_json: Path = Path("credentials/service-account.json")
    google_drive_root_folder_id: str = ""
    google_drive_reports_folder_id: str = ""
    google_drive_assessments_folder_id: str = ""
    telegram_api_id: str = ""
    telegram_api_hash: str = ""
    telegram_bot_token: str = ""
    telegram_alert_chat_id: str = ""
    discord_bot_token: str = ""
    discord_guild_id: str = ""
    discord_alerts_channel_id: str = ""
    discord_panel_channel_id: str = ""
    signal_sender_number: str = ""
    shodan_api_key: str = ""
    virustotal_api_key: str = ""
    alienvault_otx_api_key: str = ""
    greynoise_api_key: str = ""
    censys_api_id: str = ""
    censys_api_secret: str = ""
    opencorporates_api_key: str = ""
    max_panel_rounds: int = 6
    loop_detection_threshold: float = 0.65
    default_classification: str = "TLP:WHITE"
    panel_max_tokens: int = 1500
    tor_socks_proxy: str = "socks5://tor:9050"
    celery_broker_url: str = ""
    celery_result_backend: str = ""

    @field_validator("celery_broker_url", "celery_result_backend", mode="before")
    @classmethod
    def default_celery_to_redis(cls, value: str, info: ValidationInfo) -> str:
        """Default celery endpoints to Redis URL when omitted."""
        if isinstance(value, str) and value:
            return value
        redis_url = str(info.data.get("redis_url", "redis://localhost:6379/0"))
        return redis_url


settings = Settings()
