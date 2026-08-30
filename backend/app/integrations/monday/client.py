"""Monday.com GraphQL API Client.

READ-ONLY integration with monday.com API v2.
Includes exponential backoff retries, pagination, and mock data fallback.
"""

import asyncio
import httpx
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import (
    MondayAPIError,
    MondayAuthenticationError,
    MondayBoardNotFoundError
)
from app.integrations.monday.models import MondayItem, MondayFetchResult, MondayColumnValue
from app.integrations.monday.queries import GET_BOARD_ITEMS_QUERY


def generate_mock_deals_items() -> List[MondayItem]:
    """Generate realistic mock items for Deals board when API is unconfigured/offline."""
    raw_mock_deals = [
        {"id": "d1", "name": "Adani Solar Power Survey", "sector": "Energy", "val": "$450,000", "stage": "Proposal Sent", "date": "2026-09-15", "owner": "Rahul Sharma"},
        {"id": "d2", "name": "Tata Power Wind Inspection", "sector": "Energy & Utilities", "val": "350000", "stage": "Negotiation", "date": "2026-10-01", "owner": "Priya Patel"},
        {"id": "d3", "name": "NTPC Thermal Monitoring", "sector": "Energy", "val": "$200,000", "stage": "Closed Won", "date": "2026-08-10", "owner": "Rahul Sharma"},
        {"id": "d4", "name": "Indian Railways Corridor Mapping", "sector": "Infrastructure", "val": "$850,000", "stage": "Proposal Sent", "date": "2026-11-20", "owner": "Amit Verma"},
        {"id": "d5", "name": "NHAI Highway Inspection", "sector": "Infrastructure", "val": "$500,000", "stage": "Qualification", "date": "2026-12-05", "owner": "Amit Verma"},
        {"id": "d6", "name": "Coal India Pit Volume Survey", "sector": "Mining", "val": "$600,000", "stage": "Closed Won", "date": "2026-07-15", "owner": "Suresh Kumar"},
        {"id": "d7", "name": "Vedanta Mining Topography", "sector": "Mining & Minerals", "val": "$300,000", "stage": "Negotiation", "date": "2026-09-30", "owner": "Suresh Kumar"},
        {"id": "d8", "name": "Defense Border Reconnaissance", "sector": "Defense", "val": "$1,200,000", "stage": "Lead", "date": "2027-01-15", "owner": "Vikram Singh"},
        {"id": "d9", "name": "State Agriculture Crop Survey", "sector": "Agriculture", "val": "N/A", "stage": "Closed Lost", "date": "Invalid Date", "owner": "Priya Patel"},
        {"id": "d10", "name": "L&T Smart City Mapping", "sector": "Infrastructure", "val": "$750,000", "stage": "Closed Won", "date": "2026-08-01", "owner": "Amit Verma"},
    ]

    items = []
    for d in raw_mock_deals:
        items.append(
            MondayItem(
                id=d["id"],
                name=d["name"],
                column_values=[
                    MondayColumnValue(id="sector", title="Sector", text=d["sector"]),
                    MondayColumnValue(id="deal_value", title="Deal Value", text=d["val"]),
                    MondayColumnValue(id="stage", title="Stage", text=d["stage"]),
                    MondayColumnValue(id="close_date", title="Expected Close Date", text=d["date"]),
                    MondayColumnValue(id="owner", title="Owner", text=d["owner"]),
                ]
            )
        )
    return items


def generate_mock_work_orders_items() -> List[MondayItem]:
    """Generate realistic mock items for Work Orders board when API is unconfigured/offline."""
    raw_mock_wo = [
        {"id": "wo1", "name": "WO-2026-001: NTPC Solar Inspection", "client": "NTPC", "sector": "Energy", "status": "In Progress", "start": "2026-08-15", "end": "2026-09-30", "val": "$200,000", "delay": "None"},
        {"id": "wo2", "name": "WO-2026-002: Coal India Pit Mapping", "client": "Coal India", "sector": "Mining", "status": "Completed", "start": "2026-07-20", "end": "2026-08-25", "val": "$600,000", "delay": "None"},
        {"id": "wo3", "name": "WO-2026-003: L&T Smart City Drone Survey", "client": "L&T Construction", "sector": "Infrastructure", "status": "Delayed", "start": "2026-08-05", "end": "2026-09-10", "val": "$750,000", "delay": "Regulatory airspace clearance pending"},
        {"id": "wo4", "name": "WO-2026-004: Tata Power Wind Site Assessment", "client": "Tata Power", "sector": "Energy & Utilities", "status": "In Progress", "start": "2026-08-20", "end": "2026-10-15", "val": "$350,000", "delay": "Weather delays due to monsoon"},
        {"id": "wo5", "name": "WO-2026-005: Adani Green Energy Baseline", "client": "Adani Solar", "sector": "Energy", "status": "Not Started", "start": "2026-09-20", "end": "2026-11-01", "val": "$450,000", "delay": "Awaiting purchase order confirmation"},
        {"id": "wo6", "name": "WO-2026-006: NHAI Expressway Topo Survey", "client": "NHAI", "sector": "Infrastructure", "status": "Delayed", "start": "2026-08-01", "end": "2026-09-01", "val": "$500,000", "delay": "Equipment maintenance bottleneck"},
    ]

    items = []
    for w in raw_mock_wo:
        items.append(
            MondayItem(
                id=w["id"],
                name=w["name"],
                column_values=[
                    MondayColumnValue(id="client", title="Client Name", text=w["client"]),
                    MondayColumnValue(id="sector", title="Sector", text=w["sector"]),
                    MondayColumnValue(id="status", title="Status", text=w["status"]),
                    MondayColumnValue(id="start_date", title="Start Date", text=w["start"]),
                    MondayColumnValue(id="end_date", title="Target Completion Date", text=w["end"]),
                    MondayColumnValue(id="val", title="Execution Value", text=w["val"]),
                    MondayColumnValue(id="delay_reason", title="Delay Reason", text=w["delay"]),
                ]
            )
        )
    return items


