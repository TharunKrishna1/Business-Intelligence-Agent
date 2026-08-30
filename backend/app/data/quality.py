"""Data Quality Reporting module."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DataQualityReport(BaseModel):
    """Structured report detailing data quality metrics and normalization caveats."""
    total_records: int = 0
    valid_records: int = 0
    records_with_missing_values: int = 0
    invalid_dates: int = 0
    missing_monetary_values: int = 0
    normalization_actions: List[str] = Field(default_factory=list)
    records_excluded_from_calculations: List[str] = Field(default_factory=list)
    important_caveats: List[str] = Field(default_factory=list)


def analyze_data_quality(
    deals_norm: List[Dict[str, Any]],
    work_orders_norm: List[Dict[str, Any]],
    deals_actions: List[str],
    work_orders_actions: List[str],
    deals_excluded: List[Dict[str, Any]],
    work_orders_excluded: List[Dict[str, Any]],
) -> DataQualityReport:
    """Analyze normalized datasets and compile a unified DataQualityReport."""
    all_actions = deals_actions + work_orders_actions
    excluded_ids = [
        f"Deal {r.get('deal_id')}" for r in deals_excluded
    ] + [
        f"Work Order {r.get('work_order_id')}" for r in work_orders_excluded
    ]

    total_records = len(deals_norm) + len(work_orders_norm)
    missing_values = 0
    invalid_dates = 0
    missing_monetary = 0
    caveats = []

    # Deals diagnostics
    deals_missing_val_count = 0
    for d in deals_norm:
        if d.get("has_missing_value"):
            missing_values += 1
            missing_monetary += 1
            deals_missing_val_count += 1
        if d.get("has_missing_date"):
            invalid_dates += 1

    if deals_missing_val_count > 0:
        caveats.append(f"{deals_missing_val_count} deal(s) have missing monetary values and are excluded from deal value totals.")

    # Work Orders diagnostics
    wo_missing_dates_count = 0
    wo_delayed_count = 0
    for w in work_orders_norm:
        if w.get("has_missing_value"):
            missing_values += 1
            missing_monetary += 1
        if w.get("has_missing_dates"):
            invalid_dates += 1
            wo_missing_dates_count += 1
        if w.get("status") == "Delayed":
            wo_delayed_count += 1

    if wo_missing_dates_count > 0:
        caveats.append(f"{wo_missing_dates_count} work order(s) have missing or unparseable target dates.")

    if wo_delayed_count > 0:
        caveats.append(f"{wo_delayed_count} active work order(s) are currently flagged as 'Delayed' due to operational blockers.")

    valid_records = total_records - len(excluded_ids)

    if not caveats:
        caveats.append("Data quality is clean. All records normalized without critical exclusions.")

    return DataQualityReport(
        total_records=total_records,
        valid_records=valid_records,
        records_with_missing_values=missing_values,
        invalid_dates=invalid_dates,
        missing_monetary_values=missing_monetary,
        normalization_actions=all_actions,
        records_excluded_from_calculations=excluded_ids,
        important_caveats=caveats,
    )
