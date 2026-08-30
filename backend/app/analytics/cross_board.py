"""Cross-board analytics correlating sales pipeline with operational execution risk."""

import pandas as pd
from typing import Dict, Any, List


def compute_cross_board_analysis(
    deals_records: List[Dict[str, Any]],
    wo_records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Correlate pipeline demand with operational execution risk across shared sectors."""
    if not deals_records and not wo_records:
        return {
            "sector_cross_board_summary": [],
            "high_risk_sectors": [],
            "strong_execution_sectors": [],
            "match_notes": "No data available on Deals or Work Orders boards."
        }

    deals_df = pd.DataFrame(deals_records) if deals_records else pd.DataFrame()
    wo_df = pd.DataFrame(wo_records) if wo_records else pd.DataFrame()

    sectors = set()
    if not deals_df.empty and "sector" in deals_df.columns:
        sectors.update(deals_df["sector"].unique())
    if not wo_df.empty and "sector" in wo_df.columns:
        sectors.update(wo_df["sector"].unique())

    sector_summary = []
    high_risk_sectors = []
    strong_execution_sectors = []

    for sector in sorted(sectors):
        sec_str = str(sector)

        # Deals metrics for sector
        sec_deals = deals_df[deals_df["sector"] == sector] if not deals_df.empty and "sector" in deals_df.columns else pd.DataFrame()
        pipeline_val = float(sec_deals["deal_value"].dropna().sum()) if not sec_deals.empty else 0.0
        deal_count = len(sec_deals)

        # Work Orders metrics for sector
        sec_wo = wo_df[wo_df["sector"] == sector] if not wo_df.empty and "sector" in wo_df.columns else pd.DataFrame()
        wo_count = len(sec_wo)
        delayed_wo = len(sec_wo[sec_wo["status"] == "Delayed"]) if not sec_wo.empty and "status" in sec_wo.columns else 0
        completed_wo = len(sec_wo[sec_wo["status"] == "Completed"]) if not sec_wo.empty and "status" in sec_wo.columns else 0

        # Assess execution risk level
        if delayed_wo > 0 and pipeline_val > 300000:
            risk_level = "HIGH"
            risk_desc = f"High pipeline (${pipeline_val:,.0f}) with {delayed_wo} delayed work order(s) risking client satisfaction and conversion."
            high_risk_sectors.append({
                "sector": sec_str,
                "pipeline_value": round(pipeline_val, 2),
                "delayed_work_orders": delayed_wo,
                "reason": risk_desc
            })
        elif delayed_wo > 0:
            risk_level = "MODERATE"
            risk_desc = f"{delayed_wo} work order(s) delayed in this sector."
        else:
            risk_level = "LOW"
            risk_desc = "Clean operational execution with no active delays."
            if wo_count > 0 and completed_wo > 0:
                strong_execution_sectors.append(sec_str)

        sector_summary.append({
            "sector": sec_str,
            "pipeline_value": round(pipeline_val, 2),
            "deal_count": deal_count,
            "total_work_orders": wo_count,
            "delayed_work_orders": delayed_wo,
            "completed_work_orders": completed_wo,
            "risk_level": risk_level,
            "risk_description": risk_desc
        })

    return {
        "sector_cross_board_summary": sector_summary,
        "high_risk_sectors": high_risk_sectors,
        "strong_execution_sectors": strong_execution_sectors,
        "match_notes": f"Matched across {len(sectors)} shared industry sectors. Cross-board matching is performed dynamically at the Sector aggregation level."
    }
