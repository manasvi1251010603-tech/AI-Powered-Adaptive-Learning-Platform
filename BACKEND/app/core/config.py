from functools import lru_cache

from pydantic import AnyUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "AI-Powered Adaptive Learning Platform API"
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    api_v1_prefix: str = "/api/v1"

    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    redis_url: str | None = Field(default=None, alias="REDIS_URL")
    jwt_secret_key: str | None = Field(default=None, alias="JWT_SECRET_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    storage_endpoint: str | None = Field(default=None, alias="STORAGE_ENDPOINT")
    storage_bucket: str | None = Field(default=None, alias="STORAGE_BUCKET")
    storage_access_key: str | None = Field(default=None, alias="STORAGE_ACCESS_KEY")
    storage_secret_key: str | None = Field(default=None, alias="STORAGE_SECRET_KEY")
    storage_region: str | None = Field(default=None, alias="STORAGE_REGION")

    frontend_origin: AnyUrl | str = Field(
        default="http://localhost:3000",
        alias="FRONTEND_ORIGIN",
    )

    @field_validator("database_url", "redis_url", mode="before")
    @classmethod
    def empty_string_to_none(cls, value: str | None) -> str | None:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @field_validator("frontend_origin", mode="before")
    @classmethod
    def normalize_frontend_origin(cls, value: str) -> str:
        return value.rstrip("/")

    @property
    def is_development(self) -> bool:
        return self.environment.lower() in {"development", "dev", "local"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
