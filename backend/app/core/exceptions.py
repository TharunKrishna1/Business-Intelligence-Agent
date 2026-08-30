"""Custom application exceptions and error models."""

from typing import Any, Optional, Dict


class SkylarkBIException(Exception):
    """Base exception for Skylark BI Agent."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class MondayAPIError(SkylarkBIException):
    """Raised when monday.com API request fails or returns GraphQL errors."""
    pass


class MondayAuthenticationError(MondayAPIError):
    """Raised when monday.com API key is invalid or unauthorized."""
    pass


class MondayBoardNotFoundError(MondayAPIError):
    """Raised when a specified monday.com board cannot be found."""
    pass


class QueryPlannerError(SkylarkBIException):
    """Raised when Gemini structured query planning fails."""
    pass


class DataQualityError(SkylarkBIException):
    """Raised when data quality validation encounters unrecoverable errors."""
    pass


class BIAnalyticsError(SkylarkBIException):
    """Raised when deterministic BI calculations fail."""
    pass
