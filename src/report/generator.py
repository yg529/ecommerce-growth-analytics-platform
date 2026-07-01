from datetime import datetime
from pathlib import Path


def _format_rate(value: float) -> str:
    return f"{value:.2%}"


def generate_report(
    df,
    overview,
    funnel_result,
    retention_matrix,
    item_result,
    save_path=None,
):
    """Generate a Markdown analytics report."""
    report = [
        "# RetailRocket Growth Analytics Report",
        "",
        "## 1. Overview",
        f"- Total users: {overview.get('total_users', 0)}",
        f"- Total events: {overview.get('total_events', 0)}",
        f"- Total items: {overview.get('total_items', 0)}",
        f"- Buyers: {overview.get('buyers', 0)}",
        f"- Buyer conversion rate: {_format_rate(overview.get('conversion_rate', 0))}",
        "",
        "## 2. Funnel",
    ]

    for key, value in funnel_result.get("funnel", {}).items():
        report.append(f"- {key}: {value}")

    report.extend(["", "### Funnel Insights"])
    insights = funnel_result.get("insights", [])
    if insights:
        report.extend(f"- {item}" for item in insights)
    else:
        report.append("- No severe funnel drop-off found by the current rules.")

    report.extend(["", "## 3. Retention"])
    if retention_matrix is not None and not retention_matrix.empty:
        report.append(f"- Cohorts: {len(retention_matrix)}")
        report.append(f"- Average retention: {_format_rate(retention_matrix.mean().mean())}")
    else:
        report.append("- Retention matrix is empty.")

    report.extend(["", "## 4. Item Segmentation"])
    if isinstance(item_result, dict) and item_result:
        for key, value in item_result.items():
            if isinstance(value, float):
                report.append(f"- {key}: {_format_rate(value)}")
            else:
                report.append(f"- {key}: {value}")
    else:
        report.append("- Item segmentation result is unavailable.")

    report.extend(
        [
            "",
            "## 5. Recommendations",
            "- Prioritize the funnel stage with the highest drop-off.",
            "- Improve exposure and conversion for high-potential items.",
            "- Use retention and RFM segments to design lifecycle campaigns.",
        ]
    )

    final_report = "\n".join(report)

    if save_path:
        path = Path(save_path)
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        file_path.write_text(final_report, encoding="utf-8")
        return final_report, str(file_path)

    return final_report, None
