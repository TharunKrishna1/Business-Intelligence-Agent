"""Unit tests for data normalization and quality layer."""

import pytest
from app.data.normalizer import (
    parse_currency_value,
    parse_date_string,
    normalize_sector_name,
    normalize_deals_dataset,
    normalize_work_orders_dataset
)
from app.data.quality import analyze_data_quality
from app.data.validators import is_valid_number, is_valid_date_iso


def test_parse_currency_value():
    val, action = parse_currency_value("$450,000")
    assert val == 450000.0
    assert "Parsed '$450,000'" in action

    val, action = parse_currency_value("350000.50")
    assert val == 350000.50

    val, action = parse_currency_value("N/A")
    assert val is None
    assert "Invalid/N/A" in action

    val, action = parse_currency_value(None)
    assert val is None


def test_parse_date_string():
    date_iso, action = parse_date_string("2026-09-15")
    assert date_iso == "2026-09-15"

    date_iso, action = parse_date_string("15/09/2026")
    assert date_iso == "2026-09-15"
    assert "Parsed date" in action

    date_iso, action = parse_date_string("Invalid Date")
    assert date_iso is None


def test_normalize_sector_name():
    sec, action = normalize_sector_name("Energy & Utilities")
    assert sec == "Energy"

    sec, action = normalize_sector_name("solar")
    assert sec == "Energy"

    sec, action = normalize_sector_name("MINING & MINERALS")
    assert sec == "Mining"

    sec, action = normalize_sector_name("")
    assert sec == "Unknown"


def test_normalize_deals_dataset():
    raw_deals = [
        {"deal_id": "1", "deal_name": "Test Deal 1", "sector": "energy", "deal_value": "$100,000", "stage": "closed won", "expected_close_date": "2026-08-01", "owner": "Alice"},
        {"deal_id": "2", "deal_name": "Test Deal 2", "sector": "Mining & Minerals", "deal_value": "N/A", "stage": "proposal sent", "expected_close_date": "Invalid", "owner": "Bob"},
    ]
    norm, actions, excl = normalize_deals_dataset(raw_deals)
    assert len(norm) == 2
    assert norm[0]["sector"] == "Energy"
    assert norm[0]["deal_value"] == 100000.0
    assert norm[0]["stage"] == "Closed Won"
    assert norm[1]["deal_value"] is None
    assert norm[1]["has_missing_value"] is True
    assert len(actions) > 0


def test_analyze_data_quality():
    deals_norm = [
        {"deal_id": "1", "has_missing_value": False, "has_missing_date": False},
        {"deal_id": "2", "has_missing_value": True, "has_missing_date": True},
    ]
    wo_norm = [
        {"work_order_id": "w1", "has_missing_value": False, "has_missing_dates": False, "status": "In Progress"},
        {"work_order_id": "w2", "has_missing_value": False, "has_missing_dates": True, "status": "Delayed"},
    ]
    report = analyze_data_quality(deals_norm, wo_norm, ["action1"], ["action2"], [], [])
    assert report.total_records == 4
    assert report.missing_monetary_values == 1
    assert report.invalid_dates == 2
    assert len(report.important_caveats) >= 2
