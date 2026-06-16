"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Automation Toolkit"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "change-this-to-secure-secret-min-32-chars"
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://ait_user:ait_pass@localhost:5432/ait_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT Auth
    JWT_SECRET_KEY: str = "change-this-jwt-secret-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # AI Providers
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_AI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    MISTRAL_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""

    # Storage
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET: str = "ai-automation-files"

    # Integrations
    GITHUB_TOKEN: str = ""
    SLACK_BOT_TOKEN: str = ""
    DISCORD_BOT_TOKEN: str = ""
    TELEGRAM_BOT_TOKEN: str = ""
    NOTION_API_KEY: str = ""

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
