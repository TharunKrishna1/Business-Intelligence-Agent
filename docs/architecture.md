# System Architecture & Technical Specifications

## Architectural Overview

```
┌─────────────────────────────────────────────────────────┐
│              React + TypeScript + Vite UI               │
│  (ChatWindow, MetricCard, Recharts, DataQualityAlert)   │
└────────────────────────────┬────────────────────────────┘
                             │ REST API (JSON)
                             ▼
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Backend                       │
│    (/api/chat, /api/leadership-update, /api/quality)   │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                  Agent Orchestrator                     │
│  - Conversation Context Manager (Session memory)        │
│  - Query Planner (Gemini + Pydantic validation)        │
│  - monday.com GraphQL Client (httpx async + retries)    │
│  - Data Normalizer & Quality Analyzer                   │
│  - Deterministic BI Engine (Pandas analytics)          │
│  - Insight Generator (Gemini executive summary)        │
└─────────────────────────────────────────────────────────┘
```

## Key Components

1. **GraphQL Data Layer**: Async GraphQL queries to `https://api.monday.com/v2` with exponential backoff and mock fallback for standalone operation.
2. **Normalization & Quality Layer**: Converts messy strings, dates, and sector names into clean dataframes while generating a comprehensive `DataQualityReport`.
3. **Deterministic BI Analytics Engine**: Module-based analytics (`pipeline`, `sector`, `operations`, `cross_board`, `leadership`) ensuring 100% accurate financial calculations.
4. **Structured Gemini Query Planner**: Extracts intent, target boards, date filters, and sector filters into a strict Pydantic `QueryPlan`.
