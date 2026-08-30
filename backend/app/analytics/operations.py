"""Deterministic Work Orders Operations Analytics using Pandas."""

import pandas as pd
from typing import Dict, Any, List


def compute_work_order_metrics(wo_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute operational metrics from normalized Work Orders records."""
    if not wo_records:
        return {
            "total_work_orders": 0,
            "active_work_orders": 0,
            "completed_work_orders": 0,
            "delayed_work_orders": 0,
            "status_distribution": {},
            "total_execution_value": 0.0,
            "delayed_work_orders_list": [],
            "operational_delay_rate_pct": 0.0,
        }

    df = pd.DataFrame(wo_records)

    total_wo = len(df)
    valid_vals = df["execution_value"].dropna() if "execution_value" in df.columns else []
    total_exec_val = float(valid_vals.sum()) if len(valid_vals) > 0 else 0.0

    status_dist: Dict[str, int] = {}
    if "status" in df.columns:
        counts = df["status"].value_counts().to_dict()
        status_dist = {str(k): int(v) for k, v in counts.items()}

    active_count = status_dist.get("In Progress", 0) + status_dist.get("Not Started", 0) + status_dist.get("Delayed", 0)
    completed_count = status_dist.get("Completed", 0)
    delayed_count = status_dist.get("Delayed", 0)

    delay_rate = round((delayed_count / total_wo * 100.0), 2) if total_wo > 0 else 0.0

    # Extract detailed list of delayed work orders
    delayed_list = []
    if "status" in df.columns:
        delayed_df = df[df["status"] == "Delayed"]
        for _, row in delayed_df.iterrows():
            delayed_list.append({
                "work_order_id": str(row.get("work_order_id")),
                "project_name": str(row.get("project_name")),
                "client_name": str(row.get("client_name")),
                "sector": str(row.get("sector")),
                "delay_reason": str(row.get("delay_reason")),
                "execution_value": row.get("execution_value"),
                "target_completion_date": str(row.get("target_completion_date")),
            })

    return {
        "total_work_orders": total_wo,
        "active_work_orders": active_count,
        "completed_work_orders": completed_count,
        "delayed_work_orders": delayed_count,
        "status_distribution": status_dist,
        "total_execution_value": round(total_exec_val, 2),
        "delayed_work_orders_list": delayed_list,
        "operational_delay_rate_pct": delay_rate,
    }
