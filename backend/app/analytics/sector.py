"""Deterministic Sector BI Analytics using Pandas."""

import pandas as pd
from typing import Dict, Any, List


def compute_sector_metrics(deals_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute sector-level BI metrics from normalized Deals records."""
    if not deals_records:
        return {
            "pipeline_by_sector": {},
            "deal_count_by_sector": {},
            "average_deal_value_by_sector": {},
            "relative_sector_performance": [],
            "top_performing_sector": None,
        }

    df = pd.DataFrame(deals_records)

    pipeline_by_sector: Dict[str, float] = {}
    deal_count_by_sector: Dict[str, int] = {}
    avg_by_sector: Dict[str, float] = {}
    relative_perf: List[Dict[str, Any]] = []

    total_pipeline = float(df["deal_value"].dropna().sum()) if not df.empty else 0.0

    if "sector" in df.columns:
        grouped = df.groupby("sector")
        for sector_name, group in grouped:
            sec_str = str(sector_name)
            valid_vals = group["deal_value"].dropna()
            sec_val = float(valid_vals.sum()) if len(valid_vals) > 0 else 0.0
            sec_count = len(group)
            sec_avg = float(valid_vals.mean()) if len(valid_vals) > 0 else 0.0
            share_pct = round((sec_val / total_pipeline * 100.0), 2) if total_pipeline > 0 else 0.0

            pipeline_by_sector[sec_str] = round(sec_val, 2)
            deal_count_by_sector[sec_str] = sec_count
            avg_by_sector[sec_str] = round(sec_avg, 2)

            relative_perf.append({
                "sector": sec_str,
                "pipeline_value": round(sec_val, 2),
                "deal_count": sec_count,
                "average_deal_value": round(sec_avg, 2),
                "market_share_percentage": share_pct,
            })

    # Sort relative performance descending by pipeline value
    relative_perf.sort(key=lambda x: x["pipeline_value"], reverse=True)
    top_sector = relative_perf[0]["sector"] if relative_perf else None

    return {
        "pipeline_by_sector": pipeline_by_sector,
        "deal_count_by_sector": deal_count_by_sector,
        "average_deal_value_by_sector": avg_by_sector,
        "relative_sector_performance": relative_perf,
        "top_performing_sector": top_sector,
    }
