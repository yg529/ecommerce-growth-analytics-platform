import numpy as np
import pandas as pd

from src.core.validation import validate_events


def top_view_items(df, top_n=10):
    """
    统计浏览量最高的商品

    Parameters
    ----------
    df : DataFrame
        用户行为数据

    top_n : int
        返回前 N 个商品

    Returns
    -------
    DataFrame
    """

    validate_events(df)

    result = (
        df[df["event"] == "view"]
        .groupby("itemid")
        .size()
        .reset_index(name="views")
        .sort_values("views", ascending=False)
        .head(top_n)
    )

    return result

def item_conversion_analysis(df, min_views=100):
    """
    商品转化分析

    Parameters
    ----------
    df : DataFrame
        用户行为数据

    min_views : int
        最小浏览量，过滤长尾商品

    Returns
    -------
    DataFrame
        每个商品的浏览、加购、购买及转化率
    """

    validate_events(df)

    # 各事件数量统计
    summary = (
        df.groupby(["itemid", "event"])
        .size()
        .unstack(fill_value=0)
    )

    # 保证三列都存在
    for col in ["view", "addtocart", "transaction"]:
        if col not in summary.columns:
            summary[col] = 0

    summary = summary.rename(columns={
        "view": "views",
        "addtocart": "carts",
        "transaction": "buyers"
    })

    # 过滤浏览量过少商品
    summary = summary[summary["views"] >= min_views]

    # 转化率
    summary["view_to_cart"] = (
        summary["carts"] / summary["views"]
    )

    summary["cart_to_buy"] = (
        summary["buyers"] / summary["carts"]
    ).replace([np.inf, -np.inf], 0).fillna(0)

    summary["view_to_buy"] = (
        summary["buyers"] / summary["views"]
    ).replace([np.inf, -np.inf], 0).fillna(0)

    summary = (
        summary
        .sort_values(
            "view_to_buy",
            ascending=False
        )
        .reset_index()
    )

    return summary

def classify_items(df):
    """
    商品分层模型（爆款 / 潜力 / 长尾）
    """

    validate_events(df)

    summary = (
        df.groupby(["itemid", "event"])
        .size()
        .unstack(fill_value=0)
    )

    for col in ["view", "addtocart", "transaction"]:
        if col not in summary.columns:
            summary[col] = 0

    summary = summary.rename(columns={
        "view": "views",
        "addtocart": "carts",
        "transaction": "buyers"
    })

    summary["view_to_buy"] = (
        summary["buyers"] / summary["views"]
    ).replace([np.inf, -np.inf], 0).fillna(0)

    # ====== 中位数 ======
    views_median = summary["views"].median()
    conv_median = summary["view_to_buy"].median()

    # ====== 分类逻辑 ======
    def get_label(row):
        if row["views"] >= views_median and row["view_to_buy"] >= conv_median:
            return "high_value"   # 爆款
        elif row["views"] >= views_median:
            return "potential"    # 潜力
        else:
            return "long_tail"    # 长尾

    summary["category"] = summary.apply(get_label, axis=1)

    return summary.reset_index()

def item_insights(seg):
    """
    自动生成商品分层业务洞察
    """

    total = len(seg)

    # 各类别占比
    dist = seg["category"].value_counts(normalize=True)

    high_ratio = dist.get("high_value", 0)
    potential_ratio = dist.get("potential", 0)
    long_tail_ratio = dist.get("long_tail", 0)

    print("===== ITEM INSIGHTS =====")

    print(f"总商品数: {total}")
    print("")
    print(f"高价值商品占比: {high_ratio:.2%}")
    print(f"潜力商品占比: {potential_ratio:.2%}")
    print(f"长尾商品占比: {long_tail_ratio:.2%}")

    print("\n===== BUSINESS SUGGESTIONS =====")

    if high_ratio > 0.2:
        print("高价值商品较多：可加强推荐曝光")
    else:
        print("高价值商品较少：需要优化核心商品")

    if potential_ratio > 0.3:
        print("潜力商品较多：优化空间大，应提升转化率")

    if long_tail_ratio > 0.6:
        print("长尾商品占比高：需优化推荐系统或曝光策略")

    return {
        "high_value_ratio": high_ratio,
        "potential_ratio": potential_ratio,
        "long_tail_ratio": long_tail_ratio
    }

def generate_item_report(seg):
    """
    生成 Item Analysis 自动报告（Markdown）
    """

    total = len(seg)
    dist = seg["category"].value_counts(normalize=True)

    high = dist.get("high_value", 0)
    pot = dist.get("potential", 0)
    long = dist.get("long_tail", 0)

    report = f"""
# Item Analysis Report

## 1. Overview
- Total Items: {total}

## 2. Category Distribution
- High Value: {high:.2%}
- Potential: {pot:.2%}
- Long Tail: {long:.2%}

## 3. Key Insights
"""

    # 自动生成业务结论
    if high > 0.2:
        report += "- High-value items are strong, good for promotion.\n"
    else:
        report += "- High-value items are limited, need optimization.\n"

    if pot > 0.3:
        report += "- Large potential segment, focus on conversion optimization.\n"

    if long > 0.6:
        report += "- Too many long-tail items, improve recommendation system.\n"

    report += """
## 4. Recommendations
- Improve conversion for potential items
- Boost exposure for high-value items
- Reduce long-tail inefficiency
"""

    return report
