from pathlib import Path

from src.analytics.funnel import funnel_analysis
from src.analytics.item_analysis import item_insights
from src.analytics.overview import build_overview
from src.analytics.retention import retention_analysis
from src.analytics.rfm import rfm_analysis
from src.core.config import REPORT_DIR
from src.core.logger import get_logger
from src.report.generator import generate_report
from src.report.pdf_exporter import export_pdf


def _advance(progress_bar, status_text, step: int, total_steps: int, message: str):
    status_text.text(message)
    progress_bar.progress(step / total_steps)


def run_full_pipeline(df, seg, progress_bar, status_text):
    """Run dashboard analytics and report generation."""
    logger = get_logger("pipeline")
    logger.info("Pipeline started")

    total_steps = 7
    step = 0

    step += 1
    _advance(progress_bar, status_text, step, total_steps, "Computing overview...")
    overview = build_overview(df)

    step += 1
    _advance(progress_bar, status_text, step, total_steps, "Running funnel analysis...")
    funnel_result = funnel_analysis(df)

    step += 1
    _advance(progress_bar, status_text, step, total_steps, "Calculating retention...")
    retention_matrix = retention_analysis(df)

    step += 1
    _advance(progress_bar, status_text, step, total_steps, "Running RFM analysis...")
    rfm_result = rfm_analysis(df)

    step += 1
    _advance(progress_bar, status_text, step, total_steps, "Analyzing items...")
    item_result = item_insights(seg)

    step += 1
    _advance(progress_bar, status_text, step, total_steps, "Generating report...")
    report, file_path = generate_report(
        df,
        overview,
        funnel_result,
        retention_matrix,
        item_result,
        save_path=REPORT_DIR,
    )

    step += 1
    _advance(progress_bar, status_text, step, total_steps, "Exporting PDF...")
    pdf_path = export_pdf(report, str(Path(file_path).with_suffix(".pdf")))

    status_text.text("Done.")
    logger.info("Pipeline completed successfully")

    return {
        "overview": overview,
        "funnel": funnel_result,
        "retention": retention_matrix,
        "rfm": rfm_result,
        "item": item_result,
        "report_path": file_path,
        "pdf_path": pdf_path,
    }
