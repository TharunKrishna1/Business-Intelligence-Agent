"""Data normalization pipeline for messy monday.com business data."""

import re
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from app.core.logging import logger

SECTOR_MAP = {
    "energy": "Energy",
    "energy & utilities": "Energy",
    "energy and utilities": "Energy",
    "solar": "Energy",
    "wind": "Energy",
    "power": "Energy",
    "infrastructure": "Infrastructure",
    "highways": "Infrastructure",
    "roads": "Infrastructure",
    "smart city": "Infrastructure",
    "mining": "Mining",
    "mining & minerals": "Mining",
    "mining and minerals": "Mining",
    "minerals": "Mining",
    "defense": "Defense",
    "defense & security": "Defense",
    "defence": "Defense",
    "agriculture": "Agriculture",
    "agri": "Agriculture",
    "farming": "Agriculture",
}

STAGE_MAP = {
    "lead": "Lead",
    "qualification": "Qualification",
    "proposal sent": "Proposal Sent",
    "proposal": "Proposal Sent",
    "negotiation": "Negotiation",
    "under negotiation": "Negotiation",
    "closed won": "Closed Won",
    "won": "Closed Won",
    "closed lost": "Closed Lost",
    "lost": "Closed Lost",
}

WO_STATUS_MAP = {
    "not started": "Not Started",
    "unstarted": "Not Started",
    "in progress": "In Progress",
    "ongoing": "In Progress",
    "delayed": "Delayed",
    "on hold": "Delayed",
    "completed": "Completed",
    "done": "Completed",
    "finished": "Completed",
}


def parse_currency_value(val: Any) -> Tuple[Optional[float], Optional[str]]:
    """Parse messy monetary strings like '$450,000', '350000', 'N/A' into float and note action."""
    if val is None or val == "":
        return None, "Missing monetary value"
    
    val_str = str(val).strip()
    if val_str.upper() in ["N/A", "UNKNOWN", "NONE", "NULL", "-"]:
        return None, "Invalid/N/A monetary value"

    # Remove currency symbols, commas, spaces
    cleaned = re.sub(r"[^\d.-]", "", val_str)
    if not cleaned or cleaned == "-":
        return None, f"Unparseable monetary format '{val_str}'"

    try:
        parsed = float(cleaned)
        action = f"Parsed '{val_str}' -> {parsed}" if val_str != str(parsed) else None
        return parsed, action
    except ValueError:
        return None, f"Failed to parse monetary value '{val_str}'"


def parse_date_string(date_val: Any) -> Tuple[Optional[str], Optional[str]]:
    """Parse multi-format date string into ISO YYYY-MM-DD or return None."""
    if not date_val or str(date_val).strip().upper() in ["N/A", "INVALID DATE", "UNKNOWN", "NONE", "NULL", "-"]:
        return None, "Missing or invalid date string"

    date_str = str(date_val).strip()

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%b %d, %Y",
        "%B %d, %Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            iso_date = dt.strftime("%Y-%m-%d")
            action = f"Parsed date '{date_str}' -> '{iso_date}'" if date_str != iso_date else None
            return iso_date, action
        except ValueError:
            continue

    return None, f"Unrecognized date format '{date_str}'"


def normalize_sector_name(sector_raw: str) -> Tuple[str, Optional[str]]:
    """Normalize inconsistent sector/industry names."""
    if not sector_raw or sector_raw.strip().upper() in ["N/A", "UNKNOWN", "NONE", "NULL", ""]:
        return "Unknown", "Defaulted missing sector to 'Unknown'"

    clean = sector_raw.strip().lower()
    normalized = SECTOR_MAP.get(clean)
    if normalized:
        action = f"Normalized sector '{sector_raw}' -> '{normalized}'" if sector_raw != normalized else None
        return normalized, action
    
    title_case = sector_raw.strip().title()
    return title_case, f"Formatted sector '{sector_raw}' -> '{title_case}'"


def normalize_deals_dataset(raw_records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str], List[Dict[str, Any]]]:
    """Normalize Deals dataset. Returns (normalized_records, normalization_actions, excluded_records)."""
    normalized = []
    actions = []
    excluded = []

    for rec in raw_records:
        deal_id = rec.get("deal_id", "unknown")
        deal_name = rec.get("deal_name", "Unnamed Deal")
        
        # Sector normalization
        sector, sector_action = normalize_sector_name(rec.get("sector", ""))
        if sector_action:
            actions.append(f"[Deal {deal_id}] {sector_action}")

        # Currency normalization
        val_float, val_action = parse_currency_value(rec.get("deal_value"))
        if val_action:
            actions.append(f"[Deal {deal_id}] {val_action}")

        # Stage normalization
        stage_raw = rec.get("stage", "").strip()
        stage_clean = STAGE_MAP.get(stage_raw.lower(), stage_raw.title() if stage_raw else "Unknown")

        # Date normalization
        close_date, date_action = parse_date_string(rec.get("expected_close_date"))
        if date_action:
            actions.append(f"[Deal {deal_id}] {date_action}")

        norm_rec = {
            "deal_id": deal_id,
            "deal_name": deal_name,
            "sector": sector,
            "deal_value": val_float,
            "stage": stage_clean,
            "expected_close_date": close_date,
            "owner": rec.get("owner", "Unassigned"),
            "has_missing_value": val_float is None,
            "has_missing_date": close_date is None,
            "raw_record": rec
        }

        normalized.append(norm_rec)

    return normalized, actions, excluded


def normalize_work_orders_dataset(raw_records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str], List[Dict[str, Any]]]:
    """Normalize Work Orders dataset. Returns (normalized_records, normalization_actions, excluded_records)."""
    normalized = []
    actions = []
    excluded = []

    for rec in raw_records:
        wo_id = rec.get("work_order_id", "unknown")
        proj_name = rec.get("project_name", "Unnamed Project")

        # Sector normalization
        sector, sector_action = normalize_sector_name(rec.get("sector", ""))
        if sector_action:
            actions.append(f"[Work Order {wo_id}] {sector_action}")

        # Status normalization
        status_raw = rec.get("status", "").strip()
        status_clean = WO_STATUS_MAP.get(status_raw.lower(), status_raw.title() if status_raw else "Unknown")

        # Value normalization
        val_float, val_action = parse_currency_value(rec.get("execution_value"))
        if val_action:
            actions.append(f"[Work Order {wo_id}] {val_action}")

        # Date normalization
        start_date, start_action = parse_date_string(rec.get("start_date"))
        if start_action:
            actions.append(f"[Work Order {wo_id}] Start Date: {start_action}")

        target_date, target_action = parse_date_string(rec.get("target_completion_date"))
        if target_action:
            actions.append(f"[Work Order {wo_id}] Target Date: {target_action}")

        norm_rec = {
            "work_order_id": wo_id,
            "project_name": proj_name,
            "client_name": rec.get("client_name", "Unknown Client"),
            "sector": sector,
            "status": status_clean,
            "start_date": start_date,
            "target_completion_date": target_date,
            "execution_value": val_float,
            "delay_reason": rec.get("delay_reason", "").strip(),
            "has_missing_value": val_float is None,
            "has_missing_dates": start_date is None or target_date is None,
            "raw_record": rec
        }

        normalized.append(norm_rec)

    return normalized, actions, excluded
