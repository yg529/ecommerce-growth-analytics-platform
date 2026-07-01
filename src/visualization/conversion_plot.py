import matplotlib.pyplot as plt


def plot_conversion(rate):

    names = list(rate.keys())
    values = [v * 100 for v in rate.values()]

    plt.figure(figsize=(8,5))

    plt.bar(names, values)

    plt.ylabel("Conversion Rate (%)")

    plt.title("Conversion Rate")

    for i, v in enumerate(values):
        plt.text(i, v, f"{v:.2f}%")

    plt.tight_layout()

    plt.show()