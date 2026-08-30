"""Gemini-powered Structured Query Planner."""

import json
import re
from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import QueryPlannerError
from app.schemas.query_plan import QueryPlan, QueryIntent, QueryPlanFilter


QUERY_PLANNER_SYSTEM_PROMPT = """
You are the Lead Structured Query Planner for Skylark Drones Business Intelligence Agent.
Your job is to analyze founder-level business questions and convert them into a strict, validated JSON Query Plan.

Target Boards available:
1. "deals": Contains sales pipeline, deal values, stages, sectors, close dates, owners.
2. "work_orders": Contains active/completed/delayed operations projects, execution values, clients, sectors, delay reasons.

Intents available:
- "pipeline_analysis": Questions about deal pipeline totals, stage distributions, win rates, averages.
- "sector_analysis": Questions focused on industry sectors (Energy, Infrastructure, Mining, Defense, Agriculture).
- "work_order_analysis": Questions about active, completed, or delayed operational work orders/projects.
- "cross_board_analysis": Questions correlating sales deals with operational execution risks or capacity.
- "leadership_update": Requests for executive updates, summaries, weekly reports, leadership overviews.
- "general_query": Other general business inquiries.

Rules:
1. Respond ONLY with a valid JSON object matching the required schema. Do not include markdown codeblocks or prose outside JSON.
2. Extract filters like sector ("Energy", "Infrastructure", "Mining", "Defense", "Agriculture") and date_range if mentioned.
3. If the user question is completely ambiguous or missing key details, set "clarification_required": true and provide a clear "clarification_question".

JSON Output Schema:
{
  "intent": "pipeline_analysis" | "sector_analysis" | "work_order_analysis" | "cross_board_analysis" | "leadership_update" | "general_query",
  "boards_required": ["deals"] | ["work_orders"] | ["deals", "work_orders"],
  "filters": {
    "sector": string | null,
    "date_range": string | null,
    "stage": string | null,
    "status": string | null
  },
  "sector": string | null,
  "date_range": string | null,
  "metrics": [string],
  "comparison_required": boolean,
  "clarification_required": boolean,
  "clarification_question": string | null
}
"""


def rule_based_fallback_query_plan(user_query: str) -> QueryPlan:
    """Deterministic rule-based query plan fallback when LLM is offline or unconfigured."""
    q_lower = user_query.lower()

    if "leadership" in q_lower or "update" in q_lower or "executive summary" in q_lower:
        return QueryPlan(
            intent=QueryIntent.LEADERSHIP_UPDATE,
            boards_required=["deals", "work_orders"],
            metrics=["total_pipeline_value", "deal_count", "active_work_orders", "delayed_work_orders", "sector_breakdown"],
        )

    # Sector detection
    detected_sector = None
    for sec in ["energy", "infrastructure", "mining", "defense", "agriculture"]:
        if sec in q_lower:
            detected_sector = sec.capitalize()
            break

    if "delayed" in q_lower or "work order" in q_lower or "operation" in q_lower or "project" in q_lower:
        if "risk" in q_lower or "pipeline" in q_lower or detected_sector:
            return QueryPlan(
                intent=QueryIntent.CROSS_BOARD_ANALYSIS if ("pipeline" in q_lower or "risk" in q_lower) else QueryIntent.WORK_ORDER_ANALYSIS,
                boards_required=["deals", "work_orders"] if ("pipeline" in q_lower or "risk" in q_lower) else ["work_orders"],
                sector=detected_sector,
                filters=QueryPlanFilter(sector=detected_sector),
                metrics=["active_work_orders", "delayed_work_orders", "execution_value", "delay_reasons"],
            )
        return QueryPlan(
            intent=QueryIntent.WORK_ORDER_ANALYSIS,
            boards_required=["work_orders"],
            sector=detected_sector,
            filters=QueryPlanFilter(sector=detected_sector),
            metrics=["active_work_orders", "delayed_work_orders", "status_distribution"],
        )

    if detected_sector or "sector" in q_lower:
        return QueryPlan(
            intent=QueryIntent.SECTOR_ANALYSIS,
            boards_required=["deals", "work_orders"],
            sector=detected_sector,
            filters=QueryPlanFilter(sector=detected_sector),
            metrics=["pipeline_value_by_sector", "deal_count_by_sector", "average_deal_value"],
        )

    # Default Pipeline Analysis
    return QueryPlan(
        intent=QueryIntent.PIPELINE_ANALYSIS,
        boards_required=["deals"],
        metrics=["total_pipeline_value", "deal_count", "average_deal_value", "stage_distribution"],
    )


class QueryPlanner:
    """Query Planner using Gemini API with Pydantic validation and retry."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY

    def plan_query(self, user_query: str) -> QueryPlan:
        """Parse user query into a validated QueryPlan."""
        if not settings.is_gemini_configured:
            logger.info("Gemini API key not configured. Using rule-based query planner fallback.")
            return rule_based_fallback_query_plan(user_query)

        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)

            prompt = f"{QUERY_PLANNER_SYSTEM_PROMPT}\n\nUser Question: {user_query}"
            
            # Initial generation attempt
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )

            text_output = response.text or ""
            parsed_plan = self._parse_and_validate_json(text_output)
            
            if parsed_plan:
                return parsed_plan

            # Retry once with corrective instruction if invalid
            logger.warning("Initial Gemini QueryPlan response invalid. Retrying once with corrective prompt.")
            retry_prompt = f"{prompt}\n\nERROR: Your previous output was invalid. Please return ONLY a valid raw JSON object strictly conforming to the QueryPlan schema without markdown codeblocks."
            
            retry_response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=retry_prompt,
            )
            
            parsed_plan = self._parse_and_validate_json(retry_response.text or "")
            if parsed_plan:
                return parsed_plan

        except Exception as exc:
            logger.warning(f"Error calling Gemini Query Planner: {exc}. Falling back to rule-based planner.")

        return rule_based_fallback_query_plan(user_query)

    def _parse_and_validate_json(self, raw_text: str) -> Optional[QueryPlan]:
        """Extract JSON substring, parse, and validate via Pydantic."""
        try:
            # Strip markdown fenced codeblocks if present
            cleaned = raw_text.strip()
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                cleaned = match.group(0)

            data = json.loads(cleaned)

            # Standardize sector filter into root sector if needed
            if "filters" in data and isinstance(data["filters"], dict):
                filters = data["filters"]
                if not data.get("sector") and filters.get("sector"):
                    data["sector"] = filters["sector"]
                if not data.get("date_range") and filters.get("date_range"):
                    data["date_range"] = filters["date_range"]

            plan = QueryPlan(**data)
            return plan
        except Exception as exc:
            logger.debug(f"JSON validation failed: {exc}")
            return None
