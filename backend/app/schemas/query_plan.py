"""Pydantic schemas for Gemini Structured Query Planning."""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class QueryIntent(str, Enum):
    PIPELINE_ANALYSIS = "pipeline_analysis"
    SECTOR_ANALYSIS = "sector_analysis"
    WORK_ORDER_ANALYSIS = "work_order_analysis"
    CROSS_BOARD_ANALYSIS = "cross_board_analysis"
    LEADERSHIP_UPDATE = "leadership_update"
    GENERAL_QUERY = "general_query"


class QueryPlanFilter(BaseModel):
    sector: Optional[str] = None
    date_range: Optional[str] = None
    stage: Optional[str] = None
    status: Optional[str] = None
    owner: Optional[str] = None


class QueryPlan(BaseModel):
    """Structured query plan produced by Gemini AI planner."""
    intent: QueryIntent = Field(
        default=QueryIntent.PIPELINE_ANALYSIS,
        description="The primary business intent of the user's question."
    )
    boards_required: List[str] = Field(
        default_factory=lambda: ["deals"],
        description="List of monday.com board IDs or board keys required ('deals', 'work_orders')."
    )
    filters: QueryPlanFilter = Field(
        default_factory=QueryPlanFilter,
        description="Extracted filter dimensions."
    )
    sector: Optional[str] = Field(
        default=None,
        description="Extracted sector name filter if applicable."
    )
    date_range: Optional[str] = Field(
        default=None,
        description="Extracted date range filter (e.g., 'current_quarter', 'this_year')."
    )
    metrics: List[str] = Field(
        default_factory=list,
        description="Requested business metrics to calculate."
    )
    comparison_required: bool = Field(
        default=False,
        description="Whether a cross-sector or cross-period comparison is requested."
    )
    clarification_required: bool = Field(
        default=False,
        description="Set to true if the question is ambiguous and requires founder clarification."
    )
    clarification_question: Optional[str] = Field(
        default=None,
        description="Clarification question to ask the user if ambiguity exists."
    )
