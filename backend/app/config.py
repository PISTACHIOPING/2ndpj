from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
    )

    app_name: str = "AI Tech Insights API"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ai_insights"
    openai_endpoint: str | None = None
    openai_api_key: str | None = None
    openai_deployment: str | None = None
    openai_api_version: str = "2024-05-01-preview"
    slack_webhook_url: str | None = None
    enable_cors: bool = True
    cors_origins: list[str] = ["http://localhost:5173"]
    redis_url: str = "redis://localhost:6379/0"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
