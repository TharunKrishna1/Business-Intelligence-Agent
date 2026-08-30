"""Unit tests for Leadership Update generation feature."""

import pytest
from app.analytics.leadership import compile_leadership_metrics, generate_structured_leadership_update
from app.data.quality import DataQualityReport


def test_generate_structured_leadership_update():
    deals = [
        {"deal_id": "d1", "deal_name": "Solar Survey", "sector": "Energy", "deal_value": 450000.0, "stage": "Proposal Sent"},
        {"deal_id": "d2", "deal_name": "Wind Survey", "sector": "Energy", "deal_value": 350000.0, "stage": "Closed Won"},
    ]
    work_orders = [
        {"work_order_id": "w1", "project_name": "WO Solar", "client_name": "Adani", "sector": "Energy", "status": "In Progress", "execution_value": 450000.0, "delay_reason": ""},
        {"work_order_id": "w2", "project_name": "WO Wind", "client_name": "Tata", "sector": "Energy", "status": "Delayed", "execution_value": 350000.0, "delay_reason": "Airspace clearance"},
    ]
    qr = DataQualityReport(total_records=4, valid_records=4, important_caveats=["1 work order delayed"])

    payload = compile_leadership_metrics(deals, work_orders, qr)
    report_text = generate_structured_leadership_update(payload)

    assert "# Skylark Drones – Executive Leadership Update" in report_text
    assert "## 1. Executive Summary" in report_text
    assert "## 2. Sales Highlights" in report_text
    assert "## 3. Operational Highlights" in report_text
    assert "## 4. Key Risks" in report_text
    assert "## 5. Opportunities" in report_text
    assert "## 6. Data Quality Caveats" in report_text
    assert "## 7. Recommended Actions" in report_text
    assert "$800,000.00" in report_text
