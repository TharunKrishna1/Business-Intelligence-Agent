"""Monday.com raw data mapper.

Converts raw GraphQL column structures into dictionary records with normalized field keys.
"""

from typing import List, Dict, Any
from app.integrations.monday.models import MondayItem, MondayFetchResult
from app.core.logging import logger


def map_column_title_to_key(title: str) -> str:
    """Normalize a column title string into a pythonic dictionary key."""
    if not title:
        return ""
    clean = title.strip().lower()
    clean = clean.replace(" ", "_").replace("-", "_").replace("&", "and")
    return clean


def map_monday_item_to_dict(item: MondayItem) -> Dict[str, Any]:
    """Convert a single MondayItem into a flat dictionary using column titles and IDs."""
    record: Dict[str, Any] = {
        "id": item.id,
        "name": item.name,
    }

    for col in item.column_values:
        key = map_column_title_to_key(col.title or col.id)
        if key:
            record[key] = col.text if col.text is not None else col.value
            # preserve raw ID for fallback lookup
            record[f"_col_{col.id}"] = col.text if col.text is not None else col.value

    return record


def map_deals_items(items: List[MondayItem]) -> List[Dict[str, Any]]:
    """Map Deals board items into structured records."""
    records = []
    for item in items:
        raw = map_monday_item_to_dict(item)

        # Standard field resolution logic using dynamic fallback titles
        sector = (
            raw.get("sector") or raw.get("industry") or raw.get("domain") or
            raw.get("category") or ""
        )
        deal_value = (
            raw.get("deal_value") or raw.get("value") or raw.get("amount") or
            raw.get("pipeline_value") or raw.get("contract_value") or ""
        )
        stage = (
            raw.get("stage") or raw.get("status") or raw.get("pipeline_stage") or
            raw.get("deal_stage") or ""
        )
        close_date = (
            raw.get("expected_close_date") or raw.get("close_date") or
            raw.get("target_date") or raw.get("date") or ""
        )
        owner = (
            raw.get("owner") or raw.get("sales_rep") or raw.get("deal_owner") or ""
        )

        records.append({
            "raw_id": item.id,
            "deal_id": item.id,
            "deal_name": item.name,
            "sector": str(sector),
            "deal_value": deal_value,
            "stage": str(stage),
            "expected_close_date": str(close_date),
            "owner": str(owner),
            "raw_record": raw
        })
    return records


def map_work_orders_items(items: List[MondayItem]) -> List[Dict[str, Any]]:
    """Map Work Orders board items into structured records."""
    records = []
    for item in items:
        raw = map_monday_item_to_dict(item)

        client_name = (
            raw.get("client_name") or raw.get("client") or raw.get("customer") or
            raw.get("account") or ""
        )
        sector = (
            raw.get("sector") or raw.get("industry") or raw.get("domain") or ""
        )
        status = (
            raw.get("status") or raw.get("operational_status") or
            raw.get("execution_status") or raw.get("state") or ""
        )
        start_date = (
            raw.get("start_date") or raw.get("commencement_date") or ""
        )
        target_completion_date = (
            raw.get("target_completion_date") or raw.get("end_date") or
            raw.get("due_date") or raw.get("completion_date") or ""
        )
        execution_value = (
            raw.get("execution_value") or raw.get("contract_value") or
            raw.get("value") or raw.get("budget") or ""
        )
        delay_reason = (
            raw.get("delay_reason") or raw.get("blocker") or
            raw.get("notes") or raw.get("risk_factor") or ""
        )

        records.append({
            "raw_id": item.id,
            "work_order_id": item.id,
            "project_name": item.name,
            "client_name": str(client_name),
            "sector": str(sector),
            "status": str(status),
            "start_date": str(start_date),
            "target_completion_date": str(target_completion_date),
            "execution_value": execution_value,
            "delay_reason": str(delay_reason),
            "raw_record": raw
        })
    return records
