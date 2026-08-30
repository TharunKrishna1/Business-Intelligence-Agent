"""Unit tests for Agent Orchestrator and API routes."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.agent.orchestrator import AgentOrchestrator, generate_fallback_insights
from app.schemas.query_plan import QueryPlan, QueryIntent


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data


@pytest.mark.asyncio
async def test_orchestrator_pipeline_query():
    orchestrator = AgentOrchestrator()
    res = await orchestrator.process_query("How is our overall pipeline looking?")
    assert res.query_plan.intent == QueryIntent.PIPELINE_ANALYSIS
    assert "pipeline" in res.metrics
    assert res.metrics["pipeline"]["total_pipeline_value"] > 0
    assert len(res.insights) > 0
    assert res.data_quality_report.total_records > 0


@pytest.mark.asyncio
async def test_orchestrator_sector_query():
    orchestrator = AgentOrchestrator()
    res = await orchestrator.process_query("How is the energy sector performing this quarter?")
    assert res.query_plan.intent == QueryIntent.SECTOR_ANALYSIS
    assert res.query_plan.sector == "Energy"
    assert len(res.chart_data) > 0


def test_api_chat_endpoint():
    response = client.post("/api/chat", json={"message": "Which projects are delayed?"})
    assert response.status_code == 200
    data = response.json()
    assert "query_plan" in data
    assert "metrics" in data
    assert "insights" in data


def test_api_leadership_update_endpoint():
    response = client.post("/api/leadership-update", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["query_plan"]["intent"] == "leadership_update"


def test_api_data_quality_endpoint():
    response = client.get("/api/data-quality")
    assert response.status_code == 200
    data = response.json()
    assert "total_records" in data
    assert "important_caveats" in data
