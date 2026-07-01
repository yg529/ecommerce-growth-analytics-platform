from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.core.config import FIGURE_DIR


def plot_retention_heatmap(
    matrix,
    save: bool = False,
    save_path: str | Path | None = None,
    max_cohort: int = 40,
):
    """Create a retention heatmap and return the Matplotlib figure."""
    display_matrix = matrix.copy().iloc[:max_cohort]

    if not display_matrix.empty:
        display_matrix.index = pd.to_datetime(display_matrix.index).strftime("%Y-%m-%d")

    fig, ax = plt.subplots(figsize=(12, 8))

    if display_matrix.empty:
        ax.text(0.5, 0.5, "No retention data", ha="center", va="center")
        ax.set_axis_off()
    else:
        vmax = max(0.06, display_matrix.max().max())
        sns.heatmap(
            display_matrix,
            cmap="Blues",
            vmin=0,
            vmax=vmax,
            linewidths=0.3,
            cbar=True,
            annot=False,
            ax=ax,
        )

        ax.set_xlabel("Retention Day")
        ax.set_ylabel("Cohort Date")

    ax.set_title("User Retention Heatmap", fontsize=14)
    fig.tight_layout()

    if save or save_path:
        output_path = Path(save_path) if save_path else FIGURE_DIR / "02_retention_heatmap.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300, bbox_inches="tight")

    return fig
