"""Schema mapping utilities for monday.com boards."""

from typing import Dict, Any, List


DEALS_SCHEMA_STANDARD = {
    "deal_name": ["name", "title", "deal", "opportunity"],
    "sector": ["sector", "industry", "domain", "category"],
    "deal_value": ["deal_value", "value", "amount", "pipeline_value", "contract_value"],
    "stage": ["stage", "status", "pipeline_stage", "deal_stage"],
    "expected_close_date": ["expected_close_date", "close_date", "target_date", "date"],
    "owner": ["owner", "sales_rep", "deal_owner", "assignee"]
}

WORK_ORDERS_SCHEMA_STANDARD = {
    "project_name": ["name", "title", "project", "work_order"],
    "client_name": ["client_name", "client", "customer", "account"],
    "sector": ["sector", "industry", "domain"],
    "status": ["status", "operational_status", "execution_status", "state"],
    "start_date": ["start_date", "commencement_date"],
    "target_completion_date": ["target_completion_date", "end_date", "due_date", "completion_date"],
    "execution_value": ["execution_value", "contract_value", "value", "budget"],
    "delay_reason": ["delay_reason", "blocker", "notes", "risk_factor"]
}


def map_raw_record_to_schema(raw_dict: Dict[str, Any], schema_rules: Dict[str, List[str]]) -> Dict[str, Any]:
    """Map arbitrary dict keys into a target standard schema using candidate aliases."""
    mapped = {}
    for target_key, candidate_aliases in schema_rules.items():
        val = None
        for alias in candidate_aliases:
            if alias in raw_dict and raw_dict[alias] is not None:
                val = raw_dict[alias]
                break
        mapped[target_key] = val
    return mapped
