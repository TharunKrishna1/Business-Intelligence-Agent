"""Validation utilities for business data fields."""

from typing import Optional, Any
import datetime


def is_valid_number(val: Any) -> bool:
    """Check if value is a valid non-NaN float/int."""
    if val is None:
        return False
    try:
        f = float(val)
        return not (f != f)  # NaN check
    except (ValueError, TypeError):
        return False


def is_valid_date_iso(date_str: Optional[str]) -> bool:
    """Check if date string is in YYYY-MM-DD ISO format."""
    if not date_str:
        return False
    try:
        datetime.date.fromisoformat(date_str)
        return True
    except (ValueError, TypeError):
        return False
