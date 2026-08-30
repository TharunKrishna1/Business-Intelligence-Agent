"""Configuration management using Pydantic Settings."""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    # monday.com API Settings (Read-Only)
    MONDAY_API_TOKEN: Optional[str] = None
    DEALS_BOARD_ID: Optional[str] = None
    WORK_ORDERS_BOARD_ID: Optional[str] = None
    MONDAY_API_URL: str = "https://api.monday.com/v2"

    # Gemini AI API Key
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Application Settings
    APP_NAME: str = "Skylark Drones - monday.com BI Agent"
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # HTTP Client Configuration
    HTTP_TIMEOUT_SECONDS: float = 15.0
    MAX_RETRIES: int = 3
    RETRY_BACKOFF_FACTOR: float = 1.5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    @property
    def is_monday_configured(self) -> bool:
        """Returns True if monday.com API token and board IDs are provided."""
        return bool(self.MONDAY_API_TOKEN and self.DEALS_BOARD_ID and self.WORK_ORDERS_BOARD_ID)

    @property
    def is_gemini_configured(self) -> bool:
        """Returns True if Gemini API key is provided."""
        return bool(self.GEMINI_API_KEY)


settings = Settings()
