import sys
from pathlib import Path
import streamlit as st

# =========================
# path fix
# =========================
sys.path.append(str(Path(__file__).resolve().parent.parent))

# =========================
# imports
# =========================
from src.core.data_loader import load_clean_events
from src.core.config import REPORT_DIR
from src.core.logger import get_logger

from src.analytics.overview import build_overview
from src.analytics.funnel import funnel_analysis
from src.analytics.retention import retention_analysis
from src.analytics.item_analysis import classify_items, item_insights
from src.analytics.rfm import rfm_analysis

from src.visualization.item_plot import plot_item_segmentation
from src.visualization.funnel_plot import plot_funnel
from src.visualization.retention_plot import plot_retention_heatmap

from src.report.generator import generate_report
from src.report.pdf_exporter import export_pdf
from src.pipeline.runner import run_full_pipeline
from src.insights.business_insight import business_insight_pipeline

def kpi_card(label, value):
    st.markdown(
        f"""
        <div style="
            background-color:#111827;
            padding:16px;
            border-radius:12px;
            text-align:center;
            box-shadow:0 2px 6px rgba(0,0,0,0.2);
        ">
            <div style="color:#9CA3AF; font-size:14px;">{label}</div>
            <div style="color:#FFFFFF; font-size:24px; font-weight:bold;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# logger
# =========================
logger = get_logger("dashboard")

# =========================
# page config
# =========================
st.set_page_config(
    page_title="RetailRocket Analytics Dashboard",
    layout="wide"
)

# =========================
# data
# =========================
@st.cache_data
def load_data():
    return load_clean_events()

df = load_data()
logger.info(f"Data loaded: shape={df.shape}")

seg = classify_items(df)

# =========================
# sidebar
# =========================
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
        "Growth Dashboard"
    ]
)

run_btn = st.sidebar.button("Run Full Pipeline")
generate_btn = st.sidebar.button("📄 Generate Report")

# =========================
# OVERVIEW
# =========================
if page == "Overview":

    st.title("Overview Dashboard")

    overview = build_overview(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Users", overview["total_users"])
    col2.metric("Events", overview["total_events"])
    col3.metric("Items", overview["total_items"])

    st.metric("Buyers", overview["buyers"])
    st.metric("Conversion Rate", overview["conversion_rate"])

# =========================
# FUNNEL
# =========================
elif page == "Funnel Analysis":

    st.title("Funnel Analysis")

    result = funnel_analysis(df)

    st.metric("View", result["funnel"]["view"])
    st.metric("Cart", result["funnel"]["addtocart"])
    st.metric("Buy", result["funnel"]["transaction"])

    st.plotly_chart(
        plot_funnel(result["funnel"], result["drop_off"]),
        use_container_width=True
    )

    st.json(result["conversion_rate"])
    st.json(result["drop_off"])

# =========================
# RETENTION
# =========================
elif page == "Retention Analysis":

    st.title("etention Analysis")

    matrix = retention_analysis(df)

    st.dataframe(matrix)

    st.pyplot(
        plot_retention_heatmap(matrix, save_path=None)
    )

# =========================
# ITEM
# =========================
elif page == "Item Segmentation":

    st.title("Item Segmentation")

    plot_item_segmentation(seg)
    st.dataframe(seg.head(20))

elif page == "Item Insights":

    st.title("Item Insights")

    st.json(item_insights(seg))

# =========================
# RFM
# =========================
elif page == "RFM Analysis":

    st.title("RFM Analysis")

    result = rfm_analysis(df)

    st.json(result["summary"])
    st.dataframe(result["rfm_table"].head(50))

# =========================
# GROWTH DASHBOARD（核心修复）
# =========================
elif page == "Growth Dashboard":

    st.title("RetailRocket Growth Analytics Dashboard")

    overview = build_overview(df)

    # =========================
    # KPI SECTION（BI卡片化）
    # =========================
    st.markdown("### Key Metrics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card("Users", overview["total_users"])

    with c2:
        kpi_card("Events", overview["total_events"])

    with c3:
        kpi_card("Items", overview["total_items"])

    with c4:
        kpi_card("Buyers", overview["buyers"])

    st.markdown("#### Conversion Rate")
    st.markdown(
        f"""
        <div style="
            font-size:28px;
            font-weight:bold;
            color:#10B981;
            padding:10px;
        ">
        {overview["conversion_rate"]:.2%}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =========================
    # LAYOUT GRID（BI核心结构）
    # =========================
    col1, col2 = st.columns([1.2, 1])

    # =========================
    # Funnel（左侧大图）
    # =========================
    with col1:

        st.markdown("### Conversion Funnel")

        funnel_result = funnel_analysis(df)

        fig = plot_funnel(
            funnel_result["funnel"],
            funnel_result["drop_off"]
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # RFM（右侧）
    # =========================
    with col2:

        st.markdown("### RFM Overview")

        rfm_result = rfm_analysis(df)

        st.json(rfm_result["summary"])

        st.dataframe(rfm_result["rfm_table"].head(10))

    st.divider()

    # =========================
    # Retention Heatmap（全宽）
    # =========================
    st.markdown("### Retention Heatmap")

    matrix = retention_analysis(df)

    fig = plot_retention_heatmap(matrix, save_path=None)
    st.pyplot(fig)

    st.divider()

    # =========================
    # BUSINESS INSIGHTS（卡片化）
    # =========================
    st.markdown("### Business Insights")

    insights = business_insight_pipeline(
        funnel_result["funnel"],
        funnel_result.get("conversion_rate", {}),
        matrix,
        rfm_result["summary"]
    )

    def render_insight(title, items, icon):
        st.markdown(f"#### {icon} {title}")
        for i in items:
            st.markdown(
                f"""
                <div style="
                    background:#1F2937;
                    padding:10px;
                    margin:6px 0;
                    border-radius:8px;
                    color:#E5E7EB;
                ">
                    {i}
                </div>
                """,
                unsafe_allow_html=True
            )

    render_insight("Funnel Insights", insights["funnel_insights"], "📉")
    render_insight("Retention Insights", insights["retention_insights"], "📊")
    render_insight("RFM Insights", insights["rfm_insights"], "👑")

# =========================
# REPORT
# =========================
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
        save_path=REPORT_DIR
    )

    pdf_path = export_pdf(
        report,
        str(Path(file_path).with_suffix(".pdf"))
    )

    st.text_area("Report", report, height=500)

    with open(pdf_path, "rb") as f:
        st.download_button(
            "Download PDF",
            f,
            file_name="retailrocket_report.pdf",
            mime="application/pdf"
        )

# =========================
# PIPELINE
# =========================
if run_btn:

    with st.spinner("Running pipeline..."):

        progress_bar = st.progress(0)
        status_text = st.empty()

        result = run_full_pipeline(df, seg, progress_bar, status_text)

        insights = business_insight_pipeline(
            result["funnel"]["funnel"],
            result["funnel"].get("conversion_rate", {}),
            result["retention"],
            result.get("rfm", {}).get("summary", {})
        )

    st.success("Done")

    st.subheader("Insights")

    for i in insights["funnel_insights"]:
        st.write(i)

    for i in insights["retention_insights"]:
        st.write(i)

    for i in insights["rfm_insights"]:
        st.write(i)

    st.json(result["overview"])