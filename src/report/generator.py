from datetime import datetime
from pathlib import Path


def generate_report(df, overview, funnel_result, retention_matrix, item_result, save_path=None):
    """
    自动生成Markdown分析报告
    """

    report = []

    report.append("# RetailRocket 数据分析报告\n")

    # =========================
    # Overview
    # =========================
    report.append("## 1. 全局概览\n")
    report.append(f"- 总用户数: {overview.get('total_users', 0)}")
    report.append(f"- 总事件数: {overview.get('total_events', 0)}")
    report.append(f"- 商品数: {overview.get('total_items', 0)}")
    report.append(f"- 购买用户数: {overview.get('buyers', 0)}")
    report.append(f"- 转化率: {overview.get('conversion_rate', 0)}\n")

    # =========================
    # Funnel
    # =========================
    funnel = funnel_result.get("funnel", {})
    insights = funnel_result.get("insights", [])

    report.append("## 2. 用户转化漏斗\n")

    for k, v in funnel.items():
        report.append(f"- {k}: {v}")

    report.append("\n### 问题洞察")
    for i in insights:
        report.append(f"- {i}")

    # =========================
    # Retention
    # =========================
    report.append("\n## 3. 用户留存分析\n")

    try:
        report.append(f"- Cohort数量: {len(retention_matrix)}")
        report.append(f"- 平均留存率: {retention_matrix.mean().mean():.4f}")
    except:
        report.append("- 留存数据不可用")

    # =========================
    # Item
    # =========================
    report.append("\n## 4. 商品分析\n")

    if isinstance(item_result, dict):
        for k, v in item_result.items():
            report.append(f"- {k}: {v}")

    # =========================
    # Conclusion
    # =========================
    report.append("\n## 5. 总结建议\n")
    report.append("- 优化 Add to Cart → Transaction 转化率")
    report.append("- 提升高价值商品曝光")
    report.append("- 优化用户早期留存")

    final_report = "\n".join(report)

    # =========================
    # save file
    # =========================
    if save_path:
        path = Path(save_path)
        path.mkdir(parents=True, exist_ok=True)

        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        file_path = path / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_report)

        return final_report, str(file_path)

    return final_report, None