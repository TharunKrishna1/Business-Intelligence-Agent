"""Unit tests for configuration and logging."""

import logging
from app.core.config import Settings
from app.core.logging import SecretMaskingFormatter


def test_default_settings():
    settings = Settings()
    assert settings.APP_NAME == "Skylark Drones - monday.com BI Agent"
    assert settings.MONDAY_API_URL == "https://api.monday.com/v2"
    assert settings.HTTP_TIMEOUT_SECONDS == 15.0


def test_secret_masking_formatter():
    formatter = SecretMaskingFormatter()
    settings = Settings(
        MONDAY_API_TOKEN="super_secret_token_123",
        GEMINI_API_KEY="super_secret_gemini_key_456"
    )
    
    # Temporarily override settings in logger context for test
    from app.core import config
    orig_token = config.settings.MONDAY_API_TOKEN
    orig_key = config.settings.GEMINI_API_KEY
    config.settings.MONDAY_API_TOKEN = "super_secret_token_123"
    config.settings.GEMINI_API_KEY = "super_secret_gemini_key_456"
    
    try:
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="Connecting with token super_secret_token_123 and key super_secret_gemini_key_456",
            args=(), exc_info=None
        )
        formatted = formatter.format(record)
        assert "super_secret_token_123" not in formatted
        assert "***MASKED_MONDAY_TOKEN***" in formatted
        assert "super_secret_gemini_key_456" not in formatted
        assert "***MASKED_GEMINI_KEY***" in formatted
    finally:
        config.settings.MONDAY_API_TOKEN = orig_token
        config.settings.GEMINI_API_KEY = orig_key
