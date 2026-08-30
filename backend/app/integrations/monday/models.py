"""Pydantic data models for monday.com GraphQL API entities."""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class MondayColumnValue(BaseModel):
    """Raw column value from monday.com API."""
    id: str
    title: Optional[str] = None
    text: Optional[str] = None
    value: Optional[str] = None
    type: Optional[str] = None


class MondayItem(BaseModel):
    """Raw item (row) from monday.com API."""
    id: str
    name: str
    column_values: List[MondayColumnValue] = Field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class MondayItemsPage(BaseModel):
    """Paginated items wrapper from monday.com GraphQL API."""
    cursor: Optional[str] = None
    items: List[MondayItem] = Field(default_factory=list)


class MondayBoard(BaseModel):
    """Monday.com Board response model."""
    id: str
    name: str
    items_page: Optional[MondayItemsPage] = None
    items: Optional[List[MondayItem]] = None


class MondayFetchResult(BaseModel):
    """Wrapper for fetched board items."""
    board_id: str
    board_name: str
    raw_items: List[MondayItem] = Field(default_factory=list)
    is_mock: bool = False
