"""Leadership update generation module."""

from typing import Dict, Any, List
from app.analytics.pipeline import compute_pipeline_metrics
from app.analytics.sector import compute_sector_metrics
from app.analytics.operations import compute_work_order_metrics
from app.analytics.cross_board import compute_cross_board_analysis
from app.data.quality import DataQualityReport


def compile_leadership_metrics(
    deals_norm: List[Dict[str, Any]],
    work_orders_norm: List[Dict[str, Any]],
    quality_report: DataQualityReport
) -> Dict[str, Any]:
    """Compile all deterministic metrics into a unified executive leadership payload."""
    pipeline_metrics = compute_pipeline_metrics(deals_norm)
    sector_metrics = compute_sector_metrics(deals_norm)
    operations_metrics = compute_work_order_metrics(work_orders_norm)
    cross_board_metrics = compute_cross_board_analysis(deals_norm, work_orders_norm)

    return {
        "pipeline": pipeline_metrics,
        "sector": sector_metrics,
        "operations": operations_metrics,
        "cross_board": cross_board_metrics,
        "data_quality": quality_report.model_dump(),
    }


def generate_structured_leadership_update(leadership_payload: Dict[str, Any]) -> str:
    """Generate structured 7-section leadership update text from deterministic metrics."""
    p = leadership_payload.get("pipeline", {})
    s = leadership_payload.get("sector", {})
    o = leadership_payload.get("operations", {})
    cb = leadership_payload.get("cross_board", {})
    dq = leadership_payload.get("data_quality", {})

    top_sec = s.get("top_performing_sector", "N/A")
    high_risks = cb.get("high_risk_sectors", [])
    delayed_orders = o.get("delayed_work_orders_list", [])
    caveats = dq.get("important_caveats", [])

    risk_bullets = []
    if delayed_orders:
        for wo in delayed_orders:
            risk_bullets.append(f"- **{wo.get('project_name')}** ({wo.get('client_name')}): {wo.get('delay_reason') or 'Execution delay'}")
    if not risk_bullets:
        risk_bullets.append("- Operations executing without critical bottlenecks.")

    caveat_bullets = [f"- {c}" for c in caveats] if caveats else ["- All board data normalized without exclusions."]

    return f"""# Skylark Drones – Executive Leadership Update

## 1. Executive Summary
Total active sales pipeline stands at **${p.get('total_pipeline_value', 0):,.2f}** across **{p.get('deal_count', 0)}** opportunities. Operations are managing **{o.get('total_work_orders', 0)}** work orders with **{o.get('active_work_orders', 0)}** active projects and an overall execution budget of **${o.get('total_execution_value', 0):,.2f}**.

## 2. Sales Highlights
- **Total Pipeline Value**: ${p.get('total_pipeline_value', 0):,.2f}
- **Open Pipeline Value**: ${p.get('open_pipeline_value', 0):,.2f}
- **Late-Stage Pipeline (Proposal/Negotiation/Won)**: ${p.get('late_stage_pipeline_value', 0):,.2f}
- **Average Deal Value**: ${p.get('average_deal_value', 0):,.2f}
- **Top Sector**: **{top_sec}** (${s.get('pipeline_by_sector', {}).get(top_sec, 0):,.2f} pipeline)

## 3. Operational Highlights
- **Active Work Orders**: {o.get('active_work_orders', 0)}
- **Completed Work Orders**: {o.get('completed_work_orders', 0)}
- **Delayed Work Orders**: {o.get('delayed_work_orders', 0)} (Delay Rate: {o.get('operational_delay_rate_pct', 0)}%)
- **Total Execution Budget**: ${o.get('total_execution_value', 0):,.2f}

## 4. Key Risks
{chr(10).join(risk_bullets)}

## 5. Opportunities
- High-value pipeline conversion in top sector **{top_sec}**.
- Weighted pipeline projection indicates potential revenue of **${p.get('weighted_pipeline_value', 0):,.2f}**.

## 6. Data Quality Caveats
{chr(10).join(caveat_bullets)}

## 7. Recommended Actions
1. Accelerate closing negotiations for late-stage deals (${p.get('late_stage_pipeline_value', 0):,.2f}).
2. Resolve airspace clearance and weather bottlenecks on delayed work orders.
3. Align operations capacity with high-demand sectors like {top_sec}.
"""
