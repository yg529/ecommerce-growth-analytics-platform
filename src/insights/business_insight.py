import pandas as pd


def generate_funnel_insight(funnel: dict, rates: dict) -> list:
    """
    漏斗分析洞察
    """

    insights = []

    view = funnel.get("view", 0)
    cart = funnel.get("addtocart", 0)
    buy = funnel.get("transaction", 0)

    view_cart = rates.get("view_to_cart", 0)
    cart_buy = rates.get("cart_to_buy", 0)
    view_buy = rates.get("view_to_buy", 0)

    # 转化判断
    if view_cart < 0.1:
        insights.append(
            "View → Cart 转化率较低，说明商品吸引力不足或推荐不精准。建议优化推荐算法或商品展示策略。"
        )

    if cart_buy < 0.2:
        insights.append(
            "Cart → Purchase 转化率较低，说明用户在结算阶段流失严重，可能存在价格、支付或信任问题。"
        )

    if view_buy < 0.02:
        insights.append(
            "Overall 转化率偏低，建议优化整体购物路径（首页 → 商品页 → 结算）。"
        )

    if not insights:
        insights.append("✔ Funnel 转化表现正常，无明显瓶颈。")

    return insights


def generate_retention_insight(matrix: pd.DataFrame) -> list:
    """
    留存分析洞察
    """

    insights = []

    if matrix.empty:
        return ["留存数据为空"]

    day1 = matrix.get(1, pd.Series()).mean() if 1 in matrix.columns else 0
    day7 = matrix.get(7, pd.Series()).mean() if 7 in matrix.columns else 0

    if day1 < 0.2:
        insights.append(
            "Day 1 留存偏低，新用户体验可能存在问题（注册/引导流程需优化）。"
        )

    if day7 < 0.05:
        insights.append(
            "Day 7 留存较低，用户粘性不足，需要加强内容/推荐/激励机制。"
        )

    if day1 >= 0.3:
        insights.append("✔ Day 1 留存表现良好，用户初始体验较好。")

    return insights


def generate_rfm_insight(summary: dict) -> list:
    """
    RFM用户分层洞察
    """

    insights = []

    champions = summary.get("Champions", 0)
    at_risk = summary.get("At Risk", 0)
    loyal = summary.get("Loyal Users", 0)

    total = sum(summary.values()) if summary else 1

    if at_risk / total > 0.5:
        insights.append(
            "流失用户占比过高，建议启动召回策略（优惠券/Push/邮件营销）。"
        )

    if champions / total < 0.1:
        insights.append(
            "高价值用户占比低，说明用户质量不足或产品缺乏核心吸引力。"
        )

    if loyal / total > 0.3:
        insights.append("忠诚用户占比良好，具备稳定用户基础。")

    return insights


def business_insight_pipeline(funnel, rates, retention_matrix, rfm_summary) -> dict:
    """
    总洞察生成器
    """

    funnel_insights = generate_funnel_insight(funnel, rates)
    retention_insights = generate_retention_insight(retention_matrix)
    rfm_insights = generate_rfm_insight(rfm_summary)

    return {
        "funnel_insights": funnel_insights,
        "retention_insights": retention_insights,
        "rfm_insights": rfm_insights
    }