# Monday.com Business Intelligence Agent

> An AI-powered conversational Business Intelligence agent that connects directly to monday.com, cleans messy business data, performs deterministic analytics, and delivers founder-level insights through a natural language interface.

<p align="center">
  <img src="screenshots/architecture.png" alt="System Architecture" width="850">
</p>

---

## 📌 Overview

Business leaders need quick answers to questions such as:

* How is our sales pipeline looking?
* Which sector is performing the best?
* Are there any delayed work orders?
* Where are the biggest operational risks?
* Which high-value opportunities require attention?
* Can you prepare a leadership update?

However, answering these questions often requires manually collecting data from multiple business systems, cleaning inconsistent records, performing calculations, and creating ad-hoc reports.

**Monday.com Business Intelligence Agent** solves this problem by providing a conversational interface that dynamically retrieves data from monday.com boards, normalizes messy data, performs deterministic business analysis, and generates executive-level insights.

The application uses a **hybrid AI architecture**:

* **Gemini** understands natural language and generates insights.
* **Python + Pandas** performs deterministic business calculations.
* **monday.com API** provides live board data.
* The agent orchestrates the complete workflow from question to business insight.

---

# ✨ Features

## 💬 Conversational Business Intelligence

Ask natural language questions such as:

> "How is our pipeline looking?"

> "How is the energy sector performing this quarter?"

> "Which projects are delayed?"

> "Which sector has the strongest sales pipeline?"

> "Are there any operational risks associated with high-value opportunities?"

The agent interprets the question and determines:

* User intent
* Required monday.com boards
* Required filters
* Business metrics to calculate
* Whether clarification is needed

---

## 🔗 Live monday.com Integration

The application dynamically connects to monday.com using its GraphQL API.

The agent reads data from:

* **Deals Board**
* **Work Orders Board**

The application does not rely on hardcoded CSV or Excel data during runtime.

```text
User Question
      ↓
monday.com API
      ↓
Deals + Work Orders
      ↓
Data Normalization
      ↓
Business Analytics
      ↓
AI-Generated Insights
```

All monday.com operations are **read-only**.

---

## 🧹 Messy Data Handling

Real-world business data is often incomplete and inconsistent.

The application includes a dedicated data normalization layer capable of handling:

* Missing values
* Empty strings
* `N/A` values
* Invalid dates
* Inconsistent date formats
* Inconsistent sector names
* Inconsistent status values
* Numeric values stored as text
* Currency formatting inconsistencies
* Duplicate records where identifiable

Example:

```text
Energy
energy
ENERGY
Energy Sector
```

can be normalized into:

```text
energy
```

The application does not silently ignore poor-quality data.

Instead, it generates a **Data Quality Report** and communicates relevant limitations to the user.

Example:

> ⚠️ 4 records contained missing deal values and were excluded from revenue calculations.

---

# 🧠 AI Agent Architecture

The project uses a hybrid architecture designed for accuracy and explainability.

<p align="center">
  <img src="screenshots/agent-flow.png" alt="AI Agent Flow" width="900">
</p>

```text
┌───────────────────────┐
│     User Question     │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Conversation Context  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Gemini Query Planner │
│                       │
│ Intent                │
│ Filters               │
│ Metrics               │
│ Boards Required       │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Clarification Needed? │
└───────────┬───────────┘
            │
     ┌──────┴──────┐
     │             │
    Yes           No
     │             │
     ▼             ▼
Ask User      ┌──────────────────┐
              │ monday.com API   │
              │ Data Retrieval   │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Data Normalizer  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Data Quality     │
              │ Analysis         │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ BI Analytics     │
              │ Python + Pandas  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Gemini Insights  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Founder Response │
              └──────────────────┘
```

---

# 🏗️ System Architecture

<p align="center">
  <img src="screenshots/system-architecture.png" alt="System Architecture" width="900">
</p>

```text
                        ┌──────────────────────┐
                        │    React Frontend    │
                        │ Conversational UI    │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │    FastAPI Backend   │
                        │ Agent Orchestrator   │
                        └──────────┬───────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                ▼                  ▼                  ▼
        ┌──────────────┐   ┌──────────────┐  ┌──────────────┐
        │ Query Planner│   │ Data Quality │  │ Conversation │
        │    Gemini    │   │    Layer     │  │   Context    │
        └──────┬───────┘   └──────┬───────┘  └──────────────┘
               │                  │
               └────────┬─────────┘
                        ▼
             ┌──────────────────────┐
             │   monday.com API     │
             │   GraphQL Read Only  │
             └──────────┬───────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
      ┌──────────────┐    ┌──────────────┐
      │ Deals Board  │    │ Work Orders  │
      └──────┬───────┘    └──────┬───────┘
             │                   │
             └─────────┬─────────┘
                       ▼
             ┌──────────────────────┐
             │ Data Normalization   │
             │                      │
             │ • Dates              │
             │ • Values             │
             │ • Sectors            │
             │ • Status             │
             │ • Missing Data       │
             └──────────┬───────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │ BI Analytics Engine  │
             │                      │
             │ Python + Pandas      │
             └──────────┬───────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │ Insight Generator    │
             │ Gemini               │
             └──────────┬───────────┘
                        │
                        ▼
                 Business Insight
```

