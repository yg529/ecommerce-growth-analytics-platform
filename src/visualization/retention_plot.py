import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.core.config import FIGURE_DIR


def plot_retention_heatmap(
    matrix,
    save=False,
    max_cohort=40
):
    """
    绘制用户留存热力图
    """

    # 不修改原数据
    matrix = matrix.copy()

    # 只展示前40个 Cohort（GitHub 展示更美观）
    matrix = matrix.iloc[:max_cohort]

    # 日期格式化
    matrix.index = pd.to_datetime(matrix.index).strftime("%Y-%m-%d")

    plt.figure(figsize=(12, 8))

    sns.heatmap(
        matrix,
        cmap="Blues",
        vmin=0,
        vmax=0.06,          # RetailRocket 留存率较低
        linewidths=0.3,
        cbar=True,
        annot=False
    )

    plt.title("User Retention Heatmap", fontsize=14)
    plt.xlabel("Retention Day")
    plt.ylabel("Cohort Date")

    plt.tight_layout()

    if save:
        os.makedirs(FIGURE_DIR, exist_ok=True)

        plt.savefig(
            FIGURE_DIR / "02_retention_heatmap.png",
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
    plt.close()