"""Agent Orchestrator.

Orchestrates data retrieval, normalization, quality analysis, deterministic BI calculations,
and Gemini insight synthesis into a structured response.
"""

import json
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from app.core.config import settings
from app.core.logging import logger
from app.integrations.monday.client import MondayClient
from app.integrations.monday.mapper import map_deals_items, map_work_orders_items
from app.data.normalizer import normalize_deals_dataset, normalize_work_orders_dataset
from app.data.quality import analyze_data_quality, DataQualityReport
from app.analytics.pipeline import compute_pipeline_metrics
from app.analytics.sector import compute_sector_metrics
from app.analytics.operations import compute_work_order_metrics
from app.analytics.cross_board import compute_cross_board_analysis
from app.analytics.leadership import compile_leadership_metrics, generate_structured_leadership_update
from app.agent.query_planner import QueryPlanner
from app.agent.context_manager import context_manager, SessionContext
from app.agent.prompts import INSIGHT_GENERATOR_SYSTEM_PROMPT, LEADERSHIP_UPDATE_SYSTEM_PROMPT
from app.schemas.query_plan import QueryPlan, QueryIntent


class AgentResponse(BaseModel):
    """Unified response object returned to the frontend."""
    session_id: str
    query_plan: QueryPlan
    metrics: Dict[str, Any] = Field(default_factory=dict)
    insights: str
    data_quality_report: DataQualityReport
    chart_data: List[Dict[str, Any]] = Field(default_factory=list)
    clarification_required: bool = False
    clarification_question: Optional[str] = None


def generate_fallback_insights(query_plan: QueryPlan, metrics: Dict[str, Any]) -> str:
    """Deterministic template fallback for insight narrative synthesis."""
    intent = query_plan.intent

    if intent == QueryIntent.LEADERSHIP_UPDATE:
        return generate_structured_leadership_update(metrics)

    if intent == QueryIntent.SECTOR_ANALYSIS:
        sector_name = query_plan.sector or "Selected Sectors"
        pipeline = metrics.get("pipeline", {})
        sec = metrics.get("sector", {})
        sec_val = sec.get("pipeline_by_sector", {}).get(sector_name, pipeline.get("total_pipeline_value", 0))
        sec_cnt = sec.get("deal_count_by_sector", {}).get(sector_name, pipeline.get("deal_count", 0))
        return (
            f"**Executive Takeaway**: The **{sector_name}** sector accounts for **${sec_val:,.2f}** in pipeline value across {sec_cnt} deal(s).\n\n"
            f"**Sector Highlights**:\n"
            f"- Total Sector Pipeline: **${sec_val:,.2f}**\n"
            f"- Sector Deal Count: **{sec_cnt}**\n"
            f"- Sector Average Deal Value: **${sec.get('average_deal_value_by_sector', {}).get(sector_name, 0):,.2f}**\n\n"
            f"**Strategic Opportunities**:\n"
            f"- Prioritize key accounts in {sector_name} to accelerate deal closure speed."
        )

    if intent == QueryIntent.WORK_ORDER_ANALYSIS:
        ops = metrics.get("operations", {})
        return (
            f"**Executive Takeaway**: Operational team is managing **{ops.get('total_work_orders', 0)}** total work orders, "
            f"with **{ops.get('active_work_orders', 0)}** active and **{ops.get('delayed_work_orders', 0)}** flagged as delayed.\n\n"
            f"**Operational Breakdown**:\n"
            f"- Completed Projects: **{ops.get('completed_work_orders', 0)}**\n"
            f"- Delayed Projects: **{ops.get('delayed_work_orders', 0)}** (Delay rate: {ops.get('operational_delay_rate_pct', 0)}%)\n"
            f"- Total Execution Budget: **${ops.get('total_execution_value', 0):,.2f}**"
        )

    # General pipeline fallback
    pipeline = metrics.get("pipeline", {})
    return (
        f"**Executive Takeaway**: Total sales pipeline is **${pipeline.get('total_pipeline_value', 0):,.2f}** across {pipeline.get('deal_count', 0)} total deals.\n\n"
        f"**Key Metrics**:\n"
        f"- Average Deal Size: **${pipeline.get('average_deal_value', 0):,.2f}**\n"
        f"- Late-Stage Pipeline: **${pipeline.get('late_stage_pipeline_value', 0):,.2f}**\n"
        f"- Weighted Pipeline Projection: **${pipeline.get('weighted_pipeline_value', 0):,.2f}**"
    )


