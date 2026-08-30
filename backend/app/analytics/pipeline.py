"""Deterministic Pipeline BI Analytics using Pandas."""

import pandas as pd
from typing import Dict, Any, List, Optional


STAGE_WIN_PROBABILITIES = {
    "Lead": 0.10,
    "Qualification": 0.25,
    "Proposal Sent": 0.60,
    "Negotiation": 0.80,
    "Closed Won": 1.00,
    "Closed Lost": 0.00,
    "Unknown": 0.20,
}

LATE_STAGES = ["Proposal Sent", "Negotiation", "Closed Won"]
OPEN_STAGES = ["Lead", "Qualification", "Proposal Sent", "Negotiation"]


def compute_pipeline_metrics(deals_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute deterministic pipeline metrics from normalized Deals records."""
    if not deals_records:
        return {
            "total_pipeline_value": 0.0,
            "open_pipeline_value": 0.0,
            "deal_count": 0,
            "valid_deal_count": 0,
            "average_deal_value": 0.0,
            "stage_distribution": {},
            "stage_count_distribution": {},
            "late_stage_pipeline_value": 0.0,
            "weighted_pipeline_value": 0.0,
        }

    df = pd.DataFrame(deals_records)

    deal_count = len(df)
    valid_values = df["deal_value"].dropna()
    valid_deal_count = len(valid_values)

    total_pipeline_value = float(valid_values.sum()) if valid_deal_count > 0 else 0.0
    average_deal_value = float(valid_values.mean()) if valid_deal_count > 0 else 0.0

    # Open Pipeline (excludes Closed Won & Closed Lost)
    open_df = df[df["stage"].isin(OPEN_STAGES)]
    open_pipeline_value = float(open_df["deal_value"].dropna().sum()) if not open_df.empty else 0.0

    # Stage distribution (values and counts)
    stage_dist = {}
    stage_count_dist = {}
    if "stage" in df.columns:
        grouped = df.groupby("stage")
        for stage_name, group in grouped:
            sum_val = float(group["deal_value"].dropna().sum())
            cnt = len(group)
            stage_dist[str(stage_name)] = sum_val
            stage_count_dist[str(stage_name)] = cnt

    # Late stage pipeline
    late_df = df[df["stage"].isin(LATE_STAGES)]
    late_stage_pipeline_value = float(late_df["deal_value"].dropna().sum()) if not late_df.empty else 0.0

    # Weighted pipeline
    weighted_pipeline_value = 0.0
    for _, row in df.iterrows():
        val = row.get("deal_value")
        if pd.notna(val) and val is not None:
            prob = STAGE_WIN_PROBABILITIES.get(str(row.get("stage")), 0.20)
            weighted_pipeline_value += float(val) * prob

    return {
        "total_pipeline_value": round(total_pipeline_value, 2),
        "open_pipeline_value": round(open_pipeline_value, 2),
        "deal_count": deal_count,
        "valid_deal_count": valid_deal_count,
        "average_deal_value": round(average_deal_value, 2),
        "stage_distribution": stage_dist,
        "stage_count_distribution": stage_count_dist,
        "late_stage_pipeline_value": round(late_stage_pipeline_value, 2),
        "weighted_pipeline_value": round(weighted_pipeline_value, 2),
    }
