"""API Routes for Business Intelligence Agent."""

from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.agent.orchestrator import AgentOrchestrator, AgentResponse
from app.data.quality import DataQualityReport
from app.integrations.monday.client import MondayClient
from app.integrations.monday.mapper import map_deals_items, map_work_orders_items
from app.data.normalizer import normalize_deals_dataset, normalize_work_orders_dataset
from app.data.quality import analyze_data_quality
from app.core.config import settings

router = APIRouter(prefix="/api", tags=["BI Agent Query"])

orchestrator = AgentOrchestrator()


class ChatQueryRequest(BaseModel):
    message: str = Field(..., description="User business question", example="How is our overall pipeline looking?")
    session_id: Optional[str] = Field(None, description="Optional session identifier")


class LeadershipUpdateRequest(BaseModel):
    session_id: Optional[str] = None


@router.post("/chat", response_model=AgentResponse)
async def chat_query(request: ChatQueryRequest) -> AgentResponse:
    """Process founder conversational query and return metrics, insights, and charts."""
    try:
        response = await orchestrator.process_query(request.message, request.session_id)
        return response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(exc)}")


@router.post("/leadership-update", response_model=AgentResponse)
async def get_leadership_update(request: LeadershipUpdateRequest) -> AgentResponse:
    """Generate a comprehensive executive leadership update report."""
    try:
        response = await orchestrator.process_query(
            "Prepare a leadership update summarizing sales highlights, operations, risks, and recommendations",
            request.session_id
        )
        return response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate leadership update: {str(exc)}")


@router.get("/data-quality", response_model=DataQualityReport)
async def get_data_quality_report() -> DataQualityReport:
    """Fetch real-time data quality report for monday.com boards."""
    try:
        monday_client = MondayClient()
        deals_raw = await monday_client.fetch_board_items(settings.DEALS_BOARD_ID or "deals", "Deals")
        wo_raw = await monday_client.fetch_board_items(settings.WORK_ORDERS_BOARD_ID or "work_orders", "Work Orders")

        deals_mapped = map_deals_items(deals_raw.raw_items)
        wo_mapped = map_work_orders_items(wo_raw.raw_items)

        deals_norm, d_actions, d_excl = normalize_deals_dataset(deals_mapped)
        wo_norm, w_actions, w_excl = normalize_work_orders_dataset(wo_mapped)

        report = analyze_data_quality(deals_norm, wo_norm, d_actions, w_actions, d_excl, w_excl)
        return report
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to compute data quality report: {str(exc)}")
