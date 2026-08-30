# API Design & Endpoint Specification

## REST API Endpoints

### 1. `POST /api/chat`
Submits a conversational founder question and returns structured BI metrics, charts data, executive insights, and data quality caveats.

**Request Body:**
```json
{
  "message": "How is the energy sector performing this quarter?",
  "session_id": "optional-uuid"
}
```

**Response Body:**
```json
{
  "session_id": "uuid",
  "query_plan": {
    "intent": "sector_analysis",
    "boards_required": ["deals", "work_orders"],
    "filters": {"sector": "Energy"},
    "metrics": ["total_pipeline_value", "deal_count", "active_work_orders"],
    "clarification_required": false
  },
  "metrics": {
    "pipeline_value": 450000.0,
    "deal_count": 3,
    "avg_deal_value": 150000.0,
    "active_work_orders": 2,
    "delayed_work_orders": 1
  },
  "insights": "The Energy sector represents $450K in open pipeline across 3 deals...",
  "data_quality_report": {
    "total_records": 10,
    "valid_records": 9,
    "missing_values": 1,
    "important_caveats": ["1 work order is missing completion date"]
  },
  "chart_data": [
    {"name": "Closed Won", "value": 200000},
    {"name": "Proposal Sent", "value": 250000}
  ]
}
```

### 2. `POST /api/leadership-update`
Generates a comprehensive executive update summarizing sales highlights, operational updates, risks, and recommendations.

### 3. `GET /api/data-quality`
Returns current data quality diagnostics across Deals and Work Orders boards.

### 4. `GET /health`
Health check endpoint returning system status and monday.com connectivity state.
