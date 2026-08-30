"""Unit tests for QueryPlanner and QueryPlan schema."""

import pytest
from app.schemas.query_plan import QueryPlan, QueryIntent
from app.agent.query_planner import QueryPlanner, rule_based_fallback_query_plan


def test_rule_based_fallback_pipeline():
    plan = rule_based_fallback_query_plan("How is our overall pipeline looking?")
    assert plan.intent == QueryIntent.PIPELINE_ANALYSIS
    assert "deals" in plan.boards_required


def test_rule_based_fallback_sector():
    plan = rule_based_fallback_query_plan("How is the energy sector performing this quarter?")
    assert plan.intent == QueryIntent.SECTOR_ANALYSIS
    assert plan.sector == "Energy"
    assert "deals" in plan.boards_required


def test_rule_based_fallback_work_orders():
    plan = rule_based_fallback_query_plan("Which projects are delayed?")
    assert plan.intent == QueryIntent.WORK_ORDER_ANALYSIS
    assert "work_orders" in plan.boards_required


def test_rule_based_fallback_leadership():
    plan = rule_based_fallback_query_plan("Prepare a leadership update")
    assert plan.intent == QueryIntent.LEADERSHIP_UPDATE
    assert "deals" in plan.boards_required
    assert "work_orders" in plan.boards_required


def test_json_parse_and_validate():
    planner = QueryPlanner()
    raw_json = """
    ```json
    {
      "intent": "sector_analysis",
      "boards_required": ["deals", "work_orders"],
      "filters": {"sector": "Energy"},
      "metrics": ["total_pipeline_value"],
      "comparison_required": false,
      "clarification_required": false
    }
    ```
    """
    plan = planner._parse_and_validate_json(raw_json)
    assert plan is not None
    assert plan.intent == QueryIntent.SECTOR_ANALYSIS
    assert plan.sector == "Energy"
