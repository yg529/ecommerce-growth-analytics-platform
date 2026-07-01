import matplotlib.pyplot as plt


def plot_conversion(rate: dict):
    """Create a conversion-rate bar chart and return the figure."""
    names = list(rate.keys())
    values = [value * 100 for value in rate.values()]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(names, values)
    ax.set_ylabel("Conversion Rate (%)")
    ax.set_title("Conversion Rate")
    ax.tick_params(axis="x", rotation=20)

    for index, value in enumerate(values):
        ax.text(index, value, f"{value:.2f}%", ha="center", va="bottom")

    fig.tight_layout()
    return fig
