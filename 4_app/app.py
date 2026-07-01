import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.analytics.funnel import funnel_analysis
from src.analytics.item_analysis import classify_items, item_insights
from src.analytics.overview import build_overview
from src.analytics.retention import retention_analysis
from src.analytics.rfm import rfm_analysis
from src.core.config import REPORT_DIR
from src.core.data_loader import load_clean_events
from src.core.logger import get_logger
from src.insights.business_insight import business_insight_pipeline
from src.pipeline.runner import run_full_pipeline
from src.report.generator import generate_report
from src.report.pdf_exporter import export_pdf
from src.visualization.funnel_plot import plot_funnel
from src.visualization.item_plot import plot_item_segmentation
from src.visualization.retention_plot import plot_retention_heatmap


logger = get_logger("dashboard")

st.set_page_config(
    page_title="RetailRocket Analytics Dashboard",
    layout="wide",
)


def format_percent(value: float) -> str:
    return f"{value:.2%}"


def kpi_card(label: str, value):
    st.markdown(
        f"""
        <div style="
            background-color:#111827;
            padding:16px;
            border-radius:8px;
            text-align:center;
            box-shadow:0 2px 6px rgba(0,0,0,0.18);
        ">
            <div style="color:#9CA3AF; font-size:14px;">{label}</div>
            <div style="color:#FFFFFF; font-size:24px; font-weight:bold;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_data():
    return load_clean_events()


try:
    df = load_data()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.code(
        "py src/preprocessing/clean_events.py\n"
        "py -m streamlit run 4_app/app.py",
        language="powershell",
    )
    st.stop()

logger.info("Data loaded: shape=%s", df.shape)
seg = classify_items(df)

st.sidebar.title("RetailRocket Dashboard")
page = st.sidebar.radio(
    "Select Module",
    [
        "Overview",
        "Funnel Analysis",
        "Retention Analysis",
        "Item Segmentation",
        "Item Insights",
        "RFM Analysis",
        "Growth Dashboard",
    ],
)

run_btn = st.sidebar.button("Run Full Pipeline")
generate_btn = st.sidebar.button("Generate Report")

if page == "Overview":
    st.title("Overview Dashboard")

    overview = build_overview(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Users", overview["total_users"])
    col2.metric("Events", overview["total_events"])
    col3.metric("Items", overview["total_items"])
    col4.metric("Buyers", overview["buyers"])
    st.metric("Conversion Rate", format_percent(overview["conversion_rate"]))

elif page == "Funnel Analysis":
    st.title("Funnel Analysis")

    result = funnel_analysis(df)
    col1, col2, col3 = st.columns(3)
    col1.metric("View", result["funnel"].get("view", 0))
    col2.metric("Cart", result["funnel"].get("addtocart", 0))
    col3.metric("Buy", result["funnel"].get("transaction", 0))

    st.plotly_chart(
        plot_funnel(result["funnel"], result["drop_off"]),
        use_container_width=True,
    )
    st.json(result["conversion_rate"])
    st.json(result["drop_off"])

elif page == "Retention Analysis":
    st.title("Retention Analysis")

    matrix = retention_analysis(df)
    st.dataframe(matrix)
    st.pyplot(plot_retention_heatmap(matrix))

elif page == "Item Segmentation":
    st.title("Item Segmentation")

    st.pyplot(plot_item_segmentation(seg))
    st.dataframe(seg.head(20))

elif page == "Item Insights":
    st.title("Item Insights")
    st.json(item_insights(seg))

elif page == "RFM Analysis":
    st.title("RFM Analysis")

    result = rfm_analysis(df)
    st.caption(result["monetary_note"])
    st.json(result["summary"])
    st.dataframe(result["rfm_table"].head(50))

elif page == "Growth Dashboard":
    st.title("RetailRocket Growth Analytics Dashboard")

    overview = build_overview(df)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Users", overview["total_users"])
    with c2:
        kpi_card("Events", overview["total_events"])
    with c3:
        kpi_card("Items", overview["total_items"])
    with c4:
        kpi_card("Buyers", overview["buyers"])

    st.metric("Conversion Rate", format_percent(overview["conversion_rate"]))
    st.divider()

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("### Conversion Funnel")
        funnel_result = funnel_analysis(df)
        st.plotly_chart(
            plot_funnel(funnel_result["funnel"], funnel_result["drop_off"]),
            use_container_width=True,
        )

    with col2:
        st.markdown("### RFM Overview")
        rfm_result = rfm_analysis(df)
        st.caption(rfm_result["monetary_note"])
        st.json(rfm_result["summary"])
        st.dataframe(rfm_result["rfm_table"].head(10))

    st.divider()
    st.markdown("### Retention Heatmap")
    matrix = retention_analysis(df)
    st.pyplot(plot_retention_heatmap(matrix))

    st.divider()
    st.markdown("### Business Insights")
    insights = business_insight_pipeline(
        funnel_result["funnel"],
        funnel_result.get("conversion_rate", {}),
        matrix,
        rfm_result["summary"],
    )

    for title, items in [
        ("Funnel Insights", insights["funnel_insights"]),
        ("Retention Insights", insights["retention_insights"]),
        ("RFM Insights", insights["rfm_insights"]),
    ]:
        st.markdown(f"#### {title}")
        for item in items:
            st.info(item)

if generate_btn:
    overview = build_overview(df)
    funnel_result = funnel_analysis(df)
    retention_matrix = retention_analysis(df)
    item_result = item_insights(seg)

    report, file_path = generate_report(
        df,
        overview,
        funnel_result,
        retention_matrix,
        item_result,
        save_path=REPORT_DIR,
    )
    pdf_path = export_pdf(report, str(Path(file_path).with_suffix(".pdf")))

    st.text_area("Report", report, height=500)
    with open(pdf_path, "rb") as handle:
        st.download_button(
            "Download PDF",
            handle,
            file_name="retailrocket_report.pdf",
            mime="application/pdf",
        )

if run_btn:
    with st.spinner("Running pipeline..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        result = run_full_pipeline(df, seg, progress_bar, status_text)
        insights = business_insight_pipeline(
            result["funnel"]["funnel"],
            result["funnel"].get("conversion_rate", {}),
            result["retention"],
            result.get("rfm", {}).get("summary", {}),
        )

    st.success("Done")
    st.subheader("Insights")
    for block in insights.values():
        for item in block:
            st.write(item)

    st.json(result["overview"])
