# Skylark Drones – monday.com Business Intelligence Agent

A production-quality conversational AI Business Intelligence (BI) Agent designed for **Skylark Drones**. The platform dynamically reads data from monday.com **Deals** and **Work Orders** boards and answers founder-level business questions with 100% mathematical accuracy and executive-ready insights.

---

## 1. Project Overview

The Skylark Drones BI Agent connects dynamically to monday.com via the GraphQL API (Read-Only) to analyze sales pipelines and operational project execution. It features a hybrid AI architecture that combines Google Gemini for structured query planning and executive narrative synthesis with a deterministic Python/Pandas analytics engine for financial calculations.

---

## 2. Problem Statement

Founders and executive leaders face two critical challenges when relying on traditional LLM chat agents for business intelligence:
1. **Financial Hallucinations**: Standard LLMs frequently miscalculate pipeline totals, average deal values, or operational counts.
2. **Messy & Inconsistent Business Data**: Column values on live monday.com boards contain inconsistent date formats, missing monetary values, string currencies (`"$450,000"`), and unstructured status names.

This project solves both challenges through a **deterministic hybrid architecture** that normalizes raw data, calculates financial metrics deterministically, and presents executive insights alongside transparent data quality alerts.

---

## 3. Features

* **Dynamic Read-Only monday.com Integration**: Securely fetches live board data with retries, exponential backoff, and pagination.
* **Messy Data Normalization**: Sanitizes currencies, multi-format dates, sector names, and status fields into clean dataframes.
* **Transparent Data Quality Reporting**: Generates a detailed `DataQualityReport` highlighting missing values, unparseable dates, and caveats.
* **Deterministic BI Analytics Engine**: Performs 100% accurate calculations for pipeline totals, sector market share, operational delay rates, and cross-board risk joins.
* **Structured Gemini Query Planning**: Extracts intents, sector filters, and metrics into Pydantic models with single-retry corrective parsing.
* **Executive Leadership Update Feature**: One-click generation of a 7-part executive update (Summary, Sales, Operations, Risks, Opportunities, Quality Caveats, Actions).
* **Founder-Facing React Dashboard**: Modern responsive UI with metric cards, Recharts visualizations, data quality warning alerts, and suggested queries.

---

## 4. Architecture

The application implements a decoupled, production-ready hybrid architecture:

```
┌─────────────────────────────────────────────────────────┐
│            React + TypeScript + Vite Frontend           │
│   (ChatWindow, MetricCard, Recharts, DataQualityAlert)  │
└────────────────────────────┬────────────────────────────┘
                             │ REST API (HTTP JSON)
                             ▼
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Backend                       │
│    (/api/chat, /api/leadership-update, /api/quality)   │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                  Agent Orchestrator                     │
│  - Session Context Manager                              │
│  - Gemini Structured Query Planner (Pydantic validated) │
│  - monday.com GraphQL API Client (Read-Only + Retries)  │
│  - Data Normalizer & Data Quality Diagnostics Engine    │
│  - Deterministic Pandas BI Analytics Engine             │
│  - Gemini Executive Insight Generator                   │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Architecture Diagram

```
User Query ──► Session Context ──► Gemini Query Planner ──► monday.com GraphQL API
                                                                    │
                                                                    ▼