class AgentOrchestrator:
    """Main BI Agent Orchestrator pipeline."""

    def __init__(self):
        self.monday_client = MondayClient()
        self.query_planner = QueryPlanner()

    async def process_query(self, user_query: str, session_id: Optional[str] = None) -> AgentResponse:
        """Execute end-to-end conversational BI workflow."""
        session = context_manager.get_or_create_session(session_id)
        session.add_user_message(user_query)

        # 1. Gemini Query Planning
        query_plan = self.query_planner.plan_query(user_query)
        logger.info(f"Query Plan intent: '{query_plan.intent}' for session {session.session_id}")

        # Check for ambiguity clarification early exit
        if query_plan.clarification_required and query_plan.clarification_question:
            resp = AgentResponse(
                session_id=session.session_id,
                query_plan=query_plan,
                insights=f"Clarification needed: {query_plan.clarification_question}",
                data_quality_report=DataQualityReport(),
                clarification_required=True,
                clarification_question=query_plan.clarification_question,
            )
            session.add_assistant_message(resp.insights, query_plan=query_plan.model_dump())
            return resp

        # 2. Dynamic monday.com Board Fetching
        deals_raw = await self.monday_client.fetch_board_items(
            settings.DEALS_BOARD_ID or "deals_board", "Deals"
        )
        work_orders_raw = await self.monday_client.fetch_board_items(
            settings.WORK_ORDERS_BOARD_ID or "work_orders_board", "Work Orders"
        )

        # 3. Data Mapping & Normalization
        deals_mapped = map_deals_items(deals_raw.raw_items)
        wo_mapped = map_work_orders_items(work_orders_raw.raw_items)

        deals_norm, deals_actions, deals_excl = normalize_deals_dataset(deals_mapped)
        wo_norm, wo_actions, wo_excl = normalize_work_orders_dataset(wo_mapped)

        # 4. Data Quality Diagnostics
        quality_report = analyze_data_quality(
            deals_norm, wo_norm, deals_actions, wo_actions, deals_excl, wo_excl
        )

        # Apply sector filter if specified in query plan
        if query_plan.sector:
            target_sec = query_plan.sector.lower()
            deals_norm = [d for d in deals_norm if d.get("sector", "").lower() == target_sec]
            wo_norm = [w for w in wo_norm if w.get("sector", "").lower() == target_sec]

        # 5. Deterministic BI Analytics
        pipeline_res = compute_pipeline_metrics(deals_norm)
        sector_res = compute_sector_metrics(deals_norm)
        operations_res = compute_work_order_metrics(wo_norm)
        cross_board_res = compute_cross_board_analysis(deals_norm, wo_norm)

        metrics_payload = {
            "pipeline": pipeline_res,
            "sector": sector_res,
            "operations": operations_res,
            "cross_board": cross_board_res,
            "data_quality": quality_report.model_dump(),
        }

        # Build Chart Data
        chart_data = []
        if query_plan.intent == QueryIntent.SECTOR_ANALYSIS or not query_plan.sector:
            for sec, val in sector_res.get("pipeline_by_sector", {}).items():
                chart_data.append({"name": sec, "value": val, "count": sector_res.get("deal_count_by_sector", {}).get(sec, 0)})
        else:
            for stage, val in pipeline_res.get("stage_distribution", {}).items():
                chart_data.append({"name": stage, "value": val})

        # 6. Gemini Insight Generation
        insights_narrative = self._generate_insights(query_plan, metrics_payload, user_query)

        response = AgentResponse(
            session_id=session.session_id,
            query_plan=query_plan,
            metrics=metrics_payload,
            insights=insights_narrative,
            data_quality_report=quality_report,
            chart_data=chart_data,
        )

        session.add_assistant_message(
            text=insights_narrative,
            query_plan=query_plan.model_dump(),
            metrics=metrics_payload
        )

        return response

    def _generate_insights(
        self, query_plan: QueryPlan, metrics: Dict[str, Any], user_query: str
    ) -> str:
        """Call Gemini to generate narrative insights from deterministic metrics."""
        if not settings.is_gemini_configured:
            return generate_fallback_insights(query_plan, metrics)

        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)

            system_prompt = (
                LEADERSHIP_UPDATE_SYSTEM_PROMPT
                if query_plan.intent == QueryIntent.LEADERSHIP_UPDATE
                else INSIGHT_GENERATOR_SYSTEM_PROMPT
            )

            prompt = (
                f"{system_prompt}\n\n"
                f"User Question: {user_query}\n"
                f"Query Plan: {query_plan.model_dump_json()}\n"
                f"Deterministic BI Metrics: {json.dumps(metrics, indent=2)}\n\n"
                f"Provide clear, professional markdown response."
            )

            res = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )

            if res.text:
                return res.text.strip()

        except Exception as exc:
            logger.warning(f"Gemini insight generation error: {exc}. Using fallback template.")

        return generate_fallback_insights(query_plan, metrics)
