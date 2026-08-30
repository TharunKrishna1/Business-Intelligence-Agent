# Business & Technical Assumptions

1. **monday.com Board Schema Flexibility**:
   - Column IDs in monday.com boards vary across accounts. The application assumes standard column titles (e.g., "Deal Name", "Sector", "Value", "Stage", "Close Date") and provides dynamic title-to-schema mapping with fallback parsing.
   - Read-only operations are strictly enforced.

2. **Data Cleanliness & Missing Values**:
   - Real-world business data from monday.com contains missing values, string-formatted currencies (`"$150,000"`), multi-format dates (`"2026-09-01"`, `"01/09/2026"`), and raw text status values.
   - The normalization layer sanitizes data without silently dropping unparseable rows unless necessary for mathematical aggregations.

3. **Hybrid AI & Deterministic Calculations**:
   - LLMs are prone to arithmetic hallucination. All business analytics (pipeline totals, averages, stage breakdowns, cross-board joins) must be computed in Python via Pandas.
   - Gemini is used solely for natural-language query planning and executive narrative generation.

4. **Cross-Board Correlation**:
   - Deals and Work Orders boards share common business dimensions (`sector`, `client_name`). Cross-board metrics perform fuzzy matching on these dimensions and report data caveats when matching is partial.