class MondayClient:
    """Async Read-Only monday.com API Client."""

    def __init__(self, api_token: Optional[str] = None, api_url: Optional[str] = None):
        self.api_token = api_token or settings.MONDAY_API_TOKEN
        self.api_url = api_url or settings.MONDAY_API_URL
        self.timeout = settings.HTTP_TIMEOUT_SECONDS
        self.max_retries = settings.MAX_RETRIES

    def _get_headers(self) -> Dict[str, str]:
        if not self.api_token:
            raise MondayAuthenticationError("MONDAY_API_TOKEN environment variable is not configured.")
        return {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
            "API-Version": "2024-01",
        }

    async def _execute_graphql(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GraphQL query with retries and exponential backoff."""
        headers = self._get_headers()
        backoff = 1.0

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(1, self.max_retries + 1):
                try:
                    logger.debug(f"Executing monday.com GraphQL query (Attempt {attempt}/{self.max_retries})")
                    response = await client.post(
                        self.api_url,
                        headers=headers,
                        json={"query": query, "variables": variables}
                    )

                    if response.status_code == 401:
                        raise MondayAuthenticationError("Unauthorized: Invalid monday.com API Token.")
                    
                    response.raise_for_status()
                    data = response.json()

                    if "errors" in data and data["errors"]:
                        error_msg = data["errors"][0].get("message", "Unknown GraphQL error")
                        logger.error(f"monday.com GraphQL Error: {error_msg}")
                        raise MondayAPIError(f"GraphQL Error: {error_msg}")

                    return data.get("data", {})

                except (httpx.HTTPStatusError, httpx.RequestError, MondayAPIError) as exc:
                    if isinstance(exc, MondayAuthenticationError):
                        raise exc

                    logger.warning(f"monday.com API attempt {attempt} failed: {str(exc)}")
                    if attempt == self.max_retries:
                        raise MondayAPIError(f"monday.com API failed after {self.max_retries} attempts: {str(exc)}")
                    
                    await asyncio.sleep(backoff)
                    backoff *= settings.RETRY_BACKOFF_FACTOR

        raise MondayAPIError("Failed to execute monday.com query.")

    async def fetch_board_items(self, board_id: str, board_name: str = "Board") -> MondayFetchResult:
        """Fetch all items from a specified monday.com board (read-only)."""
        if not settings.is_monday_configured or not board_id:
            logger.info(f"monday.com API unconfigured. Returning mock data for {board_name} (ID: {board_id}).")
            if "deal" in board_name.lower() or board_id == settings.DEALS_BOARD_ID:
                return MondayFetchResult(board_id=board_id, board_name="Deals", raw_items=generate_mock_deals_items(), is_mock=True)
            else:
                return MondayFetchResult(board_id=board_id, board_name="Work Orders", raw_items=generate_mock_work_orders_items(), is_mock=True)

        try:
            items: List[MondayItem] = []
            cursor: Optional[str] = None
            
            while True:
                variables = {"board_id": [board_id], "limit": 500, "cursor": cursor}
                result = await self._execute_graphql(GET_BOARD_ITEMS_QUERY, variables)
                
                boards = result.get("boards", [])
                if not boards:
                    raise MondayBoardNotFoundError(f"Board with ID {board_id} not found.")

                items_page = boards[0].get("items_page", {})
                raw_page_items = items_page.get("items", [])

                for item_dict in raw_page_items:
                    col_vals = [
                        MondayColumnValue(**col) for col in item_dict.get("column_values", [])
                    ]
                    items.append(
                        MondayItem(
                            id=str(item_dict["id"]),
                            name=item_dict["name"],
                            column_values=col_vals
                        )
                    )

                cursor = items_page.get("cursor")
                if not cursor or not raw_page_items:
                    break

            logger.info(f"Successfully fetched {len(items)} items from monday.com board '{board_name}' (ID: {board_id}).")
            return MondayFetchResult(board_id=board_id, board_name=board_name, raw_items=items, is_mock=False)

        except Exception as exc:
            logger.warning(f"Error fetching from monday.com: {exc}. Falling back to mock data.")
            if "deal" in board_name.lower() or board_id == settings.DEALS_BOARD_ID:
                return MondayFetchResult(board_id=board_id, board_name="Deals", raw_items=generate_mock_deals_items(), is_mock=True)
            else:
                return MondayFetchResult(board_id=board_id, board_name="Work Orders", raw_items=generate_mock_work_orders_items(), is_mock=True)
