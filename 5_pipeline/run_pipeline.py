import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.analytics.funnel import funnel_analysis
from src.analytics.item_analysis import classify_items, item_insights
from src.analytics.overview import build_overview
from src.analytics.retention import retention_analysis
from src.analytics.rfm import rfm_analysis
from src.core.config import REPORT_DIR
from src.core.data_loader import load_clean_events
from src.report.generator import generate_report
from src.report.pdf_exporter import export_pdf


def main():
    df = load_clean_events()
    seg = classify_items(df)

    overview = build_overview(df)
    funnel_result = funnel_analysis(df)
    retention_matrix = retention_analysis(df)
    rfm_result = rfm_analysis(df)
    item_result = item_insights(seg)

    report, report_path = generate_report(
        df,
        overview,
        funnel_result,
        retention_matrix,
        item_result,
        save_path=REPORT_DIR,
    )
    pdf_path = export_pdf(report, str(Path(report_path).with_suffix(".pdf")))

    print("Pipeline completed.")
    print(f"Overview: {overview}")
    print(f"RFM summary: {rfm_result['summary']}")
    print(f"Report: {report_path}")
    print(f"PDF: {pdf_path}")


if __name__ == "__main__":
    main()
