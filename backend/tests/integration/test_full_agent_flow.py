"""End-to-end integration tests for full Skylark BI Agent conversational flow."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_full_conversational_workflow():
    # 1. Health check
    health_resp = client.get("/health")
    assert health_resp.status_code == 200

    # 2. Pipeline query
    chat_resp1 = client.post("/api/chat", json={"message": "How is our overall pipeline looking?"})
    assert chat_resp1.status_code == 200
    body1 = chat_resp1.json()
    assert body1["query_plan"]["intent"] == "pipeline_analysis"
    assert "pipeline" in body1["metrics"]
    session_id = body1["session_id"]

    # 3. Sector query in same session
    chat_resp2 = client.post("/api/chat", json={"message": "How is the energy sector performing this quarter?", "session_id": session_id})
    assert chat_resp2.status_code == 200
    body2 = chat_resp2.json()
    assert body2["session_id"] == session_id
    assert body2["query_plan"]["intent"] == "sector_analysis"
    assert body2["query_plan"]["sector"] == "Energy"

    # 4. Leadership update in same session
    lead_resp = client.post("/api/leadership-update", json={"session_id": session_id})
    assert lead_resp.status_code == 200
    body3 = lead_resp.json()
    assert body3["query_plan"]["intent"] == "leadership_update"
    assert "Executive Leadership Update" in body3["insights"]