Executive Insights ◄── Gemini Generator ◄── Pandas BI Engine ◄── Data Normalizer
```

---

## 6. Technology Stack

### Frontend
* **Framework**: React 18, TypeScript, Vite
* **Styling**: Tailwind CSS
* **Charts**: Recharts
* **Icons**: Lucide React

### Backend
* **Framework**: Python 3.11+, FastAPI, Uvicorn
* **Data Engine**: Pandas, Pydantic v2
* **HTTP Client**: httpx (Async with retries & exponential backoff)
* **Configuration**: pydantic-settings, python-dotenv

### AI Integration
* **SDK**: `google-genai` Python SDK
* **Model**: Gemini 1.5 Flash
* **Validation**: Pydantic structured output validation

---

## 7. Why This AI Architecture Was Chosen

We deliberately selected a **Hybrid Query Planning + Deterministic Analytics + Executive Generation** pattern rather than letting the LLM query raw data directly or write code on the fly. 

This architecture guarantees:
* **Zero Math Hallucinations**: Numbers are calculated by audited Python code.
* **Explainability**: Every metric can be traced back to exact Pandas calculations.
* **Security**: Read-only monday.com integration ensures zero risk of board mutations.

---

## 8. Why Deterministic Analytics Are Used

Large Language Models are probabilistic text generators, not arithmetic units. In business intelligence, a 5% error in pipeline calculations or missing a delayed work order can lead to wrong strategic decisions. Using Pandas for all aggregation ensures 100% reproducible results.

---

## 9. monday.com Integration

The integration layer (`backend/app/integrations/monday/`) features:
* **Read-Only Operations**: Only GraphQL `query` calls are executed; zero `mutation` calls exist.
* **Dynamic Mapping**: Converts arbitrary monday.com column IDs and titles into normalized schema keys.
* **Resilience**: Retries failed network calls up to 3 times with exponential backoff and timeouts.
* **Mock Fallback**: Automatically provides mock Deals and Work Orders datasets if API tokens are unconfigured or during offline testing.

---

## 10. Data Normalization Strategy

Located in `backend/app/data/normalizer.py`:
* **Currencies**: Converts `"$450,000"`, `"350000"`, `"N/A"` into clean float numbers while logging parsing actions.
* **Dates**: Parses `YYYY-MM-DD`, `DD/MM/YYYY`, `MM/DD/YYYY`, and text dates into standardized ISO strings (`YYYY-MM-DD`).
* **Sectors**: Standardizes variations like `"Energy & Utilities"`, `"solar"`, `"power"` to `"Energy"`.
* **Status**: Normalizes stage and status strings into canonical buckets (`"Proposal Sent"`, `"In Progress"`, `"Delayed"`).

---

## 11. Data Quality Handling

The data quality layer (`backend/app/data/quality.py`) compiles a transparent `DataQualityReport` returned with every API response:
* Counts valid vs missing records.
* Identifies unparseable dates or missing monetary amounts.
* Generates actionable caveats displayed directly in the user interface.
* Never silently hides bad or incomplete data.

---

## 12. Query Understanding

The query planner (`backend/app/agent/query_planner.py`) uses Gemini to classify user intent into a strict Pydantic `QueryPlan`:
* **Intents**: `pipeline_analysis`, `sector_analysis`, `work_order_analysis`, `cross_board_analysis`, `leadership_update`.
* **Filters**: Extracted sector, date range, stage, and operational status.
* **Validation**: Validated via Pydantic; retries once with a corrective prompt if invalid, and falls back to a deterministic rule-based planner if needed.

---

## 13. Business Intelligence Capabilities

* **Pipeline Analysis**: Total pipeline value, deal count, average deal size, stage breakdown, open pipeline, late-stage pipeline, weighted pipeline.
* **Sector Analysis**: Sector market share, deal count by sector, average deal size by sector, top-performing sector identification.
* **Work Order Analysis**: Active, completed, delayed work orders, operational delay rate (%), detailed delay reasons.
* **Cross-Board Analysis**: Correlates high sales pipeline sectors with active operational execution delays to identify revenue risks.

---

## 14. Leadership Update Feature

Clicking **Leadership Update** triggers a pre-aggregated cross-board analysis producing a 7-part executive update:
1. Executive Summary
2. Sales Highlights
3. Operational Highlights
4. Key Risks
5. Opportunities
6. Data Quality Caveats
7. Recommended Actions

---

## 15. Project Structure

```
Monday-Business-Intelligence-Agent/
├── backend/
│   ├── app/
│   │   ├── agent/             # Query planner, context manager, orchestrator
│   │   ├── analytics/         # Deterministic Pandas BI engines
│   │   ├── api/               # FastAPI REST routes and dependencies
│   │   ├── core/              # Config, logging, exception handlers
│   │   ├── data/              # Normalizer, validators, quality reporter
│   │   ├── integrations/      # monday.com GraphQL client and mapper
│   │   ├── schemas/           # Pydantic QueryPlan and API schemas
│   │   └── main.py            # FastAPI entry point
│   ├── tests/
│   │   ├── unit/              # Unit tests for analytics, normalizer, client
│   │   └── integration/       # End-to-end conversational workflow tests
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/               # API client
│   │   ├── components/        # ChatWindow, MetricCard, Recharts, Alerts
│   │   ├── types/             # TypeScript type definitions
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── docs/
│   ├── decision-log.md
│   ├── architecture.md
│   ├── assumptions.md
│   └── api-design.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── README.md
├── LICENSE
└── .gitignore
```

---

## 16. Local Setup Instructions

### Prerequisites
* Python 3.11+
* Node.js v18+
* npm v9+

### Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

---

## 17. monday.com Configuration Instructions

1. Log into your monday.com account.
2. Go to **Admin** -> **API** to generate a Read-Only API Token.
3. Open your Deals board and Work Orders board to copy their Board IDs from the browser URL (`https://*.monday.com/boards/{BOARD_ID}`).
4. Copy `backend/.env.example` to `backend/.env` and update the values:

