import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

from src.core.config import FIGURE_DIR


def plot_item_segmentation(seg, save=False):

    seg = seg.copy()

    # log 处理（关键）
    seg["views_log"] = np.log1p(seg["views"])

    plt.figure(figsize=(10, 7))

    sns.scatterplot(
        data=seg,
        x="views_log",
        y="view_to_buy",
        hue="category",
        alpha=0.6
    )

    plt.title("Item Segmentation (Log Scale)")
    plt.xlabel("Log(Views)")
    plt.ylabel("View → Buy Conversion")

    plt.tight_layout()

    if save:
        os.makedirs(FIGURE_DIR, exist_ok=True)

        plt.savefig(
            FIGURE_DIR / "04_item_segmentation.png",
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()