---

# 🤖 Why a Hybrid AI Architecture?

The system intentionally does **not** allow the LLM to perform all calculations independently.

Instead:

### AI handles

* Natural language understanding
* Intent detection
* Filter extraction
* Metric selection
* Clarification detection
* Executive insight generation
* Conversational responses

### Python handles

* Numerical calculations
* Aggregations
* Revenue analysis
* Pipeline calculations
* Sector comparisons
* Date filtering
* Cross-board analysis

### Example

User:

> How is the energy sector pipeline looking this quarter?

The AI generates a structured query plan:

```json
{
  "intent": "pipeline_analysis",
  "boards_required": ["deals"],
  "filters": {
    "sector": "energy",
    "date_range": "current_quarter"
  },
  "metrics": [
    "total_pipeline_value",
    "deal_count",
    "average_deal_value",
    "stage_distribution"
  ],
  "clarification_required": false
}
```

The Python analytics engine then performs the calculations.

Gemini receives the calculated results and converts them into a concise executive-level explanation.

This approach provides:

* Higher accuracy
* Reproducible calculations
* Reduced hallucination risk
* Easier debugging
* Better explainability

---

# 📊 Business Intelligence Capabilities

## Sales Pipeline Analysis

The agent can analyze:

* Total pipeline value
* Number of active deals
* Average deal value
* Deal stage distribution
* Late-stage opportunities
* Weighted pipeline when sufficient data exists

---

## Sector Analysis

The agent can provide:

* Pipeline value by sector
* Number of deals by sector
* Average deal value
* Sector comparisons
* Strongest and weakest performing sectors

---

## Work Order Analysis

The agent can analyze:

* Active work orders
* Completed work orders
* Delayed work orders
* Operational status
* Execution trends
* Data completeness

---

## Cross-Board Analysis

The agent combines information from Deals and Work Orders when meaningful relationships exist.

Example insight:

> The Energy sector has the strongest pipeline value but also shows a higher concentration of delayed work orders, indicating potential execution capacity risk.

Cross-board relationships are only created when supported by available data.

The application does not invent relationships between records.

---

# 📈 Leadership Updates

The agent can generate structured leadership updates based on the latest monday.com data.

A typical update includes:

### Executive Summary

A high-level overview of current business performance.

### Sales Highlights

* Pipeline changes
* Major opportunities
* Strong-performing sectors

### Operational Highlights

* Work order status
* Completion trends
* Delays

### Key Risks

* Pipeline concentration
* Operational bottlenecks
* Data quality concerns

### Opportunities

* High-value opportunities
* Strong sectors
* Potential areas for growth

### Recommended Actions

Data-driven suggestions based on calculated metrics.

---

# 🗂️ Project Structure

```text
monday-bi-agent/
│
├── frontend/
│   │
│   ├── src/
│   │   │
│   │   ├── api/
│   │   │   └── client.ts
│   │   │
│   │   ├── components/
│   │   │   │
│   │   │   ├── chat/
│   │   │   │   ├── ChatWindow.tsx
│   │   │   │   ├── ChatMessage.tsx
│   │   │   │   ├── ChatInput.tsx
│   │   │   │   └── SuggestedQueries.tsx
│   │   │   │
│   │   │   ├── insights/
│   │   │   │   ├── MetricCard.tsx
│   │   │   │   ├── InsightPanel.tsx
│   │   │   │   └── DataQualityAlert.tsx
│   │   │   │
│   │   │   └── charts/
│   │   │       ├── PipelineChart.tsx
│   │   │       └── SectorChart.tsx
│   │   │
│   │   ├── hooks/
│   │   │   └── useChat.ts
│   │   │
│   │   ├── types/
│   │   │   └── api.ts
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   └── package.json
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── chat.py
│   │   │   │   ├── health.py
│   │   │   │   └── leadership.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── agent/
│   │   │   ├── orchestrator.py
│   │   │   ├── query_planner.py
│   │   │   ├── context_manager.py
│   │   │   └── prompts.py
│   │   │
│   │   ├── integrations/
│   │   │   └── monday/
│   │   │       ├── client.py
│   │   │       ├── queries.py
│   │   │       ├── mapper.py
│   │   │       └── models.py
│   │   │
│   │   ├── data/
│   │   │   ├── normalizer.py
│   │   │   ├── validators.py
│   │   │   ├── quality.py
│   │   │   └── schema_mapper.py
│   │   │
│   │   ├── analytics/
│   │   │   ├── pipeline.py
│   │   │   ├── sector.py
│   │   │   ├── operations.py
│   │   │   ├── cross_board.py
│   │   │   └── leadership.py
│   │   │
│   │   ├── llm/
│   │   │   ├── gemini_client.py
│   │   │   ├── schemas.py
│   │   │   └── insight_generator.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── request.py
│   │   │   ├── response.py
│   │   │   └── query_plan.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── docs/
│   ├── architecture.md
│   ├── decision-log.md
│   ├── assumptions.md
│   └── api-design.md
│
├── screenshots/
│   ├── dashboard.png
│   ├── chat-example.png
│   ├── architecture.png
│   ├── agent-flow.png
│   └── system-architecture.png
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── README.md
├── .gitignore
└── LICENSE
```

