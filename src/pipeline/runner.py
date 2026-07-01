import sys
from pathlib import Path

# =========================
# FIX: src path
# =========================
sys.path.append(str(Path(__file__).resolve().parent.parent))

# =========================
# imports
# =========================
from src.core.logger import get_logger
from src.analytics.overview import build_overview
from src.analytics.funnel import funnel_analysis
from src.analytics.retention import retention_analysis
from src.analytics.item_analysis import item_insights
from src.report.generator import generate_report
from src.report.pdf_exporter import export_pdf
from src.core.config import REPORT_DIR


def run_full_pipeline(df, seg, progress_bar, status_text):

    logger = get_logger("pipeline")
    logger.info("Pipeline started")

    total_steps = 6
    step = 0

    # =====================
    # 1. Overview
    # =====================
    logger.info("Step 1: Overview started")
    status_text.text("Computing Overview...")

    overview = build_overview(df)

    logger.info("Step 1: Overview finished")

    step += 1
    progress_bar.progress(step / total_steps)

    # =====================
    # 2. Funnel
    # =====================
    logger.info("Step 2: Funnel started")
    status_text.text("Running Funnel...")

    funnel_result = funnel_analysis(df)

    logger.info("Step 2: Funnel finished")

    step += 1
    progress_bar.progress(step / total_steps)

    # =====================
    # 3. Retention
    # =====================
    logger.info("Step 3: Retention started")
    status_text.text("Calculating Retention...")

    retention_matrix = retention_analysis(df)

    logger.info("Step 3: Retention finished")

    step += 1
    progress_bar.progress(step / total_steps)

    # =====================
    # 4. Item
    # =====================
    logger.info("Step 4: Item analysis started")
    status_text.text("Analyzing Items...")

    item_result = item_insights(seg)

    logger.info("Step 4: Item analysis finished")

    step += 1
    progress_bar.progress(step / total_steps)

    # =====================
    # 5. Report
    # =====================
    logger.info("Step 5: Report generation started")
    status_text.text("Generating Report...")

    report, file_path = generate_report(
        df,
        overview,
        funnel_result,
        retention_matrix,
        item_result,
        save_path=REPORT_DIR
    )

    logger.info("Step 5: Report generation finished")

    step += 1
    progress_bar.progress(step / total_steps)

    # =====================
    # 6. PDF
    # =====================
    logger.info("Step 6: PDF export started")
    status_text.text("Exporting PDF...")

    pdf_path = export_pdf(
        report,
        str(Path(file_path).with_suffix(".pdf"))
    )

    logger.info("Step 6: PDF export finished")

    step += 1
    progress_bar.progress(step / total_steps)

    # =====================
    # DONE
    # =====================
    logger.info("Pipeline completed successfully")
    status_text.text("Done!")

    return {
        "overview": overview,
        "funnel": funnel_result,
        "retention": retention_matrix,
        "item": item_result,
        "report_path": file_path,
        "pdf_path": pdf_path
    }