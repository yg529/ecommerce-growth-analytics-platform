import pandas as pd


def _rate(rates: dict, *keys: str) -> float:
    for key in keys:
        if key in rates:
            return rates[key]
    return 0


def generate_funnel_insight(funnel: dict, rates: dict) -> list:
    """Generate rule-based funnel insights."""
    insights = []
    view_cart = _rate(rates, "view_to_addtocart", "view_to_cart")
    cart_buy = _rate(rates, "addtocart_to_transaction", "cart_to_buy")
    view_buy = _rate(rates, "view_to_transaction", "view_to_buy")

    if funnel.get("view", 0) == 0:
        return ["No view events were found, so funnel conversion cannot be evaluated."]

    if view_cart < 0.1:
        insights.append(
            "View-to-cart conversion is low. Review product detail pages, traffic quality and recommendation relevance."
        )

    if cart_buy < 0.2:
        insights.append(
            "Cart-to-purchase conversion is low. Check checkout friction, pricing, shipping and trust signals."
        )

    if view_buy < 0.02:
        insights.append(
            "End-to-end purchase conversion is low. The largest drop-off stage should be prioritized first."
        )

    return insights or ["Funnel conversion has no obvious rule-based warning."]


def generate_retention_insight(matrix: pd.DataFrame) -> list:
    """Generate retention insights from a cohort matrix."""
    if matrix.empty:
        return ["Retention matrix is empty."]

    day1 = matrix[1].mean() if 1 in matrix.columns else 0
    day7 = matrix[7].mean() if 7 in matrix.columns else 0
    insights = []

    if day1 < 0.2:
        insights.append(
            "Day-1 retention is weak. New-user activation and first-session value should be reviewed."
        )

    if day7 < 0.05:
        insights.append(
            "Day-7 retention is low. Consider lifecycle messages, repeat-visit triggers and better personalization."
        )

    if day1 >= 0.3:
        insights.append("Day-1 retention is relatively healthy for this dataset.")

    return insights or ["Retention has no obvious rule-based warning."]


def generate_rfm_insight(summary: dict) -> list:
    """Generate user-segment insights from RFM summary counts."""
    if not summary:
        return ["No transaction users were found, so RFM segments are unavailable."]

    champions = summary.get("Champions", 0)
    at_risk = summary.get("At Risk", 0)
    loyal = summary.get("Loyal Users", 0)
    total = sum(summary.values())
    insights = []

    if at_risk / total > 0.5:
        insights.append(
            "At-risk users dominate transaction users. Win-back campaigns should be tested."
        )

    if champions / total < 0.1:
        insights.append(
            "Champion users are limited. Increase repeat purchase incentives for recent buyers."
        )

    if loyal / total > 0.3:
        insights.append("Loyal users form a meaningful segment and can support retention programs.")

    return insights or ["RFM distribution has no obvious rule-based warning."]


def business_insight_pipeline(
    funnel: dict,
    rates: dict,
    retention_matrix: pd.DataFrame,
    rfm_summary: dict,
) -> dict:
    """Generate all dashboard insight blocks."""
    return {
        "funnel_insights": generate_funnel_insight(funnel, rates),
        "retention_insights": generate_retention_insight(retention_matrix),
        "rfm_insights": generate_rfm_insight(rfm_summary),
    }
