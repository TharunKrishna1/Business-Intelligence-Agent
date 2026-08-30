# Skylark Drones BI Agent - Decision Log & Architectural Rationale

## 1. Assumptions

Due to variable column IDs across monday.com enterprise accounts, the following assumptions were made:
- **Board Schemas**: The Deals board tracks sales opportunities (deal name, sector/industry, deal value, stage, expected close date, owner). The Work Orders board tracks project execution (project title, client name, sector, operational status, start/end dates, execution value, delay reason).
- **Read-Only Scope**: In strict compliance with security constraints, the agent performs read-only queries against monday.com GraphQL API.
- **Data Imperfections**: Real-world data from monday.com contains messy dates, string-formatted currencies (`"$450,000"`), and unstandardized sector names. The normalizer handles these gracefully without silent row deletion.

---

## 2. Technical Decisions

- **API direct integration over MCP**: Using the native monday.com GraphQL API v2 via `httpx` allows full control over async request batching, exponential backoff retries, timeouts, and custom pagination.
- **Hybrid AI + Deterministic Python Analytics Architecture**:
  - LLMs are prone to arithmetic hallucinations. We delegate all numerical calculations (totals, counts, averages, stage distributions, cross-board joins) to Pandas.
  - Gemini is used strictly for natural-language query planning (intent & filter extraction via Pydantic) and executive narrative synthesis.
- **No RAG / Vector DB for Structured Board Data**: RAG is designed for unstructured documents. Structured tabular data from monday.com is directly fetched and analyzed via SQL/Dataframe queries, preventing vector search retrieval losses. The architecture is modular so a RAG module can be plugged in later for PDF SOPs/reports.
- **FastAPI Backend + React Frontend**: FastAPI provides native Pydantic validation, async performance, and auto-generated OpenAPI documentation. React + TypeScript + Tailwind CSS delivers a responsive founder dashboard.

---

## 3. Trade-offs

- **Accuracy vs. Full LLM Autonomy**: By restricting Gemini from writing code or calculating numbers on the fly, we gain 100% mathematical reproducibility at the cost of strict schema-bound BI metrics.
- **Dynamic Retrieval vs. Caching**: Real-time fetching ensures zero data staleness but introduces API latency. We implemented exponential backoff and structured data structures to keep latency under 1.5 seconds.
- **Prototype Speed vs. Microservice Overhead**: Built as a clean modular monolith to eliminate network serialization latency and infrastructure complexity.

---

## 4. Leadership Updates Interpretation

Leadership Updates are structured 7-section executive reports generated dynamically from live business data across both boards:
1. Executive Summary
2. Sales Highlights
3. Operational Highlights
4. Key Risks
5. Opportunities
6. Data Quality Caveats
7. Recommended Actions

---

## 5. What We Would Do With More Time

1. **Redis Caching Layer**: Cache monday.com GraphQL board payloads with a 5-minute TTL.
2. **Persistent Conversation Database**: Store session chat history in PostgreSQL.
3. **Role-Based Access Control (RBAC)**: Restrict founder-level financial views based on user permissions.
4. **Auto-Discovery of Board Schemas**: Automatically infer custom monday.com column types via GraphQL introspection.
5. **RAG Integration for Unstructured Reports**: Embed internal PDF SOPs and board meeting minutes via vector search.