---

# 🛠️ Technology Stack

## Frontend

| Technology     | Purpose                     |
| -------------- | --------------------------- |
| React          | User interface              |
| TypeScript     | Type safety                 |
| Vite           | Frontend build tooling      |
| Tailwind CSS   | UI styling                  |
| TanStack Query | API state management        |
| Recharts       | Business data visualization |

## Backend

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| FastAPI    | Backend API                     |
| Python     | Application logic               |
| Pandas     | Data processing and analytics   |
| Pydantic   | Request and response validation |
| httpx      | Async HTTP requests             |

## AI

| Technology        | Purpose                          |
| ----------------- | -------------------------------- |
| Gemini            | Query understanding and insights |
| Structured Output | Reliable AI query planning       |
| Pydantic          | LLM output validation            |

## Data Source

| Technology             | Purpose                         |
| ---------------------- | ------------------------------- |
| monday.com GraphQL API | Dynamic business data retrieval |

---

# 🔄 Application Workflow

```text
1. User asks a business question
            ↓
2. Agent analyzes the question
            ↓
3. Gemini creates a structured query plan
            ↓
4. Agent determines required monday.com boards
            ↓
5. Application retrieves live board data
            ↓
6. Data normalization layer cleans the records
            ↓
7. Data quality issues are identified
            ↓
8. Python analytics engine calculates metrics
            ↓
9. Gemini generates executive-level insights
            ↓
10. Structured response is displayed to the user
```

---

# ⚙️ Installation

## Prerequisites

* Python 3.10+
* Node.js 18+
* npm
* monday.com account
* monday.com API token
* Gemini API key

---

## Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd monday-bi-agent
```

---

# 🔐 Environment Configuration

Create a file:

```text
backend/.env
```

Add:

```env
MONDAY_API_TOKEN=your_monday_api_token
DEALS_BOARD_ID=your_deals_board_id
WORK_ORDERS_BOARD_ID=your_work_orders_board_id
GEMINI_API_KEY=your_gemini_api_key
```

### Important Security Note

Never commit `.env` files.

The repository includes an `.env.example` file containing the required variables without sensitive values.

---

# 🔗 monday.com Configuration

Create two boards:

## Deals Board

Import the provided Deals dataset into a monday.com board.

Recommended fields may include:

* Deal Name
* Sector
* Deal Value
* Deal Stage
* Expected Close Date
* Status
* Customer

The exact mapping should be configured based on the imported dataset.

---

## Work Orders Board

Import the provided Work Orders dataset into a separate monday.com board.

Recommended fields may include:

* Work Order ID
* Project
* Sector
* Status
* Start Date
* End Date
* Completion Date

The backend maps monday.com column values into an internal schema before analytics are performed.

---

# ▶️ Running the Backend

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

---

# ▶️ Running the Frontend

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

# 💬 Example Queries

Try asking:

### Pipeline

```text
How is our overall pipeline looking?
```

```text
How is the energy sector pipeline performing this quarter?
```

```text
Which sector has the strongest pipeline?
```

### Operations

```text
Which work orders are delayed?
```

```text
How is our operational performance?
```

### Cross-Board Analysis

```text
Which sectors have strong pipeline opportunities but operational risks?
```

```text
Are high-value opportunities associated with delayed projects?
```

### Leadership

```text
Prepare a leadership update.
```

---

# 🧪 Testing

The project includes tests for:

### Data Normalization

* Missing values
* Invalid dates
* Multiple date formats
* Sector normalization
* Currency parsing
* Invalid numeric values

### Analytics

* Pipeline calculations
* Sector analysis
* Work order metrics
* Cross-board analysis
* No matching records

### External Integrations

External services are mocked during tests.

Unit tests do not require:

* Real monday.com credentials
* Real Gemini API keys

Run backend tests:

```bash
cd backend
pytest
```

---

# 🛡️ Security Considerations

The application follows these principles:

* API keys are stored in environment variables.
* Secrets are never committed to Git.
* Secrets are never exposed to the frontend.
* monday.com access is read-only.
* Backend errors do not expose stack traces to users.
* External API calls use timeouts.
* API failures are handled gracefully.
* Sensitive values are excluded from application logs.
* LLM output is validated before execution.

---

# ⚠️ Known Limitations

This project is a prototype and has several intentional limitations:

* Conversation context is session-based.
* No persistent database is included.
* No user authentication is implemented.
* Advanced forecasting is not included.
* Analytics are limited to available monday.com board fields.
* Cross-board relationships depend on common available dimensions.
* Complex board schema changes may require additional mapping configuration.

---

# 🔮 Future Improvements

With additional development time, the project could include:

### Data and Analytics

* Automated anomaly detection
* Revenue forecasting
* Pipeline forecasting
* Trend analysis
* Automated KPI monitoring

### AI Capabilities

* RAG for leadership documents and reports
* Historical business context
* Multi-source data integration
* More advanced agent tools
* Automated insight generation

### Production Infrastructure

* Persistent conversation storage
* Redis caching
* User authentication
* Role-based access control
* Audit logging
* Observability and monitoring
* Rate limiting

### Integrations

* CRM platforms
* Accounting software
* Google Sheets
* Internal databases
* Document repositories

---

# 🧾 Key Technical Decisions

## Why monday.com API Instead of MCP?

The direct monday.com API was selected because it provides a transparent and controlled integration for a full-stack application.

Benefits include:

* Simple deployment architecture
* Direct control over requests
* Easier debugging
* Clear authentication handling
* Straightforward read-only access

---

## Why Not Use RAG?

The primary data source is structured business data from monday.com.

Structured analytics is better handled through:

```text
API Retrieval
      ↓
Data Normalization
      ↓
Pandas Analytics
      ↓
LLM Insights
```

A vector database would add unnecessary complexity for structured data.

The architecture can be extended with RAG in the future when working with unstructured sources such as:

* Leadership reports
* PDFs
* Meeting notes
* Contracts
* SOPs

---

## Why Use Deterministic Analytics?

Business intelligence often requires numerical accuracy.

Therefore:

```text
LLM → Understand Question

Python → Calculate Metrics

LLM → Explain Results
```

This reduces the risk of AI-generated numerical errors.

---

# 🤖 AI Tools Used

AI-assisted development tools may be used during development for:

* Architecture exploration
* Code generation
* Debugging
* Documentation assistance
* Test case generation
* UI development

The final implementation, architecture, technical decisions, and integration logic are reviewed and understood by the developer.

---

# 📝 Decision Log

A detailed technical decision log is available at:

```text
docs/decision-log.md
```

It documents:

* Key assumptions
* Architecture decisions
* Technology trade-offs
* Data handling strategy
* Interpretation of leadership updates
* Future improvements

---

# 🚀 Deployment

The current repository focuses on the application implementation.

The architecture is deployment-ready through:

* Environment-based configuration
* Health endpoints
* CORS configuration
* Separation of frontend and backend
* Centralized error handling

A production deployment could host:

```text
React Frontend
        ↓
Static Hosting Platform

FastAPI Backend
        ↓
Container / Application Platform

Environment Variables
        ↓
monday.com API + Gemini API
```

---

# 📸 Application Screenshots

## Conversational Interface

<p align="center">
  <img src="screenshots/chat-example.png" alt="Business Intelligence Chat Interface" width="850">
</p>

## Pipeline Analysis

<p align="center">
  <img src="screenshots/pipeline-analysis.png" alt="Pipeline Analysis" width="850">
</p>

## Data Quality Insights

<p align="center">
  <img src="screenshots/data-quality.png" alt="Data Quality Insights" width="850">
</p>

## Leadership Update

<p align="center">
  <img src="screenshots/leadership-update.png" alt="Leadership Update" width="850">
</p>

---

# 📄 License

This project is created for demonstration and technical evaluation purposes.

---

<p align="center">
  Built as an AI-powered conversational business intelligence system for structured business data.
</p>
