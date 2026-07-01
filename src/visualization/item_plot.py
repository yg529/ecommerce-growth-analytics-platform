from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.core.config import FIGURE_DIR


def plot_item_segmentation(seg, save: bool = False, save_path: str | Path | None = None):
    """Create item segmentation scatter plot and return the figure."""
    display_data = seg.copy()
    display_data["views_log"] = np.log1p(display_data["views"])

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.scatterplot(
        data=display_data,
        x="views_log",
        y="view_to_buy",
        hue="category",
        alpha=0.6,
        ax=ax,
    )

    ax.set_title("Item Segmentation (Log Scale)")
    ax.set_xlabel("Log(Views)")
    ax.set_ylabel("View to Buy Conversion")
    fig.tight_layout()

    if save or save_path:
        output_path = Path(save_path) if save_path else FIGURE_DIR / "04_item_segmentation.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300, bbox_inches="tight")

    return fig
