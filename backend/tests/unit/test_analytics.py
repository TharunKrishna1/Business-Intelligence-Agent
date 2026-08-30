"""Unit tests for deterministic BI analytics engines."""

import pytest
from app.analytics.pipeline import compute_pipeline_metrics
from app.analytics.sector import compute_sector_metrics
from app.analytics.operations import compute_work_order_metrics
from app.analytics.cross_board import compute_cross_board_analysis
from app.analytics.leadership import compile_leadership_metrics
from app.data.quality import DataQualityReport


@pytest.fixture
def sample_deals():
    return [
        {"deal_id": "d1", "deal_name": "Deal A", "sector": "Energy", "deal_value": 450000.0, "stage": "Proposal Sent", "owner": "Alice"},
        {"deal_id": "d2", "deal_name": "Deal B", "sector": "Energy", "deal_value": 350000.0, "stage": "Negotiation", "owner": "Bob"},
        {"deal_id": "d3", "deal_name": "Deal C", "sector": "Mining", "deal_value": 600000.0, "stage": "Closed Won", "owner": "Charlie"},
        {"deal_id": "d4", "deal_name": "Deal D", "sector": "Defense", "deal_value": None, "stage": "Lead", "owner": "Alice"},
    ]


@pytest.fixture
def sample_work_orders():
    return [
        {"work_order_id": "w1", "project_name": "WO 1", "client_name": "NTPC", "sector": "Energy", "status": "In Progress", "execution_value": 200000.0, "delay_reason": ""},
        {"work_order_id": "w2", "project_name": "WO 2", "client_name": "Coal India", "sector": "Mining", "status": "Completed", "execution_value": 600000.0, "delay_reason": ""},
        {"work_order_id": "w3", "project_name": "WO 3", "client_name": "Tata Power", "sector": "Energy", "status": "Delayed", "execution_value": 350000.0, "delay_reason": "Weather delay"},
    ]


def test_compute_pipeline_metrics(sample_deals):
    res = compute_pipeline_metrics(sample_deals)
    assert res["total_pipeline_value"] == 1400000.0
    assert res["deal_count"] == 4
    assert res["valid_deal_count"] == 3
    assert res["average_deal_value"] == 466666.67
    assert res["stage_count_distribution"]["Proposal Sent"] == 1
    assert res["late_stage_pipeline_value"] == 1400000.0


def test_compute_sector_metrics(sample_deals):
    res = compute_sector_metrics(sample_deals)
    assert res["pipeline_by_sector"]["Energy"] == 800000.0
    assert res["pipeline_by_sector"]["Mining"] == 600000.0
    assert res["deal_count_by_sector"]["Energy"] == 2
    assert res["top_performing_sector"] == "Energy"


def test_compute_work_order_metrics(sample_work_orders):
    res = compute_work_order_metrics(sample_work_orders)
    assert res["total_work_orders"] == 3
    assert res["active_work_orders"] == 2
    assert res["delayed_work_orders"] == 1
    assert res["completed_work_orders"] == 1
    assert len(res["delayed_work_orders_list"]) == 1
    assert res["delayed_work_orders_list"][0]["delay_reason"] == "Weather delay"


def test_compute_cross_board_analysis(sample_deals, sample_work_orders):
    res = compute_cross_board_analysis(sample_deals, sample_work_orders)
    assert len(res["sector_cross_board_summary"]) == 3
    assert len(res["high_risk_sectors"]) == 1
    assert res["high_risk_sectors"][0]["sector"] == "Energy"


def test_compile_leadership_metrics(sample_deals, sample_work_orders):
    qr = DataQualityReport(total_records=7, valid_records=7)
    res = compile_leadership_metrics(sample_deals, sample_work_orders, qr)
    assert "pipeline" in res
    assert "sector" in res
    assert "operations" in res
    assert "cross_board" in res
    assert "data_quality" in res
