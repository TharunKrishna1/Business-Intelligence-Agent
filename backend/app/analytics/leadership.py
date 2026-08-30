"""Leadership update pre-aggregation module."""

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