```env
MONDAY_API_TOKEN=your_monday_api_token
DEALS_BOARD_ID=1234567890
WORK_ORDERS_BOARD_ID=0987654321
GEMINI_API_KEY=your_gemini_api_key
```

*(Note: If API keys are omitted, the application automatically uses mock data fallback mode).*

---

## 18. Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `MONDAY_API_TOKEN` | Read-Only monday.com API Token | `None` (triggers mock fallback) |
| `DEALS_BOARD_ID` | monday.com Deals Board ID | `None` |
| `WORK_ORDERS_BOARD_ID` | monday.com Work Orders Board ID | `None` |
| `GEMINI_API_KEY` | Google Gemini API Key | `None` (triggers fallback synthesis) |
| `ENV` | Environment name (`development`/`production`) | `development` |
| `LOG_LEVEL` | Logging verbosity (`INFO`/`DEBUG`) | `INFO` |

---

## 19. How to Run

### Start Backend API Server
```bash
cd backend
python app/main.py
```
*(Server starts at `http://localhost:8000`. Access Swagger UI at `http://localhost:8000/docs`).*

### Start Frontend Application
```bash
cd frontend
npm run dev
```
*(Application runs at `http://localhost:3000`).*

---

## 20. Example Queries

* *"How is our overall pipeline looking?"*
* *"How is the energy sector performing this quarter?"*
* *"Which projects are delayed?"*
* *"Which sector has the strongest pipeline?"*
* *"Are there operational risks associated with high-value opportunities?"*
* *"Prepare a leadership update"*

---

## 21. Testing

Run the full Pytest suite covering unit tests and integration tests:

```bash
cd backend
python -m pytest tests/ -v
```

To run frontend TypeScript typechecking:
```bash
cd frontend
npx tsc --noEmit
```

---

## 22. Security Considerations

* **Strictly Read-Only**: No GraphQL mutations exist in the codebase.
* **Secret Protection**: API tokens and keys are loaded via `.env` and never logged or sent to the frontend.
* **Secret Masking Formatter**: Custom log formatter masks tokens and keys in console outputs.
* **Centralized Exception Handling**: Internal stack traces are suppressed in production error responses.

---

## 23. Known Limitations

* **Session Memory**: Conversation memory is in-memory per session (resets on backend restart).
* **Column Matching**: Dynamic column matching relies on standard titles (e.g. "Deal Value", "Sector"). Unusually named custom columns require schema mapping rules in `schema_mapper.py`.

---

## 24. Future Improvements & Deployment Strategy

### Future Improvements
1. **Redis Caching**: Cache board GraphQL queries with 5-minute TTL.
2. **Persistent Conversation Database**: Store chat history in PostgreSQL.
3. **RAG Module**: Integrate vector search for internal unstructured PDF SOPs and board meeting minutes.

### Production Deployment Strategy
* **Backend**: Containerize using Docker and deploy to AWS ECS, GCP Cloud Run, or Render.
* **Frontend**: Build production assets (`npm run build`) and host via Vercel, Netlify, or AWS CloudFront/S3.
* **CORS & Environment**: Set `CORS_ORIGINS` to production frontend domain.

---

## 25. AI Tools Used

* **Google Antigravity**: Lead AI pair programmer assisting with architecture, modular implementation, testing, and documentation.
* **Google Gemini API**: Powering structured query planning and executive narrative synthesis.
