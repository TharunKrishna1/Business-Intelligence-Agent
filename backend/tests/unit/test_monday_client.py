"""Unit tests for monday.com client and mapper."""

import pytest
from app.integrations.monday.client import MondayClient, generate_mock_deals_items, generate_mock_work_orders_items
from app.integrations.monday.mapper import map_deals_items, map_work_orders_items, map_column_title_to_key


def test_map_column_title_to_key():
    assert map_column_title_to_key("Deal Value") == "deal_value"
    assert map_column_title_to_key("Expected Close Date") == "expected_close_date"
    assert map_column_title_to_key("Sector & Industry") == "sector_and_industry"


def test_map_mock_deals_items():
    mock_items = generate_mock_deals_items()
    assert len(mock_items) == 10
    mapped = map_deals_items(mock_items)
    assert len(mapped) == 10
    first = mapped[0]
    assert first["deal_name"] == "Adani Solar Power Survey"
    assert first["sector"] == "Energy"
    assert first["deal_value"] == "$450,000"
    assert first["stage"] == "Proposal Sent"


def test_map_mock_work_orders_items():
    mock_items = generate_mock_work_orders_items()
    assert len(mock_items) == 6
    mapped = map_work_orders_items(mock_items)
    assert len(mapped) == 6
    third = mapped[2]
    assert third["project_name"] == "WO-2026-003: L&T Smart City Drone Survey"
    assert third["client_name"] == "L&T Construction"
    assert third["status"] == "Delayed"
    assert "Regulatory airspace clearance" in third["delay_reason"]


@pytest.mark.asyncio
async def test_monday_client_mock_fallback():
    client = MondayClient()
    result = await client.fetch_board_items("123", "Deals")
    assert result.is_mock is True
    assert len(result.raw_items) > 0
